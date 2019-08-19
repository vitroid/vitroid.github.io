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


def kw_proc(word, words):
    words.add(word)
    return ""
    # return "[{0}]({0}.md)".format(word)

def hashtag_proc(x, words):
    words.add(x)
    return ""
    # return "[{0}]({0}.md)".format(x) + " "

keywords = [fn[:-3] for fn in glob.glob("*.md")]

def process_keywords(filename, lines, autolink=False):
    words = set()
    parsed = ""
    for mode, line in lines:
        if mode == "normal":
            if autolink:
                if not re.search("^#+\s", line):
                    for keyword in keywords:
                        line = re.sub("[^#]("+keyword+")", lambda x:kw_proc(x.group(1), words), line)
            # hashtag
            line = re.sub(r"#([^#\s]+)\s", lambda x:hashtag_proc(x.group(1), words), line)

    for word in words:
        if len(tuple(sf.sfind(word, '/[]!"(),;'))):
            logger.info("ELIM {0}".format(word))
            continue
        referfrom = "../ref/{0}.pickle".format(word)
        if os.path.exists(referfrom):
            logger.info("Update linklist {0}".format(word))
            with open(referfrom, mode='rb') as f:
                S = pickle.load(f)
        else:
            S = set()
            logger.info("Create linklist {0}".format(word))
        S.add(filename)
        with open(referfrom, mode='wb') as f:
            pickle.dump(S, f)

    logger.info(words)
    # return parsed

