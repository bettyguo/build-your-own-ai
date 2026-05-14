# PHASE 6 — Hostile reviewer pass

> Re-read the repo as three skeptical readers in turn:
> (a) an experienced AI engineer checking whether every linked guide is
>     actually good and actually from-scratch;
> (b) a learner who would be misled if a "from scratch" guide is secretly
>     a library wrapper;
> (c) a skeptical HN commenter ("isn't this just build-your-own-x
>     filtered, or just a links page?").
>
> Verdict: ship-ready, with the small set of fixes below already applied.

---

## What the reviewer would catch — and what was done

### A. The AI-engineer reviewer

**A1. "Why is `lucidrains/mixture-of-experts` listed when the author's own
README says to use ST-MoE instead?"**
→ **Fixed.** `st-moe-pytorch` is now the primary entry for
`mixture-of-experts`; the older repo is kept as a stepping-stone with an
explicit note. Verification log updated.

**A2. "The `small-encoder-lm` target has only one guide — feels thin."**
→ **Fixed.** Added COAX's "Building BERT with PyTorch from scratch" as a
second guide (last updated April 2026 — current). The category now has
two complementary entries: labml.ai (annotated objective + masking) and
COAX (full architecture build).

**A3. "Karpathy appears as author on 9 separate entries — is this a curated
index or a Karpathy directory?"**
→ **No fix needed; honest disclosure noted.** The concentration is real
and reflects a real fact: Karpathy is the leading author of from-scratch
ML pedagogy. The alternatives I considered for the same targets
(transformer block / inference engine / tokenizer / autograd / backprop)
were uniformly weaker. The `PLANNING/03_verification_log.md` shows the
considered set so a reader can audit independently. The right defense is
transparency, not artificial diversification.

**A4. "The Annotated Transformer is 2018 — pre-PyTorch-2.0, is it still
correct?"**
→ **Kept; technique is timeless.** The transformer architecture itself
hasn't drifted; the Annotated Transformer is the canonical
implementation walkthrough. Any reader running it will need minor PyTorch
fixes but the pedagogy is intact. Will re-confirm in the next quarterly
audit.

**A5. "AssemblyAI ASR post is from 2020. Same question."**
→ **Kept; CTC is the most stable loss in ASR.** Re-confirmed the article
loads, the code is in a publicly cloneable repo, and the loss function
hasn't changed.

**A6. "What about MLX, Triton, or Mojo-based from-scratch guides?"**
→ **Noted as a future direction.** Today, ~90% of from-scratch ML
pedagogy is PyTorch + (much smaller) JAX. MLX / Triton / Mojo will be
added as alternative-language guides appear. Tracked as an open gap
candidate for the next audit.

### B. The misled-learner reviewer

**B1. "The README shows the author, kind, and cost — but where's the
proof that each guide is actually from-scratch?"**
→ **Fixed.** The README footer now points at
`PLANNING/03_verification_log.md`, which contains the
`from_scratch_evidence` string for every guide. The full audit trail is
one click away from any reader.

**B2. "Some guides use `transformers.AutoModel` for the backbone — is
that from-scratch?"**
→ **Honest disclosure.** Two entries (the reward-model original and
moein-shariatnia/OpenAI-CLIP) use pretrained backbones from `timm` /
`transformers` for the parts that aren't the build target. The reward
head, the contrastive objective, and the CLIP projection heads are all
written by hand. The `from_scratch_evidence` field in each entry
explicitly says so. A reader who wants to also build the backbone from
scratch is pointed at the `small-gpt` / `small-encoder-lm` entries.

**B3. "Why is `learnbybuilding.ai`'s RAG tutorial missing? It calls
itself 'from scratch.'"**
→ **Documented rejection.** Verification log §"Rejected" entry 1: it
skips chunking and embeddings entirely, using Jaccard similarity. The
author acknowledges this in their own "Areas for improvement" section.
Keeping it would erode trust.

**B4. "Some guides cost money (Raschka's book) — is that against the
'curated index of free guides' spirit?"**
→ **Not against the spirit; marked clearly.** Two paid entries
(Raschka's book referenced from `small-gpt` and `sft`) are tagged
`paid`. The book is genuinely the best from-scratch teaching resource of
its kind; excluding it would be dishonest curation. A free pointer (the
public code repo) is included alongside.

### C. The skeptical HN commenter

**C1. "Isn't this just `build-your-own-x` filtered for AI?"**
→ **Answered in README §"Why this exists" and in
`PLANNING/00_think.md`.** `build-your-own-x` has 3 AI categories with
roughly 20 entries total. This has 8 categories, 40 targets, a
verification log, four written-for-this-repo originals filling gaps no
existing tutorial covers cleanly. Different scope, different bar.

**C2. "10 of your 14 gaps just say 'no guide.' That's 25% of the index
that's empty."**
→ **Honest disclosure.** The gaps are marked as gaps, not filled with
weak links — that is the *opposite* failure mode of every other AI list.
The 4 originals fill the highest-leverage gaps. The remaining 10 are an
explicit invitation to the community (the PR template makes contributing
straightforward). See "Open gaps as wanted-issues" below.

**C3. "What stops this rotting in 6 months?"**
→ **Maintenance is documented.** `docs/MAINTENANCE.md` defines weekly
automated linkcheck, monthly issue triage, quarterly re-stamp of every
`verified_on` date, yearly taxonomy review. The verification log is
designed to be re-audited rather than rewritten.

**C4. "You wrote 4 originals at launch — is that really enough to
differentiate?"**
→ **Yes, by design.** Phase 0's discipline was "don't pad originals."
Each one is short (~150 lines), runnable, and tackles a target where I
could not find a single existing good public guide. Five would have been
indulgent; four are the right count. (The originally-planned KV cache
original was dropped during research when Raschka's and HF nanoVLM's
excellent from-scratch guides surfaced — a feature, not a bug.)

### D. The originals reviewer

Re-read each original as a learner who would actually run the code:

- `reward-model.md` — pulls weight. The pairwise-loss + reward-hacking
  failure-modes section is the differentiator. **Ship.**
- `agent-memory.md` — pulls weight. The four "where this breaks"
  failure modes are not in any existing tutorial. **Ship.**
- `multi-agent.md` — pulls weight. The "when NOT to use multi-agent"
  test table is the honest content most tutorials avoid. **Ship.**
- `calibration-hallucination.md` — pulls weight. ECE + reliability
  diagram + selective prediction in one ~150-line walkthrough is not
  available elsewhere. **Ship.**

No original was found to be padding. None of the four duplicate existing
material.

---

## Open gaps as wanted-issues (for GitHub Issues post-push)

Each of the 10 remaining open gaps below should become a "wanted build
target" issue at launch. The issue body for each: brief description of
what a good from-scratch guide for it would look like, plus a pointer to
the relevant index entry.

| # | Target | Category | Hint for contributors |
|---|---|---|---|
| 1 | `embedding-layer` | Foundations | Tied vs untied embeddings, comparison plot of L2 norms, training a tiny token2vec end to end. |
| 2 | `lr-schedule` | Training | Warmup + cosine on a small run, with and without warmup, with the loss-curve comparison plot. |
| 3 | `quantization` | Inference | A from-scratch INT8 / INT4 PTQ pipeline: per-channel scales, outlier handling, accuracy vs throughput measurement. (NOT a `bitsandbytes` / `auto-gptq` tutorial.) |
| 4 | `hybrid-search` | Retrieval | BM25 + dense fused with Reciprocal Rank Fusion and learned weighting, evaluated on a small relevance set. |
| 5 | `reranker` | Retrieval | A cross-encoder trained from scratch on a small relevance dataset. Two-stage retrieval pipeline with the cost/quality trade-off measured. |
| 6 | `tool-layer` | Agents | A schema-validated tool dispatcher: JSON-Schema, argument validation, error recovery — independent of any specific agent loop. |
| 7 | `eval-harness` | Evaluation | A pluggable task runner in ~200 lines: task abstraction, prompt template, scoring function, reproducibility seed. (NOT a `lm-evaluation-harness` tutorial.) |

The four originals at launch cover the other four gaps (reward-model,
agent-memory, multi-agent, calibration-hallucination).

A post-Phase-6 gap-filling sweep filled three additional gaps with
verified guides (`sampling`, `mixed-precision`, `ppo-grpo`) — see the
verification log for the additions and the rationale.

---

## What did NOT need fixing

- Tooling — `validate_entries.py`, `linkcheck.py`, `build_readme.py` are
  small, clear, well-tested.
- CI — both workflows are sensible; PR-time validation + drift check +
  quick linkcheck, scheduled full linkcheck with auto-issue.
- Taxonomy — 8 ordered categories cover the modern stack cleanly. No
  obviously missing category, no obviously redundant category.
- Entry schema — the `from_scratch_evidence` field is doing its job.
- Naming — "build-your-own-ai" is the right noun; the README leads with
  it.

---

## State at end of Phase 6

| | |
|---|---|
| Build targets | 40 |
| Verified guides | **41** (up from 39 after this review; **45** after the post-Phase-6 gap-filling sweep) |
| Open gaps | 14 after Phase 6 → **11** after gap-filling sweep |
| Originals | 4 |
| URLs link-checked live | 53/53 after Phase 6 → **57/57** after gap-filling sweep (3 sibling-repo placeholders intentionally ignored throughout) |
| Rejected guides | 5 after Phase 6 → **6** (added the rejection of Amit Chaudhary's tool-calling article for being partial) |
| Fixes applied during this review | 2 entry-level (MoE / encoder-LM) + 1 README footer pointer |

The hostile-review pass made the index *better*, not just *defended*. It
upgraded one entry (MoE), broadened another (encoder-LM), and surfaced
the curation paper trail to readers (verification-log pointer in README).

The subsequent gap-filling sweep added 4 more verified guides across 3
gap targets, taking total guide count from 41 → 45 and open gaps from
14 → 11. Importantly, when one more candidate (Amit Chaudhary's tool
calling article) was found to only partially cover its target, it was
rejected rather than padded in — the bar held.
