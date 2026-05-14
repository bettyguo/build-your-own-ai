# `originals/`

Short, original from-scratch starter guides for build targets where no good
public guide exists today. These are the **differentiation lever** of this
repo — written to fill the worst gaps, not to author an alternative
textbook.

Discipline: each original is ≤ ~1500 words and ≤ ~150 lines of code; it must
be genuinely runnable; and it must clearly mark itself as `[original]` so a
reader never mistakes it for a curated link.

## Current originals

| Target | Why it exists |
|---|---|
| [`reward-model.md`](reward-model.md) | RLHF tutorials skip straight to PPO; the reward model is the foundational object. |
| [`agent-memory.md`](agent-memory.md) | Most current tutorials lean on a framework; the from-scratch version is genuinely missing. |
| [`multi-agent.md`](multi-agent.md) | The "without CrewAI / AutoGen" build is rare and high-value. |
| [`calibration-hallucination.md`](calibration-hallucination.md) | Eval guides exist; this specific lens almost none. |
| [`lr-schedule.md`](lr-schedule.md) | The warmup + cosine recipe everyone uses, with the loss-curve experiment that makes it click — usually hidden inside larger tutorials. |
| [`reranker.md`](reranker.md) | Cross-encoder from scratch — every other tutorial routes through `sentence-transformers`. |
| [`tool-layer.md`](tool-layer.md) | A schema-validated tool dispatcher with the JSON-validation + error-recovery patterns that frameworks hide. |
| [`eval-harness.md`](eval-harness.md) | Task / runner / scorer / reporter — the four-abstraction kernel of `lm-evaluation-harness`. |

Note: KV cache was originally planned as an `originals/` candidate. During
Phase 3 verification, Sebastian Raschka's "Understanding and Coding the KV
Cache in LLMs from Scratch" and Hugging Face's "KV Cache from scratch in
nanoVLM" were both found to cover it cleanly — so the target ships with
verified guides rather than an original. This is the verification process
working as intended.

The four additional originals (lr-schedule, reranker, tool-layer, eval-harness)
were written after two research sweeps confirmed those targets genuinely
lack public from-scratch guides — they fill verified gaps, not padding.

## Style

- One topic per file. Open with the build target's one-line promise.
- Show the **smallest** correct implementation first; expand outward only
  where the reader gains something concrete.
- Cross-reference the index entry: each original starts with `Index entry:
  [Category → Target](../README.md#anchor)`.
- Cite primary sources for any claim that isn't proved by the code itself.
