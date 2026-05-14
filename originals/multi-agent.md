# Multi-agent orchestration — from scratch

> **[original]** · part of [`build-your-own-ai/originals/`](README.md).
> _A short, runnable starter guide for a build target where no good public
> from-scratch guide exists today._

**Index entry:** [Agents → Multi-agent orchestration](../README.md#agents)

---

## The one-line promise

A **planner** agent decomposes a task and dispatches subtasks to
**worker** agents; the planner aggregates results and decides when the
task is done. The whole loop is ~150 lines of plain Python — no CrewAI,
no AutoGen — so you can see exactly where the coordination cost lives.

## What you'll understand after

- The simplest useful multi-agent pattern (planner / workers) — and how
  more elaborate patterns are variations on it.
- The honest answer to "is multi-agent better than one good agent?"
- Why most multi-agent failures are coordination bugs, not model bugs.

## Step 1 — Worker

A worker is just a single-purpose agent. It takes a subtask and a context,
runs its own reason-act-observe loop, and returns a result.

```python
from dataclasses import dataclass
from typing import Callable

@dataclass
class Worker:
    name: str
    system: str                       # role-specific system prompt
    tools: dict[str, Callable]        # subset of tools this worker may use
    llm: Callable

    def run(self, subtask: str, context: str) -> str:
        # The full agent loop lives elsewhere — see ../README.md#agents.
        # For brevity, we treat each worker run as a self-contained
        # single-turn call with tools.
        return run_agent_loop(
            llm=self.llm,
            system=self.system,
            user=f"Subtask: {subtask}\n\nContext:\n{context}",
            tools=self.tools,
            max_turns=8,
        )
```

The crucial point: a worker's system prompt should be **narrow**. "You
are a researcher; your job is to find sources and quote them." Not "you
are a helpful AI assistant." The narrower the role, the less the planner
has to fight against worker drift.

## Step 2 — Planner

The planner decides:
1. What subtasks exist.
2. Which worker handles each.
3. When the overall task is done.

The decisive design choice: the planner's output is **structured JSON**, not
free-form prose. That is what makes the dispatch loop deterministic.

```python
import json

PLANNER_SYSTEM = """
You coordinate a team of specialized worker agents.
Available workers: {worker_names}.

For each turn, output a JSON object:
{{
  "action": "dispatch" | "finish",
  "worker": <one of the available worker names>,         // if action == "dispatch"
  "subtask": <natural-language subtask>,                  // if action == "dispatch"
  "rationale": <one sentence>,
  "final_answer": <string>                                // if action == "finish"
}}

Do not output anything else.
""".strip()

class Planner:
    def __init__(self, llm, workers: list[Worker]):
        self.llm = llm
        self.workers = {w.name: w for w in workers}
        self.system = PLANNER_SYSTEM.format(
            worker_names=", ".join(self.workers.keys())
        )

    def step(self, task: str, history: list[dict]) -> dict:
        prompt = (
            f"Task: {task}\n\n"
            f"History of dispatches so far:\n"
            + ("\n".join(json.dumps(h) for h in history) or "(none)")
            + "\n\nNext action:"
        )
        raw = self.llm.complete(system=self.system, user=prompt)
        return json.loads(raw)   # validation: see Step 4
```

## Step 3 — Orchestration loop

```python
@dataclass
class DispatchRecord:
    worker: str
    subtask: str
    result: str

def orchestrate(planner: Planner, task: str, max_dispatches: int = 8) -> str:
    history: list[DispatchRecord] = []
    for turn in range(max_dispatches):
        action = planner.step(task, [h.__dict__ for h in history])

        if action["action"] == "finish":
            return action["final_answer"]

        worker = planner.workers[action["worker"]]
        context = "\n\n".join(
            f"# {h.worker} on '{h.subtask}'\n{h.result}" for h in history
        )
        result = worker.run(action["subtask"], context)
        history.append(DispatchRecord(
            worker=action["worker"], subtask=action["subtask"], result=result,
        ))

    # ran out of dispatches without a finish action
    return planner.llm.complete(
        system="Summarize the team's findings into a final answer.",
        user="\n\n".join(f"{h.worker}: {h.result}" for h in history),
    )
```

## Step 4 — The bug nobody warns you about: malformed planner JSON

Every multi-agent system that uses LLM-generated plans hits this within
the first ten runs:

1. Planner outputs JSON with a trailing comma.
2. `json.loads` raises.
3. The whole orchestration crashes.

Wrap the parse in a one-shot retry with a corrective prompt. If that
still fails, fall back to finishing with whatever you have.

```python
def parse_plan(raw: str) -> dict | None:
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return None
```

In `planner.step`, retry once with the error message in the prompt before
giving up.

## Step 5 — Workers that don't share context: the silent killer

The most common multi-agent failure is workers acting on stale or missing
context. Two anti-patterns to avoid:

- **The planner forgot to include prior results in the worker's
  context.** Result: workers re-do work or contradict each other. The
  orchestration loop above concatenates *all* prior worker outputs into
  the context — overkill for short tasks, mandatory for long ones.
- **Workers can't see each other's tool outputs.** If worker A retrieves
  a file and worker B needs to edit it, B has to find the file again
  unless A's tool output is in the shared context. Pass it.

## When NOT to use multi-agent

Honest test before adopting this pattern:

| Test | Verdict |
|---|---|
| Can one well-prompted agent with a good toolset do this in fewer LLM calls? | If yes, **use one agent.** |
| Are the subtasks genuinely heterogeneous (different tools, different system prompts, different success criteria)? | If no, **use one agent.** |
| Can subtasks be done in parallel? | If yes, multi-agent has a real win on latency. |
| Is the task long enough that one agent's context window becomes the bottleneck? | If yes, multi-agent's worker-level context isolation actually helps. |

Most "multi-agent" tutorials fail the first two questions and end up as
one-agent-with-extra-steps. The version above will *work* — but the
question is always "should you."

## What to read next

- The [agent loop guide](../README.md#agents) — workers are just agents,
  so the same patterns apply at a smaller scale.
- The [agent memory guide](agent-memory.md) — long multi-agent runs need
  shared memory, not just shared context strings.
- Anthropic's "Building effective agents" post for the broader pattern
  zoo (chained calls, routing, parallelization, orchestrator-worker —
  this guide is the last one, with code).
