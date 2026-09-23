#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Assign short paper IDs from a Paperpile JSON export (incremental)."""

from __future__ import annotations

import argparse
import glob
import os
import re
import sys
from typing import Any

try:
    import yaml
except ImportError:
    sys.stderr.write("PyYAML is required: pip install PyYAML\n")
    sys.exit(1)

import json

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
MD_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_YAML = os.path.join(MD_DIR, "paper_ids.yaml")
DEFAULT_YEAR_FROM = 2022

# Japanese family-name → Latin initial used in short IDs
JP_INITIAL = {
    "松本": "M",
    "松本正和": "M",
    "田中": "T",
    "二井矢": "N",
    "河原": "K",
}

PAPER_ID_RE = re.compile(r"^[A-Z]{1,12}20\d{2}[A-Z]?$")


def load_json(path: str) -> list[dict[str, Any]]:
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        raise SystemExit(f"Expected a JSON array: {path}")
    return data


def find_latest_paperpile(root: str) -> str:
    paths = sorted(
        glob.glob(os.path.join(root, "Paperpile*.json")),
        key=os.path.getmtime,
    )
    if not paths:
        raise SystemExit(f"No Paperpile*.json under {root}; pass --json")
    return paths[-1]


def paper_year(p: dict[str, Any]) -> int | None:
    y = (p.get("published") or {}).get("year")
    if y is None:
        return None
    return int(y)


def paper_sort_key(p: dict[str, Any]) -> tuple:
    pub = p.get("published") or {}
    return (
        paper_year(p) or 0,
        int(pub.get("month") or 0),
        int(pub.get("day") or 0),
        p.get("citekey") or "",
    )


def normalize_doi(doi: str | None) -> str | None:
    if not doi:
        return None
    d = doi.strip().lower()
    for prefix in ("https://doi.org/", "http://doi.org/", "doi:"):
        if d.startswith(prefix):
            d = d[len(prefix) :]
    return d or None


def author_initial(author: dict[str, Any]) -> str:
    last = (author.get("last") or "").strip()
    if not last:
        return "?"
    if last in JP_INITIAL:
        return JP_INITIAL[last]
    if ord(last[0]) < 128:
        return last[0].upper()
    for key, initial in JP_INITIAL.items():
        if last.startswith(key):
            return initial
    return "?"


def base_code(authors: list[dict[str, Any]], year: int) -> str:
    return "".join(author_initial(a) for a in authors) + str(year)


def existing_md_ids(md_dir: str) -> set[str]:
    ids: set[str] = set()
    for name in os.listdir(md_dir):
        if not name.endswith(".md"):
            continue
        stem = name[:-3]
        if PAPER_ID_RE.match(stem):
            ids.add(stem)
    return ids


