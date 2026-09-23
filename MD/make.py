#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import glob
import os
import json
import hashlib
import time
import unicodedata
from collections import defaultdict

import urllib.request
import urllib.parse
import base64
import io
import re

from logging import getLogger, basicConfig, INFO, DEBUG

basicConfig(level=INFO)

from ktree import keyword_tree, keyword_find
from tagcloud import tagcloud

ForceUpdate = len(sys.argv) > 1 and sys.argv[1] == "-f"

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
WIKI_DIR = os.path.join(ROOT, "_wiki")
CACHE_DIR = os.path.join(ROOT, "_cache")
IMG_CACHE_DIR = os.path.join(CACHE_DIR, "img")
REF_DIR = os.path.join(ROOT, "_ref")
BACKLINKS_JSON = os.path.join(REF_DIR, "backlinks.json")
VISUAL_CACHE = os.path.join(CACHE_DIR, "visual.json")
FAILED_URLS = os.path.join(CACHE_DIR, "failed_urls.json")
TN_DIR = os.path.join(ROOT, "tn")
FAIL_TTL = 7 * 24 * 3600
WORD_BAD_CHARS = '/[]!"(),;'
ROOT_MD_KEEP = {
    "README.md",
    "CHANGELOG.md",
    "LICENSE.md",
    "CONTRIBUTING.md",
}

interwikinames = {
    "youtube": '{{% include youtubePlayer.html id="{0}" %}}',
    "amzn": "[{1}](http://amzn.asia/d/{0})",
    "amazon": "[![{1}](http://images-jp.amazon.com/images/P/{0}.09.LZZZZZZZ.jpg)](http://www.amazon.co.jp/exec/obidos/ASIN/{0})",
    "doi": "[{1}](https://doi.org/{0})",
    "DOI": "[{1}](https://doi.org/{0})",
    "github": "[{1}](https://github.com/vitroid/{0})",
    "sb": "[{1}](https://scrapbox.io/vitroid/{0})",
    "scrapbox-vitroid": "[{1}](https://scrapbox.io/vitroid/{0})",
    "storage": "[{1}](http://theochem.chem.okayama-u.ac.jp/vitroid/{0})",
}


logger = getLogger()


def nfc(s):
    return unicodedata.normalize("NFC", s)


def yaml_scalar(s):
    special = ":#{}[]&*?|>!%@`'\""
    if (
        not s
        or any(c in s for c in special)
        or s.strip() != s
        or s[0] in "-?"
        or s.lower() in ("null", "true", "false", "yes", "no", "on", "off")
    ):
        return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'
    return s


def write_if_changed(path, content):
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            if f.read() == content:
                return False
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return True


def load_json(path, default):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return default


def save_json(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)


def word_ok(word):
    return word and not any(c in word for c in WORD_BAD_CHARS)


def wiki_path(page):
    return os.path.join(WIKI_DIR, nfc(page) + ".md")


def md_parser(filename):
    mode = "normal"
    with open(filename, encoding="utf-8") as f:
        for line in f:
            line = nfc(line)
            if line[:3] == "```":
                if mode == "normal":
                    mode = line[3:]
                else:
                    mode = "normal"
            if mode == "normal" and line[:4] == "    ":
                yield "quote", line
            elif mode == "normal" and line[:2] == "{%":
                yield "special", line
            else:
                yield mode, line


