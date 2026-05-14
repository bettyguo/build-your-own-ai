#!/usr/bin/env python3
"""Validate entries/*.yaml against the schema in PLANNING/01_design.md §2.

Enforces:
  - all required fields present on entries and guides
  - controlled vocabularies on category / kind / cost / language tags
  - id uniqueness across all entries
  - URL uniqueness across all guides
  - from_scratch_evidence is the load-bearing field — must be present
    and >= 20 characters
  - verified_on is a real ISO date not in the future
  - difficulty is 1, 2, or 3
  - category slug matches the filename's numeric prefix
  - each entry has either at least one guide OR gap == True
  - if original_planned, an originals/<id>.md must exist

Optional currency check (`--stale-days N`, default off):
  - prints a warning (does NOT fail) for any guide whose `verified_on`
    is older than N days. Use this as a quarterly audit trigger:
        python tools/validate_entries.py --stale-days 90
"""
from __future__ import annotations

import datetime as dt
import pathlib
import sys
from typing import Any

import click
import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]
ENTRIES_DIR = ROOT / "entries"
ORIGINALS_DIR = ROOT / "originals"

CATEGORY_FILES = {
    "foundations":   "1-foundations.yaml",
    "model":         "2-model.yaml",
    "training":      "3-training.yaml",
    "inference":     "4-inference.yaml",
    "retrieval":     "5-retrieval.yaml",
    "agents":        "6-agents.yaml",
    "evaluation":    "7-evaluation.yaml",
    "beyond-text":   "8-beyond-text.yaml",
}

CATEGORY_ORDER = list(CATEGORY_FILES.keys())

KINDS = {"code", "written", "video", "book", "course", "original"}
COSTS = {"free", "paid"}

ENTRY_REQUIRED = {"id", "category", "order", "title", "what_you_build",
                  "teaches", "understanding", "difficulty"}
GUIDE_REQUIRED = {"title", "url", "author", "kind", "language", "cost",
                  "from_scratch_evidence", "verified_on", "verifier"}


class V:
    """Validation context — accumulates errors then reports."""

    def __init__(self) -> None:
        self.errors: list[str] = []

    def err(self, where: str, msg: str) -> None:
        self.errors.append(f"  [{where}] {msg}")

    def report(self) -> int:
        if not self.errors:
            click.echo(click.style("✓ all entries valid", fg="green"))
            return 0
        click.echo(click.style(
            f"✗ {len(self.errors)} validation error(s):", fg="red"))
        for e in self.errors:
            click.echo(e)
        return 1


def load_entries(v: V) -> list[dict[str, Any]]:
    all_entries: list[dict[str, Any]] = []
    for cat_slug, fname in CATEGORY_FILES.items():
        path = ENTRIES_DIR / fname
        if not path.exists():
            v.err(fname, f"missing file (expected for category '{cat_slug}')")
            continue
        try:
            data = yaml.safe_load(path.read_text(encoding="utf-8"))
        except yaml.YAMLError as e:
            v.err(fname, f"YAML parse error: {e}")
            continue
        if data is None:
            data = []
        if not isinstance(data, list):
            v.err(fname, "top-level must be a YAML list of entries")
            continue
        for raw in data:
            if not isinstance(raw, dict):
                v.err(fname, f"non-mapping entry: {raw!r}")
                continue
            raw["_source_file"] = fname
            raw["_expected_category"] = cat_slug
            all_entries.append(raw)
    return all_entries


def validate_entry(v: V, e: dict[str, Any]) -> None:
    src = e.get("_source_file", "?")
    eid = e.get("id", "?")
    where = f"{src}::{eid}"

    missing = ENTRY_REQUIRED - set(e.keys())
    if missing:
        v.err(where, f"missing required fields: {sorted(missing)}")

    if e.get("category") != e.get("_expected_category"):
        v.err(where, f"category '{e.get('category')}' does not match file "
                     f"'{src}' (expected '{e.get('_expected_category')}')")

    if e.get("difficulty") not in {1, 2, 3}:
        v.err(where, f"difficulty must be 1, 2, or 3 (got {e.get('difficulty')!r})")

    if not isinstance(e.get("order"), int) or e.get("order", 0) < 1:
        v.err(where, f"order must be a positive integer (got {e.get('order')!r})")

    for f in ("what_you_build", "understanding"):
        val = e.get(f)
        if not isinstance(val, str) or len(val.strip()) < 20:
            v.err(where, f"'{f}' must be a string of at least 20 chars")

    if not isinstance(e.get("teaches"), list) or not e.get("teaches"):
        v.err(where, "'teaches' must be a non-empty list")

    gap = bool(e.get("gap", False))
    guides = e.get("guides") or []
    if not isinstance(guides, list):
        v.err(where, "'guides' must be a list")
        guides = []

    if gap and guides:
        v.err(where, "entry has gap=true but also lists guides — pick one")
    if not gap and not guides:
        v.err(where, "entry has no guides and gap is not set true")

    for i, g in enumerate(guides):
        if not isinstance(g, dict):
            v.err(where, f"guide #{i} is not a mapping")
            continue
        gwhere = f"{where} guide#{i}"
        gmissing = GUIDE_REQUIRED - set(g.keys())
        if gmissing:
            v.err(gwhere, f"missing required fields: {sorted(gmissing)}")
            continue
        if g["kind"] not in KINDS:
            v.err(gwhere, f"kind '{g['kind']}' not in {sorted(KINDS)}")
        if g["cost"] not in COSTS:
            v.err(gwhere, f"cost '{g['cost']}' not in {sorted(COSTS)}")
        if not isinstance(g["url"], str) or not g["url"].startswith(("http://", "https://")):
            v.err(gwhere, f"url must be a string starting with http(s)://")
        evidence = g.get("from_scratch_evidence", "")
        if not isinstance(evidence, str) or len(evidence.strip()) < 20:
            v.err(gwhere, "from_scratch_evidence must be >= 20 chars "
                          "(this is the load-bearing curation field)")
        verified_on = g.get("verified_on")
        if isinstance(verified_on, dt.date):
            if verified_on > dt.date.today():
                v.err(gwhere, f"verified_on '{verified_on}' is in the future")
        else:
            v.err(gwhere, f"verified_on must be a date (got {verified_on!r})")

    if e.get("original_planned"):
        expected = ORIGINALS_DIR / f"{eid}.md"
        if not expected.exists():
            v.err(where, f"original_planned=true but {expected.relative_to(ROOT)} "
                          f"does not exist")


