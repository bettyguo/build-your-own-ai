# PHASE 3 — Verification log

> Append-only record of every guide considered for the index. Each entry
> notes whether the guide was **accepted** (genuinely from-scratch, live,
> current) or **rejected** (and why). This file is the curation paper trail.

Verifier: `bettyguo` (Betty Guo / Dongxin Guo)
Initial verification window: 2026-05-14
Method: `WebFetch` to confirm each URL resolves; read README / opening
section; record one concrete from-scratch signal; reject if the guide is
primarily library configuration or product/framework wrapping.

---

## Summary

- **62** build targets across 8 categories (+expansion phases 7, 8, 9).
- **80** verified guides accepted across **53** targets.
- **9** targets ship as open `gap`. **All 9** are filled by originals/.
- **17** guides were considered and rejected (reasons logged below).
- **1** mid-research scope change: KV cache was originally tier-1 of the
  `originals/` plan; verification surfaced two excellent existing
  from-scratch guides, so KV cache now ships with curated links instead.

Zero entries are unverified. All 94 URLs reachable on 2026-05-14
(`linkcheck.py --quick` green; report at `tools/linkcheck-report.md`).

### Additions from the Phase 6 hostile-review pass (2026-05-14)

- ✓ Added **COAX — Building BERT with PyTorch from scratch** (small-encoder-lm)
  to broaden beyond labml.ai. Hand-written embeddings, attention, multi-head
  attention, encoder stack — no `transformers.BertModel`.
- ✓ Replaced **mixture-of-experts** primary with **st-moe-pytorch** (also
  lucidrains) — the author's own recommended successor. Kept the older
  repo as a secondary "stepping stone" entry with a clear note.

### Additions from the post-Phase-6 gap-filling pass (2026-05-14)

After Phase 6 concluded, ran a research sweep against the 10 remaining
open gaps. Three gaps yielded genuine, verified from-scratch guides:

- ✓ Added **Maxime Labonne — Decoding Strategies in LLMs** (sampling).
  Hand-written `greedy_search`, `beam_search`, `top_k_sampling`,
  `nucleus_sampling` over raw logits — no `model.generate` shortcut.
- ✓ Added **Taeksang Peter Kim — Mixed Precision Training from Scratch**
  (mixed-precision). Goes below `torch.cuda.amp.autocast` to implement
  loss scaling, FP32 master weights, and mixed-precision matmul with
  custom cuBLAS kernels — reveals what AMP actually does.
- ✓ Added **vwxyzjn/lm-human-preference-details** + the HF blog
  "N Implementation Details of RLHF with PPO" (ppo-grpo). The repo is a
  self-described "simple-to-read and minimal reference implementation"
  of PPO RLHF in PyTorch; the blog explains the 20+ details that make a
  from-scratch run actually work.

### Additions from the second gap-filling pass (2026-05-14)

Ran a more targeted sweep against the 7 still-open gaps. Three more
yielded:

- ✓ Added **Jake Tae — Word2vec from Scratch (NumPy)** and
  **OlgaChernytska/word2vec-pytorch** (embedding-layer). Jake's version
  is the pedagogical NumPy walkthrough; Olga's is the PyTorch
  reproduction of the original word2vec paper with explicit deviation
  notes.
- ✓ Added **Maxime Labonne — Introduction to Weight Quantization**
  (quantization). Hand-written `absmax_quantize` and `zeropoint_quantize`
  functions in PyTorch — `bitsandbytes` is introduced afterward for
  contrast, not as the implementation.
- ✓ Added **Andrey Chauzov — Hybrid retrieval with reciprocal rank fusion**
  (hybrid-search). Author explicitly chooses to implement RRF from scratch
  rather than use a vector DB's built-in fusion.

### Phase-7 expansion (2026-05-14)

After two unsuccessful gap-filling sweeps confirmed that four targets
genuinely lacked good public from-scratch guides, those four became
new originals:

- ✓ `originals/lr-schedule.md` — warmup + cosine in code, with the
  three-way loss-curve experiment that makes it click.
- ✓ `originals/reranker.md` — cross-encoder + pointwise BCE loss + the
  two-stage pipeline with the cost/quality trade-off measured.
- ✓ `originals/tool-layer.md` — schema + dispatcher + lightweight
  JSON-Schema validation, with the three error paths everyone hits.
