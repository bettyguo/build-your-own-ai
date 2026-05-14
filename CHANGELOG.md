# Changelog

The README's "Last updated" badge tracks the most recent `verified_on` date
across all entries. This file records human-meaningful milestones.

## 2026-05-14 — Initial launch

- 8 categories, **43 build targets**, ordered by difficulty.
- **54 verified from-scratch guides** across 35 targets covering
  Foundations, The Model, Training, Inference, Retrieval, Agents,
  Evaluation, and Beyond Text. See `PLANNING/03_verification_log.md`
  for the full audit trail.
- **8 original starter guides** for targets where verification confirmed
  no good public from-scratch guide exists: reward model, agent memory,
  multi-agent orchestration, calibration/hallucination, learning-rate
  schedule, cross-encoder reranker, tool-calling layer, eval harness.
  (KV cache was originally planned as an original but two excellent
  external guides surfaced during verification — that target now ships
  with curated links.)
- **Every target is covered.** No empty gap shipped at launch — each
  has either verified external guides or a curator-authored original.
- Tooling: `validate_entries.py`, `linkcheck.py`, `build_readme.py`.
- CI: PR validation + weekly scheduled link-check.

### Phase-7 expansion notes

The launch state reflects a Phase-7 disciplined expansion on top of the
master prompt's six phases:

- **3 new build targets** added where the original taxonomy had real
  holes: LoRA (parameter-efficient fine-tuning), distributed training
  (DDP from scratch), long-context RoPE scaling.
- **4 new originals** written for the 4 targets that survived two
  research sweeps without yielding a from-scratch guide that met the
  curation bar.
- Total expansion: 40 → 43 targets, 49 → 54 verified guides, 4 → 8
  originals, 0 → 0 weak / mislabeled guides slipped in. The bar held.
