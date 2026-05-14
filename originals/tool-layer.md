# Tool / function-calling layer — from scratch

> **[original]** · part of [`build-your-own-ai/originals/`](README.md).
> _A short, runnable starter guide for a build target where no good public
> from-scratch guide exists today._

**Index entry:** [Agents → Tool / function-calling layer](../README.md#agents)

---

## The one-line promise

A tool layer is three things: a **schema** so the model knows how to
call your function, a **dispatcher** that routes the model's JSON to
the right Python callable, and a **validator** that catches broken
arguments before they crash you. ~100 lines of plain Python, no
Pydantic-AI, no Instructor, no LangChain.

## What you'll understand after

- What "function calling" actually is at the wire level (a JSON blob
  in a specific shape).
- Why ~30% of agent runs fail on malformed tool arguments and what to
  do about it.
- How to keep the loop alive when a tool errors out — the difference
  between an agent and a one-shot prompt.

## Step 1 — The schema

The OpenAI / Anthropic / Gemini tool-calling specs converge on roughly
the same JSON-Schema-shaped object per tool:

```python
from dataclasses import dataclass, field
from typing import Callable, Any

@dataclass
class Tool:
    name: str
    description: str
    parameters: dict                    # JSON-Schema-shaped dict
    fn: Callable[..., Any]              # the actual Python implementation

def make_schema(tools: list[Tool]) -> list[dict]:
    """The blob you send the model in the tools= parameter."""
    return [
        {
            "name": t.name,
            "description": t.description,
            "input_schema": t.parameters,
        }
        for t in tools
    ]
```

For most tools, the JSON-Schema is small enough to write by hand:

```python
read_file = Tool(
    name="read_file",
    description="Read the contents of a file given an absolute path.",
    parameters={
        "type": "object",
        "properties": {"path": {"type": "string"}},
        "required": ["path"],
    },
    fn=lambda path: open(path).read(),
)
```

For tools with more arguments, the [tool-anatomy article by Amit
Chaudhary](https://amitness.com/posts/function-calling-schema/) shows
how to auto-generate the schema from Python type hints. That's the
optional polish; the dispatcher below is the load-bearing part.

## Step 2 — The dispatcher

The model's response carries zero or more `tool_use` blocks. Each has
a name and a JSON argument dict. Dispatch is a dict lookup plus a
function call.

```python
@dataclass
class ToolCall:
    id: str
    name: str
    arguments: dict

@dataclass
class ToolResult:
    id: str
    name: str
    output: str           # always string; the model reads it back
    is_error: bool = False

def dispatch(tools: dict[str, Tool], call: ToolCall) -> ToolResult:
    if call.name not in tools:
        return ToolResult(call.id, call.name,
                          f"unknown tool '{call.name}'", is_error=True)
    try:
        result = tools[call.name].fn(**call.arguments)
        return ToolResult(call.id, call.name, str(result))
    except TypeError as e:
        # wrong argument names / types — the most common failure
        return ToolResult(call.id, call.name,
                          f"argument error: {e}", is_error=True)
    except Exception as e:
        return ToolResult(call.id, call.name,
                          f"tool failed: {type(e).__name__}: {e}",
                          is_error=True)
```

Three failure paths, all caught, all turned into strings the model can
read on the next turn. The bug that wastes the most engineering time
is letting a `TypeError` propagate up and crash the agent loop.

## Step 3 — Validation (light JSON-Schema)

The model will sometimes hallucinate arguments — wrong types, missing
required fields, extra fields. You can catch most of these with ~20
lines of validation, without pulling in `jsonschema`:

```python
def validate(schema: dict, args: dict) -> str | None:
    """Returns None if valid, else an error message."""
    required = schema.get("required", [])
    for key in required:
        if key not in args:
            return f"missing required argument '{key}'"
    props = schema.get("properties", {})
    for key, val in args.items():
        if key not in props:
            return f"unknown argument '{key}'"
        expected = props[key].get("type")
        if expected == "string" and not isinstance(val, str):
            return f"'{key}' must be a string, got {type(val).__name__}"
        if expected == "integer" and not isinstance(val, int):
            return f"'{key}' must be an integer, got {type(val).__name__}"
        # extend as needed
    return None
```

Wire it in:

```python
def dispatch(tools, call):
    if call.name not in tools:
        return ToolResult(call.id, call.name,
                          f"unknown tool '{call.name}'", is_error=True)
    err = validate(tools[call.name].parameters, call.arguments)
    if err:
        return ToolResult(call.id, call.name, err, is_error=True)
    ...
```

Now the model gets a clear `"missing required argument 'path'"` back
instead of a Python traceback — and on the next turn it usually fixes
the call.

## Step 4 — Loop integration

In the [agent loop](../README.md#agents), each turn looks like:

```python
def turn(client, messages, tools):
    response = client.messages.create(
        model=MODEL,
        max_tokens=2048,
        tools=make_schema(list(tools.values())),
        messages=messages,
    )
    messages.append({"role": "assistant", "content": response.content})

    tool_results = []
    for block in response.content:
        if block.type == "tool_use":
            call = ToolCall(id=block.id, name=block.name, arguments=block.input)
            result = dispatch(tools, call)
            tool_results.append({
                "type": "tool_result",
                "tool_use_id": result.id,
                "content": result.output,
                "is_error": result.is_error,
            })

    if tool_results:
        messages.append({"role": "user", "content": tool_results})
        return False  # not done, loop again
    return True  # no tool calls → final answer reached
```

The dispatcher and validator do their work inside this turn. The agent
loop never sees raw exceptions; it sees string results — error
messages included.

## Step 5 — Three failure modes that bite everyone

1. **The model invents a tool you didn't declare.** Caught by the
   "unknown tool" branch in `dispatch`. Don't fail the run — return
   the error string, let the model pick another tool next turn.
2. **The model passes valid JSON but wrong semantics** (e.g. a relative
   path when you required absolute). Your `fn` raises an exception →
   `dispatch` catches → model sees the error → model retries. Make
   your error strings *actionable*: "path must be absolute (e.g.
   '/home/user/file.txt')" beats "ValueError".
3. **An infinite tool loop.** The model calls a tool, gets an error,
   calls the same tool with the same args, gets the same error, …
   Solve this in the *agent loop*, not the tool layer: cap the total
   turns, and if the last 3 tool calls were identical, abort with a
   clear message.

## What to read next

- The [agent loop entry](../README.md#agents) — where this tool layer
  plugs in.
- The [coding agent entry](../README.md#agents) — production-shape
  examples of the read/edit/bash tools this pattern enables.
- The [multi-agent original](multi-agent.md) — same dispatcher
  pattern, applied to dispatching subtasks to workers.
