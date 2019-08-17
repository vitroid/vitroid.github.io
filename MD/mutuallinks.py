#!/usr/bin/env python

# scan all md files and make the link lists

import os
import glob
import re
from logging import getLogger, basicConfig, INFO, DEBUG
from collections import defaultdict

def make_page(filename="", links={}):
    with open("../" + filename, "w") as file:
        if os.path.exists(filename):
            file.write("".join(open(filename).readlines()))
        else:
            file.write("# {0}\n\n".format(filename[:-3]))
        # reverse link list
        if len(links):
            file.write("## Linked from\n\n")
            for link in sorted(links):
                file.write("* [{1}]({0})\n".format(link, link[:-3]))
        file.write("\n\n----\n[Edit](https://github.com/vitroid/vitroid.github.io/edit/master/MD/{0})\n".format(filename))
    

basicConfig(level=INFO)
logger = getLogger()

D = defaultdict(set)

for filename in glob.glob("*.md"):
    logger.info(filename)
    for line in open(filename).readlines():
        for m in re.finditer(r"\[([^\[]+)\]\(([^\)]+)\)", line):
            if m.group(1)+".md" ==  m.group(2):
                # internal page
                D[m.group(2)].add(filename)
                logger.info((m.group(1), filename))




for filename in glob.glob("*.md"):
    make_page(filename=filename, links=D[filename])

for tag in D:
    if not os.path.exists(tag) and "/" not in tag:
        make_page(filename=tag, links=D[tag])
            
