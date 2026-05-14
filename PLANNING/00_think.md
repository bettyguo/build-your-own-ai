# PHASE 0 — THINK: `build-your-own-ai`

> Goal of this document: validate the noun + format, fix the scope boundary, inventory the build targets, study `build-your-own-x`'s recipe, map where original content can move the needle, place this repo in its constellation, and surface the risks honestly.

---

## 1. Noun and format validation

**The noun is open.** Web/GitHub searches for "build your own ai," "build llm from scratch," "build your own X ai" return three classes of result — none of which occupy the *canonical curated index for AI* slot:

1. **Single from-scratch tutorials / books**, e.g. Sebastian Raschka's `rasbt/LLMs-from-scratch` (book + code), Karpathy's `nanoGPT` / `build-nanogpt` / "Let's build GPT" video, Khaliladib11/Transformer-from-scratch, FareedKhan-dev/create-million-parameter-llm-from-scratch, hamzafarooq/building-llm-applications-from-scratch. Each is a deep dive on one build target — *not* an index that maps the stack.
2. **General awesome-X AI lists**, e.g. `steven2358/awesome-generative-ai`, `eudk/awesome-ai-tools`, `mahseema/awesome-ai-tools`, `Zijian-Ni/awesome-ai-agents-2026`, `caramaschiHG/awesome-ai-agents-2026`. These are *tool / product / framework* directories — the opposite of "build it from scratch." They link to libraries you would *use*, not to guides that teach by reimplementation.
3. **General awesome-AI-learning lists**, e.g. `louisfb01/start-llms`, `youssefHosni/Awesome-AI-Data-Guided-Projects`. Broader learning material — courses, papers, blog posts, project ideas — not specifically the from-scratch reimplementation format.

**The format works and is well known.** `codecrafters-io/build-your-own-x` is the #1 most-starred repository on GitHub (~500k stars). It is a *single README* with ~32 alphabetized categories (3D Renderer, BitTorrent Client, Blockchain, Database, Docker, Emulator, Git, Neural Network, Operating System, Programming Language, Text Editor, Web Browser, …) and one-line entries formatted `[**Language**: _Title_](URL)`. The structure proves the format. Its AI footprint is thin: an *AI Model* category, a *Neural Network* category, and *Visual Recognition System* — a few dozen entries total across the entire AI stack.

**Conclusion.** The slot — *the canonical curated index of from-scratch guides for the modern AI stack* — is empty. `build-your-own-x` proves the format is the strongest knowledge artifact in the category; it just has not been applied with focus and a real curation bar to AI. That is the opening this repo fills.

---

## 2. Scope discipline — the key risk control

The format is high-leverage but easily diluted. Scope is the difference between a sharp, canonical artifact and "yet another awesome list."

### IN scope

Curated entries to **from-scratch guides** for components of the **modern AI stack**:

- Foundations: tokenizers, embeddings, autograd
- The Model: attention, transformer blocks, positional encodings, MoE, small from-scratch LMs
- Training: training loops, optimizers, schedulers, fine-tuning (SFT), preference-tuning (DPO / RLHF-style)
- Inference: minimal inference engines, KV caches, sampling, speculative decoding, quantization
- Retrieval: BM25, vector search (HNSW / IVF), rerankers, a full RAG pipeline
- Agents: agent loop, tool/function calling, memory, multi-agent orchestration
- Evaluation: eval harnesses, calibration / hallucination checks, judge-model pipelines
- Beyond text: diffusion (image), small multimodal models, audio (speech recognition, TTS), code models

Each entry must teach by *reimplementing the thing*, not by *calling a library that already does the thing*.

### OUT of scope — bright lines

