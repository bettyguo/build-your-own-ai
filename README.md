<p align="center">
  <img src="assets/banner.png" alt="build-your-own-ai" width="720" onerror="this.style.display='none'">
</p>

<h1 align="center">build-your-own-ai</h1>

<p align="center">
  <strong>Master modern AI by building it from scratch.</strong><br>
  A curated index of the best build-it-yourself guides for tokenizers,
  attention, training loops, RAG, agents, evals, and more.
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/content-CC--BY--4.0-blue.svg" alt="content license"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/code-MIT-green.svg" alt="code license"></a>
  <img src="https://img.shields.io/badge/last%20updated-2026-05-14-brightgreen.svg" alt="last updated">
  <img src="https://img.shields.io/badge/targets-40-informational.svg" alt="target count">
  <img src="https://img.shields.io/badge/originals-4-purple.svg" alt="originals">
</p>

---

## Why this exists

You don't really understand the AI stack until you've built it from scratch.

This is the curated index of the best guides that teach by **reimplementation** —
no "use library X" tutorials, no thin product walkthroughs, no framework
configurators. Every entry teaches you the thing by making you build the thing.

Modeled on the [`build-your-own-x`](https://github.com/codecrafters-io/build-your-own-x)
format (the most-starred repository on GitHub, ~500k stars). Same recipe,
focused tightly on the modern AI stack.

## How to use this

- Each category is a **layer of the stack**, ordered by difficulty.
- Each build target lists **1–3 verified from-scratch guides**, plus *what
  you'll understand after* working through them.
- Difficulty: `★☆☆` easy · `★★☆` real but tractable in an afternoon ·
  `★★★` weekend project.
- `[original]` = an in-repo starter guide for a target where no good public
  guide exists yet (see [`originals/`](originals/)).

## Table of contents

1. [Foundations](#foundations)
1. [The Model](#the-model)
1. [Training](#training)
1. [Inference](#inference)
1. [Retrieval](#retrieval)
1. [Agents](#agents)
1. [Evaluation](#evaluation)
1. [Beyond Text](#beyond-text)

---

### Foundations
_The machinery before the model._

#### Tokenizer (BPE) <sub>★★☆ · afternoon</sub>

**What you build:** A byte-pair-encoding tokenizer that turns raw text into a vocabulary of subword tokens — the same idea that powers GPT-class tokenizers.

**What you'll understand after:** Why models see tokens, not characters or words — and why that single decision shapes every downstream cost and behavior.

- [**Python**: _minbpe_](https://github.com/karpathy/minbpe) — Andrej Karpathy · code · free
- [**Python**: _Let's build the GPT Tokenizer_](https://www.youtube.com/watch?v=zduSFxRajkE) — Andrej Karpathy · video · free

#### Embedding layer <sub>★☆☆ · easy</sub>

**What you build:** A learned lookup table that maps token IDs to dense vectors — the entry point every modern LM shares.

**What you'll understand after:** How discrete tokens become differentiable vectors, why dimensionality choices matter, and why the same matrix often ties to the output head.

> _Open gap — no good from-scratch guide verified yet. Contributions welcome (see `CONTRIBUTING.md`)._

#### Autograd / micro-framework <sub>★★☆ · afternoon</sub>

**What you build:** A scalar-valued autograd engine with reverse-mode differentiation — the kernel of PyTorch/JAX in ~150 lines.

**What you'll understand after:** Why neural networks are 'just' big differentiable functions, and what every deep-learning framework is doing under the hood.

- [**Python**: _micrograd_](https://github.com/karpathy/micrograd) — Andrej Karpathy · code · free

#### Backprop by hand on an MLP <sub>★★☆ · afternoon</sub>

**What you build:** A multi-layer perceptron trained on a toy task with gradients computed manually, then verified against autograd.

**What you'll understand after:** The gradient flow through every layer — so 'why is loss not going down' stops being a black box.

- [**Python**: _Neural Networks: Zero to Hero (lectures 1–4)_](https://github.com/karpathy/nn-zero-to-hero) — Andrej Karpathy · course · free

### The Model
_Attention to a full small LM._

#### Attention from scratch <sub>★★☆ · afternoon</sub>

**What you build:** Scaled dot-product attention, then multi-head attention, in pure tensor primitives — no `nn.MultiheadAttention`.

**What you'll understand after:** Exactly how attention computes a weighted average of values — and why 'attention is all you need' is more than a slogan.

- [**Python**: _Understanding and Coding Self-Attention, Multi-Head Attention, Causal-Attention, and Cross-Attention in LLMs_](https://magazine.sebastianraschka.com/p/understanding-and-coding-self-attention) — Sebastian Raschka · written · free
- [**Python**: _The Annotated Transformer_](https://nlp.seas.harvard.edu/2018/04/03/attention.html) — Alexander 'Sasha' Rush (Harvard NLP) · written · free

#### Positional encodings <sub>★★☆ · afternoon</sub>

**What you build:** Sinusoidal positional encodings, learned positional embeddings, and Rotary Position Embedding (RoPE) — all from scratch.

**What you'll understand after:** Why attention is permutation-equivariant by default and how each scheme breaks that symmetry differently.

- [**Mixed**: _Rotary Embeddings: A Relative Revolution_](https://blog.eleuther.ai/rotary-embeddings/) — EleutherAI (Biderman, Black, Foster, Gao, Hallahan, He, Wang, Wang) · written · free
- [**Python**: _Rotary Positional Embeddings (RoPE)_](https://nn.labml.ai/transformers/rope/index.html) — labml.ai · written · free

#### Transformer block <sub>★★☆ · afternoon</sub>

**What you build:** A single decoder-only transformer block — LayerNorm, multi-head self-attention, MLP, residual connections — stacked into a model.

**What you'll understand after:** Why the same block stacked 12, 24, 96 times scales — and the role each sub-layer plays.

- [**Python**: _nanoGPT — `model.py`_](https://github.com/karpathy/nanoGPT/blob/master/model.py) — Andrej Karpathy · code · free

#### A small GPT <sub>★★☆ · afternoon</sub>

**What you build:** A complete decoder-only language model: tokenizer → embedding → N transformer blocks → output head — trained end-to-end on a small corpus.

**What you'll understand after:** How every modern frontier model is, at its core, a much bigger version of what you just trained.

- [**Python**: _Let's reproduce GPT-2 (124M) — build-nanogpt_](https://github.com/karpathy/build-nanogpt) — Andrej Karpathy · video · free
- [**Python**: _nanoGPT_](https://github.com/karpathy/nanoGPT) — Andrej Karpathy · code · free
- [**Python**: _nanochat_](https://github.com/karpathy/nanochat) — Andrej Karpathy · code · free
- [**Python**: _Build a Large Language Model (From Scratch)_](https://github.com/rasbt/LLMs-from-scratch) — Sebastian Raschka · book · paid

#### A small encoder LM (BERT-style) <sub>★★☆ · afternoon</sub>

**What you build:** A masked-language-model encoder, pretrained on a toy corpus, then fine-tuned with a classification head.

**What you'll understand after:** Why encoder models still win on classification and retrieval — and what they cannot do that decoders can.

- [**Python**: _Masked Language Model (MLM)_](https://nn.labml.ai/transformers/mlm/index.html) — labml.ai · written · free
- [**Python**: _Building BERT with PyTorch from scratch_](https://coaxsoft.com/blog/building-bert-with-pytorch-from-scratch) — COAX Software · written · free

#### Mixture-of-Experts block <sub>★★★ · weekend</sub>

**What you build:** A sparse MoE layer: a gating router that picks top-k experts per token, plus a load-balancing auxiliary loss.

**What you'll understand after:** How frontier models scale parameter count cheaply at inference, and why MoE training is notoriously fiddly.

- [**Python**: _st-moe-pytorch_](https://github.com/lucidrains/st-moe-pytorch) — Phil Wang (lucidrains) · code · free
- [**Python**: _mixture-of-experts (Shazeer-style)_](https://github.com/lucidrains/mixture-of-experts) — Phil Wang (lucidrains) · code · free

#### State-space / Mamba-style block <sub>★★★ · weekend</sub>

**What you build:** A minimal selective state-space model layer — a serious linear-time alternative to attention.

**What you'll understand after:** Why SSMs handle long sequences cheaply, and where they trade off against attention.

- [**Python**: _mamba-minimal_](https://github.com/johnma2006/mamba-minimal) — John Ma · code · free

### Training
_How models learn._

#### Training loop <sub>★★☆ · afternoon</sub>

**What you build:** A complete training loop: data loader, forward pass, loss, optimizer step, eval, checkpointing — the mechanics every book glosses over.

**What you'll understand after:** Why training infrastructure is most of the work even when the model code is a few hundred lines.

- [**Python**: _A full training loop — Hugging Face LLM Course (Ch 3.4)_](https://huggingface.co/learn/llm-course/chapter3/4) — Hugging Face · course · free
- [**Python**: _nanoGPT — `train.py`_](https://github.com/karpathy/nanoGPT/blob/master/train.py) — Andrej Karpathy · code · free

#### Optimizer (SGD → Adam → AdamW) <sub>★★☆ · afternoon</sub>

**What you build:** SGD with momentum, then Adam, then AdamW — implemented from scratch and compared on the same toy problem.

**What you'll understand after:** Why AdamW dominates LLM pretraining and what every term in the update rule is doing.

- [**Python**: _Adam Optimizer (annotated PyTorch implementation)_](https://nn.labml.ai/optimizers/adam.html) — labml.ai · written · free

#### Learning-rate schedule <sub>★☆☆ · easy</sub>

**What you build:** Linear warmup + cosine decay schedule, plotted against loss curves on a small training run.

**What you'll understand after:** Why almost every modern run uses this exact shape and how badly things break without warmup.

> _Open gap — no good from-scratch guide verified yet. Contributions welcome (see `CONTRIBUTING.md`)._

#### Mixed precision + gradient accumulation <sub>★★☆ · afternoon</sub>

**What you build:** FP16/BF16 forward pass with FP32 master weights, plus gradient accumulation to simulate large batches on small GPUs.

**What you'll understand after:** The practical scaling tricks that turn a 'too big to fit' run into one you can actually do.

> _Open gap — no good from-scratch guide verified yet. Contributions welcome (see `CONTRIBUTING.md`)._

#### Supervised fine-tuning (SFT) <sub>★★☆ · afternoon</sub>

**What you build:** Fine-tune a small base LM on an instruction dataset — the first half of every modern post-training pipeline.

**What you'll understand after:** Why the same base model can become a chatbot, a coding assistant, or a math tutor depending purely on the SFT data.

- [**Python**: _Build a Large Language Model (From Scratch) — Chapter 7: Instruction fine-tuning_](https://github.com/rasbt/LLMs-from-scratch/tree/main/ch07) — Sebastian Raschka · book · paid

#### Reward model <sub>★★★ · weekend</sub>

**What you build:** Train a reward model on pairwise preference data — the scoring function that drives every RLHF-style pipeline.

**What you'll understand after:** How human preferences become a differentiable signal — and why this single object is RLHF's most fragile component.

> _Gap target — original starter guide planned in [`originals/reward-model.md`](originals/reward-model.md)._

#### DPO / preference tuning <sub>★★★ · weekend</sub>

**What you build:** A Direct Preference Optimization loop that aligns a model from preferences alone — no separate reward model, no RL.

**What you'll understand after:** Why DPO replaced RLHF for many teams, and the trade-offs it makes.

- [**Python**: _DPO from scratch (LLMs-from-scratch Ch 7.4)_](https://github.com/rasbt/LLMs-from-scratch/blob/main/ch07/04_preference-tuning-with-dpo/dpo-from-scratch.ipynb) — Sebastian Raschka · code · free

#### PPO / GRPO-style RL loop <sub>★★★ · weekend</sub>

**What you build:** A miniature RL post-training loop — policy update with KL penalty and advantage estimation, on a tiny model.

**What you'll understand after:** What the 'RL' in RLHF actually does, and where it differs from classic RL.

> _Open gap — no good from-scratch guide verified yet. Contributions welcome (see `CONTRIBUTING.md`)._

### Inference
_Making a trained model useful._

#### Sampling (greedy / temp / top-k / top-p) <sub>★☆☆ · easy</sub>

**What you build:** Decoding-strategy functions: greedy, temperature, top-k, nucleus (top-p) — and a side-by-side comparison on the same prompt.

**What you'll understand after:** Why the same model can sound creative or robotic depending entirely on three lines of decoding code.

> _Open gap — no good from-scratch guide verified yet. Contributions welcome (see `CONTRIBUTING.md`)._

#### KV cache <sub>★★☆ · afternoon</sub>

**What you build:** A key/value cache that turns O(n²) decoding into O(n) — by far the biggest single inference optimization.

**What you'll understand after:** Why the second token is faster than the first, and why long contexts blow up memory.

- [**Python**: _Understanding and Coding the KV Cache in LLMs from Scratch_](https://magazine.sebastianraschka.com/p/coding-the-kv-cache-in-llms) — Sebastian Raschka · written · free
- [**Python**: _KV Cache from scratch in nanoVLM_](https://huggingface.co/blog/kv-cache) — Aritra Roy Gosthipaty, Kashif Rasul, Pedro Cuenca et al. (Hugging Face) · written · free

#### Minimal inference engine <sub>★★★ · weekend</sub>

**What you build:** A `generate()` loop with batching, padding, stop tokens, and the KV cache — what llama.cpp / vLLM do at their core.

**What you'll understand after:** What makes an inference engine fast and where the production complexity actually lives.

- [**C**: _llama2.c_](https://github.com/karpathy/llama2.c) — Andrej Karpathy · code · free

#### Speculative decoding <sub>★★★ · weekend</sub>

**What you build:** A draft + verify decoder: a small fast model proposes tokens, the target model checks them in parallel.

**What you'll understand after:** How modern inference stacks get 2–3× throughput without changing the target model.

- [**Python**: _Speculative-Decoding (Leviathan et al. 2023, PyTorch)_](https://github.com/romsto/Speculative-Decoding) — Romain Storaï · code · free

#### Quantization (INT8 / INT4) <sub>★★★ · weekend</sub>

**What you build:** Post-training quantization of a small LM to INT8 and INT4 — with the accuracy/throughput trade-off measured.

**What you'll understand after:** Why 4-bit inference is the default for local deployment, and what it actually costs.

> _Open gap — no good from-scratch guide verified yet. Contributions welcome (see `CONTRIBUTING.md`)._

### Retrieval
_External memory for LMs._

#### BM25 from scratch <sub>★☆☆ · easy</sub>

**What you build:** Lexical retrieval scoring — the classical TF-IDF descendant that still wins on many real benchmarks.

**What you'll understand after:** Why the boring lexical baseline is hard to beat — and why pure vector search alone is rarely enough.

- [**Python**: _Quick Introduction to Okapi BM25_](https://ethen8181.github.io/machine-learning/search/bm25_intro.html) — Ethen Liu · written · free

#### Vector search (brute force → HNSW) <sub>★★☆ · afternoon</sub>

**What you build:** A brute-force nearest-neighbor index, then a from-scratch HNSW implementation — the algorithm behind most vector databases.

**What you'll understand after:** What every vector DB is actually doing in its hot path, and where the speed comes from.

- [**Python**: _HNSW (tutorial implementation)_](https://github.com/brtholomy/hnsw) — brtholomy · code · free
- [**Python**: _Hierarchical Navigable Small Worlds (HNSW)_](https://www.pinecone.io/learn/series/faiss/hnsw/) — Pinecone Learn · written · free

#### Hybrid search (BM25 + vector) <sub>★★☆ · afternoon</sub>

**What you build:** A retriever that combines BM25 and dense scores — with Reciprocal Rank Fusion and learned weighting compared head to head.

**What you'll understand after:** Why production retrieval is almost never one model — and how the fusion choices change recall.

> _Open gap — no good from-scratch guide verified yet. Contributions welcome (see `CONTRIBUTING.md`)._

#### Reranker (cross-encoder) <sub>★★☆ · afternoon</sub>

**What you build:** A cross-encoder that scores (query, document) pairs — trained from scratch on a small relevance dataset.

**What you'll understand after:** Why the best retrieval pipelines are always 'retrieve cheap, rerank expensive,' and what that actually buys you.

> _Open gap — no good from-scratch guide verified yet. Contributions welcome (see `CONTRIBUTING.md`)._

#### End-to-end RAG pipeline (no frameworks) <sub>★★☆ · afternoon</sub>

**What you build:** Chunk → embed → retrieve → answer, in plain Python — no LangChain, no LlamaIndex, no vector DB SDK.

**What you'll understand after:** What RAG frameworks actually do, why most of the value is in the chunking + retrieval + prompt, and where they hide complexity.

- [**Python**: _Code a simple RAG from scratch_](https://huggingface.co/blog/ngxson/make-your-own-rag) — Xuan-Son Nguyen (ngxson) · written · free

### Agents
_LMs that take actions._

#### Agent loop <sub>★★☆ · afternoon</sub>

**What you build:** The reason → act → observe → repeat loop — the kernel of every agentic AI system — written from scratch.

**What you'll understand after:** Why 'agent' is a loop, not a framework — and how a few hundred lines reproduces the spine of Claude Code / Gemini CLI / Cursor agent mode.

- [**Python**: _The Agent Execution Loop: Building an Agent From Scratch_](https://victordibia.com/blog/agent-execution-loop/) — Victor Dibia · written · free
- [**Python**: _Building effective agents_](https://www.anthropic.com/research/building-effective-agents) — Anthropic · written · free

#### Tool / function-calling layer <sub>★★☆ · afternoon</sub>

**What you build:** A schema-validated tool dispatcher: declare tools, validate the model's JSON arguments, execute, feed results back.

**What you'll understand after:** What 'tool use' actually is at the wire level, why broken JSON is the most common bug, and how to keep the loop alive when a tool fails.

> _Open gap — no good from-scratch guide verified yet. Contributions welcome (see `CONTRIBUTING.md`)._

#### Agent memory (short + long term) <sub>★★☆ · afternoon</sub>

**What you build:** A two-tier memory: a recent-message buffer + a vector-recall long-term store — written without a memory framework.

**What you'll understand after:** How agents stay coherent across long sessions without unbounded context — and where naive approaches break.

> _Gap target — original starter guide planned in [`originals/agent-memory.md`](originals/agent-memory.md)._

#### Multi-agent orchestration <sub>★★★ · weekend</sub>

**What you build:** A planner + workers loop from scratch — no CrewAI, no AutoGen — coordinating multiple LM roles on one task.

**What you'll understand after:** When multi-agent is genuinely better than one good agent, and when it's a coordination cost masquerading as cleverness.

> _Gap target — original starter guide planned in [`originals/multi-agent.md`](originals/multi-agent.md)._

#### Coding agent (file edits + shell) <sub>★★★ · weekend</sub>

**What you build:** A minimal Claude-Code-style agent: read/edit files, run shell commands, observe results, iterate to a goal.

**What you'll understand after:** What today's coding agents actually do under the hood — and why prompt + tools + loop is most of the magic.

- [**Mixed**: _How to build a coding agent (free workshop)_](https://ghuntley.com/agent/) — Geoffrey Huntley · written · free
- [**Python**: _Build an AI Coding Agent in Python_](https://www.freecodecamp.org/news/build-an-ai-coding-agent-in-python/) — Lane Wagner (boot.dev / freeCodeCamp) · course · free

### Evaluation
_Knowing if it actually works._

#### Eval harness <sub>★★☆ · afternoon</sub>

**What you build:** A pluggable task runner: task → prompt template → model call → score — the miniature of `lm-evaluation-harness`.

**What you'll understand after:** Why eval harnesses are 80% data engineering and how to keep results comparable across model versions.

> _Open gap — no good from-scratch guide verified yet. Contributions welcome (see `CONTRIBUTING.md`)._

#### LLM-as-judge <sub>★★☆ · afternoon</sub>

**What you build:** Pairwise and pointwise judge prompts, agreement statistics, and a position-bias sanity check — on a small eval set.

**What you'll understand after:** When LLM-as-judge is reliable, when it's a circular argument, and how to measure that line.

- [**Mixed**: _Using LLM-as-a-Judge For Evaluation: A Complete Guide_](https://hamel.dev/blog/posts/llm-judge/) — Hamel Husain · written · free
- [**Python**: _Using LLM-as-a-judge for an automated and versatile evaluation_](https://huggingface.co/learn/cookbook/llm_judge) — Aymeric Roucher (Hugging Face) · written · free

#### Calibration / hallucination check <sub>★★★ · weekend</sub>

**What you build:** Confidence vs. accuracy curves on a QA dataset — measuring whether the model's stated confidence tracks its real correctness.

**What you'll understand after:** Why 'the model said it was sure' is worthless unless you've measured the calibration — and how to actually measure it.

> _Gap target — original starter guide planned in [`originals/calibration-hallucination.md`](originals/calibration-hallucination.md)._

### Beyond Text
_Vision, audio, multimodal._

#### Diffusion model (DDPM) <sub>★★★ · weekend</sub>

**What you build:** A toy image diffusion model — forward noising, reverse denoising, training a U-Net to predict noise.

**What you'll understand after:** Why a model trained to predict noise can generate images, and how DDPM/DDIM/etc. relate.

- [**Python**: _denoising-diffusion-pytorch_](https://github.com/lucidrains/denoising-diffusion-pytorch) — Phil Wang (lucidrains) · code · free
- [**Python**: _Hugging Face Diffusion Models Course (Unit 1: Introduction)_](https://huggingface.co/learn/diffusion-course/unit0/1) — Jonathan Whitaker, Lewis Tunstall (Hugging Face) · course · free

#### CLIP-style contrastive model <sub>★★★ · weekend</sub>

**What you build:** A small dual-encoder (image + text) trained with an InfoNCE contrastive loss — multimodal alignment from scratch.

**What you'll understand after:** How a single embedding space can host both modalities, and why CLIP-style models underpin most modern multimodal systems.

- [**Python**: _Simple Implementation of OpenAI CLIP model_](https://github.com/moein-shariatnia/OpenAI-CLIP) — Moein Shariatnia · code · free

#### Speech recognition (CTC) <sub>★★★ · weekend</sub>

**What you build:** A toy automatic-speech-recognition model: audio features → encoder → CTC loss → greedy decoding.

**What you'll understand after:** How variable-length audio aligns to text without forced alignment, and why CTC is still the workhorse loss for ASR.

- [**Python**: _Building an End-to-End Speech Recognition Model in PyTorch_](https://www.assemblyai.com/blog/end-to-end-speech-recognition-pytorch) — Michael Nguyen (AssemblyAI) · written · free


## Originals

Short from-scratch starter guides for build targets where no good public guide
exists today. These are the **differentiation lever** of this repo — written
to fill the worst gaps, not to author an alternative textbook.

See [`originals/`](originals/) for the full set.

## Scope (what's in, what's out)

**IN:** from-scratch builds of components of the modern AI stack — tokenizers,
attention, training loops, KV caches, RAG, agents, evals, diffusion, …

**OUT:** general programming builds (see [`build-your-own-x`](https://github.com/codecrafters-io/build-your-own-x));
"use library X" tutorials; product / framework directories; broad career
roadmaps; interview prep.

## Peers

Three sibling repositories — each owns its own noun:

- [**`ai-engineer-roadmap`**](https://github.com/bettyguo/ai-engineer-roadmap) —
  *the path*. Breadth of the AI-engineering career: what to learn, in what order,
  what to read, what to use.
- [**`harness-engineer-roadmap`**](https://github.com/bettyguo/harness-engineer-roadmap) —
  *the harness*. Building and operating agent harnesses, coding agents, IDE integrations.
- [**`llm-interview-prep`**](https://github.com/bettyguo/llm-interview-prep) —
  *the test*. Interview and system-design prep for LLM/AI roles.

This repo is where you go to **build the thing**.

## Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md). Every new entry requires:

1. The URL.
2. One line of **evidence** that the guide is genuinely from-scratch (not a
   library wrapper).
3. A verification date — the guide was confirmed live and current within
   the last 24 months (or the technique is timeless).

Spotted a guide that's mislabeled as "from scratch" but actually a framework
tutorial? Open a [not-from-scratch report](.github/ISSUE_TEMPLATE/not-from-scratch.md).

## Maintenance

- Scheduled weekly link-check via CI.
- Quarterly audit of the verification log.
- Currently: **40 build targets** · **41 guides** ·
  **4 originals** · **14 open gaps**.

The full curation paper trail — every accepted and rejected guide with
evidence — lives in [`PLANNING/03_verification_log.md`](PLANNING/03_verification_log.md).

## License

Content: [CC-BY-4.0](LICENSE) · Code: [MIT](LICENSE).

## Curator

[**Betty Guo (Dongxin Guo / 郭东欣)**](https://github.com/bettyguo) — final-year
PhD candidate in Computer Science, [University of Hong Kong](https://www.cs.hku.hk/),
advised by [Prof. Siu-Ming Yiu](https://www.cs.hku.hk/people/academic-staff/smyiu).
ORCID: [0009-0000-2388-1072](https://orcid.org/0009-0000-2388-1072).

## Star history

<a href="https://star-history.com/#bettyguo/build-your-own-ai&Date">
  <img src="https://api.star-history.com/svg?repos=bettyguo/build-your-own-ai&type=Date" alt="Star history" width="600">
</a>
