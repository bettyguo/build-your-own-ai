# `docs/LAUNCH.md` — launch playbook

> Drafts for the Day-0 push. Tone: confident, factual, no marketing fluff.
> The repo's value is the curation and the originals — say that, don't
> embellish.

---

## Show HN

**Title:**
> Show HN: build-your-own-ai – a curated index of build-it-from-scratch guides for the modern AI stack

**Body (≤ 1500 chars):**
```
You don't really understand the AI stack until you've built it from scratch.

`build-your-own-x` (the #1 most-starred repo on GitHub) proved that the
"learn it by reimplementing it" index is the single most powerful
knowledge-artifact format there is. But it covers AI thinly — three small
categories among the 32.

build-your-own-ai applies the same format with focus and a real curation
bar to AI specifically: 8 categories (Foundations, The Model, Training,
Inference, Retrieval, Agents, Evaluation, Beyond Text), 40 build targets
in difficulty order, 39 verified from-scratch guides at launch.

Every linked guide is web-verified and tagged with concrete evidence of
why it qualifies as "from scratch" (not a library tutorial in disguise).
14 targets ship as marked gaps — the honest answer to "what does the AI
stack lack a good from-scratch guide for in 2026." Four of those gaps
are filled with original starter guides written for this repo:

  • Reward model from scratch
  • Agent memory from scratch
  • Multi-agent orchestration from scratch
  • Calibration / hallucination check from scratch

CI link-checks the whole index weekly. Curation log is in
PLANNING/03_verification_log.md — every accepted and rejected guide is
documented with evidence.

License: CC-BY-4.0 (content) / MIT (code). PRs welcome — the PR template
demands a one-line from-scratch evidence per added guide. Open to taking
the 14 gaps off my hands.

→ https://github.com/bettyguo/build-your-own-ai
```

---

## X (Twitter) thread

**1/**
build-your-own-x is the #1 most-starred repo on GitHub because reimplementing things from scratch is how you actually understand them.

But the AI section is thin.

I built `build-your-own-ai`: the same format, focused on the AI stack.
🔗 github.com/bettyguo/build-your-own-ai

**2/**
8 categories, 40 build targets, in difficulty order:

Foundations → The Model → Training → Inference → Retrieval → Agents → Evaluation → Beyond Text

Every entry is a from-scratch guide, never a library wrapper. 39 verified guides at launch.

**3/**
The curation bar is the product. Every linked guide has:
- a URL, an author
- one-line **evidence** of why it qualifies as from-scratch
- a verification date

5 candidate guides were rejected during verification — those reasons are logged in `PLANNING/03_verification_log.md`. Receipts.

**4/**
14 targets ship as marked **gaps**. No good public from-scratch guide exists for them today (yet).

For 4 of those — the highest-leverage — I wrote original starter guides:

• Reward model
• Agent memory
• Multi-agent orchestration
• Calibration / hallucination check

**5/**
Three sibling repos, each owning its own noun:
- `ai-engineer-roadmap` — the path
- `harness-engineer-roadmap` — the harness
- `llm-interview-prep` — the test
- **`build-your-own-ai`** — the place you go to *build the thing*

**6/**
The 10 open gaps are intentional: I want the community to fill them.
PR template demands the from-scratch evidence. Issue template exists
specifically to report mislabeled guides.

If you've written a good from-scratch guide for one of those gaps — send a PR.

🔗 github.com/bettyguo/build-your-own-ai

---

## Reddit — r/MachineLearning

**Title:** [P] build-your-own-ai — a curated index of build-it-from-scratch guides for the modern AI stack

**Body:**
> Hi r/MachineLearning,
>
> I put together `build-your-own-ai`, modeled directly on
> `codecrafters-io/build-your-own-x` but focused on the AI stack and with
> a real curation bar. Every linked guide is verified live, confirmed to
> actually teach by reimplementation (not "use library X"), and tagged
> with concrete evidence of why it qualifies.
>
> 8 categories, 40 build targets, 39 verified guides at launch. 14 targets
> ship as marked gaps; 4 of those have original starter guides I wrote
> myself (reward model, agent memory, multi-agent orchestration,
> calibration/hallucination check) — the rest I'd love community PRs for.
>
> Honest stuff:
> - Verification log lists every guide I considered AND every one I
>   rejected, with reasons (`PLANNING/03_verification_log.md`).
> - Scheduled weekly CI link-check.
> - PR template specifically calls out the from-scratch evidence
>   requirement.
>
> 🔗 https://github.com/bettyguo/build-your-own-ai
>
> Feedback / gap fills / "you missed an obvious guide" reports all welcome.

## Reddit — r/learnmachinelearning

**Title:** I made a curated index of "build it from scratch" guides for the modern AI stack — would love feedback

**Body:**
> Background: I'm a CS PhD at HKU and I noticed that the best way I ever
> learned an ML concept was to reimplement it from scratch. There are
> great individual from-scratch guides scattered around (Karpathy's
> nanoGPT, Raschka's KV cache article, Anthropic's Building Effective
> Agents, the Annotated Transformer, etc.) but no canonical index that
> pulls them together with a real curation bar.
>
> So I built one, modeled on `build-your-own-x`. 8 categories, 40 build
> targets in difficulty order, 39 verified guides, and 4 original starter
> guides I wrote for gap targets.
>
> If you're learning AI by building, this should save you a lot of "is
> this tutorial any good?" time.
>
> https://github.com/bettyguo/build-your-own-ai

## Reddit — r/LocalLLaMA

**Title:** Curated index of build-it-from-scratch guides for the AI stack — KV cache, inference engines, RAG, agents

**Body:**
> Practical-leaning: a curated index of from-scratch guides for the parts
> of the AI stack r/LocalLLaMA actually cares about — KV cache,
> minimal inference engines (karpathy/llama2.c), RAG without frameworks,
> agents without LangChain, quantization (still an open gap if anyone has
> a good guide).
>
> https://github.com/bettyguo/build-your-own-ai

---

## Newsletter outreach paragraph

> Hi <name>,
>
> I'd love your eyes on `build-your-own-ai` — a curated index of
> from-scratch guides for the AI stack, modeled on `build-your-own-x`.
> 40 build targets, 39 verified guides, and 4 original starter guides for
> high-leverage gaps. The curation bar — every guide tagged with evidence
> of *why* it qualifies as from-scratch — is the differentiator.
>
> If it fits your audience, here's the URL: github.com/bettyguo/build-your-own-ai
>
> Happy to write a short guest post or supply specific guide pulls for
> your readers (e.g. "the 5 best from-scratch agent loop guides").
>
> — Betty (Dongxin Guo), final-year PhD, HKU

---

## Coordination notes

- Launch best mid-week (Tue/Wed) at 10am ET — peak HN window.
- Don't post all four (HN + X + Reddit ×3) within the same hour; stagger
  by 30–60 min so signals don't compete.
- After 24 hours, follow up to commenters with substantive replies; the
  HN post will get curation-bar challenges — answer them by pointing at
  the verification log.
