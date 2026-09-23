#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate paper wiki pages from Paperpile JSON + paper_ids.yaml via Gemini.

Usage:
  python3 -m venv MD/.venv-papers
  MD/.venv-papers/bin/pip install -r MD/requirements-papers.txt

  # 1) assign / refresh short ids (incremental; safe to re-run)
  MD/.venv-papers/bin/python MD/assign_paper_ids.py --json "Paperpile - References - ….json"

  # 2) generate missing MD pages (skips existing unless --force)
  MD/.venv-papers/bin/python MD/gen_paper_pages.py --json "Paperpile - References - ….json"

Requires GEMINI_API_KEY in repo-root .env
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections import defaultdict
from typing import Any

try:
    import yaml
except ImportError:
    sys.stderr.write("PyYAML is required. See MD/requirements-papers.txt\n")
    sys.exit(1)

try:
    from dotenv import load_dotenv
except ImportError:
    sys.stderr.write("python-dotenv is required. See MD/requirements-papers.txt\n")
    sys.exit(1)

try:
    from google import genai
except ImportError:
    sys.stderr.write("google-genai is required. See MD/requirements-papers.txt\n")
    sys.exit(1)

# Reuse helpers from assign_paper_ids
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from assign_paper_ids import (  # noqa: E402
    DEFAULT_YAML,
    MD_DIR,
    ROOT,
    find_latest_paperpile,
    load_json,
    load_yaml,
    normalize_doi,
    paper_year,
)

DEFAULT_MODEL = "gemini-3.6-flash"
PAPERS_MD = os.path.join(MD_DIR, "papers.md")


def format_author_list(authors: list[dict[str, Any]]) -> str:
    """Nature-ish for Latin; 「姓 名」 for Japanese."""
    if not authors:
        return ""
    parts = []
    for a in authors:
        last = (a.get("last") or "").strip()
        initials = (a.get("initials") or "").strip()
        first = (a.get("first") or "").strip()
        # Japanese: last/first contain non-ASCII
        if last and ord(last[0]) > 127:
            if first:
                parts.append(f"{last} {first}")
            else:
                parts.append(last)
            continue
        if not initials and first:
            if first and ord(first[0]) < 128:
                initials = "".join(
                    p[0].upper() for p in first.replace("-", " ").split() if p
                )
            else:
                initials = first
        if initials and ord(initials[0]) < 128:
            init_fmt = ".".join(list(initials.replace(".", ""))) + "."
            parts.append(f"{last}, {init_fmt}")
        elif initials:
            parts.append(f"{last} {initials}")
        else:
            parts.append(last)
    if len(parts) == 1:
        return parts[0]
    if len(parts) == 2:
        return f"{parts[0]} & {parts[1]}"
    return ", ".join(parts[:-1]) + f" & {parts[-1]}"


def format_citation(p: dict[str, Any]) -> str:
    authors = format_author_list(p.get("author") or [])
    title = (p.get("title") or "").strip().rstrip(".")
    journal = (p.get("journal") or p.get("journalfull") or "").strip()
    year = paper_year(p) or ""
    doi = p.get("doi")
    vol = p.get("volume")
    pages = p.get("pages")
    bits = []
    if authors:
        bits.append(authors)
    if title:
        bits.append(title + ".")
    mid = journal
    if vol:
        mid = f"{journal} {vol}" if journal else str(vol)
        if pages:
            mid += f", {pages}"
    elif pages and journal:
        mid = f"{journal}, {pages}"
    if mid:
        bits.append(mid)
    if year:
        bits.append(f"({year})")
    cite = " ".join(bits)
    if doi:
        cite += f" [doi:{doi}]"
    return cite


def find_record(records: list[dict[str, Any]], entry: dict[str, Any]) -> dict[str, Any] | None:
    doi = entry.get("doi")
    pid = entry.get("paperpile_id")
    citekey = entry.get("citekey")
    # Build pseudo list of "entries" from records for match_entry style
    ndoi = normalize_doi(doi)
    if ndoi:
        for p in records:
            if normalize_doi(p.get("doi")) == ndoi:
                return p
    if pid:
        for p in records:
            if p.get("_id") == pid:
                return p
    if citekey:
        for p in records:
            if p.get("citekey") == citekey:
                return p
    return None


def related_ids(state: dict[str, Any], exclude: str) -> list[str]:
    return [e["id"] for e in state.get("papers") or [] if e.get("id") and e["id"] != exclude]


