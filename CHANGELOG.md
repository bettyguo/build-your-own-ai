# Changelog

The README's "Last updated" badge tracks the most recent `verified_on` date
across all entries. This file records human-meaningful milestones.

## 2026-05-14 — Initial launch

- 8 categories, 40 build targets, ordered by difficulty.
- **39 verified from-scratch guides** across 26 targets covering
  Foundations, The Model, Training, Inference, Retrieval, Agents,
  Evaluation, and Beyond Text. See `PLANNING/03_verification_log.md`
  for the full audit trail.
- **14 open gaps** intentionally shipped as marked slots rather than
  weak links — these are the real terrain of "what does the AI stack
  lack a good from-scratch guide for in 2026."
- **4 original starter guides** written for high-value gap targets:
  reward model, agent memory, multi-agent orchestration,
  calibration/hallucination check. (KV cache, originally planned, was
  replaced by two excellent verified guides — the curation process
  working as intended.)
- Tooling: `validate_entries.py`, `linkcheck.py`, `build_readme.py`.
- CI: PR validation + weekly scheduled link-check.
