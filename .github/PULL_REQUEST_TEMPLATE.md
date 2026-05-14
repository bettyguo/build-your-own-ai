<!--
Thanks for contributing. This repo's value is its curation bar — please
take 60 seconds to confirm the boxes below. PRs with empty checkboxes will
be asked for the info; PRs that add a guide that turns out to be a library
tutorial will be reverted with a polite note.
-->

## What this PR does

<!-- One or two sentences. -->

## Type of change

- [ ] Adds a new build-target entry
- [ ] Adds a new guide to an existing entry
- [ ] Removes / corrects a broken or mislabeled entry
- [ ] Adds / updates an `originals/` guide
- [ ] Tooling / CI / docs only

## For added guides — the curation bar

For each new guide URL, I confirm:

- [ ] The guide teaches by **reimplementation**, not by configuring a library.
- [ ] I can point to a concrete spot in the guide that proves this — and I
      have written that sentence in `from_scratch_evidence`.
- [ ] The guide is currently working — code runs / page loads / video plays.
- [ ] I have set `verified_on` to today's date and `verifier` to my handle.

## Validation

- [ ] `python tools/validate_entries.py` passes locally.
- [ ] `python tools/build_readme.py` ran; the regenerated `README.md` is
      committed along with the YAML changes.

## Anything else
