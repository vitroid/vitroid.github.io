#!/usr/bin/env python

import sys
import glob
import os
import scrapbox2md as s2m
import process_keywords as pk
import pickle
# from imagesize import getsizes
import urllib.request
from PIL import Image

from logging import getLogger, basicConfig, INFO, DEBUG
basicConfig(level=INFO)

import re
from ktree import *

from tagcloud import tagcloud

ForceUpdate=len(sys.argv) > 1 and sys.argv[1] == "-f"

interwikinames = { "youtube": '{{% include youtubePlayer.html id="{0}" %}}',
                   "amazon" : '[![{1}](http://images-jp.amazon.com/images/P/{0}.09.LZZZZZZZ.jpg)](http://www.amazon.co.jp/exec/obidos/ASIN/{0})',
                   "doi"    : '[{1}](https://doi.org/{0})',
                   "DOI"    : '[{1}](https://doi.org/{0})',
                   "github" : '[{1}](https://github.com/vitroid/{0})',
                   "sb"     : '[{1}](https://scrapbox.io/vitroid/{0})',
                   "scrapbox-vitroid": '[{1}](https://scrapbox.io/vitroid/{0})',
                   "storage": '[{1}](http://theochem.chem.okayama-u.ac.jp/vitroid/{0})',
}




def aspect(images):
    #  width / height of a set of images
    if len(images) == 0:
        return 1
    rw = 0
    for image, title in images:
        w, h = image.size
        rw += w / h
    return rw


def visualindex():
    newest = sorted(glob.glob("*.md"), key=lambda x: -os.path.getmtime(x))
    # logger.info(newest[:20])
    s = ""

    logger.info("Generating visual index.")
    row = 0
    tnnum = 0
    try:
        os.makedirs("../tn")
    except:
        pass
    while row < 10:
        images = [] # URL, size, and MD page title
        while aspect(images) < 3:
            found = False
            while not found and len(newest) > 0:
                page = newest.pop(0)
                title = page[:-3]
                for line in open("../"+page).readlines():
                    m = re.search(r"!\[[^\]]*\]\(([^\)]+)\)", line)
                    if m:
                        url = m.group(1)
                        logger.info(url)
                        try:
                            method, loc = url.split(":")
                            url = method+":"+urllib.parse.quote(loc)
                            image = Image.open(urllib.request.urlopen(url, timeout=2))
                        except:
                            continue
                        if image is not None:
                            images.append((image, title))
                            found = True
                            break
        width = 749
        height = width / aspect(images)
        # in raw HTML
        s += "<div class='vi'>\n"
        for image, title in images:
            w, h = image.size
            w *= height / h
            #save w, height
            tn = image.resize((int(w),int(height)))
            logger.info("  {1} {0}".format(title, tnnum))
            tn.save("../tn/{0}.png".format(tnnum))
            s += "  <a href='/{0}'><img src='/tn/{1}.png' /></a>\n".format(title, tnnum)
            tnnum += 1
        s += "</div>\n\n"
        row += 1

    return s



def md_parser(filename):
    mode = "normal"
    for line in open(filename).readlines():
        if line[:3] == '```':
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


def kw_proc(word):
    # for jekyll
    return "[{0}](/{0})".format(word)
#    return "[{0}]({0}.md)".format(word)




def formatPage(title, kwtree, processed=None, linked=None, autolink=False):
    """
    Format a page from a parsed page and a link list.

    Parse and move the file in MD/ into appropriate places.
    """
    tags = []

    def hashtag_proc(x):
        # for jekyll
        tags.append(x)
        return "[{0}](/{0})".format(x) + " "


    logger = getLogger()
    body = ""
    if processed is not None:
        for mode, line in md_parser(processed):
            # logger.info((mode,line))
            if mode == "normal":
                # process autolinks
                if autolink:
                    head = 0
                    s = ""
                    while len(line):
                        if line[0] == "#":
                            # might be a hashtag
                            if line[1] not in "# ":
                                # it is a hashtag
                                m = re.search(r"\s", line[1:])
                                if m:
                                    # logger.info((m.span(),line))
                                    # logger.info(line[head+1:head+1+m.span()[0]])
                                    tag = line[1:1+m.span()[0]]
                                    s += "[{0}](/{0})".format(tag)
                                    tags.append(tag)
                                    line = line[m.span()[1]:]
                                    continue
                            s += line[0]
                            line = line[1:]
                            continue
                        # protect plain URL link and also convert as an MD link
                        m = re.search(r"^(https?://[^\s\)]+)[\s\)]", line)
                        if m:
                            matched = m.group(1)
                            name,ext = os.path.splitext(matched)
                            if ext in (".jpg", ".JPG", ".png", ".PNG", ".gif", ".GIF"):
                                s += "!"
                                logger.info("    Automatic IMG link: {0}".format(matched))
                            else:
                                logger.info("    Automatic URL link: {0}".format(matched))
                            s += "[{0}]({0})".format(matched)
                            line = line[len(matched):]
                            continue
                        # bypass special syntaxes
                        m = re.search(r"^\[([^\]]*)\]", line)
                        # Bracketed
                        if m:
                            label = m.group(1)
                            m2 = re.search(r"\(([^\)]*)\)", line[len(label)+2:])
                            # Followed by parens
                            if m2:
                                link = m2.group(1)
                                line = line[len(label)+len(link)+4:]
                            else:
                                line = line[len(label)+2:]
                                link = label
                            # logger.info(link)
                            methodloc = link.split(":", 1)
                            methodloc.append("")
                            method, loc = methodloc[:2]
                            # logger.info(methodloc)
                            if method in interwikinames:
                                html = interwikinames[method].format(loc, label)
                                s += html
                                logger.info("    InterWikiName {0} {1} {2}".format(method, loc, html))
                            else:
                                s += "[{0}]({1})".format(label, link)
                            continue

                        # autolinker
                        found = keyword_find(line, kwtree)
                        if found:
                            # logger.info(line[:head])
                            # for jekyll
                            s += "[{0}](/{0})".format(line[:found])
                            #prefix = line[:head] + "[{0}]({0}.md)".format(line[head:head+found])
                            line = line[found:]
                        else:
                            s += line[0]
                            line = line[1:]
                    line = s
                else:
                    # process hashtag
                    line = re.sub(r"#([^#\s]+)\s", lambda x:hashtag_proc(x.group(1)), line)
            body += line
    footer = ""
    if linked is not None:
        if os.path.exists(linked):
            links = list(pickle.load(open(linked, "rb")))
            # logger.info(links)
            footer += "\n\n## Linked from\n\n"
            for link in sorted(links):
                footer += "* [{0}](/{0})\n".format(link[:-3])
            footer += "\n\n"
    if processed is not None:
        footer += "----\n\n[Edit](https://github.com/vitroid/vitroid.github.io/edit/master/MD/{0}.md)\n\n".format(title)

    datestr = None
    for tag in tags:
        m = re.search(r"^([1-2]\d\d\d)-(\d+)-(\d+)$", tag)
        if m:
            datestr = "{0:04d}-{1:02d}-{2:02d}".format(int(m.group(1)), int(m.group(2)), int(m.group(3)))

    header = "---\n"
    m = re.search(r"^[\d-]+$", title)
    if m:
        title = "#"+title
    header += "title: {0}\n".format(title)
    #if datestr:
    #    header += "date: {0}\n".format(datestr) # no effect, rather harmful
    header += "---\n"
    return header + body + footer, tags



