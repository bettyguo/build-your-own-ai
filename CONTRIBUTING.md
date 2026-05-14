# Contributing to `build-your-own-ai`

Thanks for considering a contribution. This repo lives or dies by its
**curation bar** — one mislabeled "from scratch" guide erodes trust in the
whole index. Please read this short page before opening a PR.

## The rule

> **A guide qualifies only if it teaches by reimplementation, not by
> configuring a library.**

Concretely, a guide is *in* if:
- It writes the data structures and algorithms by hand (numpy / torch
  primitives are fine; black-box `model = AutoModel.from_pretrained(...)`
  for the thing being taught is not).
- A reader walks away knowing *how* the thing works internally.

A guide is *out* if its primary teaching method is "install package X and
call its functions." Even if package X is excellent. Those resources may
belong in [`ai-engineer-roadmap`](https://github.com/bettyguo/ai-engineer-roadmap)
or elsewhere — just not here.

## Local setup

```
git clone https://github.com/bettyguo/build-your-own-ai.git
cd build-your-own-ai
python -m venv .venv
.venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r tools/requirements.txt
```

## Adding a new entry

1. Open the right YAML file in [`entries/`](entries/). They are ordered by
   category and by difficulty within each category.
2. Add your entry following the schema (see existing entries for examples).
   **Required fields** for every guide:
   - `title`, `url`, `author`
   - `kind` (`code` | `written` | `video` | `book` | `course`)
   - `language` (`Python`, `Mixed`, etc.)
   - `cost` (`free` | `paid`)
   - `from_scratch_evidence` — *one sentence pointing to where in the guide
     the from-scratch property is visible.* Example:
     > "Implements multi-head attention from `torch.matmul` primitives in
     > section 3; no `transformers.MultiheadAttention` import anywhere."
   - `verified_on` — ISO date, today's date.
   - `verifier` — your GitHub handle.
3. Regenerate the README:
   ```
   python tools/validate_entries.py
   python tools/build_readme.py
   ```
4. Commit the regenerated `README.md` along with your YAML changes.
5. Open a PR — CI will re-run validation, drift-check the README, and check
   that your new URL is live.

## Adding a new build target

If a build target you care about isn't listed at all, please open a
[new-build-target](https://github.com/bettyguo/build-your-own-ai/issues/new?template=new-build-target.md)
issue *before* the PR. We want to keep the taxonomy coherent, and new
targets need a quick discussion on where they slot in.

## Reporting a not-from-scratch guide

The fastest way to keep the curation bar high. Open a
[not-from-scratch report](https://github.com/bettyguo/build-your-own-ai/issues/new?template=not-from-scratch.md)
with a one-line case for why the guide is mislabeled. Confirmed reports are
acted on within the next audit cycle.

## Style

- One sentence in `what_you_build` and one in `understanding`. The index is
  scannable — long entries hurt the reader.
- No emoji-heavy descriptions, no marketing language. Plain English. The
  thing being built carries the appeal.
- One language tag per guide (`Python`, `Rust`, `Mixed`, etc.). Use `Mixed`
  when the guide spans multiple languages.

## Maintenance promise

We re-verify every link weekly via CI and run a full audit quarterly. If
your PR enters the index, your `verified_on` date is the start of its
lifecycle; the maintainers re-stamp it on each audit.
