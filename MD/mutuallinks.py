#!/usr/bin/env python

# scan all md files and make the link lists

import os
import glob
import re
from logging import getLogger, basicConfig, INFO, DEBUG
from collections import defaultdict

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
    with open("../" + filename, "w") as file:
        if os.path.exists(filename):
            file.write("".join(open(filename).readlines()))
        # reverse link list
        if len(D[filename]):
            file.write("## Linked from\n\n")
            for fn in sorted(D[filename]):
                file.write("* [{1}]({0})\n".format(fn, fn[:-3]))

    
