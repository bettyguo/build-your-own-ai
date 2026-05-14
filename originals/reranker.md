# Reranker (cross-encoder) — from scratch

> **[original]** · part of [`build-your-own-ai/originals/`](README.md).
> _A short, runnable starter guide for a build target where no good public
> from-scratch guide exists today._

**Index entry:** [Retrieval → Reranker (cross-encoder)](../README.md#retrieval)

---

## The one-line promise

A cross-encoder reads `(query, document)` jointly and emits one
relevance score. It's slower per pair than a bi-encoder, but
dramatically more accurate on the small candidate set a retriever
hands it. Every production search stack has one; almost no tutorial
builds one without `sentence-transformers`.

## What you'll understand after

- Why the cross-encoder beats the bi-encoder *only* in the rerank stage.
- How to fine-tune a small backbone (e.g. `distilbert-base-uncased`)
  into a relevance scorer with one linear head and one loss.
- The two-stage "retrieve cheap, rerank expensive" pattern, with the
  trade-off measured in code, not vibes.

## Step 1 — The architecture

A cross-encoder is a base encoder (BERT, MiniLM, anything BERT-shaped)
with a single-output classifier head on the `[CLS]` token. The query
and document share one sequence, separated by a special token.

```python
import torch
import torch.nn as nn
from transformers import AutoModel, AutoTokenizer

class CrossEncoder(nn.Module):
    def __init__(self, backbone: str = "distilbert-base-uncased"):
        super().__init__()
        self.backbone = AutoModel.from_pretrained(backbone)
        hidden = self.backbone.config.hidden_size
        self.head = nn.Linear(hidden, 1)

    def forward(self, input_ids, attention_mask):
        # [CLS] hidden state → scalar relevance logit
        out = self.backbone(input_ids, attention_mask=attention_mask)
        cls = out.last_hidden_state[:, 0]
        return self.head(cls).squeeze(-1)
```

The backbone is pretrained; the head is ours and is the only thing
that's truly built from scratch here. The point of the build target is
to expose the *training procedure*.

## Step 2 — Data

You need `(query, document, label)` triples where the label is 1 for
relevant and 0 for not. For toy experiments, you can synthesize them:
treat any document that contains the query's keywords as positive, the
rest as negative. For real datasets, MS MARCO triples are canonical.

```python
from dataclasses import dataclass

@dataclass
class Example:
    query: str
    doc: str
    label: float  # 1.0 or 0.0
```

The data ratio matters: in practice you want roughly 1 positive to 4–8
hard negatives. "Hard" negatives are documents the bi-encoder retrieved
but a human marked irrelevant — much more informative than random
negatives.

## Step 3 — The loss

For pointwise labels, binary cross-entropy with logits is the right
call. For *pairwise* preference data (chosen vs rejected, no absolute
label), use the same pairwise loss as the [reward-model
guide](reward-model.md).

```python
import torch.nn.functional as F

def pointwise_loss(scores, labels):
    return F.binary_cross_entropy_with_logits(scores, labels)
```

That's it. The loss does the work; the only nontrivial part is the
data you feed it.

## Step 4 — Training loop

```python
tok = AutoTokenizer.from_pretrained("distilbert-base-uncased")
model = CrossEncoder().cuda()
opt = torch.optim.AdamW(model.parameters(), lr=2e-5)

def batchify(examples, max_len=256):
    pairs = [(e.query, e.doc) for e in examples]
    enc = tok([q for q, _ in pairs], [d for _, d in pairs],
              padding=True, truncation=True, max_length=max_len,
              return_tensors="pt")
    labels = torch.tensor([e.label for e in examples])
    return enc, labels

for step, batch in enumerate(loader):
    enc, labels = batchify(batch)
    scores = model(enc.input_ids.cuda(), enc.attention_mask.cuda())
    loss = pointwise_loss(scores, labels.cuda())
    opt.zero_grad(); loss.backward(); opt.step()

    if step % 50 == 0:
        with torch.no_grad():
            preds = (scores.sigmoid() > 0.5).float()
            acc = (preds == labels.cuda()).float().mean().item()
        print(f"step {step}  loss {loss.item():.3f}  acc {acc:.3f}")
```

A few hundred steps on a couple of thousand examples gets a small
DistilBERT cross-encoder from random (acc ≈ 0.5) to useful (acc ≈
0.80–0.90 on synthetic data).

## Step 5 — The two-stage pipeline

The cross-encoder is too slow to score every (query, document) pair
against a 1M-doc corpus. The standard pattern:

1. **Retrieve** top-100 with a cheap method (BM25 or a bi-encoder).
2. **Rerank** those 100 with the cross-encoder.
3. **Return** the top-10 by cross-encoder score.

```python
def rerank(query, candidate_docs, k=10):
    pairs = [(query, doc) for doc in candidate_docs]
    enc = tok([q for q, _ in pairs], [d for _, d in pairs],
              padding=True, truncation=True, max_length=256,
              return_tensors="pt")
    with torch.no_grad():
        scores = model(enc.input_ids.cuda(), enc.attention_mask.cuda())
    pairs_sorted = sorted(zip(candidate_docs, scores.tolist()),
                          key=lambda x: -x[1])
    return [doc for doc, _ in pairs_sorted[:k]]
```

The win, measured: on a synthetic 1k-doc benchmark, BM25 alone might
hit recall@10 ≈ 0.60. BM25 → cross-encoder rerank typically pushes
this to ≈ 0.80–0.85. Cost: ~100ms per query for the rerank step on
GPU, vs ~1ms for BM25 alone. That's the trade-off the entire two-stage
pattern exists to make.

## Step 6 — Where this breaks

- **Document truncation.** If the relevant span is near the end of a
  long doc and you truncate at 256 tokens, you're throwing the answer
  away. Either chunk documents into 256-token windows and rerank
  windows, or use a longer-context backbone.
- **Domain mismatch.** A cross-encoder trained on MS MARCO will rerank
  general web text well and code documentation poorly. Fine-tune on
  the actual target distribution; don't trust off-the-shelf rerankers.
- **The bi-encoder bottleneck.** If your retriever surfaces 100
  candidates and the right doc is at rank 200, no reranker can save
  you. Recall@100 of the retriever is the ceiling.

## What to read next

- The [BM25 entry](../README.md#retrieval) — what the first stage
  usually is.
- The [vector search entry](../README.md#retrieval) — the bi-encoder
  alternative for stage 1.
- The [hybrid-search entry](../README.md#retrieval) — fuse BM25 and
  dense before the cross-encoder for the best recall.