def build_prompt(short_id: str, record: dict[str, Any], related: list[str]) -> str:
    citation = format_citation(record)
    abstract = (record.get("abstract") or "").strip()
    title = record.get("title") or ""
    year = paper_year(record)
    related_s = ", ".join(related[:40]) if related else "(none)"
    abs_block = abstract if abstract else "(No abstract in the bibliographic record.)"
    return f"""あなたは物理化学の研究室のウェブ管理者です。次の論文について、既存サイトの記事体裁に合わせた Markdown 本文だけを出力してください。
前置き・後書き・コードフェンスは不要です。

# 体裁（必須）

1行目: 書誌情報（次の citation をほぼそのまま使う。必要なら軽微な整形のみ）
空行
高校生が読んでわかる日本語の解説（2〜4段落。研究内容の意義をかみ砕く。専門用語は初出で短く説明。可能なら related short ids への言及を括弧書きで、例: (MT2011)）
空行
## Abstract
空行
日本語の要旨（Abstract の内容を日本語で。末尾に「(Geminiによる概要の機械翻訳)」と付ける。英語 Abstract が無い場合は、タイトルと書誌から短い日本語要約を作り、末尾を「(要旨情報なし・Geminiによる要約)」とする）
空行
英語 Abstract 原文（ある場合のみ。無い場合はこのブロック自体を省略）
空行
タグ行: #research #papers #paper{{YEAR}} に加え、内容に合うタグを数個（例: #water #ice #clathratehydrate #GenIce）。タグは半角スペース区切り、行末にスペース不要。

# 入力

short_id: {short_id}
year: {year}
title: {title}
citation: {citation}
related_short_ids: {related_s}

English abstract:
{abs_block}
"""


def call_gemini(client: genai.Client, model: str, prompt: str) -> str:
    import time

    from google.genai import errors as genai_errors

    last_err: Exception | None = None
    for attempt in range(8):
        try:
            resp = client.models.generate_content(model=model, contents=prompt)
            text = getattr(resp, "text", None) or ""
            if not text and getattr(resp, "candidates", None):
                parts = []
                for c in resp.candidates:
                    content = getattr(c, "content", None)
                    if not content:
                        continue
                    for part in getattr(content, "parts", []) or []:
                        t = getattr(part, "text", None)
                        if t:
                            parts.append(t)
                text = "\n".join(parts)
            text = text.strip()
            if text.startswith("```"):
                text = re.sub(r"^```(?:markdown|md)?\n?", "", text)
                text = re.sub(r"\n?```$", "", text).strip()
            return text
        except (genai_errors.ServerError, genai_errors.ClientError) as e:
            last_err = e
            msg = str(e)
            m = re.search(r"[Pp]lease retry in ([0-9.]+)s", msg)
            if m:
                wait = float(m.group(1)) + 1.0
            elif "429" in msg or "RESOURCE_EXHAUSTED" in msg:
                wait = min(90, 5 * (attempt + 1))
            elif isinstance(e, genai_errors.ServerError):
                wait = min(60, 2 ** attempt)
            else:
                raise
            sys.stderr.write(
                f"API busy ({type(e).__name__}); retry in {wait:.0f}s "
                f"(attempt {attempt + 1}/8)\n"
            )
            time.sleep(wait)
    raise RuntimeError(f"Gemini failed after retries: {last_err}")

def ensure_tags(body: str, year: int | None) -> str:
    if re.search(r"(?m)^#research\b", body):
        return body
    y = year or ""
    return body.rstrip() + f"\n\n#research #papers #paper{y}\n"