logger = getLogger()

# scrapbox conversion
logger.info("Converting Scrapbox pages.")
for file in glob.glob("*.sb"):
    mdfile = file[:-2] + "md"
    if not os.path.exists(mdfile) or os.path.getmtime(mdfile) < os.path.getmtime(file):
        title = file[:-3]
        lines = open(file).readlines()
        md = s2m.scrapbox2md(title, lines, autolink=True)
        logger.info("  {0}".format(file))
        open(mdfile, "w").write(md)

import urllib.request
import wiki2md as w2m

logger = getLogger()
# FSwiki conversion
logger.info("Converting FSWiki pages.")
for wikifile in glob.glob("wiki/*.wiki"):
    title = urllib.request.unquote(os.path.basename(wikifile).replace("+", " "), 'euc-jp')[:-5].replace("/", "_")
    sbfile = title + ".sb"
    mdfile = title + ".md"
    # logger.info(wikifile)
    if not os.path.exists(sbfile):
        if not os.path.exists(mdfile) or os.path.getmtime(mdfile) < os.path.getmtime(wikifile):
            md = w2m.wiki2md(open(wikifile, encoding="euc-jp"), title=title)
            logger.info("  {0}".format(wikifile))
            open(mdfile, "w").write(md)


rep = 1
if ForceUpdate:
    rep = 2

for R in range(rep):
    logger.info("Update link references.")
    for file in glob.glob("*.md"):
        target = "../" + file
        if True: # ALWAYS ForceUpdate or not os.path.exists(target) or os.path.getmtime(target) < os.path.getmtime(file):
            # if the original md is editted
            # md_parser adds line attributes
            md = [x for x in md_parser(file)]
            logger.info("  {0}".format(file))
            pk.process_keywords(file, md, autolink=True)

    pages = [file[:-3]      for file in glob.glob("*.md")]
    words = [file[:-7][8:]  for file in glob.glob("../_ref/*.pickle")]
    kwtree = keyword_tree(pages)


    logger.info("Parse and update Markdown pages.")
    for page in pages:
        processed = page + ".md"
        linked    = "../_ref/" + page + ".pickle"
        target    = "../" + page + ".md"
        go = ForceUpdate
        if not os.path.exists(target):
            go = True
        elif os.path.getmtime(target) < os.path.getmtime(processed):
            go = True
        elif os.path.exists(linked) and os.path.getmtime(target) < os.path.getmtime(linked):
            go = True
        if go:
            logger.info("  {0}".format(page))
            formatted, tags = formatPage(page, kwtree, processed=processed, linked=linked, autolink=True)
            open(target, "w").write(formatted)


    logger.info("Update virtual pages.")
    virtual = dict()
    for page in words:
        processed = page + ".md"
        linked    = "../_ref/" + page + ".pickle"
        target    = "../" + page + ".md"
        if (ForceUpdate and not os.path.exists(processed)) or ( (not os.path.exists(target)) or ( (not os.path.exists(processed))
                                             and os.path.getmtime(target) < os.path.getmtime(linked)) ):
            N = len(pickle.load(open(linked, "rb")))
            logger.info("  {0}: ({1})".format(page, N))
            formatted, tags = formatPage(page, kwtree, linked=linked, autolink=True)
            open(target, "w").write(formatted)
        if not os.path.exists(processed):
            N = len(pickle.load(open(linked, "rb")))
            # logger.info("  >>{1} {0}".format(page, N))
            if N >= 5:
                virtual[page] = N

for x in sorted(virtual, key=lambda x:-virtual[x])[:20]:
    logger.info("Candidates for the menu item: {0}".format(x))

open("../_includes/visual.html", "w").write(visualindex())

s = tagcloud(words)
open("../_includes/tagcloud.html", "w").write(s)