- ✓ `originals/eval-harness.md` — task / runner / scorer / reporter
  with the four ways "comparable" breaks.

Three new build targets were also added — genuine omissions from the
original taxonomy:

- ✓ `lora` (Training) — Raschka book Appendix E + Jake Tae LoRA post.
  LoRA is the way almost everyone fine-tunes; not having it was a real
  taxonomy hole.
- ✓ `distributed-training` (Training) — PyTorch's official DDP tutorial
  + Kevin Yang's walkthrough. Multi-GPU training was a glaring
  taxonomy hole given that every nontrivial training run uses it.
- ✓ `long-context-rope-scaling` (Model) — Aman Arora's "How LLMs Scaled
  from 512 to 2M Context" deep dive. Position Interpolation → NTK →
  YaRN with PyTorch code.

One candidate rejected during Phase-7 verification:

- ✗ Sebastian Raschka — "Practical Tips for Finetuning LLMs Using LoRA"
  (https://magazine.sebastianraschka.com/p/practical-tips-for-finetuning-llms).
  Author explicitly says "this article is focused on the broader ideas
  and takeaways from working with LoRA—a top-down view," not the
  from-scratch implementation. Raschka's book appendix-E (accepted
  separately) covers the implementation.

### Phase-8 expansion (2026-05-14)

A second user-requested breadth pass. **5 new build targets** added in
genuine omission areas; **1 secondary guide** added; **1 candidate
rejected**. The curation bar held: every addition has a verified
from_scratch_evidence string.

- ✓ `layer-normalization` (Foundations) — labml.ai's annotated LayerNorm.
  Mean / variance / scale / shift computed from PyTorch primitives, not
  `nn.LayerNorm`.
- ✓ `grouped-query-attention` (Model) — Max Shap's 16-line GQA + the
  fkodom PyTorch reproduction of the paper. Both implement GQA without
  `nn.MultiheadAttention`.
- ✓ `retrieval-evaluation` (Retrieval) — Pinecone's "Evaluation Measures
  in Information Retrieval." Recall@K, MRR, MAP@K, NDCG@K all
  hand-written in Python.
- ✓ `vision-transformer` (Beyond Text) — tintn/vision-transformer-from-scratch.
  Patch embedding + encoder + classification head in pure PyTorch with
  a companion blog post.
- ✓ `latent-diffusion` (Beyond Text) — labml.ai's annotated Latent
  Diffusion Models. VAE + UNet + CLIP text embedder, all custom modules,
  no `diffusers` library.
- ✓ Added `karpathy/llm.c` as a secondary guide to `small-gpt` — pure
  C/CUDA reproduction of GPT-2 / GPT-3 miniseries pretraining, no
  PyTorch.
- ✗ Rejected `qywu.github.io` gradient-checkpointing tutorial — uses
  `torch.utils.checkpoint.checkpoint()` directly, which is the thing
  being taught. No from-scratch guide found for `gradient-checkpointing`
  in this pass; the target was not added since the curation bar would
  have to be lowered to admit any candidate.

### Tooling notes

- Added `medium.com/@maxshapp/...` to `tools/.linkcheckignore` with a
  documented reason: Medium aggressively 403s bots on `/@username/`
  paths, even though the article loads in browsers and was verified at
  curation time. The exception is scoped to the single URL, not all of
  Medium.
- `build_readme.py` now renders per-category target + guide counts in
  the TOC so readers can pick a layer to dig into without scrolling.

### Phase-9 expansion (2026-05-14)

A targeted safety/alignment pass. The original taxonomy had no row for
this area; instead of adding a thin new top-level category (only 2 of 4
candidate targets had verified from-scratch guides), the two verified
targets were folded into existing categories:

- ✓ `constitutional-ai` (Training, between DPO and PPO-GRPO) — Cameron
  Wolfe's RLAIF article (mechanism-level walkthrough) + the open RLHF
  Book chapter (Nathan Lambert).
- ✓ `watermarking` (Inference, between speculative-decoding and
  quantization) — the official Kirchenbauer et al. lm-watermarking repo
  (ICML 2023 paper code) + Brian Pulfer's educational PyTorch
  re-implementation.

Two candidate targets *did not* yield from-scratch guides and were
**not** added to keep the bar:

