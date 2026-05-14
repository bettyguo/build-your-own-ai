# Eval harness — from scratch

> **[original]** · part of [`build-your-own-ai/originals/`](README.md).
> _A short, runnable starter guide for a build target where no good public
> from-scratch guide exists today._

**Index entry:** [Evaluation → Eval harness](../README.md#evaluation)

---

## The one-line promise

An eval harness is four small abstractions: a **task** (the dataset
and how to prompt it), a **runner** (loops over examples, calls the
model), a **scorer** (one number per example), and a **reporter**
(aggregates and surfaces results). ~200 lines of Python and you have a
miniature `lm-evaluation-harness` that's actually pluggable.

## What you'll understand after

- Why eval harnesses are 80% data engineering and 20% model code.
- What makes results *comparable* across model versions (and the four
  ways that breaks).
- How to plug in a new task in five minutes, which is the test of
  whether your harness is real or just a script.

## Step 1 — The four abstractions

```python
from dataclasses import dataclass, field
from typing import Callable, Iterable

@dataclass
class Example:
    """One row of a dataset."""
    prompt: str
    expected: str
    meta: dict = field(default_factory=dict)

@dataclass
class Task:
    """Everything needed to evaluate on a dataset."""
    name: str
    examples: Iterable[Example]
    score_fn: Callable[[str, str, dict], float]   # (output, expected, meta) → [0, 1]
    template_fn: Callable[[Example], str] = lambda e: e.prompt
```

A task is data + a scoring function + a prompt template. Notice what
*isn't* in `Task`: the model. That's the load-bearing design choice —
tasks are model-agnostic.

## Step 2 — The runner

The runner is dumb. It iterates, calls the model, scores, collects.

```python
@dataclass
class Result:
    task: str
    example_id: int
    prompt: str
    output: str
    expected: str
    score: float

def run(task: Task, model_fn: Callable[[str], str],
        limit: int | None = None) -> list[Result]:
    out: list[Result] = []
    for i, ex in enumerate(task.examples):
        if limit is not None and i >= limit:
            break
        prompt = task.template_fn(ex)
        output = model_fn(prompt)
        score = task.score_fn(output, ex.expected, ex.meta)
        out.append(Result(task.name, i, prompt, output, ex.expected, score))
    return out
```

`model_fn: (prompt) -> output` is the entire model interface. You can
plug in Claude, GPT, a local LM, or a stub for testing — same signature.

## Step 3 — A real scoring function

Three patterns cover most of what people do:

```python
def exact_match(output: str, expected: str, _meta) -> float:
    return float(output.strip() == expected.strip())

def normalized_match(output: str, expected: str, _meta) -> float:
    norm = lambda s: " ".join(s.lower().split())
    return float(norm(output) == norm(expected))

def multiple_choice(output: str, expected: str, meta) -> float:
    """expected is the letter; meta['choices'] lists them."""
    out = output.strip().upper()
    # accept "A", "(A)", "A.", "**A**" etc.
    return float(out and out[0] == expected.strip().upper())
```

For more complex tasks (math reasoning, code execution, free-form QA),
you'd write `score_fn = lambda o, e, m: judge_with_llm(o, e)`. Same
shape; different implementation.

## Step 4 — A concrete task

```python
mcq = Task(
    name="toy-mcq",
    examples=[
        Example(prompt="Q: 2+2?\nA) 3\nB) 4\nC) 5\nAnswer:",
                expected="B", meta={"choices": ["A", "B", "C"]}),
        Example(prompt="Q: capital of France?\nA) Berlin\nB) Madrid\nC) Paris\nAnswer:",
                expected="C", meta={"choices": ["A", "B", "C"]}),
    ],
    score_fn=multiple_choice,
)
```

Running it:

```python
def claude_fn(prompt: str) -> str:
    # however you call your model
    return client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=8,
        messages=[{"role": "user", "content": prompt}],
    ).content[0].text

results = run(mcq, claude_fn)
acc = sum(r.score for r in results) / len(results)
print(f"{mcq.name}: accuracy {acc:.3f}")
```

## Step 5 — The reporter

Aggregating one task is trivial; aggregating five tasks across three
model versions is where harnesses earn their keep.

```python
import json

def report(all_results: dict[str, list[Result]]) -> dict:
    """all_results: {task_name: [Result, ...], ...}"""
    out = {}
    for task_name, results in all_results.items():
        if not results:
            continue
        out[task_name] = {
            "n": len(results),
            "mean_score": sum(r.score for r in results) / len(results),
            "n_correct": sum(1 for r in results if r.score >= 0.99),
        }
    return out

def save(all_results, path):
    with open(path, "w") as f:
        json.dump({k: [r.__dict__ for r in v] for k, v in all_results.items()},
                  f, indent=2)
```

Save the per-example results, not just the aggregate. When a future
model regression hits, you'll need the raw `output` field to diff.

## Step 6 — The four ways "comparable" breaks

Eval results stop being comparable across runs when *any* of these
silently drift:

1. **The prompt template.** Adding a single newline can shift accuracy
   by 5%. Version the `template_fn` and log its hash with every run.
2. **The decoding params.** Greedy vs sampling at temperature 0.7 are
   different evals. Pin temperature, top-p, max-tokens; log them.
3. **The data split.** "MMLU" today is not the MMLU of three years
   ago. Pin the dataset version (commit hash, HF dataset revision).
4. **The scoring function.** Loosening `normalized_match` to accept
   substrings will inflate every score. Version the scorer.

A real harness either pins all four explicitly or refuses to compare
runs whose pinned values differ. The toy version above pins none of
them — adding that discipline is the next step after this guide.

## Step 7 — Why not just use `lm-evaluation-harness`?

EleutherAI's `lm-evaluation-harness` is excellent and is the right
tool for serious benchmarking. But if you've never built one, you
won't understand:

- Why custom tasks are so much harder than the docs suggest.
- Where the data-pipeline failure modes are.
- What "few-shot" actually does to your inputs (it injects context
  ahead of every example via the same `template_fn` mechanism).

The version above is the kernel `lm-evaluation-harness` wraps in
considerably more code. Build this first; you'll read theirs with new
eyes.

## What to read next

- The [LLM-as-judge entry](../README.md#evaluation) — for tasks where
  exact match doesn't work, the `score_fn` is itself an LLM call.
- The [calibration / hallucination original](calibration-hallucination.md)
  — another `score_fn` shape, where the model's confidence is part of
  the score.
- `EleutherAI/lm-evaluation-harness` — the production version. The
  abstractions match almost one-for-one; the engineering is the
  difference.