def load_yaml(path: str) -> dict[str, Any]:
    if not os.path.exists(path):
        return {"year_from": DEFAULT_YEAR_FROM, "papers": []}
    with open(path, encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    data.setdefault("year_from", DEFAULT_YEAR_FROM)
    data.setdefault("papers", [])
    return data


def dump_yaml(path: str, data: dict[str, Any]) -> None:
    # Prefer stable, readable order
    with open(path, "w", encoding="utf-8") as f:
        yaml.safe_dump(
            data,
            f,
            allow_unicode=True,
            sort_keys=False,
            default_flow_style=False,
        )


def match_entry(
    papers: list[dict[str, Any]],
    *,
    doi: str | None,
    paperpile_id: str | None,
    citekey: str | None,
) -> dict[str, Any] | None:
    ndoi = normalize_doi(doi)
    if ndoi:
        for e in papers:
            if normalize_doi(e.get("doi")) == ndoi:
                return e
    if paperpile_id:
        for e in papers:
            if e.get("paperpile_id") == paperpile_id:
                return e
    if citekey:
        for e in papers:
            if e.get("citekey") == citekey:
                return e
    return None


def next_free_id(base: str, used: set[str]) -> str:
    candidates = [base] + [base + chr(ord("A") + i) for i in range(26)]
    for c in candidates:
        if c not in used:
            return c
    raise SystemExit(f"No free short id for base {base}")


def md_exists_for(md_dir: str, short_id: str) -> bool:
    return os.path.exists(os.path.join(md_dir, short_id + ".md"))


def scan_md_dois(md_dir: str) -> dict[str, str]:
    """Map normalized DOI → short id from existing MD/*.md heads."""
    by_doi: dict[str, str] = {}
    for name in os.listdir(md_dir):
        if not name.endswith(".md") or not PAPER_ID_RE.match(name[:-3]):
            continue
        stem = name[:-3]
        path = os.path.join(md_dir, name)
        try:
            with open(path, encoding="utf-8") as f:
                head = f.read(2000)
        except OSError:
            continue
        m = re.search(r"doi:([0-9a-zA-Z./\-_()]+)", head, re.I)
        if m:
            by_doi[normalize_doi(m.group(1))] = stem
    return by_doi


def assign(
    source_path: str,
    yaml_path: str,
    year_from: int,
    dry_run: bool,
) -> dict[str, Any]:
    records = load_json(source_path)
    state = load_yaml(yaml_path)
    existing_entries: list[dict[str, Any]] = list(state.get("papers") or [])
    used_ids = existing_md_ids(MD_DIR) | {
        e["id"] for e in existing_entries if e.get("id")
    }

    recent = [p for p in records if (paper_year(p) or 0) >= year_from]
    recent.sort(key=paper_sort_key)
    doi_to_md = scan_md_dois(MD_DIR)

    added: list[dict[str, Any]] = []

    # Mark missing
    source_dois = {normalize_doi(p.get("doi")) for p in recent if p.get("doi")}
    source_ids = {p.get("_id") for p in recent if p.get("_id")}
    source_citekeys = {p.get("citekey") for p in recent if p.get("citekey")}

    for entry in existing_entries:
        present = False
        if normalize_doi(entry.get("doi")) and normalize_doi(entry.get("doi")) in source_dois:
            present = True
        elif entry.get("paperpile_id") and entry.get("paperpile_id") in source_ids:
            present = True
        elif entry.get("citekey") and entry.get("citekey") in source_citekeys:
            present = True
        if present:
            entry.pop("missing_in_source", None)
        else:
            if not entry.get("missing_in_source"):
                entry["missing_in_source"] = True
                sys.stderr.write(
                    f"warning: {entry.get('id')} missing in source JSON\n"
                )

    yaml_owned = {e["id"] for e in existing_entries if e.get("id")}

    for p in recent:
        doi = p.get("doi")
        pid = p.get("_id")
        citekey = p.get("citekey")
        entry = match_entry(
            existing_entries, doi=doi, paperpile_id=pid, citekey=citekey
        )
        year = paper_year(p)
        if year is None:
            continue

        if entry:
            if citekey:
                entry["citekey"] = citekey
            if doi:
                entry["doi"] = doi
            if pid:
                entry["paperpile_id"] = pid
            if p.get("title"):
                entry["title"] = p.get("title")
            entry["year"] = year
            entry["existing"] = md_exists_for(MD_DIR, entry["id"])
            entry.pop("missing_in_source", None)
            continue

        ndoi = normalize_doi(doi)
        base = base_code(p.get("author") or [], year)
        if ndoi and ndoi in doi_to_md and doi_to_md[ndoi] not in yaml_owned:
            # Existing MD stamped with this DOI wins (e.g. MT2022)
            short_id = doi_to_md[ndoi]
        else:
            short_id = next_free_id(base, used_ids | yaml_owned)

        used_ids.add(short_id)
        yaml_owned.add(short_id)
        new_entry = {
            "id": short_id,
            "citekey": citekey,
            "doi": doi,
            "paperpile_id": pid,
            "year": year,
            "title": p.get("title"),
            "existing": md_exists_for(MD_DIR, short_id),
        }
        new_entry = {k: v for k, v in new_entry.items() if v is not None}
        existing_entries.append(new_entry)
        added.append(new_entry)

    state["year_from"] = year_from
    state["last_source"] = os.path.basename(source_path)
    state["papers"] = existing_entries

    print(f"source: {source_path}")
    print(f"year_from: {year_from}")
    print(f"total assigned: {len(existing_entries)}")
    print(f"newly added: {len(added)}")
    for e in existing_entries:
        flag = "EXISTING" if e.get("existing") else "new"
        miss = " MISSING" if e.get("missing_in_source") else ""
        print(
            f"  {e['id']:12s}  {flag:8s}{miss}  "
            f"{e.get('citekey') or '-'}  {e.get('doi') or '-'}"
        )

    if dry_run:
        print("(dry-run: not writing YAML)")
        return state

    dump_yaml(yaml_path, state)
    print(f"wrote {yaml_path}")
    return state


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--json",
        dest="json_path",
        help="Paperpile JSON export (default: latest Paperpile*.json in repo root)",
    )
    ap.add_argument(
        "--yaml",
        dest="yaml_path",
        default=DEFAULT_YAML,
        help=f"assignment file (default: {DEFAULT_YAML})",
    )
    ap.add_argument(
        "--year-from",
        type=int,
        default=DEFAULT_YEAR_FROM,
        help=f"include papers from this year (default: {DEFAULT_YEAR_FROM})",
    )
    ap.add_argument(
        "--dry-run",
        action="store_true",
        help="print assignment without writing YAML",
    )
    args = ap.parse_args()
    json_path = args.json_path or find_latest_paperpile(ROOT)
    if not os.path.isabs(json_path):
        cand = json_path
        if not os.path.exists(cand):
            cand = os.path.join(ROOT, json_path)
        json_path = cand
    assign(json_path, args.yaml_path, args.year_from, args.dry_run)


if __name__ == "__main__":
    main()