def walk_normal_line(line, kwtree, autolink):
    """
    1パスでハッシュタグ・InterWiki・オートリンクを処理する。
    returns (formatted_line, words, tags)
    """
    words = set()
    tags = []
    # FSWiki datetime プラグイン: Unix 時刻はそのまま出し、,bbstime などは捨てる
    line = re.sub(
        r"\{\{\s*datetime\s+(\d+)(?:,\w+)?\s*\}\}",
        r"{{ \1 }}",
        line,
    )
    if not autolink:
        def hashtag_proc(m):
            tag = m.group(1)
            tags.append(tag)
            words.add(tag)
            return "[{0}](/{0}) ".format(tag)

        return re.sub(r"#([^#\s]+)\s", hashtag_proc, line), words, tags

    s = []
    while line:
        if line[0] == "#":
            if len(line) > 1 and line[1] not in "# ":
                m = re.search(r"\s", line[1:])
                if m:
                    tag = line[1 : 1 + m.span()[0]]
                    s.append("[{0}](/{0})".format(tag))
                    tags.append(tag)
                    words.add(tag)
                    line = line[m.span()[1] :]
                    continue
            s.append(line[0])
            line = line[1:]
            continue
        m = re.search(r"^(https?://[^\s\)]+)[\s\)]", line)
        if m:
            matched = m.group(1)
            name, ext = os.path.splitext(matched)
            if ext in (".jpg", ".JPG", ".png", ".PNG", ".gif", ".GIF"):
                s.append("!")
                logger.debug("    Automatic IMG link: {0}".format(matched))
            else:
                logger.debug("    Automatic URL link: {0}".format(matched))
            s.append("[{0}]({0})".format(matched))
            line = line[len(matched) :]
            continue
        m = re.search(r"^\[([^\]]*)\]", line)
        if m:
            label = m.group(1)
            m2 = re.search(r"^\(([^\)]*)\)", line[len(label) + 2 :])
            if m2:
                link = m2.group(1)
                line = line[len(label) + len(link) + 4 :]
            else:
                line = line[len(label) + 2 :]
                link = label
            methodloc = link.split(":", 1)
            methodloc.append("")
            method, loc = methodloc[:2]
            if method in interwikinames:
                html = interwikinames[method].format(loc, label)
                s.append(html)
                logger.debug(
                    "    InterWikiName {0} {1} {2}".format(method, loc, html)
                )
            else:
                s.append("[{0}]({1})".format(label, link))
            continue

        found = keyword_find(line, kwtree)
        if found:
            word = line[:found]
            s.append("[{0}](/{0})".format(word))
            words.add(word)
            line = line[found:]
        else:
            s.append(line[0])
            line = line[1:]
    return "".join(s), words, tags


def process_body(title, kwtree, processed=None, autolink=True):
    """本文のオートリンクとキーワード抽出を同時に行う。"""
    tags = []
    words = set()
    body = ""
    if processed is not None:
        for mode, line in md_parser(processed):
            if mode == "normal":
                line, w, t = walk_normal_line(line, kwtree, autolink=autolink)
                words.update(w)
                tags.extend(t)
            body += line
    return body, tags, words


def wrap_page(title, body, linked=None, has_source=False):
    """front matter と Linked from / Edit を付ける。走査はしない。"""
    footer = ""
    if linked:
        footer += "\n\n## Linked from\n\n"
        for link in sorted(linked):
            footer += "- [{0}](/{0})\n".format(link)
        footer += "\n\n"
    if has_source:
        footer += (
            "----\n\n[Edit](https://github.com/vitroid/vitroid.github.io/edit/master/MD/{0}.md)\n\n".format(
                title
            )
        )

    display = title
    if re.search(r"^[\d-]+$", title):
        display = "#" + title
    header = "---\n"
    header += "title: {0}\n".format(yaml_scalar(display))
    header += "permalink: {0}\n".format(yaml_scalar("/" + title))
    header += "---\n"
    return header + body + footer


def aspect(images):
    if len(images) == 0:
        return 1
    rw = 0
    for image, title in images:
        w, h = image.size
        rw += w / h
    return rw


def url_key(url):
    return hashlib.sha256(url.encode("utf-8")).hexdigest()[:16]


def first_image_url(title):
    for path in (wiki_path(title), os.path.join(os.path.dirname(__file__), title + ".md")):
        if not os.path.exists(path):
            continue
        with open(path, encoding="utf-8") as f:
            for line in f:
                m = re.search(r"!\[[^\]]*\]\(([^\)]+)\)", line)
                if m:
                    return m.group(1)
    return None


