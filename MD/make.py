#!/usr/bin/env python

import glob
import os
import scrapbox2md as s2m
import process_keywords as pk
import pickle
from logging import getLogger, basicConfig, INFO, DEBUG
basicConfig(level=INFO)





def formatPage(title, target, processed=None, linked=None):
    """
    Format a page from a parsed page and a link list.
    """
    logger = getLogger()
    with open(target, "w") as file:
        if processed is None:
            file.write("# {0}\n\n".format(title))
        else:
            file.write("".join(open(processed).readlines()))
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
    md = file[:-2] + "md"
    if not os.path.exists(md) or os.path.getmtime(md) < os.path.getmtime(file):
        print(md)
        s2m.scrapbox2md(file, md)

for file in glob.glob("*.md"):
    processed = "../processed/" + file
    if not os.path.exists(processed) or os.path.getmtime(processed) < os.path.getmtime(file):
        print(processed)
        pk.process_keywords(file, processed)



pages = [file[:-3][13:] for file in glob.glob("../processed/*.md")]
words = [file[:-7][7:]  for file in glob.glob("../ref/*.pickle")]


for page in pages:
    processed = "../processed/" + page + ".md"
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
        formatPage(page, target, processed=processed, linked=linked)

    for page in words:
        processed = "../processed/" + page + ".md"
        linked    = "../ref/" + page + ".pickle"
        target    = "../" + page + ".md"
        if not os.path.exists(target) or (not os.path.exists(processed)
                                      and os.path.getmtime(target) < os.path.getmtime(linked)):
            formatPage(page, target, linked=linked)
