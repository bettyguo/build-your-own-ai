# Reward model — from scratch

> **[original]** · part of [`build-your-own-ai/originals/`](README.md).
> _A short, runnable starter guide for a build target where no good public
> from-scratch guide exists today._

**Index entry:** [Training → Reward model](../README.md#training)

---

## The one-line promise

A reward model maps a `(prompt, response)` pair to a scalar score that
approximates human preference. It is the fragile object that every
RLHF / PPO / GRPO pipeline depends on. Most tutorials skip straight to PPO
and treat the reward model as a black box. Here, you build it.

## What you'll understand after

- Why a reward model is just a classifier with a scalar head.
- What pairwise ranking loss is, and why it works even on noisy labels.
- The single most common failure mode: reward hacking. How to spot it.

## Prerequisites

- A small base LM you can load (e.g. a GPT-2-124M or any 100M-class HF model).
- A preference dataset with `prompt`, `chosen`, `rejected` columns
  (Anthropic's `hh-rlhf` is canonical; for a toy run, generate one yourself
  with two different prompts to the same base model).
- PyTorch ≥ 2.0.

## Step 1 — The architecture

A reward model is the base LM with the language-model head removed and a
single linear `→ 1` head bolted on top of the last hidden state. Take the
hidden state at the position of the last non-pad token; project to a
scalar.

```python
import torch
import torch.nn as nn
from transformers import AutoModel  # for the base only — the RM head is ours

class RewardModel(nn.Module):
    def __init__(self, base_name: str = "gpt2"):
        super().__init__()
        self.backbone = AutoModel.from_pretrained(base_name)
        hidden = self.backbone.config.hidden_size
        self.head = nn.Linear(hidden, 1, bias=False)

    def forward(self, input_ids, attention_mask):
        # last_hidden_state: [B, T, H]
        h = self.backbone(input_ids, attention_mask=attention_mask).last_hidden_state
        # take hidden state at last non-pad position
        last_idx = attention_mask.sum(dim=1) - 1                  # [B]
        last_h = h[torch.arange(h.size(0)), last_idx]             # [B, H]
        return self.head(last_h).squeeze(-1)                      # [B]
```

We use `AutoModel` to grab a pretrained backbone — but the reward head is
ours and the training objective below is hand-written.

## Step 2 — The loss

The pairwise loss says: the chosen response's score should beat the
rejected response's score. We minimize `-log σ(r_chosen - r_rejected)`.

```python
def pairwise_loss(r_chosen, r_rejected):
    # Bradley-Terry / pairwise logistic — no margin term.
    return -torch.nn.functional.logsigmoid(r_chosen - r_rejected).mean()
```

That's the entire training objective. Three lines, no library.

## Step 3 — The training loop

```python
import torch
from torch.utils.data import DataLoader
from transformers import AutoTokenizer

tok = AutoTokenizer.from_pretrained("gpt2")
tok.pad_token = tok.eos_token

def tokenize_pair(batch):
    chosen = tok(batch["prompt_and_chosen"],   padding=True, truncation=True,
                 max_length=512, return_tensors="pt")
    rejected = tok(batch["prompt_and_rejected"], padding=True, truncation=True,
                   max_length=512, return_tensors="pt")
    return chosen, rejected

rm = RewardModel("gpt2").cuda()
opt = torch.optim.AdamW(rm.parameters(), lr=1e-5)

for step, batch in enumerate(loader):
    chosen, rejected = tokenize_pair(batch)
    r_c = rm(chosen.input_ids.cuda(),   chosen.attention_mask.cuda())
    r_r = rm(rejected.input_ids.cuda(), rejected.attention_mask.cuda())
    loss = pairwise_loss(r_c, r_r)

    opt.zero_grad()
    loss.backward()
    torch.nn.utils.clip_grad_norm_(rm.parameters(), 1.0)
    opt.step()

    if step % 50 == 0:
        # accuracy = fraction of pairs where chosen > rejected
        with torch.no_grad():
            acc = (r_c > r_r).float().mean().item()
        print(f"step {step}  loss {loss.item():.3f}  pairwise_acc {acc:.3f}")
```

The headline metric is **pairwise accuracy**: on a held-out set of
preference pairs, how often does the chosen response score higher? In our
tiny experiments on 1k pairs this typically rises from ~0.50 (random) to
~0.65–0.75 within a few hundred steps on GPT-2-124M.

## Step 4 — The thing nobody tells you about: reward hacking

A reward model trained on a small dataset will latch onto surface
correlations. The classic failure modes:

- **Length bias.** Longer responses score higher, regardless of quality.
  Sanity check: plot `reward` against `response_length`. If correlation
  > 0.4, your reward model is mostly a length detector.
- **Style bias.** Markdown bullet points score higher because the
  preference dataset preferred them. The model never learned the actual
  helpfulness criterion.
- **Out-of-distribution overconfidence.** On responses unlike anything in
  training, the reward is meaningless but the score is often large in
  magnitude. KL-regularizing the downstream RL run against a reference
  policy partly mitigates this — but the right fix is more diverse data.

Sanity check before plugging into PPO/GRPO: compute `reward(prompt,
random_string)` and `reward(prompt, prompt)`. Both should score *worse*
than your real responses. If they don't, the reward model is broken.

## What to read next

- The original RLHF paper (Stiennon et al. 2020) and InstructGPT (Ouyang
  et al. 2022) for the full pipeline.
- The DPO paper (Rafailov et al. 2023) for the now-popular alternative
  that drops the reward model entirely — and the [DPO-from-scratch
  notebook](https://github.com/rasbt/LLMs-from-scratch/blob/main/ch07/04_preference-tuning-with-dpo/dpo-from-scratch.ipynb)
  for the implementation.

## Caveats and scope

This is a **starter** implementation — ~50 lines of model and loss code,
the minimum that captures the idea. Production reward models add: longer
context, multiple ranked completions, regularization against the base
policy, ensembling, and a lot more data. None of those change the central
object: a base LM with a scalar head, trained with pairwise ranking loss.
That is what you now understand.