- `red-teaming` — every candidate (DeepTeam, similar libraries) is a
  framework, not an educational from-scratch tutorial. Adding the
  target with a framework-tutorial as the only "guide" would violate
  the curation rule.
- `refusal-training` / safety fine-tuning — current literature is
  research papers (ACTOR, SPF, SAP, Rational), not pedagogical
  walkthroughs. No accepted target.

The decision *not* to add a Safety & Alignment top-level category is
itself documented curation work — a thin two-target category would
have been weaker than absorbing the two verified targets into where
they naturally fit.

### Phase-10 expansion (2026-05-14)

A breadth pass targeting the build-target areas that a 2026 reader
would expect an authoritative from-scratch AI index to cover. **11 new
build targets, 15 new verified guides, 1 new original** — every
addition has a quoted from-scratch evidence string, the curation bar
held, two candidates were rejected.

**Foundations (+2):**

- ✓ `weight-init` — Phillip Lippe (UvA-DL Tutorial 3, hosted by PyTorch
  Lightning). Hand-written constant / variance / Xavier / Kaiming
  initializers with the activation-variance-vanishing experiment that
  motivates each. Educational lecture series.
- ✓ `dropout` — Nilanjan Chattopadhyay (2020-04-20). Custom `Dropout`
  with `bernoulli_` masking, inverted-dropout `(out * mask) / (1 - p)`
  scaling at training, and `if self.training` eval-mode passthrough.
  PyTorch's `nn.Dropout` is shown afterward for contrast only.

**Model (+2):**

- ✓ `activations` — Aziz Belaweid's "What Is SwiGLU? How to Implement
  It?" (2024-03-13). Hand-written `class SwiGLU(nn.Module)` with the
  `F.silu(W1·x) * W3·x` gating; the GLU family derivation accompanies.
- ✓ `flash-attention` — two complementary refs: Shreyansh Singh's
  `FlashAttention-PyTorch` (FA1–FA4 in plain PyTorch for algorithmic
  clarity, no CUDA) + Alex Dremov's annotated Triton walkthrough
  (2025-01-12) with the tiled / online-softmax pseudocode and the
  running-max + running-denominator recurrence.

**Training (+1 new target + 1 carved-out target):**

- ✓ `knowledge-distillation` — official PyTorch tutorial by Alexandros
  Chariton (manual KL on temperature-scaled softmax, the `T²` rescale,
  hard-label CE combined; no KD library) + labml.ai's annotated
  Hinton-et-al-2015 implementation.
- ✓ `grpo` — `policy-gradient/GRPO-Zero`. README states "We implement
  almost everything from scratch and only depend on `tokenizers` for
  tokenization and `pytorch` for training." DeepSeek-R1-style GRPO
  (group-relative advantage, no critic, clipped objective, KL penalty).
  The original `ppo-grpo` target's title was tightened to "PPO-style RL
  loop (RLHF)" to reflect that GRPO now has its own row.

**Inference (+1 new target):**

- ✓ `structured-decoding` — shipped as a `gap` with `original_planned:
  true`. Rejected `dottxt-ai.github.io/outlines/...structured_generation_explanation/`
  (404). Searched for a strict from-scratch FSM-over-vocab walkthrough;
  available material is either conceptual (BentoML, vLLM blog,
  AnalyticsVidhya, LMSYS-XGrammar) or library usage (Outlines docs).
  Wrote `originals/structured-decoding.md` covering the toy yes/no FSM,
  the regex FSM, the JSON-schema example, the vocab-mismatch dead-end
  failure mode, and three honest gotchas. 80 lines of code, runnable.

**Retrieval (+1):**

- ✓ `graphrag` — `stephenc222/example-graphrag`. Full pipeline
  (chunk → entity & relationship extraction → graph construction →
  Leiden community detection → community summarization → query answer
  synthesis) in standalone Python functions; does NOT use Microsoft's
  `graphrag` library. Implements the "From Local to Global" paper.

**Agents (+3):**

- ✓ `react-pattern` — `mattambrogi/agent-implementation` ("a simple
  implementation of the ReAct Agent Pattern", following Simon Willison;
  three files, no framework) + Shafiqul Islam's "Create ReAct AI Agent
  from Scratch using Python Without any Framework" article.