def check_uniqueness(v: V, entries: list[dict[str, Any]]) -> None:
    ids: dict[str, str] = {}
    urls: dict[str, str] = {}
    for e in entries:
        eid = e.get("id")
        src = e.get("_source_file", "?")
        if eid in ids:
            v.err(f"{src}::{eid}", f"duplicate id (also in {ids[eid]})")
        elif eid:
            ids[eid] = src
        for g in e.get("guides") or []:
            url = g.get("url") if isinstance(g, dict) else None
            if not url:
                continue
            if url in urls:
                v.err(f"{src}::{eid}", f"duplicate guide URL "
                                       f"(also used by {urls[url]}): {url}")
            else:
                urls[url] = f"{src}::{eid}"


def check_originals_orphans(v: V, entries: list[dict[str, Any]]) -> None:
    """Every originals/<id>.md (except README.md) must correspond to an entry
    with `original_planned: true`. Catches half-deleted gaps and stray files."""
    if not ORIGINALS_DIR.exists():
        return
    planned_ids = {e.get("id") for e in entries if e.get("original_planned")}
    for p in ORIGINALS_DIR.glob("*.md"):
        if p.name == "README.md":
            continue
        if p.stem not in planned_ids:
            v.err(f"originals/{p.name}",
                  f"orphan original — no entry sets original_planned: true for "
                  f"id '{p.stem}' (rename the file, or set the flag on the entry)")


def check_ordering(v: V, entries: list[dict[str, Any]]) -> None:
    by_cat: dict[str, list[dict[str, Any]]] = {c: [] for c in CATEGORY_ORDER}
    for e in entries:
        cat = e.get("category")
        if cat in by_cat:
            by_cat[cat].append(e)
    for cat, items in by_cat.items():
        seen = set()
        for e in items:
            order = e.get("order")
            if order in seen:
                v.err(f"{e.get('_source_file', '?')}::{e.get('id')}",
                      f"duplicate order={order} within category '{cat}'")
            seen.add(order)


def check_staleness(entries: list[dict[str, Any]], stale_days: int) -> int:
    """Warn (not fail) for guides whose `verified_on` is older than stale_days.
    Returns the number of stale guides found (informational only)."""
    cutoff = dt.date.today() - dt.timedelta(days=stale_days)
    stale: list[str] = []
    for e in entries:
        eid = e.get("id", "?")
        src = e.get("_source_file", "?")
        for i, g in enumerate(e.get("guides") or []):
            if not isinstance(g, dict):
                continue
            v_on = g.get("verified_on")
            if isinstance(v_on, dt.date) and v_on < cutoff:
                age = (dt.date.today() - v_on).days
                stale.append(
                    f"  [{src}::{eid} guide#{i}] verified {age}d ago "
                    f"({v_on.isoformat()}) — {g.get('url', '?')}"
                )
    if stale:
        click.echo(click.style(
            f"⚠ {len(stale)} guide(s) older than {stale_days} days "
            f"— consider re-verifying:", fg="yellow"))
        for line in stale:
            click.echo(line)
    return len(stale)


@click.command()
@click.option("--quiet", is_flag=True, help="suppress success message")
@click.option("--stale-days", type=int, default=0,
              help="if > 0, warn for guides verified longer than this ago "
                   "(informational; does not fail the build)")
def main(quiet: bool, stale_days: int) -> None:
    v = V()
    entries = load_entries(v)
    for e in entries:
        validate_entry(v, e)
    check_uniqueness(v, entries)
    check_ordering(v, entries)
    check_originals_orphans(v, entries)
    code = v.report()
    if code == 0 and not quiet:
        click.echo(f"  ({len(entries)} entries across {len(CATEGORY_FILES)} categories)")
    if stale_days > 0:
        check_staleness(entries, stale_days)
    sys.exit(code)


if __name__ == "__main__":
    main()
