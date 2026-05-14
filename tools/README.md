# `tools/`

Three small Python scripts. Source of truth lives in `entries/*.yaml`; the
`README.md` at repo root is **generated**. Edit YAML, not the README.

```
pip install -r tools/requirements.txt
python tools/validate_entries.py        # schema + from-scratch evidence + dedup
python tools/build_readme.py            # regenerate README.md from YAML
python tools/linkcheck.py --quick       # check every URL is live (~30 s)
python tools/linkcheck.py --full        # exhaustive check (used in scheduled CI)
```

CI runs `validate_entries.py` + a `build_readme.py` drift check + `linkcheck.py --quick`
on every PR. A scheduled workflow runs `linkcheck.py --full` weekly and opens an
issue if any URL has rotted.
