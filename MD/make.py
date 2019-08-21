#!/usr/bin/env python

import glob
import os
import scrapbox2md as s2m
import process_keywords as pk
import pickle
from logging import getLogger, basicConfig, INFO, DEBUG
basicConfig(level=INFO)
import re
from ktree import *        

def visualindex():
    newest = sorted([x for x in glob.glob("*.md")], key=lambda x: os.path.getmtime(x))
    s = ""
    
    for row in range(4):
        for col in range(3):
            found = False
            while not found:
                page = newest.pop(0)
                for line in open(page).readlines():
                    m = re.search(r"!\[[^\]]*\]\(([^\)]+)\)", line)
                    if m:
                        s += "[![]({0})]({1})\n".format(m.group(1), page[:-3])
                        found = True
                        break
        s += "\n"

    return s


    
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
    # for jekyll
    return "[{0}](/{0})".format(word)
#    return "[{0}]({0}.md)".format(word)

def hashtag_proc(x):
    # for jekyll
    return "[{0}](/{0})".format(x) + " "
#    return "[{0}]({0}.md)".format(x) + " "


def formatPage(title, target, kwtree, processed=None, linked=None, autolink=False):
    """
    Format a page from a parsed page and a link list.
    """
    logger = getLogger()
    with open(target, "w") as file:
        # yaml header (required for custom jekyll)
        file.write("---\n---\n")
        if processed is None:
            file.write("# {0}\n\n".format(title))
        else:
            for mode, line in md_parser(processed):
                logger.info((mode,line))
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
                                        logger.info((m.span(),line))
                                        logger.info(line[head+1:head+1+m.span()[0]])
                                        s += "[{0}](/{0})".format(line[1:1+m.span()[0]])
                                        line = line[m.span()[1]:]
                                        continue
                                s += line[0]
                                line = line[1:]
                                continue
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
                file.write(line)
        if linked is not None:
            if os.path.exists(linked):
                links = list(pickle.load(open(linked, "rb")))
                # logger.info(links)
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
        md = s2m.scrapbox2md(title, lines, autolink=True)
        open(mdfile, "w").write(md)
        
for file in glob.glob("*.md"):
    target = "../" + file
    if not os.path.exists(target) or os.path.getmtime(target) < os.path.getmtime(file):
        # if the original md is editted
        # md_parser adds line attributes
        md = [x for x in md_parser(file)]
        pk.process_keywords(file, md, autolink=True)


pages = [file[:-3]      for file in glob.glob("*.md")]
words = [file[:-7][7:]  for file in glob.glob("../ref/*.pickle")]
kwtree = keyword_tree(pages)

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
        formatPage(page, target, kwtree, processed=processed, linked=linked, autolink=True)


for page in words:
    processed = page + ".md"
    linked    = "../ref/" + page + ".pickle"
    target    = "../" + page + ".md"
    if (not os.path.exists(target)) or ( (not os.path.exists(processed))
                                         and os.path.getmtime(target) < os.path.getmtime(linked)):
        formatPage(page, target, kwtree, linked=linked, autolink=True)

#with open("index.md") as f:
#    open("../index.md", "w").write(f.read() + visualindex())
