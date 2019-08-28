#!/usr/bin/env python

"""
convert wiki attachments
"""
import sys
import glob
import os
import urllib.request
from collections import defaultdict
import re
from logging import getLogger, basicConfig, INFO, DEBUG
basicConfig(level=INFO)
logger = getLogger()

D = defaultdict(dict)

for file in glob.glob("_attach/matto/*"):
    eucname = os.path.basename(file).replace("+"," ")
    name = urllib.request.unquote(eucname,'euc-jp')
    n = name.find(".")
    assert n>= 0
    article = name[:n]
    attach  = name[n+1:]
    D[article][attach] = file

for article in D:
    mdpath = article + ".md"
    print(mdpath)
    if os.path.exists(mdpath):
        wikipath = "wiki/" + urllib.request.quote(article.encode("euc-jp")).replace("%20","+").replace("-", "%2D") + ".wiki"
        if not os.path.exists(wikipath):
            logger.warning("Not exist: {0} {1}".format(wikipath, mdpath))
            continue
        links = set()
        for line in open(wikipath, encoding="euc-jp").readlines():
            if len(line) > 2:
                if line[:2] != "//":
                    matches = re.findall(r"{{(thumbnail|thumbnail2|ref|ref_image)\s+([^}]+)}}", line)
                    for f,arg in matches:
                        if f in ("thumbnail", "thumbnail2"):
                            links |= set(arg.split(","))
                        elif f in ("ref",):
                            links.add(arg.split(",")[0])
                        else:
                            logger.info(f)
                            links.add(arg)
        logger.info((article, links))
        for link in links:
            if link not in D[article]:
                logger.warning("Unknown attachment: {0}".format(link))
                logger.warning(wikipath)
                logger.warning("{0}".format(D[article].keys()))
            else:
                folder = "../{0}".format(article)
                target = "{0}/{1}".format(folder, link)
                logger.info(target)
                if not os.path.exists(folder):
                    os.makedirs(folder)
                if not os.path.exists(target):
                    open(target, "wb").write(open(D[article][link], "rb").read())



        
                        
                            
                        

    