- ✓ `tree-of-thoughts` — Stephen Collins, "How to Implement a Tree of
  Thoughts in Python" (2024-07-05). Custom `ThoughtNode` (thought +
  children list), `explore_thoughts` prompts for k next-thoughts per
  leaf, `run` iterates expansion. Anthropic API directly; no ToT framework.
- ✓ `mcp-server` — Anthropic's free "Introduction to Model Context
  Protocol" course on Skilljar (official MCP Python SDK, primitives:
  tools / resources / prompts) + David Parry's "Understanding MCP
  Through Raw STDIO Communication" (2025-07-17, raw JSON-RPC 2.0 over
  STDIO, stdlib only — "No frameworks, no magic — just the protocol in
  its purest form").

**Beyond Text (+1):**

- ✓ `multimodal-vlm` — HF's nanoVLM blog (Aritra Roy Gosthipaty et al.).
  The defining VLM components — the modality-projection module (pixel
  shuffle + linear) and the joint training loop — are written from
  scratch in PyTorch (`modality_projector.py`, `vision_language_model.py`).
  Pretrained SigLIP + SmolLM2 backbones are reused — the same
  backbone-reuse policy as the existing `clip` target (which uses
  `timm` / `transformers` backbones). No `AutoModelForVision2Seq`.

**Rejected during Phase-10 verification:**

- ✗ HF blog "Code a simple RAG from scratch" *alternative* via
  `learnbybuilding.ai` — see existing rejection above.
- ✗ Anyscale "Continuous Batching" blog (2023-06-22, Cade Daniel et al.) —
  conceptual marketing piece. "We'll cover the basics of how LLM
  inference works and highlight inefficiencies in traditional
  request-based dynamic batching." Points readers to vLLM / TGI; no
  scheduler loop implemented. The `continuous-batching` target was
  *not* added since no from-scratch reference exists.
- ✗ Philipp Schmid's MCP intro — uses `FastMCP` decorator; abstracts
  away JSON-RPC. The from-scratch view of MCP is the Anthropic course
  + Parry's raw-STDIO article (both accepted above).
- ✗ Wei-Meng Lee, "Hands-on MCP" (CODE Magazine, 2026 May/June) — same
  reason: FastMCP-based, abstracts the JSON-RPC layer.
- ✗ Ceshine Lee's "Implementing Beam Search Part 1" — described as
  "source code analysis of OpenNMT-py", not a standalone implementation.
  `beam-search` was *not* added since the existing `sampling` target
  already includes Maxime Labonne's `beam_search` function.
- ✗ Astarag Mohapatra's ColBERT tutorial — uses `colbert-ai`'s
  `Indexer` / `Searcher` directly. The late-interaction mechanism is
  described conceptually but not implemented. `colbert-late-interaction`
  was *not* added as a target.
- ✗ Hey Amit "Contrastive Learning of Sentence Embeddings from Scratch"
  (2024-11-28) — title misleading; the article loads pretrained BERT
  and only demonstrates cosine similarity, never implements the
  contrastive loss or training loop. `sentence-embedding` was *not*
  added.
- ✗ Tom Aarsen's "Training and Finetuning Embedding Models" HF blog
  (2024-05-28) — uses `sentence_transformers.losses.MultipleNegativesRankingLoss`;
  loss + trainer abstracted by the library.
- ✗ Akash Modi's "Logical Reasoning with ReAct Agent from Scratch (Part 1)"
  (2024-10-05) — explicitly defers implementation to Part 2; Part 1
  is concept-only. `react-pattern` accepted via two other refs above.