def open_cached_image(url, failed, now):
    """画像をローカルキャッシュから開く。無ければ取得して保存。失敗したら None。"""
    from PIL import Image

    if ":" not in url:
        rel = url.lstrip("/")
        local = os.path.join(ROOT, rel)
        try:
            image = Image.open(local)
            image.load()
            failed.pop(url, None)
            return image
        except Exception:
            logger.warning("No image retrieved: {0}".format(url[:80]))
            failed[url] = now
            return None

    if url in failed and not ForceUpdate:
        if now - failed[url] < FAIL_TTL:
            return None

    method, loc = url.split(":", 1)
    if method == "data":
        key = url_key(url)
        cache_path = os.path.join(IMG_CACHE_DIR, key)
        if os.path.exists(cache_path):
            try:
                image = Image.open(cache_path)
                image.load()
                failed.pop(url, None)
                return image
            except Exception:
                pass
        try:
            header, body = loc.split(",", 1)
            datatype, encoding = header.split(";")
            assert encoding == "base64"
            raw = base64.decodebytes(body.encode("utf-8"))
            os.makedirs(IMG_CACHE_DIR, exist_ok=True)
            with open(cache_path, "wb") as f:
                f.write(raw)
            failed.pop(url, None)
            return Image.open(io.BytesIO(raw))
        except Exception:
            logger.warning("No image retrieved (data URI).")
            failed[url] = now
            return None

    quoted = method + ":" + urllib.parse.quote(loc, safe="/:?&=%#")
    key = url_key(quoted)
    cache_path = os.path.join(IMG_CACHE_DIR, key)
    if os.path.exists(cache_path):
        try:
            image = Image.open(cache_path)
            image.load()
            failed.pop(url, None)
            return image
        except Exception:
            pass
    try:
        os.makedirs(IMG_CACHE_DIR, exist_ok=True)
        with urllib.request.urlopen(quoted, timeout=2) as resp:
            raw = resp.read()
        with open(cache_path, "wb") as f:
            f.write(raw)
        failed.pop(url, None)
        return Image.open(io.BytesIO(raw))
    except Exception:
        logger.warning("No image retrieved: {0}".format(url[:80]))
        failed[url] = now
        return None


def visualindex(source_pages):
    newest = sorted(
        (p + ".md" for p in source_pages),
        key=lambda x: (-(os.path.getmtime(x) if os.path.exists(x) else 0), x),
    )
    logger.info("Generating visual index.")
    try:
        from PIL import Image  # noqa: F401
    except ImportError:
        logger.warning("Pillow not installed; skip visual index.")
        return None
    os.makedirs(TN_DIR, exist_ok=True)
    os.makedirs(CACHE_DIR, exist_ok=True)

    prev = load_json(VISUAL_CACHE, {})
    failed = load_json(FAILED_URLS, {})
    now = time.time()
    failed = {u: t for u, t in failed.items() if now - t < FAIL_TTL}

    rows = []  # list of (items, images, height)
    remaining = list(newest)
    while len(rows) < 10 and remaining:
        items = []
        images = []
        while aspect(images) < 3 and remaining:
            page = remaining.pop(0)
            title = page[:-3]
            url = first_image_url(title)
            if not url:
                continue
            logger.debug(url if len(url) < 100 else url[:50] + " ... " + url[-50:])
            image = open_cached_image(url, failed, now)
            if image is None:
                continue
            images.append((image, title))
            items.append({"page": title, "url": url})
        if not images:
            break
        height = 749 / aspect(images)
        rows.append((items, images, height))

    fingerprint = [items for items, _images, _h in rows]
    prev_fp = prev.get("fingerprint")
    visual_html = os.path.join(ROOT, "_includes", "visual.html")
    tn_ok = all(
        os.path.exists(os.path.join(TN_DIR, "{0}.png".format(i)))
        for i in range(sum(len(items) for items, _im, _h in rows))
    )
    if (
        not ForceUpdate
        and prev_fp == fingerprint
        and tn_ok
        and os.path.exists(visual_html)
    ):
        logger.info("Visual index unchanged, skip.")
        save_json(FAILED_URLS, failed)
        return None

    s = ""
    tnnum = 0
    for items, images, height in rows:
        s += "<div class='vi'>\n"
        for (image, title), item in zip(images, items):
            w, h = image.size
            w *= height / h
            tn = image.resize((max(int(w), 1), max(int(height), 1)))
            logger.info("  {1} {0}".format(title, tnnum))
            tn.save(os.path.join(TN_DIR, "{0}.png".format(tnnum)))
            s += "  <a href='/{0}'><img src='/tn/{1}.png' /></a>\n".format(title, tnnum)
            tnnum += 1
        s += "</div>\n\n"

    save_json(VISUAL_CACHE, {"fingerprint": fingerprint})
    save_json(FAILED_URLS, failed)
    return s


