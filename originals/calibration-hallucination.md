# Calibration / hallucination check — from scratch

> **[original]** · part of [`build-your-own-ai/originals/`](README.md).
> _A short, runnable starter guide for a build target where no good public
> from-scratch guide exists today._

**Index entry:** [Evaluation → Calibration / hallucination check](../README.md#evaluation)

---

## The one-line promise

A well-calibrated model that says "I'm 90% sure" is right about 90% of
the time. The gap between stated confidence and real accuracy —
**Expected Calibration Error (ECE)** — is the single most useful number
for spotting hallucinations that look confident. Most eval guides talk
about accuracy; this one teaches you to measure trust.

## What you'll understand after

- How to **elicit** a confidence score from a model that doesn't expose
  raw logits.
- How to **bin** predictions and compute Expected Calibration Error.
- How to plot a **reliability diagram** so a single picture tells you
  whether the model is over- or underconfident.
- How to convert ECE into **selective prediction**: "answer only when
  confidence ≥ τ; abstain otherwise."

## Step 1 — Eliciting confidence

For an open-weights model, the cleanest confidence signal is the model's
own probability for its chosen answer — i.e. softmax over the answer
token logits. For closed-weights APIs, you ask:

> "Provide your answer **and** a confidence value between 0 and 100
> reflecting how sure you are."

This is noisier than raw logits but it works. Validate it by checking
that the resulting confidences span the [0, 1] range — a model that
always says "95" is not actually expressing confidence.

```python
import re
from dataclasses import dataclass

@dataclass
class Prediction:
    answer: str
    confidence: float    # in [0, 1]
    correct: bool        # filled in after grading

PROMPT = """
Answer the question. Then on a new line write "Confidence: X" where X is
an integer 0-100 reflecting your confidence in the answer.

Question: {question}
"""

def elicit(llm, question: str) -> tuple[str, float]:
    raw = llm.complete(PROMPT.format(question=question))
    answer_line, conf_line = raw.split("Confidence:")
    answer = answer_line.strip()
    conf = float(re.search(r"\d+", conf_line).group()) / 100.0
    return answer, min(max(conf, 0.0), 1.0)
```

## Step 2 — Computing Expected Calibration Error

Bin predictions by confidence, compute accuracy within each bin, and take
the weighted absolute gap.

```python
import numpy as np

def expected_calibration_error(preds: list[Prediction], n_bins: int = 10) -> float:
    confs    = np.array([p.confidence for p in preds])
    corrects = np.array([float(p.correct) for p in preds])

    edges = np.linspace(0, 1, n_bins + 1)
    ece = 0.0
    for lo, hi in zip(edges[:-1], edges[1:]):
        mask = (confs > lo) & (confs <= hi)
        if mask.sum() == 0:
            continue
        avg_conf = confs[mask].mean()
        avg_acc  = corrects[mask].mean()
        weight   = mask.sum() / len(preds)
        ece += weight * abs(avg_conf - avg_acc)
    return ece
```

A perfectly calibrated model has ECE = 0. In practice you see:

- Frontier chat models on simple factual QA: ECE ≈ 0.05–0.15. Slightly
  overconfident.
- Smaller open models on the same: ECE ≈ 0.15–0.35. Mostly overconfident
  on questions they don't know.
- Any model in a domain it hasn't seen: ECE ≈ 0.3+. The confidence
  signal is barely correlated with correctness.

## Step 3 — The reliability diagram

One plot tells you everything.

```python
import matplotlib.pyplot as plt

def reliability_diagram(preds: list[Prediction], n_bins: int = 10):
    confs    = np.array([p.confidence for p in preds])
    corrects = np.array([float(p.correct) for p in preds])
    edges = np.linspace(0, 1, n_bins + 1)
    mids = (edges[:-1] + edges[1:]) / 2

    accs = []
    for lo, hi in zip(edges[:-1], edges[1:]):
        mask = (confs > lo) & (confs <= hi)
        accs.append(corrects[mask].mean() if mask.sum() else np.nan)

    plt.figure(figsize=(5, 5))
    plt.plot([0, 1], [0, 1], "k--", label="perfectly calibrated")
    plt.bar(mids, accs, width=1.0 / n_bins, edgecolor="black", alpha=0.7,
            label="model")
    plt.xlabel("predicted confidence")
    plt.ylabel("empirical accuracy")
    plt.title("Reliability diagram")
    plt.legend()
    plt.show()
```

If the bars sit consistently *below* the diagonal, the model is
**overconfident** — the classic hallucination signature. If consistently
above, it is underconfident and you're leaving useful signal unused.

## Step 4 — Selective prediction

Once you trust your confidence signal even a little, you can choose to
**abstain** when confidence is below a threshold τ. This trades coverage
(fraction of questions answered) for selective accuracy (accuracy on the
ones you do answer).

```python
def selective_accuracy(preds: list[Prediction], tau: float) -> tuple[float, float]:
    answered = [p for p in preds if p.confidence >= tau]
    if not answered:
        return 0.0, 0.0
    selective_acc = sum(p.correct for p in answered) / len(answered)
    coverage = len(answered) / len(preds)
    return selective_acc, coverage
```

A useful operating point: pick the largest τ such that coverage ≥ 50%.
That τ is your "answer only when reasonably sure" threshold.

## Step 5 — Sanity-checking your hallucination check

Two failure modes to spot before you trust the numbers:

1. **The model always reports the same confidence.** If the elicited
   confidence has standard deviation < 0.05, your confidence channel is
   broken — change the prompt (ask for a more granular score, or for
   reasoning before the score) until you see real spread.
2. **Confidence is bimodal at 50 and 100.** Common for instruction-tuned
   models that "hedge" or "commit." Calibration on bimodal output is
   meaningless. Force a continuous integer 0–100 in the prompt and parse
   strictly.

## What to read next

- "On Calibration of Modern Neural Networks" (Guo et al. 2017) — the
  paper that put ECE on the map.
- "Language Models (Mostly) Know What They Know" (Kadavath et al. 2022)
  — large LMs' self-confidence is surprisingly informative.
- The [eval harness gap](../README.md#evaluation) — the calibration
  check above is one task in a real eval harness; the broader harness
  pattern is the next thing to build.
