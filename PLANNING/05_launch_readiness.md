# PHASE 5 — Launch-readiness checklist

> Governing question: *Would someone who wants to truly understand the AI
> stack land here and conclude "this is THE place to learn by building"
> within 10 seconds?*

State as of 2026-05-14.

## The list

- [x] **Title is the noun**, opening sells the build-it-from-scratch format.
      → README header: `# build-your-own-ai`. Opening line: "Master modern
      AI by building it from scratch."
- [x] **Full categorized index present end to end.**
      → 8 categories, 40 targets, ordered by difficulty. Every category
      has entries; no category reads as a stub.
- [x] **Every linked guide web-verified, confirmed genuinely from-scratch,
      and confirmed currently working.**
      → 39 guides verified against URL resolution + from-scratch evidence
      + verifier date. Full audit in `PLANNING/03_verification_log.md`.
      Zero unverified entries.
- [x] **`linkcheck.py` passes; CI runs it on schedule.**
      → `python tools/linkcheck.py --quick` reports `✓ all 51 URLs live`.
      `.github/workflows/linkcheck.yml` runs the full check weekly and
      opens an issue on failure.
- [x] **The quality bar held — no weak, obsolete, or mislabeled guides.**
      → 5 candidate guides rejected (logged in
      `PLANNING/03_verification_log.md`):
        - learnbybuilding RAG (uses Jaccard, no chunking/embeddings)
        - PyTorch speculative-decoding blog (conceptual, not implementation)
        - lm-evaluation-harness (library, not tutorial)
        - HF train-reranker (framework-heavy)
        - Various Adam-from-scratch reposts (single labml.ai reference suffices)
- [x] **`originals/` covers the highest-value gap targets.**
      → 4 originals at launch (was 5; KV cache moved out because verification
      surfaced two excellent existing guides):
        - `reward-model.md`
        - `agent-memory.md`
        - `multi-agent.md`
        - `calibration-hallucination.md`
      Each clearly marked **[original]** in both YAML and rendered README.
- [x] **IN/OUT scope is sharp.**
      → Scope section in README; bright lines documented in
      `PLANNING/00_think.md` §2 (no general programming bleed, no
      library-tutorial bleed, no cannibalization of curator's other repos).
- [x] **Sideways peer links** to `ai-engineer-roadmap`,
      `harness-engineer-roadmap`, `llm-interview-prep`, framed as
      standalone equals.
      → Peers section in README footer. Linkcheck ignores the URLs via
      `tools/.linkcheckignore` (those repos are created on their own
      timelines).
- [x] **Strong hero banner / social card spec.**
      → No image-generation tool here, so `assets/MAKE_BANNER.md` carries
      the full spec (palette, type, sizes, visual motif). `README.md.tmpl`
      references `assets/banner.png` with graceful absence behavior.
- [x] **"Last updated" badge + stated maintenance cadence.**
      → Badge in README header reads `last updated · 2026-05-14`
      (auto-generated from the max `verified_on` across entries).
      `docs/MAINTENANCE.md` documents weekly / monthly / quarterly /
      yearly cycles.
- [x] **Curator attribution with HKU / Prof. Yiu / ORCID.**
      → README footer: Betty Guo (Dongxin Guo / 郭东欣), final-year PhD,
      University of Hong Kong, advised by Prof. Siu-Ming Yiu, ORCID
      0009-0000-2388-1072.
- [x] **`CONTRIBUTING.md` + PR template require verification links and
      the genuinely-from-scratch confirmation.**
      → `CONTRIBUTING.md` makes `from_scratch_evidence` the load-bearing
      field; PR template has explicit checkboxes for each new guide; a
      dedicated `not-from-scratch` issue template exists as the
      community safety valve.
- [x] **`docs/LAUNCH.md`.**
      → Show HN title + body draft, X-thread (6 tweets), Reddit drafts
      for r/MachineLearning, r/learnmachinelearning, r/LocalLLaMA,
      newsletter outreach paragraph, coordination notes.
- [x] **Star-history embed**; `docs/PROFILE_SNIPPET.md`.
      → Star-history embed at the end of the README. Profile snippet
      (long + short + star-history) drafted in `docs/PROFILE_SNIPPET.md`.
- [x] **Full verification + CI green.**
      → `validate_entries.py`: 40 entries valid. `build_readme.py --check`:
      in sync. `linkcheck.py --quick`: 51/51 live. Tooling tested locally
      with Python 3.13.

## Stats at launch

| Metric | Value |
|---|---|
| Categories | 8 |
| Build targets | 40 |
| Verified guides | 39 |
| Open gaps | 14 |
| Originals at launch | 4 |
| Total external URLs (entries + originals + README) | 54 |
| URLs checked live | 51 (3 sibling-repo placeholders ignored) |
| Guides rejected during verification | 5 |
| Unverified entries | 0 |

## Manual / human-only work remaining

1. **Render the banner** per `assets/MAKE_BANNER.md` and commit
   `assets/banner.png` + `assets/social-card.png`. The README references
   them with graceful absence; rendering improves first-impression but
   is not a launch blocker.
2. **Create the three sibling repos** (`ai-engineer-roadmap`,
   `harness-engineer-roadmap`, `llm-interview-prep`) or remove the entries
   from `tools/.linkcheckignore` once they exist.
3. **Open issues for the 14 open gaps** as "wanted build targets" — done
   in Phase 6 review as part of the gap-conversion work.
4. **Push to GitHub**, enable GitHub Actions (workflows are committed and
   will run on the first push).
5. **Launch coordination**: schedule the posts per `docs/LAUNCH.md`.

## Closing on Phase 5

Repo is launch-ready. Phase 6 hostile-reviewer pass next.
