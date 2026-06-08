<h1 align="center">build-your-own-ai</h1>

<p align="center">
  <strong>Master modern AI by building it from scratch.</strong><br>
  A curated index of the best build-it-yourself guides for tokenizers,
  attention, training loops, RAG, agents, evals, and more.
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/content-CC--BY--4.0-blue.svg" alt="content license"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/code-MIT-green.svg" alt="code license"></a>
  <img src="https://img.shields.io/badge/targets-62-informational.svg" alt="target count">
  <img src="https://img.shields.io/badge/guides-80-informational.svg" alt="guide count">
  <img src="https://img.shields.io/badge/originals-9-purple.svg" alt="originals">
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
- **Depth at a glance:** category totals appear in the table of contents
  below — pick the layer you want to dig into.

## Table of contents

1. [Foundations](#foundations) — 7 targets · 9 guides
1. [The Model](#the-model) — 11 targets · 21 guides
1. [Training](#training) — 13 targets · 17 guides
1. [Inference](#inference) — 7 targets · 8 guides
1. [Retrieval](#retrieval) — 7 targets · 7 guides
1. [Agents](#agents) — 8 targets · 9 guides
1. [Evaluation](#evaluation) — 3 targets · 2 guides
1. [Beyond Text](#beyond-text) — 6 targets · 7 guides

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

- [**Python**: _Word2vec from Scratch (NumPy)_](https://jaketae.github.io/study/word2vec/) — Jake Tae · written · free
- [**Python**: _word2vec-pytorch (reproduction of the original paper)_](https://github.com/OlgaChernytska/word2vec-pytorch) — Olga Chernytska · code · free

#### Autograd / micro-framework <sub>★★☆ · afternoon</sub>

**What you build:** A scalar-valued autograd engine with reverse-mode differentiation — the kernel of PyTorch/JAX in ~150 lines.

**What you'll understand after:** Why neural networks are 'just' big differentiable functions, and what every deep-learning framework is doing under the hood.

- [**Python**: _micrograd_](https://github.com/karpathy/micrograd) — Andrej Karpathy · code · free

#### Backprop by hand on an MLP <sub>★★☆ · afternoon</sub>

**What you build:** A multi-layer perceptron trained on a toy task with gradients computed manually, then verified against autograd.

**What you'll understand after:** The gradient flow through every layer — so 'why is loss not going down' stops being a black box.

- [**Python**: _Neural Networks: Zero to Hero (lectures 1–4)_](https://github.com/karpathy/nn-zero-to-hero) — Andrej Karpathy · course · free

#### Layer normalization (LN, RMSNorm) <sub>★☆☆ · easy</sub>

**What you build:** LayerNorm and RMSNorm implemented from scratch — the normalization that sits inside every transformer block.

**What you'll understand after:** Why every modern transformer block sandwiches sub-layers with normalization — and what the gain / bias parameters are doing.

- [**Python**: _Layer Normalization (annotated PyTorch implementation)_](https://nn.labml.ai/normalization/layer_norm/index.html) — labml.ai · written · free

#### Weight initialization (Xavier / Kaiming) <sub>★☆☆ · easy</sub>

**What you build:** Xavier (Glorot) and Kaiming (He) initialization from scratch — derived from the variance-preservation requirement and verified empirically by tracking activation variance across layers.

**What you'll understand after:** Why a deep net's loss explodes-then-flattens with naive `randn` init, and why the right initializer keeps gradients alive through 50+ layers.

- [**Python**: _Tutorial 3: Initialization and Optimization (UvA Deep Learning)_](https://lightning.ai/docs/pytorch/stable/notebooks/course_UvA-DL/03-initialization-and-optimization.html) — Phillip Lippe (UvA / PyTorch Lightning) · course · free

#### Dropout <sub>★☆☆ · easy</sub>

**What you build:** Inverted dropout from scratch — Bernoulli masking, the 1/(1−p) scale at training time, and the eval-mode passthrough.

**What you'll understand after:** Why dropout is regularization, why the scale factor lives at train time (not eval), and why monitoring train/val gap is the only way to set p.

- [**Python**: _Regularization from Scratch — Dropout_](https://nilanjanchattopadhyay.github.io/basics/2020/04/20/Regularization-from-Scratch-Dropout.html) — Nilanjan Chattopadhyay · written · free

### The Model
_Attention to a full small LM._

#### Attention from scratch <sub>★★☆ · afternoon</sub>

**What you build:** Scaled dot-product attention, then multi-head attention, in pure tensor primitives — no `nn.MultiheadAttention`.

**What you'll understand after:** Exactly how attention computes a weighted average of values — and why 'attention is all you need' is more than a slogan.

- [**Python**: _Understanding and Coding Self-Attention, Multi-Head Attention, Causal-Attention, and Cross-Attention in LLMs_](https://magazine.sebastianraschka.com/p/understanding-and-coding-self-attention) — Sebastian Raschka · written · free
- [**Python**: _The Annotated Transformer_](https://nlp.seas.harvard.edu/2018/04/03/attention.html) — Alexander 'Sasha' Rush (Harvard NLP) · written · free

#### Grouped-query / multi-query attention <sub>★★☆ · afternoon</sub>

**What you build:** GQA and MQA — attention variants where Q heads outnumber KV heads — implemented from scratch as a drop-in alternative to multi-head attention.

**What you'll understand after:** Why LLaMA-2 70B, Mistral, and most frontier models use GQA — and how the same code recovers MHA at one extreme and MQA at the other.

- [**Python**: _Grouped Query Attention (GQA) explained with code_](https://medium.com/@maxshapp/grouped-query-attention-gqa-explained-with-code-e56ee2a1df5a) — Max Shap · written · free
- [**Python**: _grouped-query-attention-pytorch_](https://github.com/fkodom/grouped-query-attention-pytorch) — fkodom · code · free

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
- [**C**: _llm.c (LLM training in pure C/CUDA)_](https://github.com/karpathy/llm.c) — Andrej Karpathy · code · free

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

#### Long context (RoPE scaling, NTK, YaRN) <sub>★★★ · weekend</sub>

**What you build:** Position Interpolation and NTK-aware / YaRN RoPE scaling — the techniques that extend a pretrained model from a 4k context to 32k+.

**What you'll understand after:** Why the same model trained on 2k tokens can be coaxed into 100k context with a few lines of math — and where each scaling scheme breaks.

- [**Python**: _How LLMs Scaled from 512 to 2M Context: A Technical Deep Dive_](https://amaarora.github.io/posts/2025-09-21-rope-context-extension.html) — Aman Arora · written · free

#### State-space / Mamba-style block <sub>★★★ · weekend</sub>

**What you build:** A minimal selective state-space model layer — a serious linear-time alternative to attention.

**What you'll understand after:** Why SSMs handle long sequences cheaply, and where they trade off against attention.

- [**Python**: _mamba-minimal_](https://github.com/johnma2006/mamba-minimal) — John Ma · code · free

#### Activations (GELU, SiLU, SwiGLU) <sub>★★☆ · afternoon</sub>

**What you build:** GELU and SiLU (Swish) implemented from their definitions, then assembled into SwiGLU — the gated FFN that every post-2023 frontier LLM (LLaMA, Mistral, DeepSeek, Qwen, Gemma) uses.

**What you'll understand after:** Why the FFN in modern LLMs is not `Linear → ReLU → Linear` but a gated three-matrix variant, and how a one-line tweak (`F.silu(W1·x) * W3·x`) shows up in every state-of-the-art checkpoint.

- [**Python**: _What Is SwiGLU? How to Implement It? And Why Does It Work?_](https://azizbelaweid.substack.com/p/what-is-swiglu-how-to-implement-it) — Aziz Belaweid · written · free

#### Flash Attention <sub>★★★ · weekend</sub>

**What you build:** Flash Attention's tiled / online-softmax algorithm from scratch — first in plain PyTorch for algorithmic clarity, then (optionally) in a Triton kernel to see where the speedup actually comes from.

**What you'll understand after:** Why Flash Attention is faster *and* uses less memory than naive attention — it never materializes the full N×N attention matrix — and why the same recipe (FA1 → FA2 → FA3 → FA4) keeps showing up in every fast-inference paper.

- [**Python**: _FlashAttention-PyTorch (FA1–FA4, educational)_](https://github.com/shreyansh26/FlashAttention-PyTorch) — Shreyansh Singh · code · free
- [**Python**: _Understanding Flash Attention — Writing the Algorithm from Scratch in Triton_](https://alexdremov.me/understanding-flash-attention-writing-the-algorithm-from-scratch-in-triton/) — Alex Dremov · written · free

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

> _Gap target — original starter guide planned in [`originals/lr-schedule.md`](originals/lr-schedule.md)._

#### Mixed precision + gradient accumulation <sub>★★☆ · afternoon</sub>

**What you build:** FP16/BF16 forward pass with FP32 master weights, plus gradient accumulation to simulate large batches on small GPUs.

**What you'll understand after:** The practical scaling tricks that turn a 'too big to fit' run into one you can actually do.

- [**Mixed**: _Mixed Precision Training from Scratch_](https://tspeterkim.github.io/posts/mixed-precision-from-scratch) — Taeksang Peter Kim · written · free

#### Distributed training (DDP from scratch) <sub>★★☆ · afternoon</sub>

**What you build:** A multi-GPU training run using PyTorch's Distributed Data Parallel — process groups, the gradient all-reduce, and the launch script — assembled from primitives.

**What you'll understand after:** What `DistributedDataParallel` actually does in your backward pass, and why the all-reduce overlaps with backward computation.

- [**Python**: _Getting Started with Distributed Data Parallel (official PyTorch tutorial)_](https://docs.pytorch.org/tutorials/intermediate/ddp_tutorial.html) — Shen Li (with edits by Joe Zhu and Chirag Pandya) · written · free
- [**Python**: _Distributed data parallel training in PyTorch_](https://yangkky.github.io/2019/07/08/distributed-pytorch-tutorial.html) — Kevin Yang · written · free

#### Supervised fine-tuning (SFT) <sub>★★☆ · afternoon</sub>

**What you build:** Fine-tune a small base LM on an instruction dataset — the first half of every modern post-training pipeline.

**What you'll understand after:** Why the same base model can become a chatbot, a coding assistant, or a math tutor depending purely on the SFT data.

- [**Python**: _Build a Large Language Model (From Scratch) — Chapter 7: Instruction fine-tuning_](https://github.com/rasbt/LLMs-from-scratch/tree/main/ch07) — Sebastian Raschka · book · paid

#### LoRA / parameter-efficient fine-tuning <sub>★★☆ · afternoon</sub>

**What you build:** A LoRA (low-rank adapter) layer from scratch — two low-rank matrices bolted onto a frozen pretrained linear layer — and a fine-tune that updates < 1% of parameters.

**What you'll understand after:** Why a 4096×4096 weight matrix can be adapted with ~65k extra parameters, and what that buys (and costs) compared with full fine-tuning.

- [**Python**: _Build a Large Language Model (From Scratch) — Appendix E: Parameter-efficient Finetuning with LoRA_](https://github.com/rasbt/LLMs-from-scratch/tree/main/appendix-E) — Sebastian Raschka · book · paid
- [**Python**: _LoRA (Jake Tae)_](https://jaketae.github.io/study/lora/) — Jake Tae · written · free

#### Reward model <sub>★★★ · weekend</sub>

**What you build:** Train a reward model on pairwise preference data — the scoring function that drives every RLHF-style pipeline.

**What you'll understand after:** How human preferences become a differentiable signal — and why this single object is RLHF's most fragile component.

> _Gap target — original starter guide planned in [`originals/reward-model.md`](originals/reward-model.md)._

#### Constitutional AI / RLAIF <sub>★★★ · weekend</sub>

**What you build:** The two-stage Constitutional AI pipeline: (1) supervised self-critique and revision against a list of principles, then (2) RLAIF — preference labels generated by an AI judge instead of humans.

**What you'll understand after:** Why Claude's safety training scales without armies of human labelers — and the trade-offs of swapping human feedback for model feedback.

- [**Python**: _RLAIF: Reinforcement Learning from AI Feedback_](https://cameronrwolfe.substack.com/p/rlaif-reinforcement-learning-from) — Cameron R. Wolfe · written · free
- [**Python**: _RLHF Book — Constitutional AI & AI Feedback_](https://rlhfbook.com/c/13-cai) — Nathan Lambert · book · free

#### DPO / preference tuning <sub>★★★ · weekend</sub>

**What you build:** A Direct Preference Optimization loop that aligns a model from preferences alone — no separate reward model, no RL.

**What you'll understand after:** Why DPO replaced RLHF for many teams, and the trade-offs it makes.

- [**Python**: _DPO from scratch (LLMs-from-scratch Ch 7.4)_](https://github.com/rasbt/LLMs-from-scratch/blob/main/ch07/04_preference-tuning-with-dpo/dpo-from-scratch.ipynb) — Sebastian Raschka · code · free

#### PPO-style RL loop (RLHF) <sub>★★★ · weekend</sub>

**What you build:** A miniature RL post-training loop — policy update with KL penalty and advantage estimation, on a tiny model.

**What you'll understand after:** What the 'RL' in RLHF actually does, and where it differs from classic RL.

- [**Python**: _lm-human-preference-details (PyTorch reproduction of OpenAI's RLHF)_](https://github.com/vwxyzjn/lm-human-preference-details) — Shengyi Costa Huang · code · free
- [**Python**: _The N Implementation Details of RLHF with PPO_](https://huggingface.co/blog/the_n_implementation_details_of_rlhf_with_ppo) — Shengyi Costa Huang, Tianlin Liu, Leandro von Werra (Hugging Face) · written · free

#### Knowledge distillation <sub>★★☆ · afternoon</sub>

**What you build:** A teacher → student distillation: the soft-label loss (KL-div on temperature-scaled logits) combined with the hard-label cross-entropy, training a small student to recover most of a big teacher's accuracy.

**What you'll understand after:** Why you can compress a 70B model into a 7B model with most of the quality intact — and why the student often *outperforms* the same architecture trained from labels alone.

- [**Python**: _Knowledge Distillation Tutorial (official PyTorch)_](https://docs.pytorch.org/tutorials/beginner/knowledge_distillation_tutorial.html) — Alexandros Chariton · written · free
- [**Python**: _Distilling the Knowledge in a Neural Network (annotated PyTorch)_](https://nn.labml.ai/distillation/index.html) — labml.ai · written · free

#### GRPO (DeepSeek-R1 style) <sub>★★★ · weekend</sub>

**What you build:** Group Relative Policy Optimization from scratch — sample G completions per prompt, score them with a verifiable reward, normalize advantages within the group, and update the policy with a clipped PPO-style objective and KL penalty.

**What you'll understand after:** Why DeepSeek-R1 ditched the value model and what that buys (less memory, simpler training) — and why GRPO is the algorithm behind the recent reasoning-model wave.

- [**Python**: _GRPO-Zero — DeepSeek-R1's GRPO from scratch_](https://github.com/policy-gradient/GRPO-Zero) — policy-gradient (open-source contributors) · code · free

### Inference
_Making a trained model useful._

#### Sampling (greedy / temp / top-k / top-p) <sub>★☆☆ · easy</sub>

**What you build:** Decoding-strategy functions: greedy, temperature, top-k, nucleus (top-p) — and a side-by-side comparison on the same prompt.

**What you'll understand after:** Why the same model can sound creative or robotic depending entirely on three lines of decoding code.

- [**Python**: _Decoding Strategies in Large Language Models_](https://huggingface.co/blog/mlabonne/decoding-strategies) — Maxime Labonne · written · free

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

#### LLM watermarking <sub>★★★ · weekend</sub>

**What you build:** A token-level watermark: bias decoding toward a pseudo-random 'green' subset of the vocabulary at each step, then a statistical detector that recovers the watermark with interpretable p-values — the Kirchenbauer et al. recipe.

**What you'll understand after:** How model outputs can be tagged in a way that's detectable but doesn't change human-perceived quality — and where the watermark breaks under paraphrasing.

- [**Python**: _lm-watermarking (official Kirchenbauer et al. implementation)_](https://github.com/jwkirchenbauer/lm-watermarking) — John Kirchenbauer (paper authors) · code · free
- [**Python**: _LMWatermark (educational PyTorch re-implementation)_](https://github.com/BrianPulfer/LMWatermark) — Brian Pulfer · code · free

#### Structured / constrained decoding (JSON, regex, grammar) <sub>★★☆ · afternoon</sub>

**What you build:** Logit-masked decoding that constrains generation to a regex, JSON-schema, or context-free grammar — by compiling the constraint into a finite-state machine over the vocabulary and zeroing out invalid tokens at every step.

**What you'll understand after:** Why 'structured output' isn't an LLM capability — it's the *sampler's* job — and why the same FSM-over-vocab trick underpins Outlines, XGrammar, vLLM's guided decoding, and OpenAI's strict JSON mode.

> _Gap target — original starter guide planned in [`originals/structured-decoding.md`](originals/structured-decoding.md)._

#### Quantization (INT8 / INT4) <sub>★★★ · weekend</sub>

**What you build:** Post-training quantization of a small LM to INT8 and INT4 — with the accuracy/throughput trade-off measured.

**What you'll understand after:** Why 4-bit inference is the default for local deployment, and what it actually costs.

- [**Python**: _Introduction to Weight Quantization_](https://towardsdatascience.com/introduction-to-weight-quantization-2494701b9c0c/) — Maxime Labonne · written · free

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

- [**Python**: _Hybrid retrieval with reciprocal rank fusion: solving the score normalization problem_](https://avchauzov.github.io/blog/2025/hybrid-retrieval-rrf-rank-fusion/) — Andrey Chauzov · written · free

#### Reranker (cross-encoder) <sub>★★☆ · afternoon</sub>

**What you build:** A cross-encoder that scores (query, document) pairs — trained from scratch on a small relevance dataset.

**What you'll understand after:** Why the best retrieval pipelines are always 'retrieve cheap, rerank expensive,' and what that actually buys you.

> _Gap target — original starter guide planned in [`originals/reranker.md`](originals/reranker.md)._

#### Retrieval evaluation (Recall@K, MRR, NDCG) <sub>★☆☆ · easy</sub>

**What you build:** A small evaluation kit that scores a retriever's output against a labeled set — Recall@K, Mean Reciprocal Rank, MAP@K, and NDCG@K, all from primitives.

**What you'll understand after:** Why 'top-3 looks right' isn't an evaluation — and what each metric tells you that the others don't (recall is set-level; MRR cares only about the first hit; NDCG weights position with diminishing returns).

- [**Python**: _Evaluation Measures in Information Retrieval_](https://www.pinecone.io/learn/offline-evaluation/) — Pinecone Learn · written · free

#### End-to-end RAG pipeline (no frameworks) <sub>★★☆ · afternoon</sub>

**What you build:** Chunk → embed → retrieve → answer, in plain Python — no LangChain, no LlamaIndex, no vector DB SDK.

**What you'll understand after:** What RAG frameworks actually do, why most of the value is in the chunking + retrieval + prompt, and where they hide complexity.

- [**Python**: _Code a simple RAG from scratch_](https://huggingface.co/blog/ngxson/make-your-own-rag) — Xuan-Son Nguyen (ngxson) · written · free

#### GraphRAG <sub>★★★ · weekend</sub>

**What you build:** Microsoft's GraphRAG pipeline from scratch — chunk → entity & relationship extraction with an LLM → knowledge-graph construction → Leiden community detection → community summarization → query-focused answer synthesis.

**What you'll understand after:** Why graph-structured retrieval beats vanilla RAG on multi-hop and aggregation questions — and what the full GraphRAG paper actually does, end to end, without the framework.

- [**Python**: _example-graphrag (end-to-end GraphRAG pipeline from scratch)_](https://github.com/stephenc222/example-graphrag) — Stephen Collins · code · free

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

> _Gap target — original starter guide planned in [`originals/tool-layer.md`](originals/tool-layer.md)._

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

#### ReAct pattern (Reasoning + Acting) <sub>★★☆ · afternoon</sub>

**What you build:** The Thought → Action → Observation loop from the original ReAct paper, with regex-based action parsing and tool dispatch — no LangChain, no LlamaIndex.

**What you'll understand after:** Why 'ReAct' is a prompting pattern, not an LLM capability — and how a single regex turns text into agency.

- [**Python**: _agent-implementation (basic ReAct agent from scratch)_](https://github.com/mattambrogi/agent-implementation) — Matt Ambrogi · code · free
- [**Python**: _Create ReAct AI Agent from Scratch using Python Without any Framework_](https://shafiqulai.github.io/blogs/blog_3.html) — Shafiqul Islam Sumon · written · free

#### Tree of Thoughts (deliberate reasoning) <sub>★★☆ · afternoon</sub>

**What you build:** A Tree-of-Thoughts reasoner: a `ThoughtNode` tree expanded breadth-wise by repeatedly prompting the LLM for k candidate next-thoughts, traversed iteratively until a stopping condition.

**What you'll understand after:** Why some problems demand search over reasoning paths instead of a single chain — and the cost trade-off you accept when you pay 2× to 10× the inference budget for it.

- [**Python**: _How to Implement a Tree of Thoughts in Python_](https://stephencollins.tech/posts/how-to-implement-a-tree-of-thoughts-in-python) — Stephen Collins · written · free

#### MCP server (Model Context Protocol) <sub>★★☆ · afternoon</sub>

**What you build:** An MCP server and client built from scratch — first with the official Python SDK to expose tools / resources / prompts, then at the protocol level over raw STDIO + JSON-RPC to see what's actually on the wire.

**What you'll understand after:** Why MCP is 'USB-C for LLMs' — and how a 20-line server unlocks Claude Desktop, Cursor, and every MCP-aware host without any per-host integration.

- [**Python**: _Introduction to Model Context Protocol (official Anthropic course)_](https://anthropic.skilljar.com/introduction-to-model-context-protocol) — Anthropic · course · free
- [**Mixed**: _Understanding MCP Through Raw STDIO Communication_](https://foojay.io/today/understanding-mcp-through-raw-stdio-communication/) — David Parry · written · free

### Evaluation
_Knowing if it actually works._

#### Eval harness <sub>★★☆ · afternoon</sub>

**What you build:** A pluggable task runner: task → prompt template → model call → score — the miniature of `lm-evaluation-harness`.

**What you'll understand after:** Why eval harnesses are 80% data engineering and how to keep results comparable across model versions.

> _Gap target — original starter guide planned in [`originals/eval-harness.md`](originals/eval-harness.md)._

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

#### Vision Transformer (ViT) <sub>★★☆ · afternoon</sub>

**What you build:** A Vision Transformer from scratch — patch embedding, transformer encoder over patches, classification head — trained on CIFAR-10 or similar.

**What you'll understand after:** Why 'an image is worth 16×16 words' — and why the same transformer that does language can do vision once you tokenize pixels.

- [**Python**: _vision-transformer-from-scratch_](https://github.com/tintn/vision-transformer-from-scratch) — Tin Nguyen · code · free

#### Diffusion model (DDPM) <sub>★★★ · weekend</sub>

**What you build:** A toy image diffusion model — forward noising, reverse denoising, training a U-Net to predict noise.

**What you'll understand after:** Why a model trained to predict noise can generate images, and how DDPM/DDIM/etc. relate.

- [**Python**: _denoising-diffusion-pytorch_](https://github.com/lucidrains/denoising-diffusion-pytorch) — Phil Wang (lucidrains) · code · free
- [**Python**: _Hugging Face Diffusion Models Course (Unit 1: Introduction)_](https://huggingface.co/learn/diffusion-course/unit0/1) — Jonathan Whitaker, Lewis Tunstall (Hugging Face) · course · free

#### Latent diffusion (Stable Diffusion-style) <sub>★★★ · weekend</sub>

**What you build:** A latent diffusion model — VAE encoder/decoder + a UNet diffusion model that runs in the VAE's latent space, plus text conditioning via CLIP — the recipe behind Stable Diffusion.

**What you'll understand after:** Why Stable Diffusion is fast: it diffuses in a 64×64 latent space, not a 512×512 pixel space — and what the VAE / UNet / CLIP play in the trade-off.

- [**Python**: _Latent Diffusion Models (annotated PyTorch implementation)_](https://nn.labml.ai/diffusion/stable_diffusion/latent_diffusion.html) — labml.ai · written · free

#### CLIP-style contrastive model <sub>★★★ · weekend</sub>

**What you build:** A small dual-encoder (image + text) trained with an InfoNCE contrastive loss — multimodal alignment from scratch.

**What you'll understand after:** How a single embedding space can host both modalities, and why CLIP-style models underpin most modern multimodal systems.

- [**Python**: _Simple Implementation of OpenAI CLIP model_](https://github.com/moein-shariatnia/OpenAI-CLIP) — Moein Shariatnia · code · free

#### Speech recognition (CTC) <sub>★★★ · weekend</sub>

**What you build:** A toy automatic-speech-recognition model: audio features → encoder → CTC loss → greedy decoding.

**What you'll understand after:** How variable-length audio aligns to text without forced alignment, and why CTC is still the workhorse loss for ASR.

- [**Python**: _Building an End-to-End Speech Recognition Model in PyTorch_](https://www.assemblyai.com/blog/end-to-end-speech-recognition-pytorch) — Michael Nguyen (AssemblyAI) · written · free

#### Vision-language model (VLM) <sub>★★★ · weekend</sub>

**What you build:** A small vision-language model: a SigLIP image encoder + a SmolLM2 language backbone joined by a hand-written pixel-shuffle + linear *modality-projection* connector, jointly fine-tuned on image-text data — the nanoVLM recipe.

**What you'll understand after:** Where the 'multi' in multimodal lives — almost entirely in the connector and the training data — and why so many modern VLMs (LLaVA, Idefics, SmolVLM, Phi-Vision) share the same template.

- [**Python**: _nanoVLM: The simplest, fastest repository for training/finetuning small-sized VLMs_](https://huggingface.co/blog/nanovlm) — Aritra Roy Gosthipaty, Andrés Marafioti, Sergio Paniego et al. (Hugging Face) · written · free


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

- Scheduled link-check via CI.
- Quarterly audit of the verification log.
- Currently: **62 build targets** · **80 guides** ·
  **9 originals** · **9 open gaps**.

The full curation trail — every accepted and rejected guide with
evidence — lives in [`PLANNING/03_verification_log.md`](PLANNING/03_verification_log.md).

## License

Content: [CC-BY-4.0](LICENSE) · Code: [MIT](LICENSE).

