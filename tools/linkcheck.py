#!/usr/bin/env python3
"""Verify every URL in entries/, originals/, and README.md is live.

Two modes:
  --quick  short timeouts, parallel HEAD with GET fallback (CI-on-PR)
  --full   longer timeouts, retry on 429, written report (scheduled weekly)

Writes a Markdown report to tools/linkcheck-report.md. Exits non-zero if
any URL is hard-broken (4xx/5xx that does not recover on backoff).
"""
from __future__ import annotations

import asyncio
import pathlib
import re
import sys
from collections import defaultdict
from typing import Iterable

import click
import httpx
import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]
ENTRIES_DIR = ROOT / "entries"
ORIGINALS_DIR = ROOT / "originals"
README = ROOT / "README.md"
REPORT = ROOT / "tools" / "linkcheck-report.md"
IGNORE_FILE = ROOT / "tools" / ".linkcheckignore"

URL_RE = re.compile(r"https?://[^\s)>\]\"']+")
USER_AGENT = "build-your-own-ai-linkcheck/1.0 (+https://github.com/bettyguo/build-your-own-ai)"


def load_ignore_patterns() -> list[str]:
    if not IGNORE_FILE.exists():
        return []
    out: list[str] = []
    for raw in IGNORE_FILE.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if line and not line.startswith("#"):
            out.append(line)
    return out


def is_ignored(url: str, patterns: list[str]) -> bool:
    return any(p in url for p in patterns)


def urls_from_yaml(path: pathlib.Path) -> Iterable[tuple[str, str]]:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or []
    except yaml.YAMLError:
        return
    if not isinstance(data, list):
        return
    for e in data:
        if not isinstance(e, dict):
            continue
        eid = e.get("id", "?")
        for g in e.get("guides") or []:
            if isinstance(g, dict) and g.get("url"):
                yield g["url"], f"{path.name}::{eid}"
        for url in e.get("see_also") or []:
            if isinstance(url, str):
                yield url, f"{path.name}::{eid} (see_also)"


def urls_from_markdown(path: pathlib.Path) -> Iterable[tuple[str, str]]:
    if not path.exists():
        return
    text = path.read_text(encoding="utf-8", errors="replace")
    for m in URL_RE.finditer(text):
        url = m.group(0).rstrip(".,)")
        yield url, path.name


def collect_urls() -> dict[str, list[str]]:
    urls: dict[str, list[str]] = defaultdict(list)
    for f in sorted(ENTRIES_DIR.glob("*.yaml")):
        for url, where in urls_from_yaml(f):
            urls[url].append(where)
    for f in sorted(ORIGINALS_DIR.glob("*.md")):
        for url, where in urls_from_markdown(f):
            urls[url].append(where)
    for url, where in urls_from_markdown(README):
        urls[url].append(where)
    return urls


async def check_one(client: httpx.AsyncClient, url: str,
                    timeout: float, retries: int) -> tuple[int | None, str]:
    last_status: int | None = None
    last_msg = "no response"
    for attempt in range(retries + 1):
        try:
            r = await client.head(url, timeout=timeout, follow_redirects=True)
            if r.status_code == 405 or r.status_code >= 400:
                r = await client.get(url, timeout=timeout, follow_redirects=True)
            last_status = r.status_code
            if r.status_code < 400:
                return r.status_code, "ok"
            last_msg = f"HTTP {r.status_code}"
            if r.status_code in (429, 503) and attempt < retries:
                await asyncio.sleep(2 ** attempt)
                continue
            return r.status_code, last_msg
        except httpx.HTTPError as e:
            last_msg = type(e).__name__
            if attempt < retries:
                await asyncio.sleep(2 ** attempt)
                continue
            return last_status, last_msg
    return last_status, last_msg


async def run(urls: dict[str, list[str]], timeout: float, retries: int,
              concurrency: int) -> list[tuple[str, int | None, str, list[str]]]:
    sem = asyncio.Semaphore(concurrency)
    results: list[tuple[str, int | None, str, list[str]]] = []

    async with httpx.AsyncClient(headers={"user-agent": USER_AGENT}) as client:
        async def worker(url: str, where: list[str]) -> None:
            async with sem:
                status, msg = await check_one(client, url, timeout, retries)
                results.append((url, status, msg, where))

        await asyncio.gather(*(worker(u, w) for u, w in urls.items()))
    return results


def write_report(results: list[tuple[str, int | None, str, list[str]]]) -> None:
    ok = [r for r in results if r[1] is not None and r[1] < 400]
    bad = [r for r in results if not (r[1] is not None and r[1] < 400)]
    lines = ["# Link-check report",
             "",
             f"- Total URLs: **{len(results)}**",
             f"- OK: **{len(ok)}**",
             f"- Broken / unreachable: **{len(bad)}**",
             ""]
    if bad:
        lines.append("## Failures")
        lines.append("")
        for url, status, msg, where in sorted(bad, key=lambda r: r[0]):
            lines.append(f"- `{status}` {msg} — {url}")
            for w in where:
                lines.append(f"  - referenced from: {w}")
        lines.append("")
    REPORT.write_text("\n".join(lines), encoding="utf-8")


@click.command()
@click.option("--quick", "mode", flag_value="quick", default=True)
@click.option("--full", "mode", flag_value="full")
@click.option("--concurrency", default=10, show_default=True)
def main(mode: str, concurrency: int) -> None:
    timeout = 10.0 if mode == "quick" else 60.0
    retries = 1 if mode == "quick" else 3
    urls = collect_urls()
    ignore_patterns = load_ignore_patterns()
    if ignore_patterns:
        before = len(urls)
        urls = {u: w for u, w in urls.items() if not is_ignored(u, ignore_patterns)}
        skipped = before - len(urls)
        if skipped:
            click.echo(f"skipping {skipped} URL(s) per tools/.linkcheckignore")
    if not urls:
        click.echo("no URLs found")
        REPORT.write_text("# Link-check report\n\n(no URLs)\n", encoding="utf-8")
        sys.exit(0)

    click.echo(f"checking {len(urls)} URLs ({mode} mode)...")
    results = asyncio.run(run(urls, timeout, retries, concurrency))
    write_report(results)

    bad = [r for r in results if not (r[1] is not None and r[1] < 400)]
    if bad:
        click.echo(click.style(
            f"✗ {len(bad)} broken URL(s) — see {REPORT.relative_to(ROOT)}",
            fg="red"))
        for url, status, msg, _where in bad[:20]:
            click.echo(f"  [{status}] {msg} — {url}")
        sys.exit(1)
    click.echo(click.style(f"✓ all {len(results)} URLs live", fg="green"))
    sys.exit(0)


if __name__ == "__main__":
    main()
