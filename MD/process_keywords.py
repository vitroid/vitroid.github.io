#!/usr/bin/env python

# scan all md files and make the link lists

import glob
import re
from logging import getLogger, basicConfig, INFO, DEBUG
import sys
import pickle
import os
import smartfind as sf

basicConfig(level=INFO)
logger = getLogger()


def hashtag_proc(x, words):
    words.add(x)
    return ""
    # return "[{0}]({0}.md)".format(x) + " "

from ktree import *

keywords = [fn[:-3] for fn in glob.glob("*.md")]
kwtree = keyword_tree(keywords)
# logger.info(kwtree)

if __name__ == "__main__":
    for word in ("かもめだった", "LDAがいい", "ice T研究のため", "ice T3", "ice T"):
        print(word, keyword_find(word, kwtree))

def process_keywords(filename, lines, autolink=False):
    words = set()
    parsed = ""
    for mode, line in lines:
        if mode == "normal":
            if autolink:
                head = 0
                processed = ""
                # logger.info(line)
                while head < len(line):
                    if line[head] == "#":
                        # might be a hashtag
                        if line[head+1] not in "# ":
                            # it is a hashtag
                            m = re.search(r"\s", line[head+1:])
                            if m:
                                words.add(line[head+1:head+1+m.span()[0]])
                                head += m.span()[1]
                                continue
                        head += 1
                        continue
                    found = keyword_find(line[head:], kwtree)
                    if found:
                        words.add(line[head:head+found])
                        head += found
                    else:
                        head += 1
            else:
                # hashtag
                line = re.sub(r"#([^#\s]+)\s", lambda x:hashtag_proc(x.group(1), words), line)

    for word in words:
        if len(tuple(sf.sfind(word, '/[]!"(),;'))):
            logger.info("  ELIM {0}".format(word))
            continue
        referfrom = "../_ref/{0}.pickle".format(word)
        if os.path.exists(referfrom):
            logger.info("  Update linklist {0}".format(word))
            with open(referfrom, mode='rb') as f:
                S = pickle.load(f)
        else:
            S = set()
            logger.info("  Create linklist {0}".format(word))
        L0 = len(S)
        S.add(filename)
        if L0 != len(S):
            with open(referfrom, mode='wb') as f:
                pickle.dump(S, f)

    # return parsed

