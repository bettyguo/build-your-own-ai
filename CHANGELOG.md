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

### Phase-8 expansion notes

A second breadth pass added **5 new build targets**, **1 secondary
guide**, **0 weak guides slipped in**:

- `layer-normalization` (Foundations), `grouped-query-attention` (Model),
  `retrieval-evaluation` (Retrieval), `vision-transformer` (Beyond Text),
  `latent-diffusion` (Beyond Text).
- Plus `karpathy/llm.c` added as a second guide to `small-gpt`.
- Phase 8 totals: 43 → 50 targets, 54 → 65 guides, 8 → 8 originals.

### Phase-9 expansion notes (2026-05-14)

A safety/alignment pass. Two targets folded into existing categories:
`constitutional-ai` (Training) with Cameron Wolfe + the open RLHF Book,
and `watermarking` (Inference) with the canonical Kirchenbauer et al.
implementation + Brian Pulfer's educational re-implementation. Two
further candidates (`red-teaming`, `refusal-training`) were considered
and rejected — every plausible reference was a library or a paper, not
a pedagogical from-scratch tutorial. Phase-9 totals: 50 → 52 targets,
65 → 69 guides.

### Phase-10 expansion notes (2026-05-14)

A breadth pass focused on areas that a 2026 reader would expect of an
authoritative from-scratch index:

- **11 new build targets**, **15 new verified guides**, **1 new original**,
  **0 weak guides slipped in** (Phase 10 starts from the Phase-9 baseline
  of 52 targets / 69 guides / 8 originals):
  - Foundations: `weight-init` (Xavier/Kaiming via UvA-DL), `dropout`
    (Chattopadhyay).
  - Model: `activations` (Belaweid's SwiGLU walkthrough),
    `flash-attention` (Shreyansh Singh's plain-PyTorch FA1-FA4
    + Alex Dremov's Triton walkthrough).
  - Training: `knowledge-distillation` (official PyTorch tutorial +
    labml.ai), `grpo` (DeepSeek-R1-style GRPO via GRPO-Zero, split
    from the existing PPO entry).
  - Inference: `structured-decoding` — new target shipped with an
    original (FSM-over-vocabulary logit masking, the real mechanism
    behind Outlines / XGrammar / OpenAI strict JSON mode).
  - Retrieval: `graphrag` (stephenc222's Leiden-community pipeline).
  - Agents: `react-pattern` (Ambrogi + Islam), `tree-of-thoughts`
    (Stephen Collins), `mcp-server` (Anthropic's free Skilljar course
    + Parry's raw-STDIO walkthrough).
  - Beyond Text: `multimodal-vlm` (HF's nanoVLM — connector + joint
    training from scratch, same backbone-reuse policy as the existing
    CLIP target).
- Phase-10 totals: 52 → **62 targets**, 69 → **80 guides**, 8 → **9
  originals**, 0 → 0 weak guides. All 94 URLs reachable.
- Tooling: validator gained a `--stale-days N` currency check and an
  orphan-originals guard; README badges now also surface the live
  guide count and a link-health pill.
