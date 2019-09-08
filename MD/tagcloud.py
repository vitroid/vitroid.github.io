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

ForceUpdate = False


logger = getLogger()

pages = [file[:-3]      for file in glob.glob("*.md")]
words = [file[:-7][8:]  for file in glob.glob("../_ref/*.pickle")]
kwtree = keyword_tree(pages)

def tagcloud(words):
    logger.info("Update tagcloud.")
    virtual = dict()
    MAX=0
    for page in words:
        processed = page + ".md"
        linked    = "../_ref/" + page + ".pickle"
        if not os.path.exists(processed):
            N = len(pickle.load(open(linked, "rb")))
            if N >= 2:
                virtual[page] = N
                if N > MAX:
                    MAX=N

    s = "<div class='tc'>\n"

    for tag in sorted(virtual):
        N = virtual[tag]
        fontsize = 80 + 220 * N // MAX
        gray     = 0 + 150 * (MAX-N) // MAX
        gray     = "#{0:02x}{0:02x}{0:02x}".format(gray)
        s += "<span class='tag' style='font-size:{0}%;' ><a href='{2}' style='color:{1};'>{2}</a></span>\n".format(fontsize,gray,tag)

    s += "</div>"
    return s

def main():
    open("../_includes/tagcloud.html", "w").write(s)


