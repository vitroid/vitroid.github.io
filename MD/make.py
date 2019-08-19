#!/usr/bin/env python

import glob
import os
import scrapbox2md as s2m
import process_keywords as pk
import pickle
from logging import getLogger, basicConfig, INFO, DEBUG
basicConfig(level=INFO)
import re
        

def md_parser(filename):
    mode = "normal"
    for line in open(filename).readlines():
        if line[:3] == '```':
            if mode == "normal":
                mode = line[3:].split()[0]
            else:
                mode = "normal"
        if mode == "normal" and line[:4] == "    ":
            yield "quote", line
        else:
            yield mode, line


def kw_proc(word):
    return "[{0}]({0}.md)".format(word)

def hashtag_proc(x):
    return "[{0}]({0}.md)".format(x) + " "


def formatPage(title, target, keywords, processed=None, linked=None, autolink=False):
    """
    Format a page from a parsed page and a link list.
    """
    logger = getLogger()
    with open(target, "w") as file:
        if processed is None:
            file.write("# {0}\n\n".format(title))
        else:
            for mode, line in md_parser(processed):
                logger.info((mode,line))
                if mode == "normal":
                    # process autolinks
                    if autolink:
                        if not re.search("^#+\s", line):
                            for keyword in keywords:
                                line = re.sub("[^#]("+keyword+")", lambda x:kw_proc(x.group(1)), line)
                    # process hashtag
                    line = re.sub(r"#([^#\s]+)\s", lambda x:hashtag_proc(x.group(1)), line)
                file.write(line)
        if linked is not None:
            if os.path.exists(linked):
                links = list(pickle.load(open(linked, "rb")))
                logger.info(links)
                file.write("## Linked from\n\n")
                for link in sorted(links):
                    file.write("* [{1}]({0})\n".format(link, link[:-3]))
        if processed is not None:
            file.write("\n\n----\n[Edit](https://github.com/vitroid/vitroid.github.io/edit/master/MD/{0}.md)\n".format(title))
        
                

for file in glob.glob("*.sb"):
    mdfile = file[:-2] + "md"
    if not os.path.exists(mdfile) or os.path.getmtime(mdfile) < os.path.getmtime(file):
        title = file[:-3]
        lines = open(file).readlines()
        md = s2m.scrapbox2md(title, lines)
        open(mdfile, "w").write(md)
        
for file in glob.glob("*.md"):
    target = "../" + file
    if not os.path.exists(target) or os.path.getmtime(target) < os.path.getmtime(file):
        # if the original md is editted
        # md_parser adds line attributes
        md = [x for x in md_parser(file)]
        pk.process_keywords(file, md)


pages = [file[:-3]      for file in glob.glob("*.md")]
words = [file[:-7][7:]  for file in glob.glob("../ref/*.pickle")]


for page in pages:
    processed = page + ".md"
    linked    = "../ref/" + page + ".pickle"
    target    = "../" + page + ".md"
    go = False
    if not os.path.exists(target):
        go = True
    elif os.path.getmtime(target) < os.path.getmtime(processed):
        go = True
    elif os.path.exists(linked) and os.path.getmtime(target) < os.path.getmtime(linked):
        go = True
    if go:
        formatPage(page, target, keywords=pages, processed=processed, linked=linked)

for page in words:
    processed = page + ".md"
    linked    = "../ref/" + page + ".pickle"
    target    = "../" + page + ".md"
    if (not os.path.exists(target)) or ( (not os.path.exists(processed))
                                         and os.path.getmtime(target) < os.path.getmtime(linked)):
        formatPage(page, target, keywords=pages, linked=linked)