def cleanup_root_md():
    removed = 0
    for name in os.listdir(ROOT):
        if not name.endswith(".md"):
            continue
        if name in ROOT_MD_KEEP:
            continue
        path = os.path.join(ROOT, name)
        if os.path.isfile(path):
            os.remove(path)
            removed += 1
    if removed:
        logger.info("Removed {0} generated markdown files from repo root.".format(removed))


def cleanup_stale_wiki(wanted):
    if not os.path.isdir(WIKI_DIR):
        return
    removed = 0
    for name in os.listdir(WIKI_DIR):
        if not name.endswith(".md"):
            continue
        page = nfc(name[:-3])
        if page not in wanted:
            os.remove(os.path.join(WIKI_DIR, name))
            removed += 1
    if removed:
        logger.info("Removed {0} stale pages from _wiki/.".format(removed))


def convert_scrapbox():
    files = glob.glob("*.sb")
    if not files:
        return
    logger.info("Converting Scrapbox pages.")
    import scrapbox2md as s2m

    for file in files:
        mdfile = file[:-2] + "md"
        if not os.path.exists(mdfile) or os.path.getmtime(mdfile) < os.path.getmtime(
            file
        ):
            title = file[:-3]
            lines = open(file, encoding="utf-8").readlines()
            md = s2m.scrapbox2md(title, lines, autolink=True)
            logger.info("  {0}".format(file))
            open(mdfile, "w", encoding="utf-8").write(md)


def main():
    convert_scrapbox()
    os.makedirs(WIKI_DIR, exist_ok=True)
    os.makedirs(REF_DIR, exist_ok=True)

    pages = [nfc(file[:-3]) for file in glob.glob("*.md")]
    source_pages = set(pages)
    source_folded = {p.casefold(): p for p in pages}
    kwtree = keyword_tree(pages)

    logger.info("Parse Markdown pages.")
    graph = defaultdict(set)
    bodies = {}
    for page in pages:
        body, tags, words = process_body(
            page, kwtree, processed=page + ".md", autolink=True
        )
        bodies[page] = body
        for word in words:
            word = nfc(word)
            if not word_ok(word):
                continue
            key = source_folded.get(word.casefold(), word)
            graph[key].add(page)

    logger.info("Write wiki pages.")
    written = 0
    for page in pages:
        content = wrap_page(
            page, bodies[page], linked=graph.get(page), has_source=True
        )
        if write_if_changed(wiki_path(page), content):
            logger.info("  {0}".format(page))
            written += 1

    logger.info("Update virtual pages.")
    virtual = dict()
    for word, refs in graph.items():
        if word in source_pages:
            continue
        N = len(refs)
        content = wrap_page(word, "", linked=refs, has_source=False)
        if write_if_changed(wiki_path(word), content):
            logger.info("  {0}: ({1})".format(word, N))
            written += 1
        if N >= 5:
            virtual[word] = N

    wanted = source_pages | set(graph.keys())
    cleanup_stale_wiki(wanted)
    cleanup_root_md()

    logger.info("Wrote {0} pages.".format(written))
    for x in sorted(virtual, key=lambda x: -virtual[x])[:20]:
        logger.debug("Candidates for the menu item: {0}".format(x))

    graph_out = {k: sorted(v) for k, v in graph.items()}
    save_json(BACKLINKS_JSON, graph_out)

    html = visualindex(source_pages)
    if html is not None:
        path = os.path.join(ROOT, "_includes", "visual.html")
        if write_if_changed(path, html):
            logger.info("Updated visual.html")

    s = tagcloud(graph, source_pages)
    path = os.path.join(ROOT, "_includes", "tagcloud.html")
    if write_if_changed(path, s):
        logger.info("Updated tagcloud.html")


if __name__ == "__main__":
    main()
