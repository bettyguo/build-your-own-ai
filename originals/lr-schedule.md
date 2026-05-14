# Learning-rate schedule — from scratch

> **[original]** · part of [`build-your-own-ai/originals/`](README.md).
> _A short, runnable starter guide for a build target where no good public
> from-scratch guide exists today._

**Index entry:** [Training → Learning-rate schedule](../README.md#training)

---

## The one-line promise

Two functions, twenty lines of code: **linear warmup** to a peak rate,
then **cosine decay** to a tiny floor. This is the schedule used by
GPT-2, GPT-3, LLaMA, Mistral, and almost every modern pretraining run.
Most tutorials hide it in a `transformers` config; here you write it,
plot it, and watch the loss curves change.

## What you'll understand after

- Why naive constant-LR training spikes early and never recovers.
- Why warmup matters disproportionately for transformers (attention is
  sensitive to early gradient noise).
- How the schedule's shape interacts with batch size — and why
  shrinking the batch without also shrinking the warmup is a recipe for
  divergence.

## Step 1 — Write the schedule as a function of step

The schedule is a multiplier on the peak learning rate. At step `s`:

```python
import math

def lr_multiplier(step: int, warmup_steps: int, total_steps: int,
                  min_ratio: float = 0.1) -> float:
    """Linear warmup → cosine decay.
    Returns a multiplier in [min_ratio, 1.0] applied to the peak LR.
    """
    if step < warmup_steps:
        return step / max(1, warmup_steps)
    progress = (step - warmup_steps) / max(1, total_steps - warmup_steps)
    progress = min(progress, 1.0)
    cosine = 0.5 * (1.0 + math.cos(math.pi * progress))
    return min_ratio + (1.0 - min_ratio) * cosine
```

Two parameters that matter: `warmup_steps` (typical: 2–10% of total
steps for LM pretraining) and `min_ratio` (typical: 0.1, i.e. the floor
is 10% of peak).

## Step 2 — Plug it into the optimizer

PyTorch's `LambdaLR` takes any callable that returns a multiplier:

```python
import torch
from torch.optim.lr_scheduler import LambdaLR

peak_lr = 3e-4
warmup_steps = 200
total_steps = 2000

opt = torch.optim.AdamW(model.parameters(), lr=peak_lr)
sched = LambdaLR(opt, lr_lambda=lambda s: lr_multiplier(s, warmup_steps, total_steps))
```

Call `sched.step()` once per optimizer step (not per epoch). The
optimizer's current LR is now `peak_lr * lr_multiplier(step, ...)`.

## Step 3 — Plot it before you train

The single most useful debugging artifact in this whole topic. If your
schedule looks wrong, your run will fail in ways that masquerade as
data or model bugs.

```python
import matplotlib.pyplot as plt

steps = range(total_steps)
lrs = [peak_lr * lr_multiplier(s, warmup_steps, total_steps) for s in steps]
plt.plot(steps, lrs)
plt.xlabel("step")
plt.ylabel("learning rate")
plt.axvline(warmup_steps, ls="--", color="grey", label="end of warmup")
plt.legend()
plt.show()
```

You should see: a triangle ramp up to peak by step 200, then a smooth
half-cosine down to 3e-5 (10% of 3e-4) by step 2000.

## Step 4 — The experiment that makes it click

Train a tiny LM for 2000 steps three ways and overlay the loss curves:

1. **Constant LR.** `peak_lr = 3e-4`, no schedule.
2. **Cosine decay, no warmup.** `warmup_steps = 0`.
3. **Warmup + cosine.** the function above.

What you'll see, robustly across small transformer runs:

- **Constant LR**: loss spikes in the first ~50 steps as attention
  scores blow up before the residual stream stabilizes. Sometimes
  recovers, often gets stuck in a worse plateau than (3).
- **Cosine without warmup**: same early instability, plus the peak LR
  is applied immediately to a model that can't handle it.
- **Warmup + cosine**: smooth descent. The warmup phase visibly
  flattens the early loss curve; cosine decay slowly settles the model
  into a low-loss basin.

## Step 5 — The interaction nobody warns you about: batch size

When you halve the batch size, the effective gradient noise doubles.
You typically want to:

- **Halve the peak LR** (some teams keep it; both are defensible).
- **Roughly *quadruple* the warmup steps** if your peak LR stayed put —
  small batches need more steps to give attention scores time to
  settle.

The wrong move: shrink batch, keep peak LR, keep warmup. Result: an
early divergence that looks like a bad initialization but isn't.

## Step 6 — Three honest gotchas

1. **`sched.step()` placement.** Call it after `optimizer.step()`, not
   before. Calling it before causes the *first* update to use the
   wrong LR (step 0 returns ratio 0 in warmup mode, which means no
   update happens).
2. **Gradient accumulation.** If you accumulate over N micro-batches,
   `sched.step()` should run once per *optimizer* step, not once per
   micro-batch. Otherwise the schedule "completes" N× faster than
   intended.
3. **Resuming from a checkpoint.** Save and restore the *scheduler*
   state, not just the optimizer. Otherwise a resumed run starts at
   step 0 of the warmup and re-warms.

## What to read next

- The [training-loop entry](../README.md#training) — the schedule's
  natural home is inside a fully written training loop.
- The [optimizer entry](../README.md#training) — Adam / AdamW updates
  rules show why the LR multiplier matters at each parameter.
- "Attention Is All You Need" (Vaswani et al. 2017) §5.3 — the original
  warmup recipe for Transformers, where this whole shape came from.
