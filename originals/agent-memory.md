# Agent memory — from scratch

> **[original]** · part of [`build-your-own-ai/originals/`](README.md).
> _A short, runnable starter guide for a build target where no good public
> from-scratch guide exists today._

**Index entry:** [Agents → Agent memory](../README.md#agents)

---

## The one-line promise

Agent memory is two things layered: a **short-term buffer** that fits in
the context window, and a **long-term store** that the agent retrieves
from on demand. Almost every existing tutorial outsources both to a
memory framework. Here, you build them — ~100 lines, plain Python.

## What you'll understand after

- Why a context window is a budget and how to spend it.
- What summarization-on-overflow actually does, and when it loses
  information that matters.
- How retrieval-augmented memory differs from RAG: same machinery,
  different time scale.

## The two-tier model

```
+-------------------------------+
|  short-term buffer (window)   |   recent messages, fits in context
+-------------------------------+
            |  overflows
            v
+-------------------------------+
|  long-term store (vector DB)  |   summarized, retrievable
+-------------------------------+
            |  on every turn
            v
        retrieved snippets re-enter the context
```

## Step 1 — The short-term buffer

A bounded FIFO of messages, measured in tokens. When it overflows, we
*summarize* the oldest messages into a single message and push that
summary to the long-term store.

```python
from dataclasses import dataclass, field
from typing import Callable

@dataclass
class Message:
    role: str       # "user" | "assistant" | "tool" | "summary"
    content: str
    tokens: int     # measured at insertion

@dataclass
class ShortTermMemory:
    budget: int                                   # max tokens in the buffer
    summarize: Callable[[list[Message]], str]     # see Step 3
    archive:   Callable[[Message], None]          # see Step 2
    messages: list[Message] = field(default_factory=list)

    def add(self, msg: Message) -> None:
        self.messages.append(msg)
        self._evict_if_needed()

    def render(self) -> list[Message]:
        return list(self.messages)

    def _evict_if_needed(self) -> None:
        while sum(m.tokens for m in self.messages) > self.budget:
            # summarize the oldest half and replace with one summary message
            half = max(1, len(self.messages) // 2)
            old, keep = self.messages[:half], self.messages[half:]
            summary_text = self.summarize(old)
            tokens = len(summary_text.split())  # rough; use your tokenizer
            summary_msg = Message("summary", summary_text, tokens)
            self.archive(summary_msg)           # also send to long-term
            self.messages = [summary_msg] + keep
```

Note the design: we do not silently drop messages. Every overflow path
goes through summarization *and* archival. If the summarizer loses
information, the long-term store still has the raw form for retrieval.

## Step 2 — The long-term store

A vector store with `add` and `search`. We are deliberately not using a
vector database library — this is ~30 lines of numpy and proves the idea.

```python
import numpy as np
from typing import Callable

@dataclass
class LongTermMemory:
    embed: Callable[[str], np.ndarray]
    rows: list[tuple[str, np.ndarray]] = field(default_factory=list)

    def add(self, msg: Message) -> None:
        self.rows.append((msg.content, self.embed(msg.content)))

    def search(self, query: str, k: int = 3) -> list[str]:
        if not self.rows:
            return []
        q = self.embed(query)
        scores = [(text, float(np.dot(q, e) / (np.linalg.norm(q) * np.linalg.norm(e))))
                  for text, e in self.rows]
        scores.sort(key=lambda x: -x[1])
        return [text for text, _ in scores[:k]]
```

In production you'd replace the linear scan with HNSW or a real vector
DB. The interface stays identical.

## Step 3 — Summarization

The simplest summarizer is one more LLM call. We pass the old messages
back to a small model with a one-shot prompt asking for a concise summary
that preserves named entities, decisions, and unresolved questions.

```python
def make_summarizer(llm):
    SYSTEM = (
        "Summarize the following conversation in <= 80 tokens. "
        "Preserve: named entities, decisions made, and unresolved questions. "
        "Drop: pleasantries, repetitions."
    )
    def summarize(msgs: list[Message]) -> str:
        body = "\n".join(f"[{m.role}] {m.content}" for m in msgs)
        return llm.complete(system=SYSTEM, user=body)
    return summarize
```

The single most common bug here is summarizers that drop names and IDs.
Test it: feed the summarizer five messages containing a unique ID, ask
it to summarize, then check if the ID survives.

## Step 4 — Putting it together in the agent loop

```python
class Agent:
    def __init__(self, llm, embed, budget=4000):
        self.lt = LongTermMemory(embed=embed)
        self.st = ShortTermMemory(
            budget=budget,
            summarize=make_summarizer(llm),
            archive=self.lt.add,
        )
        self.llm = llm

    def step(self, user_text: str) -> str:
        self.st.add(Message("user", user_text, len(user_text.split())))

        # retrieve from long-term, conditioned on the *current* user turn
        recalled = self.lt.search(user_text, k=3)
        recall_block = "\n".join(f"- {r}" for r in recalled) if recalled else "(none)"

        # render the prompt
        history = self.st.render()
        prompt = (
            f"# Relevant past context\n{recall_block}\n\n"
            + "\n".join(f"[{m.role}] {m.content}" for m in history)
            + "\n[assistant]"
        )

        reply = self.llm.complete(prompt)
        self.st.add(Message("assistant", reply, len(reply.split())))
        return reply
```

A few things worth noticing:

- Retrieval happens **on every turn**, not just on overflow. Otherwise the
  agent forgets the long-term store exists until the buffer fills.
- The retrieval query is the latest user turn. Better: the latest few
  turns concatenated, or a query rewrite step. Try both.
- We embed message content, not (message, role) pairs. The role survives
  through the verbatim text.

## Where this breaks (read this before deploying)

1. **Summarizer drift.** Successive summaries of summaries lose detail
   exponentially. After a few overflows the buffer may contain only
   abstract paraphrases. Mitigation: always keep the most recent N raw
   messages unsummarized; only summarize the older tail.

2. **Retrieval drift.** As the long-term store grows, the same query
   pulls noisier matches. Add a similarity threshold; below it, return
   nothing.

3. **No deduplication.** Two near-identical user turns produce two
   near-identical embeddings; retrieval returns both. Add a deduplication
   pass when writing to long-term.

4. **No forgetting.** The store grows forever. For long-running agents,
   add a decay or eviction policy (least-recently-recalled is a sane
   default).

## What to read next

- The [agent loop guide](../README.md#agents) for how this slots into the
  reason → act → observe cycle.
- Anthropic's "Contextual Retrieval" post for production-grade tricks
  applied to the retrieval step.
- The [RAG pipeline guide](../README.md#retrieval) — same retrieval
  machinery applied at document, not message, granularity.