def update_papers_md(state: dict[str, Any], papers_path: str = PAPERS_MD) -> None:
    """Ensure #paperYYYY sections list assigned short ids (newest years on top)."""
    if not os.path.exists(papers_path):
        content = "# papers\n\n#著作\n\n(少しずつ追加しています)\n\n#research #papers\n"
    else:
        with open(papers_path, encoding="utf-8") as f:
            content = f.read()

    by_year: dict[int, list[str]] = defaultdict(list)
    for e in state.get("papers") or []:
        y = e.get("year")
        sid = e.get("id")
        if y and sid:
            by_year[int(y)].append(sid)

    # For each year >= year_from, ensure section exists and contains ids
    year_from = int(state.get("year_from") or 2022)
    for year in sorted(by_year.keys(), reverse=True):
        if year < year_from:
            continue
        ids = by_year[year]
        header = f"#paper{year}"
        # Build bullet list (newest first within year = reverse assignment order is fine;
        # keep YAML order)
        bullets = "\n".join(f"* {i}" for i in ids)

        pattern = re.compile(
            rf"(?ms)^({re.escape(header)}\s*\n)(.*?)(?=^#paper\d|^#research\b|\Z)"
        )
        m = pattern.search(content)
        if m:
            # Merge: keep existing bullets not in ids, prepend missing from ids
            old_block = m.group(2)
            existing = re.findall(r"(?m)^\*\s+(\S+)", old_block)
            merged: list[str] = []
            seen: set[str] = set()
            for i in ids:
                if i not in seen:
                    merged.append(i)
                    seen.add(i)
            for i in existing:
                if i not in seen:
                    merged.append(i)
                    seen.add(i)
            new_block = "\n".join(f"* {i}" for i in merged) + "\n\n"
            content = content[: m.start(2)] + new_block + content[m.end(2) :]
        else:
            # Insert after "#著作..." block / before first #paper that is older, or after intro
            insert = f"\n{header}\n\n{bullets}\n\n"
            # Find first #paperN with N < year, or #paper with smaller, else before #research at end
            placed = False
            for m2 in re.finditer(r"(?m)^#paper(\d+)\s*$", content):
                y2 = int(m2.group(1))
                if y2 < year:
                    content = content[: m2.start()] + insert + content[m2.start() :]
                    placed = True
                    break
            if not placed:
                m3 = re.search(r"(?m)^#research\b", content)
                if m3:
                    content = content[: m3.start()] + insert + content[m3.start() :]
                else:
                    content = content.rstrip() + "\n" + insert

        # Ensure MD/paperYYYY.md stub exists
        stub = os.path.join(MD_DIR, f"paper{year}.md")
        if not os.path.exists(stub):
            with open(stub, "w", encoding="utf-8") as f:
                f.write(f"# paper{year}\n\n")

    with open(papers_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"updated {papers_path}")


def generate_one(
    client: genai.Client,
    model: str,
    short_id: str,
    record: dict[str, Any],
    related: list[str],
    force: bool,
) -> bool:
    out_path = os.path.join(MD_DIR, f"{short_id}.md")
    if os.path.exists(out_path) and not force:
        print(f"skip {short_id} (exists; use --force to overwrite)")
        return False
    prompt = build_prompt(short_id, record, related)
    print(f"generating {short_id} ...")
    body = call_gemini(client, model, prompt)
    if not body:
        sys.stderr.write(f"error: empty response for {short_id}\n")
        return False
    body = ensure_tags(body, paper_year(record))
    if not body.endswith("\n"):
        body += "\n"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(body)
    print(f"wrote {out_path}")
    return True


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--json", dest="json_path", help="Paperpile JSON export")
    ap.add_argument("--yaml", dest="yaml_path", default=DEFAULT_YAML)
    ap.add_argument("--id", dest="only_id", help="generate only this short id")
    ap.add_argument("--force", action="store_true", help="overwrite existing MD")
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument(
        "--update-index-only",
        action="store_true",
        help="only refresh papers.md from paper_ids.yaml",
    )
    ap.add_argument(
        "--skip-index",
        action="store_true",
        help="do not update papers.md",
    )
    args = ap.parse_args()

    load_dotenv(os.path.join(ROOT, ".env"))
    state = load_yaml(args.yaml_path)

    if args.update_index_only:
        update_papers_md(state)
        return

    json_path = args.json_path or find_latest_paperpile(ROOT)
    if not os.path.isabs(json_path) and not os.path.exists(json_path):
        json_path = os.path.join(ROOT, json_path)
    records = load_json(json_path)

    entries = list(state.get("papers") or [])
    if args.only_id:
        entries = [e for e in entries if e.get("id") == args.only_id]
        if not entries:
            raise SystemExit(f"id not in {args.yaml_path}: {args.only_id}")

    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise SystemExit("GEMINI_API_KEY not set (expected in .env)")

    client = genai.Client(api_key=api_key)
    related_all = related_ids(state, "")
    n_ok = 0
    import time

    for i, entry in enumerate(entries):
        sid = entry["id"]
        rec = find_record(records, entry)
        if rec is None:
            sys.stderr.write(
                f"warning: {sid} not found in JSON (citekey={entry.get('citekey')})\n"
            )
            continue
        if generate_one(
            client,
            args.model,
            sid,
            rec,
            [r for r in related_all if r != sid],
            args.force,
        ):
            n_ok += 1
            # Free-tier friendly pacing between successful calls
            if i + 1 < len(entries):
                time.sleep(2.0)
    if not args.skip_index:
        update_papers_md(state)
    print(f"done: generated {n_ok} page(s)")


if __name__ == "__main__":
    main()
