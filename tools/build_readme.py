#!/usr/bin/env python3
"""Regenerate README.md from entries/*.yaml + README.md.tmpl.

The README is *generated*, never hand-edited. CI runs this and `git diff`s
against the committed README — drift fails the build.
"""
from __future__ import annotations

import datetime as dt
import pathlib
import sys
from typing import Any

import click
import yaml
from jinja2 import Environment, FileSystemLoader, StrictUndefined

ROOT = pathlib.Path(__file__).resolve().parents[1]
ENTRIES_DIR = ROOT / "entries"
ORIGINALS_DIR = ROOT / "originals"
README = ROOT / "README.md"
TMPL = ROOT / "README.md.tmpl"

CATEGORIES = [
    ("foundations",   "1-foundations.yaml", "Foundations",
     "The machinery before the model."),
    ("model",         "2-model.yaml", "The Model",
     "Attention to a full small LM."),
    ("training",      "3-training.yaml", "Training",
     "How models learn."),
    ("inference",     "4-inference.yaml", "Inference",
     "Making a trained model useful."),
    ("retrieval",     "5-retrieval.yaml", "Retrieval",
     "External memory for LMs."),
    ("agents",        "6-agents.yaml", "Agents",
     "LMs that take actions."),
    ("evaluation",    "7-evaluation.yaml", "Evaluation",
     "Knowing if it actually works."),
    ("beyond-text",   "8-beyond-text.yaml", "Beyond Text",
     "Vision, audio, multimodal."),
]


def slug(s: str) -> str:
    return (s.lower()
             .replace(" ", "-")
             .replace("/", "-")
             .replace("(", "")
             .replace(")", "")
             .replace(",", "")
             .replace(".", ""))


def stars(n: int) -> str:
    return "★" * n + "☆" * (3 - n)


def difficulty_label(n: int) -> str:
    return {1: "easy", 2: "afternoon", 3: "weekend"}.get(n, "?")


def load_category(fname: str) -> list[dict[str, Any]]:
    path = ENTRIES_DIR / fname
    if not path.exists():
        return []
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or []
    if not isinstance(data, list):
        return []
    return sorted(data, key=lambda e: e.get("order", 0))


def render_entry(e: dict[str, Any]) -> str:
    title = e["title"]
    diff = stars(e["difficulty"])
    lines = [f"#### {title} <sub>{diff} · {difficulty_label(e['difficulty'])}</sub>",
             "",
             f"**What you build:** {e['what_you_build']}",
             "",
             f"**What you'll understand after:** {e['understanding']}",
             ""]
    if e.get("gap"):
        if e.get("original_planned"):
            lines.append(f"> _Gap target — original starter guide planned in "
                         f"[`originals/{e['id']}.md`](originals/{e['id']}.md)._")
        else:
            lines.append("> _Open gap — no good from-scratch guide verified yet. "
                         "Contributions welcome (see `CONTRIBUTING.md`)._")
        lines.append("")
    else:
        for g in e.get("guides") or []:
            tag_kind = g["kind"]
            tag_cost = g["cost"]
            extra = ""
            if g["kind"] == "original":
                extra = " · **[original]**"
            lines.append(
                f"- [**{g['language']}**: _{g['title']}_]({g['url']}) — "
                f"{g['author']} · {tag_kind} · {tag_cost}{extra}"
            )
        lines.append("")
    return "\n".join(lines)


def render_category(slug_: str, fname: str, name: str, blurb: str) -> str:
    entries = load_category(fname)
    out = [f"### {name}", f"_{blurb}_", ""]
    if not entries:
        out.append("> _(no entries yet)_")
        out.append("")
        return "\n".join(out)
    for e in entries:
        out.append(render_entry(e))
    return "\n".join(out)


def last_updated(all_entries: list[dict[str, Any]]) -> str:
    dates = []
    for e in all_entries:
        for g in e.get("guides") or []:
            v = g.get("verified_on") if isinstance(g, dict) else None
            if isinstance(v, dt.date):
                dates.append(v)
    return max(dates).isoformat() if dates else "n/a"


def count_originals() -> int:
    if not ORIGINALS_DIR.exists():
        return 0
    return len([p for p in ORIGINALS_DIR.glob("*.md") if p.name != "README.md"])


def gather_stats(all_entries: list[dict[str, Any]]) -> dict[str, Any]:
    by_cat: dict[str, int] = {c[0]: 0 for c in CATEGORIES}
    gaps = 0
    guides = 0
    for e in all_entries:
        cat = e.get("category")
        if cat in by_cat:
            by_cat[cat] += 1
        if e.get("gap"):
            gaps += 1
        guides += len(e.get("guides") or [])
    return {
        "by_cat": by_cat,
        "gaps": gaps,
        "guides": guides,
        "targets": len(all_entries),
        "originals": count_originals(),
    }


@click.command()
@click.option("--check", is_flag=True,
              help="exit 1 if README.md on disk differs from regenerated output")
def main(check: bool) -> None:
    env = Environment(loader=FileSystemLoader(str(ROOT)),
                      undefined=StrictUndefined,
                      keep_trailing_newline=True)
    tmpl = env.get_template("README.md.tmpl")

    all_entries: list[dict[str, Any]] = []
    sections: list[str] = []
    toc: list[str] = []
    for slug_, fname, name, blurb in CATEGORIES:
        entries = load_category(fname)
        all_entries.extend(entries)
        sections.append(render_category(slug_, fname, name, blurb))
        toc.append(f"1. [{name}](#{slug(name)})")

    stats = gather_stats(all_entries)
    rendered = tmpl.render(
        sections="\n".join(sections),
        toc="\n".join(toc),
        last_updated=last_updated(all_entries),
        target_count=stats["targets"],
        guide_count=stats["guides"],
        gap_count=stats["gaps"],
        original_count=stats["originals"],
    )

    if check:
        existing = README.read_text(encoding="utf-8") if README.exists() else ""
        if existing != rendered:
            click.echo(click.style(
                "✗ README.md is out of sync with entries/ — run "
                "`python tools/build_readme.py` and commit the diff.",
                fg="red"))
            sys.exit(1)
        click.echo(click.style("✓ README.md is in sync", fg="green"))
        sys.exit(0)

    README.write_text(rendered, encoding="utf-8")
    click.echo(click.style(
        f"✓ wrote README.md — {stats['targets']} targets, {stats['guides']} "
        f"guides, {stats['gaps']} gaps, {stats['originals']} originals",
        fg="green"))


if __name__ == "__main__":
    main()