- **General programming builds** — `build-your-own-x`'s turf (DBs, OSes, browsers, text editors, BitTorrent, Git, programming languages). Do *not* duplicate. The differentiator is AI-native.
- **"Use library X" tutorials** — even if the framework is fashionable (LangChain, LlamaIndex, vLLM, AutoGen, CrewAI, etc.), a guide that mostly *configures* a library is the opposite of from-scratch. Such guides may appear in `ai-engineer-roadmap` as resources, but not here.
- **Product / framework directories** — those are the awesome-X-tools genre. Different noun.
- **AI Engineering breadth & career path** — that is `ai-engineer-roadmap`'s noun. This repo points *to* it sideways, does not replicate it.
- **Harness / agent / IDE engineering** — that is `harness-engineer-roadmap`'s noun. This repo's "build your own agent loop" entry is a hands-on instance, not the breadth of harness engineering.
- **Interview prep, system design Q&A, leetcode-style problems** — that is `llm-interview-prep`'s noun.
- **Application templates** ("build a ChatGPT clone in N hours" using OpenAI's API). The thing being built must be the *internals*, not a thin wrapper.

### Edge cases (decisions logged)

- Karpathy's `nanoGPT` is in — it is the canonical from-scratch GPT, full training loop included.
- A "build a RAG with LangChain in 30 minutes" tutorial is **out**. A "build a RAG pipeline from scratch with no frameworks" tutorial is **in**.
- "Build your own coding agent" (e.g. boot.dev / freeCodeCamp's Lane Wagner walkthrough) is in — it builds the agent loop itself. Tutorials that mostly call a hosted Agents API and decorate prompts are out.
- "Build your own tokenizer" via Karpathy's `minbpe` is in. A blog that says "use `tiktoken`" is out.
- A pure paper walkthrough with no runnable code is out. A from-scratch reimplementation of a paper with code is in.

---

## 3. Build-target inventory (25–40 candidates)

For each: one-line "what you build," concept taught, estimated difficulty (★ / ★★ / ★★★), and a first guess at whether a good from-scratch guide exists today (`✓ exists`, `~ thin / dated`, `✗ gap` — candidate for `originals/`).

### Foundations

| # | Target | What you build | Teaches | Difficulty | Existing guide? |
|---|---|---|---|---|---|
| 1 | **Tokenizer (BPE)** | A byte-pair-encoding tokenizer from scratch | Subword tokenization, vocab construction | ★★ | ✓ exists (Karpathy `minbpe`) |
| 2 | **Embedding layer** | Word / token embeddings, learned vectors | Lookup tables, dense reps | ★ | ~ thin (mostly tucked inside larger tutorials) |
| 3 | **Autograd / micro-framework** | A scalar-valued autograd engine | Reverse-mode AD, computational graphs | ★★ | ✓ exists (Karpathy `micrograd`) |
| 4 | **Backprop by hand** | Manual backward for an MLP | Chain rule, gradient flow | ★★ | ✓ exists (Karpathy "neural networks: zero to hero" early lectures) |

### The Model

| # | Target | What you build | Teaches | Difficulty | Existing guide? |
|---|---|---|---|---|---|
| 5 | **Attention from scratch** | Scaled dot-product + multi-head attention | The core mechanism | ★★ | ✓ exists (multiple) |
| 6 | **Positional encodings** | Sinusoidal + RoPE | Position info without recurrence | ★★ | ~ thin (often elided) |
| 7 | **Transformer block** | LN + MHA + MLP + residuals, stacked | The decoder-only stack | ★★ | ✓ exists |
| 8 | **A small GPT** | An end-to-end tiny LM trained on toy text | The whole pipeline at small scale | ★★ | ✓ exists (`nanoGPT`, `build-nanogpt`) |
| 9 | **A small BERT / encoder LM** | MLM pretraining + classification head | Encoder side, MLM objective | ★★ | ~ thin compared to decoder side |
| 10 | **Mixture-of-Experts** | Routing + experts + load balancing loss | Sparse activation, scaling | ★★★ | ~ thin (mostly papers; few good from-scratch guides) |
| 11 | **State-space / Mamba-style block** | A minimal SSM layer | Long-context alternatives to attention | ★★★ | ~ thin (✗ candidate for `originals/`) |

### Training

| # | Target | What you build | Teaches | Difficulty | Existing guide? |
|---|---|---|---|---|---|
| 12 | **Training loop** | Data loader, loss, optimizer step, eval | The mechanics that books gloss over | ★★ | ✓ exists |
| 13 | **Optimizer (SGD / Adam / AdamW)** | Adam from scratch in numpy or torch | Momentum, adaptive lr, weight decay | ★★ | ~ thin (often a one-liner) |
| 14 | **Learning-rate schedule** | Warmup + cosine + decay | Scheduling that actually matters | ★ | ~ thin |
| 15 | **Mixed precision / grad accumulation** | Manual FP16/BF16 + accumulation | Practical scaling tricks | ★★ | ~ thin (✗ candidate for `originals/`) |
| 16 | **Supervised fine-tuning (SFT)** | Fine-tune a small base on instructions | The first half of post-training | ★★ | ✓ exists (Raschka book Ch 7) |
| 17 | **DPO / preference tuning** | Direct preference optimization loop | Aligning without a reward model | ★★★ | ~ thin (papers + a few notebooks) |
| 18 | **A from-scratch reward model** | Train a reward head + pairwise loss | The RLHF-style scoring side | ★★★ | ✗ gap (candidate for `originals/`) |
| 19 | **PPO / GRPO-style RL loop** | Policy update + KL penalty + advantage | RL for LLMs in miniature | ★★★ | ~ thin (Hugging Face has parts; few clean from-scratch) |

### Inference

| # | Target | What you build | Teaches | Difficulty | Existing guide? |
|---|---|---|---|---|---|
| 20 | **Sampling (greedy / temp / top-k / top-p)** | Sampler functions for a tiny LM | Decoding strategies | ★ | ~ thin (often mentioned, rarely isolated) |
| 21 | **KV cache** | Cache K/V across decode steps | The single biggest inference win | ★★ | ~ thin (✗ candidate for `originals/`) |
| 22 | **Minimal inference engine** | A `generate()` loop with batching | What llama.cpp etc. do at the core | ★★★ | ~ thin |
| 23 | **Speculative decoding** | Draft model + verify with target | Modern inference acceleration | ★★★ | ~ thin (papers + a few blogs) |
| 24 | **Quantization (INT8 / INT4)** | Post-training quantization of a small LM | Memory & throughput trade-offs | ★★★ | ~ thin |

### Retrieval

| # | Target | What you build | Teaches | Difficulty | Existing guide? |
|---|---|---|---|---|---|
| 25 | **BM25 from scratch** | Lexical retrieval scoring | The classical baseline that still wins | ★ | ✓ exists |
| 26 | **Vector search (brute force → HNSW)** | A toy ANN index | How vector DBs actually work | ★★ | ~ thin (HNSW from scratch is rare) |
| 27 | **Reranker (cross-encoder)** | Score (query, doc) pairs | Why two-stage retrieval matters | ★★ | ~ thin |
| 28 | **End-to-end RAG pipeline** | Chunk → embed → retrieve → answer, no frameworks | RAG's actual moving parts | ★★ | ✓ exists (HF `make-your-own-rag`, learnbybuilding.ai) |
| 29 | **Hybrid search (BM25 + vector)** | Fuse lexical + dense | Production-realistic retrieval | ★★ | ~ thin |

### Agents

| # | Target | What you build | Teaches | Difficulty | Existing guide? |
|---|---|---|---|---|---|
| 30 | **Agent loop** | Reason → act → observe → repeat | The kernel of agentic AI | ★★ | ✓ exists (Victor Dibia, boot.dev/Lane Wagner) |
| 31 | **Tool / function-calling layer** | Schema-validated tool dispatch | How agents touch the world | ★★ | ~ thin (mostly framework tutorials) |
| 32 | **Agent memory (short + long term)** | Conversation buffer + vector recall | Statefulness without a framework | ★★ | ~ thin (✗ candidate for `originals/`) |
| 33 | **Multi-agent orchestration** | A planner + workers loop, from scratch | Coordination without CrewAI/AutoGen | ★★★ | ~ thin (✗ candidate for `originals/`) |
| 34 | **Coding agent (file-edit + shell)** | A minimal Claude-Code-like agent | What today's coding agents actually do | ★★★ | ✓ exists (ghuntley, boot.dev, Laracasts) |

### Evaluation

| # | Target | What you build | Teaches | Difficulty | Existing guide? |
|---|---|---|---|---|---|
| 35 | **Eval harness** | Task → prompt → score, pluggable | What `lm-evaluation-harness` does in miniature | ★★ | ~ thin |
| 36 | **LLM-as-judge** | Pairwise + pointwise judge prompts + agreement | Evaluating without ground truth | ★★ | ~ thin |
| 37 | **Calibration / hallucination check** | Confidence vs. accuracy curves on QA | Trust signals beyond accuracy | ★★★ | ✗ gap (candidate for `originals/`) |

### Beyond text

| # | Target | What you build | Teaches | Difficulty | Existing guide? |
|---|---|---|---|---|---|
| 38 | **Diffusion model (DDPM)** | A toy image diffusion model from scratch | Forward/reverse process, score matching | ★★★ | ✓ exists (lucidrains, fast.ai, HF `diffusion-models-class`) |
| 39 | **CLIP-style contrastive model** | Image+text encoders + InfoNCE | Multimodal alignment | ★★★ | ~ thin (✗ candidate for `originals/`) |
| 40 | **Speech recognition (CTC)** | A toy ASR with CTC loss | Audio sequence learning | ★★★ | ~ thin |

**Counts.** 40 candidate build targets across 8 categories. After Phase-3 curation, expect roughly 30–35 to ship with verified guides; the rest become `originals/` candidates or marked gaps.

---

## 4. Competitive structural study — the `build-your-own-x` recipe

Extracted from a direct read of the README + structural analyses:

1. **One file is the product.** A single `README.md` carries ~99% of the value. No multi-page site. The flat artifact is what makes it sharable, screenshottable, and forkable.
2. **Alphabetized top-level categories.** ~32 of them. Each is a noun ("Database," "Operating System"). Categories are anchored so you can deep-link.
3. **Entries are one line.** Format: `[**Language**: _Title_](URL)`. Language in **bold** for visual scanning, title in *italic*, link directly external.
4. **Entries grouped by language within each category.** Lets a reader filter by their stack at a glance.
5. **Optional `[video]` / `[free]` markers.** Light metadata; no schema overhead.
6. **No descriptions** in the index itself. The title carries the promise; the click delivers. (This repo will diverge slightly — a one-line "what you'll understand after" note adds enough value to justify the extra height, and it differentiates from `build-your-own-x` without bloating.)
7. **Quality bar is implicit but real.** No spam links, no obvious dead ones, no library tutorials disguised as from-scratch. The community polices it via PRs.
8. **Permissive licensing** (CC0) — frictionless to fork, mirror, archive.

**Recipe applied here:**
- Keep the single-README spine.
- Use the same compact entry format, plus one short "what you'll understand" line — the AI stack rewards a tiny bit of map.
- Difficulty tag (★/★★/★★★) and `free`/`paid` markers up front.
- `original` tag for `originals/`-authored guides.
- The structural source of truth is YAML in `entries/`; `build_readme.py` regenerates the README. Contributors edit YAML, not markdown — fewer formatting fights, easier validation.

---

## 5. Original-content opportunity map — where `originals/` earns its keep

Targets where existing from-scratch guides are absent, thin, or out-of-date. These are the **differentiation lever** for this repo — every minute spent here compounds because none of the alternatives have it.

**Tier 1 — write originals on launch (highest leverage):**

- **KV cache from scratch** (#21) — a topic every inference talk references and almost no tutorial isolates well. A clean 200-line walkthrough is a goldmine.
- **Reward model from scratch** (#18) — RLHF tutorials skip straight to PPO; the reward model itself is the foundational object.
- **Agent memory (short + long term)** (#32) — almost all current tutorials lean on a framework. From-scratch is genuinely missing.
- **Multi-agent orchestration from scratch** (#33) — same gap; the "without CrewAI/AutoGen" version is high-value.
- **Calibration / hallucination check** (#37) — eval guides exist; this specific lens almost none.

**Tier 2 — write originals soon after launch:**

- **Mamba/SSM-style block from scratch** (#11) — papers exist, clean teaching guide does not.
- **Mixed-precision + gradient accumulation** (#15) — the practical scaling trick everyone needs.
- **CLIP-style contrastive model** (#39) — surprising gap given how foundational CLIP is.
- **Speculative decoding** (#23) — modern, important, under-taught.
- **Tool / function-calling layer from scratch** (#31) — most guides outsource this to a framework.

**Discipline:** do not pad. Five tier-1 originals at launch is plenty. More originals don't make the index better; they dilute curatorial focus. The job of `originals/` is to fill the worst gaps, not to author an alternative textbook.

---

## 6. Constellation map

Four standalone peers, none nested. Each owns a distinct noun.

- **`build-your-own-ai`** (this repo) — *learn by building*. The curated index of from-scratch guides for the AI stack.
- **`ai-engineer-roadmap`** — *the path*. Breadth of the AI-engineering career: what to learn in what order, what to read, what to use. Resource pointers.
- **`harness-engineer-roadmap`** — *the harness*. How to build, debug, and operate agent harnesses / coding agents / IDE integrations. Overlaps with this repo on "build your own agent loop" — there the noun is the *practitioner discipline*; here it's the *one-day hands-on build*.
- **`llm-interview-prep`** — *the test*. System-design and interview material for LLM/AI roles.

**Cross-link rule (placed in Phase 4):** a small "Peers" block in each README, listing the other three with a one-line statement of what each owns. Same wording in all four. No primacy implied. From this repo: "If you want the path, see `ai-engineer-roadmap`. If you want harness engineering, see `harness-engineer-roadmap`. If you want interview prep, see `llm-interview-prep`. This repo is where you go to *build the thing*."

---

## 7. Risk log

| Risk | Likelihood | Severity | Mitigation |
|---|---|---|---|
| **Overlap with curator's own learning repos** (`ai-engineer-roadmap`, `llm-interview-prep` in particular) cannibalizes attention | High | High | Scope discipline in §2. This repo is the *one* place where the deliverable is hands-on from-scratch guides. The other repos point *to* this repo for that need. |
| **Format already attempted by general awesome-X lists** so reader sees "just another list" | Medium | High | (a) Sharp focus on from-scratch only; (b) the quality bar — every link verified, every guide confirmed genuinely from-scratch; (c) originals fill gaps competitors cannot match without writing new content. |
| **Broken / obsolete / mislabeled links** corrode the "canonical" property — and this is published under a real PhD identity | High at first draft (~10% rate per Operating Contract) | Catastrophic | `linkcheck.py` in CI on a schedule; `validate_entries.py` enforces the from-scratch flag with a PR template that demands evidence; `PLANNING/03_verification_log.md` records every check. Audit to zero before launch. |
| **Thin launch** — index that looks like a stub kills initial momentum | Medium | High | Day-one launch requires complete category coverage end-to-end. Per Phase 5 checklist, no category may ship with zero entries or only `gap` markers. |
| **Library-tutorial bleed** — a guide that *says* "from scratch" but mostly imports `transformers` slips in | High without enforcement | High | The "is-this-actually-from-scratch" check in `validate_entries.py`; PR template confirmation; the hostile review in Phase 6 specifically hunts for this. |
| **Authorial overreach in `originals/`** — writing too many originals dilutes the curator-of-the-best-in-the-field positioning into yet-another-textbook | Medium | Medium | Cap originals at the tier-1 list (~5 at launch). Each original must be short (≤ ~1500 words + ≤ ~150 lines code), runnable, and clearly marked. |
| **Naming collision / dilution** — many "build llm from scratch" repos exist | High (already true) | Medium | The differentiator is the *index*, not another tutorial. Title and opening lines lead with "curated index" + the `build-your-own-x`-lineage framing. |
| **Maintenance decay** — links rot, guides go stale, the repo becomes embarrassing | Certain over time | Medium | Stated maintenance cadence in README; scheduled `linkcheck.py` CI; "Last updated" badge; the verification log is reusable for re-audits. |

---

## 8. Open questions

1. **Difficulty tags — 3-tier vs 5-tier?** Going with ★/★★/★★★ for scan speed; can refine in Phase 1 if a target genuinely needs ★★★★.
2. **One guide per target, or many?** Default: 1–3 verified guides per target. More than three is taste-curation, not the-best-of. If a target has many comparable guides, list 2–3 and link the rest as "see also."
3. **`originals/` writing style.** Long-form Markdown with embedded runnable Python? Or pointer to a `originals/<name>/notebook.ipynb`? Decision deferred to Phase 1; both are acceptable. Bias toward Markdown for index parity.
4. **Entry format file extension.** YAML or TOML? YAML is more familiar to ML readers; going with YAML in Phase 1 unless `validate_entries.py` design pushes back.
5. **Should the index include closed-source / paid guides (books, paid courses) at all?** Yes if they are world-class (Raschka's book, fast.ai's paid path), tagged `paid`, with a free-alternative pointer where one exists. Excluding all paid material would drop several of the best from-scratch resources in existence.
6. **Anchor structure / TOC.** Auto-generated from category names; confirmed in Phase 1 wireframe.
7. **Social card / banner.** No image-generation tool here, so Phase 4/5 will produce `assets/MAKE_BANNER.md` with the spec for a human to render.

---

## Assumptions logged (proceeding without human confirmation, per the autonomous instruction)

- Repo will use YAML entries → `build_readme.py` regenerates README.
- 8 top-level categories per the candidate spine; final ordering and inside-category ordering set in Phase 1.
- Difficulty tags ★ / ★★ / ★★★.
- Tier-1 originals at launch: KV cache, reward model, agent memory, multi-agent orchestration, calibration/hallucination check. (5 originals — exactly the differentiation lever, no padding.)
- Paid guides allowed if world-class, tagged `paid`, with a free pointer when available.
- License: CC-BY-4.0 for content, MIT for code (matches the master prompt).
- Single-README spine is the product; the YAML is plumbing.

---

## CHECKPOINT 0 — exit conditions

- [x] Noun and format slot confirmed empty.
- [x] **Scope boundary set** (IN / OUT, including bright lines against the curator's own peer repos).
- [x] Build-target inventory: 40 candidates across 8 categories.
- [x] `build-your-own-x` recipe extracted and applied.
- [x] **Original-content opportunity map**: 5 tier-1 originals identified.
- [x] Constellation map: 4 standalone peers.
- [x] Risk log with mitigations.
- [x] Open questions logged; assumptions logged to proceed autonomously.

Proceeding to Phase 1 (DESIGN — taxonomy + repo architecture).
