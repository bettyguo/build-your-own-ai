# Maintenance

## Cadence

| Cycle | What |
|---|---|
| Weekly (automated) | `linkcheck.py --full` via the `linkcheck` GitHub Action; failures open / update an issue. |
| Monthly | Curator reviews open issues with the `broken-link` / `curation` labels and merges or closes them. |
| Quarterly | Full audit: re-stamp `verified_on` dates for every entry, re-confirm the from-scratch evidence against the current state of each guide, prune any guide that's drifted into library-tutorial territory, sweep for new build targets. |
| Yearly | Re-evaluate the taxonomy: have any categories become irrelevant? Is a new category needed (e.g., new modality, new paradigm)? |

## The audit procedure

For each entry in `entries/*.yaml`:

1. Open the guide URL. Confirm it loads, the title and author still match.
2. Skim the guide. Confirm the `from_scratch_evidence` statement is still
   accurate (the guide hasn't been rewritten to use a library).
3. Bump `verified_on` to today's date.
4. If the guide has rotted, decide:
   - Replace with a still-live equivalent → update the entry.
   - No equivalent exists → mark the entry `gap: true` and consider an
     `originals/` write-up.

Audit results live in `PLANNING/03_verification_log.md`. Append, don't
overwrite — the running log is a credibility asset.

## When CI complains

- **`validate_entries.py` fails**: schema violation, dedup collision, or
  missing `from_scratch_evidence`. The error message points to the file
  and entry. Fix the YAML.
- **`build_readme.py --check` fails**: someone edited `README.md` by hand
  or forgot to regenerate after editing YAML. Run `python tools/build_readme.py`
  and commit the diff.
- **`linkcheck.py` fails**: a URL returned a hard 4xx/5xx after retries.
  Either fix the URL or remove the entry. If the failure is upstream rate
  limiting that recovers later, the scheduled job will self-resolve next
  week.

## Quarterly currency check

Run on the 1st of every quarter:

```
python tools/validate_entries.py --stale-days 90
```

This warns (does not fail) for any guide whose `verified_on` is more
than 90 days old. Each warning is a re-verification trigger: open the
URL, confirm the from-scratch evidence still holds, bump `verified_on`
in the YAML. The Phase-10 build of `validate_entries.py` introduced
this flag and the orphan-originals guard; both are documented in
`PLANNING/03_verification_log.md`.