- ✗ `FullStackRetrieval-com/RetrievalTutorials` (Greg Kamradt's "5 Levels
  of Text Splitting") — notebook header states "This tutorial will use
  code from LangChain & Llama Index"; Levels 1–4 are LangChain wrappers.
  A `chunking-strategies` target was *not* added, since accepting it
  would require lowering the curation bar to admit a library tutorial
  as "from scratch."

### Phase-10 tooling improvements

- `validate_entries.py --stale-days N` — opt-in currency check that
  warns (does not fail) for any guide whose `verified_on` is older
  than N days. Use case: quarterly audit trigger.
- `validate_entries.py` now also runs an *orphan originals* guard:
  every file in `originals/*.md` (except `README.md`) must correspond
  to an entry with `original_planned: true`. Catches half-deleted gaps
  and stray files.
- `README.md.tmpl` gained two badges: live guide count and a
  link-health pill.

---

## Accepted

### Foundations

- ✓ **karpathy/minbpe** — `tokenizer-bpe`
  https://github.com/karpathy/minbpe · code · Python · free · author: Andrej Karpathy
  Evidence: `BasicTokenizer` / `RegexTokenizer` / `GPT4Tokenizer` implemented from primitives. `tiktoken` appears only in tests for cross-validation.
- ✓ **Karpathy — Let's build the GPT Tokenizer (video)** — `tokenizer-bpe`
  https://www.youtube.com/watch?v=zduSFxRajkE · video · free
  Evidence: Companion lecture to `minbpe`; merges are coded step by step on screen from an empty file.
- ✓ **karpathy/micrograd** — `autograd-micro`
  https://github.com/karpathy/micrograd · code · Python · free · author: Andrej Karpathy
  Evidence: ~100-line autograd engine + ~50-line `nn` module; reverse-mode autodiff over scalar `Value`s, no PyTorch dependency.
- ✓ **karpathy/nn-zero-to-hero** — `backprop-by-hand`
  https://github.com/karpathy/nn-zero-to-hero · course · Python · free · author: Andrej Karpathy
  Evidence: Lecture 1 builds micrograd from empty file; lecture 4 ("Becoming a Backprop Ninja") computes every MLP gradient by hand and verifies against autograd.

### The Model

- ✓ **Raschka — Understanding and Coding Self-Attention** — `attention-from-scratch`
  https://magazine.sebastianraschka.com/p/understanding-and-coding-self-attention · written · Python · free · 2024-01-14
  Evidence: Custom `SelfAttention` class with `queries @ keys.T`, hand-written softmax, explicit contrast with `nn.MultiheadAttention`.
- ✓ **The Annotated Transformer** — `attention-from-scratch`
  https://nlp.seas.harvard.edu/2018/04/03/attention.html · written · Python · free · author: Sasha Rush (Harvard NLP)
  Evidence: Line-by-line PyTorch reimplementation of "Attention Is All You Need" — encoder/decoder, attention, positional encoding, training all hand-written.
- ✓ **EleutherAI — Rotary Embeddings: A Relative Revolution** — `positional-encodings`
  https://blog.eleuther.ai/rotary-embeddings/ · written · free · 2021-04-20
  Evidence: Mathematical derivation + PyTorch/JAX implementations pulled from EleutherAI codebases.
- ✓ **labml.ai — RoPE** — `positional-encodings`
  https://nn.labml.ai/transformers/rope/index.html · written · Python · free
  Evidence: Annotated `RotaryPositionalEmbeddings` class implemented from the paper.
- ✓ **karpathy/nanoGPT — model.py** — `transformer-block`
  https://github.com/karpathy/nanoGPT/blob/master/model.py · code · Python · free
  Evidence: ~300 lines defining `CausalSelfAttention`, `Block`, `GPT` in PyTorch primitives. No `nn.Transformer` / `transformers`.
- ✓ **karpathy/build-nanogpt** — `small-gpt`
  https://github.com/karpathy/build-nanogpt · video · Python · free
  Evidence: Companion to 4-hour "Let's reproduce GPT-2 (124M)" lecture; git commits walk through nanoGPT being built from an empty file.
- ✓ **karpathy/nanoGPT** — `small-gpt`
  https://github.com/karpathy/nanoGPT · code · Python · free
  Evidence: Reproduces GPT-2 (124M) on OpenWebText, ~600 lines total. Note: README marks it superseded by `nanochat`; kept because the 124M build is the educational reference point.
- ✓ **karpathy/nanochat** — `small-gpt`
  https://github.com/karpathy/nanochat · code · Python · free
  Evidence: Successor to nanoGPT covering the full ChatGPT-like pipeline — tokenization, pretraining, finetuning, inference, chat UI — all from scratch.
- ✓ **rasbt/LLMs-from-scratch (book repo)** — `small-gpt` and `sft`
  https://github.com/rasbt/LLMs-from-scratch · book · Python · paid (book) / free (code)
  Evidence: Book's principle is "from scratch without any external LLM libraries" in pure PyTorch. Code is free; book is paid.
- ✓ **labml.ai — Masked Language Model (MLM)** — `small-encoder-lm`
  https://nn.labml.ai/transformers/mlm/index.html · written · Python · free
  Evidence: Annotated PyTorch implementation of BERT-style MLM pretraining.
- ✓ **lucidrains/mixture-of-experts** — `mixture-of-experts`
  https://github.com/lucidrains/mixture-of-experts · code · Python · free · author: Phil Wang
  Evidence: Sparsely-gated MoE from the Shazeer et al. paper — custom gating, top-k routing, load-balancing loss. (Maintenance note: README points users toward an ST-MoE successor; the original is still suitable as an educational reference.)
- ✓ **johnma2006/mamba-minimal** — `ssm-mamba-block`
  https://github.com/johnma2006/mamba-minimal · code · Python · free
  Evidence: Single-file pure-PyTorch Mamba. README explicitly states `mamba_ssm` CUDA is *not* used; the SSM block is in PyTorch primitives.

### Training

- ✓ **Hugging Face LLM Course — A full training loop (Ch 3.4)** — `training-loop`
  https://huggingface.co/learn/llm-course/chapter3/4 · course · Python · free
  Evidence: Section drops the `Trainer` API; loop, AMP, gradient accumulation, gradient clipping are written by hand.
- ✓ **karpathy/nanoGPT — train.py** — `training-loop`
  https://github.com/karpathy/nanoGPT/blob/master/train.py · code · Python · free
  Evidence: ~300-line training loop — data iteration, AMP, grad accumulation, cosine schedule, DDP — no wrapper Trainer.
- ✓ **labml.ai — Adam optimizer** — `optimizer-from-scratch`
  https://nn.labml.ai/optimizers/adam.html · written · Python · free
  Evidence: Subclasses `torch.optim.Optimizer`; first-moment, second-moment, bias-correction, parameter update all written by hand, annotated against the paper.
- ✓ **rasbt/LLMs-from-scratch — Chapter 7** — `sft`
  https://github.com/rasbt/LLMs-from-scratch/tree/main/ch07 · book · Python · paid
  Evidence: Instruction fine-tuning loop in pure PyTorch with prompt loss-masking; no `transformers.Trainer` or TRL `SFTTrainer`.
- ✓ **rasbt/LLMs-from-scratch — DPO from scratch notebook** — `dpo`
  https://github.com/rasbt/LLMs-from-scratch/blob/main/ch07/04_preference-tuning-with-dpo/dpo-from-scratch.ipynb · code · Python · free
  Evidence: Implements the DPO log-ratio loss directly in PyTorch; no TRL `DPOTrainer`.

### Inference

- ✓ **Raschka — Understanding and Coding the KV Cache from Scratch** — `kv-cache`
  https://magazine.sebastianraschka.com/p/coding-the-kv-cache-in-llms · written · Python · free · 2025-06-17
  Evidence: Side-by-side `gpt_ch04.py` (no cache) vs `gpt_with_kv_cache.py` (with cache) — cache written explicitly in PyTorch, ~5× speedup measured.
- ✓ **HF — KV Cache from scratch in nanoVLM** — `kv-cache`
  https://huggingface.co/blog/kv-cache · written · Python · free · 2025-06-04
  Evidence: Per-layer KV cache built into the nanoVLM attention block — prefill/decode separation written explicitly, 38% speedup.
- ✓ **karpathy/llama2.c** — `inference-engine`
  https://github.com/karpathy/llama2.c · code · C · free
  Evidence: 700-line `run.c` — tokenizer, transformer forward, KV cache, sampling — all in pure C, no external ML library.
- ✓ **romsto/Speculative-Decoding** — `speculative-decoding`
  https://github.com/romsto/Speculative-Decoding · code · Python · free
  Evidence: PyTorch implementation of the Leviathan et al. paper; classic autoregressive and speculative paths are written side by side.

### Retrieval

- ✓ **Ethen Liu — Quick Introduction to Okapi BM25** — `bm25`
  https://ethen8181.github.io/machine-learning/search/bm25_intro.html · written · Python · free
  Evidence: Custom `BM25` class with `fit` / `score` — TF, DF, IDF, length normalization all computed by hand, no `rank_bm25`.
- ✓ **brtholomy/hnsw** — `vector-search`
  https://github.com/brtholomy/hnsw · code · Python · free
  Evidence: Readable Python that mirrors the original paper's pseudocode — `Insert` and `SearchLayer` from scratch, performance sacrificed for clarity.
- ✓ **Pinecone — Hierarchical Navigable Small Worlds (HNSW)** — `vector-search`
  https://www.pinecone.io/learn/series/faiss/hnsw/ · written · Python · free
  Evidence: Walks skip-lists → NSW → HNSW with code snippets and parameter-tuning experiments. Conceptual pair for brtholomy/hnsw.
- ✓ **HF — Code a simple RAG from scratch** — `rag-pipeline`
  https://huggingface.co/blog/ngxson/make-your-own-rag · written · Python · free · author: Xuan-Son Nguyen · 2024-10-29
  Evidence: Vector DB as a plain Python list, `cosine_similarity` from primitives, no LangChain/LlamaIndex/Chroma.

### Agents

- ✓ **Victor Dibia — The Agent Execution Loop** — `agent-loop`
  https://victordibia.com/blog/agent-execution-loop/ · written · Python · free · 2025-12-09
  Evidence: Custom `Agent` class with `AsyncOpenAI`; loop, tool dispatch, termination written explicitly. Framework comparison comes *after* the from-scratch build.
- ✓ **Anthropic — Building effective agents** — `agent-loop`
  https://www.anthropic.com/research/building-effective-agents · written · Python · free · 2024-12-19
  Evidence: Explicit guidance "use LLM APIs directly: many patterns can be implemented in a few lines of code"; companion cookbook shows patterns without frameworks.
- ✓ **ghuntley — How to build a coding agent (free workshop)** — `coding-agent`
  https://ghuntley.com/agent/ · written · Mixed · free · 2025-08-24
  Evidence: '~300 lines of code running in a loop' — five tool primitives (read, list, bash, search, edit) and the agent loop all written by hand.
- ✓ **Lane Wagner — Build an AI Coding Agent in Python** — `coding-agent`
  https://www.freecodecamp.org/news/build-an-ai-coding-agent-in-python/ · course · Python · free
  Evidence: boot.dev / freeCodeCamp course directly against the Gemini API; agentic loop and tools written by the learner.

### Evaluation

- ✓ **Hamel Husain — Using LLM-as-a-Judge for Evaluation** — `llm-as-judge`
  https://hamel.dev/blog/posts/llm-judge/ · written · Mixed · free · 2024-10-29
  Evidence: Seven-step process — write the judge prompt, validate against a domain expert's labels, iterate until > 90% agreement. No judge library.
- ✓ **HF Cookbook — LLM-as-a-judge (Aymeric Roucher)** — `llm-as-judge`
  https://huggingface.co/learn/cookbook/llm_judge · written · Python · free
  Evidence: Notebook with raw `InferenceClient` calls; measures Pearson correlation with human raters and iterates the prompt.

### Beyond Text

- ✓ **lucidrains/denoising-diffusion-pytorch** — `diffusion-ddpm`
  https://github.com/lucidrains/denoising-diffusion-pytorch · code · Python · free
  Evidence: Custom `Unet` + `GaussianDiffusion` from the Ho et al. paper. No `diffusers` library.
- ✓ **HF Diffusion Models Course — Unit 1** — `diffusion-ddpm`
  https://huggingface.co/learn/diffusion-course/unit0/1 · course · Python · free
  Evidence: Unit 1 syllabus is "Introduction to 🤗 Diffusers and implementation from 0" — the from-scratch notebook precedes the library-based units.
- ✓ **moein-shariatnia/OpenAI-CLIP** — `clip`
  https://github.com/moein-shariatnia/OpenAI-CLIP · code · Python · free
  Evidence: Separate image + text encoders + projection heads in PyTorch; contrastive loss written explicitly. `timm`/`transformers` provide backbones only.
- ✓ **AssemblyAI / Michael Nguyen — Building an End-to-End Speech Recognition Model in PyTorch** — `asr-ctc`
  https://www.assemblyai.com/blog/end-to-end-speech-recognition-pytorch · written · Python · free · 2020-12-01
  Evidence: Deep-Speech-2-style architecture (residual CNNs + bidirectional GRUs) trained with CTC; no pretrained Wav2Vec2/Whisper checkpoint.

---

## Rejected (and why)

- ✗ **learnbybuilding.ai — A beginner's guide to building a RAG application from scratch** (Bill Chambers)
  https://learnbybuilding.ai/tutorials/rag-from-scratch
  Reason: technically library-free (uses Jaccard similarity + Ollama) but skips chunking and embeddings entirely. Author flags this in an "Areas for improvement" section. The point of a from-scratch RAG guide is to teach the embedding + retrieval + generation triad — this one only covers 1/3.

- ✗ **PyTorch Blog — A Hitchhiker's Guide to Speculative Decoding**
  https://pytorch.org/blog/hitchhikers-guide-speculative-decoding/
  Reason: a conceptual blog post / production-release announcement, not an implementation walkthrough. Points readers to IBM's HF TGI fork and the `fms-fsdp` repo for actual code. Useful background reading but not a from-scratch guide.

- ✗ **EleutherAI/lm-evaluation-harness**
  https://github.com/EleutherAI/lm-evaluation-harness
  Reason: this is the *library* — the production framework for running benchmarks. By definition, "use lm-eval-harness" is the opposite of "build your own eval harness." The eval-harness target therefore ships as a gap (candidate for an original or for a future from-scratch tutorial).

- ✗ **HF blog — Training and Finetuning Reranker Models with Sentence Transformers**
  https://huggingface.co/blog/train-reranker
  Reason: tutorial is built around the `sentence-transformers` library; the cross-encoder objective is hidden behind framework abstractions. The reranker target ships as a gap.

- ✗ **Various Adam-from-scratch Medium articles**
  Reason: labml.ai's annotated Adam is the authoritative, well-maintained reference for the same content. One canonical link beats three lossy reposts.

- ✗ **Amit Chaudhary — The Anatomy of Tool Calling** (for `tool-layer`)
  https://amitness.com/posts/function-calling-schema/
  Reason: covers function-to-JSON-schema conversion well but stops short of dispatch, runtime validation, and error recovery. The `tool-layer` target requires the full end-to-end dispatcher — partial coverage would mislead a learner. Kept as a gap.

- ✗ **carloodq/rrf** (for `hybrid-search`)
  https://github.com/carloodq/rrf
  Reason: uses the `rank_bm25` library and a vector-DB SDK for the retrieval halves; the manual notebook is mostly orchestration around those. Chauzov's article (accepted above) implements RRF more directly and was preferred.

- ✗ **HF blog — Training and Finetuning Reranker Models with Sentence Transformers** (for `reranker`)
  https://huggingface.co/blog/train-reranker
  Reason (re-affirmed): tutorial is built around the `sentence-transformers` library; the cross-encoder objective is hidden behind framework abstractions. Re-checked during the second sweep — same conclusion.

---

## Open gaps (8 targets — all now filled by originals/)

- `lr-schedule` (Training) — [`originals/lr-schedule.md`](../originals/lr-schedule.md)
- `reward-model` (Training) — [`originals/reward-model.md`](../originals/reward-model.md)
- `reranker` (Retrieval) — [`originals/reranker.md`](../originals/reranker.md)
- `tool-layer` (Agents) — [`originals/tool-layer.md`](../originals/tool-layer.md)
- `agent-memory` (Agents) — [`originals/agent-memory.md`](../originals/agent-memory.md)
- `multi-agent` (Agents) — [`originals/multi-agent.md`](../originals/multi-agent.md)
- `eval-harness` (Evaluation) — [`originals/eval-harness.md`](../originals/eval-harness.md)
- `calibration-hallucination` (Evaluation) — [`originals/calibration-hallucination.md`](../originals/calibration-hallucination.md)

All 8 open gaps are now filled by curator-authored originals. Every
target in the index has either a verified external guide or an original.

---

## Notes for re-audit

- The PyTorch blog rejection above is good evidence that "blog post about a paper" is rarely a from-scratch guide — a useful heuristic for future contributions.
- `lucidrains/mixture-of-experts` is the right educational reference today but is being deprecated in favor of `ST-MoE`. Reassess at the next quarterly audit.
- `nanoGPT` is officially "deprecated" in favor of `nanochat` per its own README. Both are kept because nanoGPT is the smaller / more focused educational artifact; nanochat is the more complete pipeline. Reassess at the next quarterly audit.
- The 14 open gaps represent the real terrain of "what does the AI stack lack a good from-scratch guide for in 2026" — a high-leverage list for future originals.
