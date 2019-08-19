#!/usr/bin/env python

import sys
import re
from logging import getLogger, basicConfig, INFO, DEBUG
import requests

def determine_imagetype(urlbase):
    url = urlbase + ".jpg"
    response = requests.head(url)
    if response.status_code == 200:
        return url
    url = urlbase + ".png"
    response = requests.head(url)
    if response.status_code == 200:
        return url
    url = urlbase + ".gif"
    response = requests.head(url)
    if response.status_code == 200:
        return url
    return None


def bracket_proc(x, autolink=False):
    logger = getLogger()
    x = x[1:len(x)-1]
    if x[-5:] == ".icon":
        # Icons are not available.
        return ""
    elements = x.split(" ")
    extlink = False
    if elements[0][:4] == "http":
        url   = elements[0]
        label = " ".join(elements[1:])
        extlink = True
    elif elements[-1][:4] == "http":
        url   = elements[-1]
        label = " ".join(elements[:-1])
        extlink = True
    if extlink:
        if url[-3:] in ("jpg", "png"):
            return "![{0}]({1})".format(label, url)
        if url[:17] == "https://gyazo.com":
            urlbase = "https://i.gyazo.com" + url[17:]
            imageurl = determine_imagetype(urlbase)
            if imageurl is not None:
                return "![{0}]({1})".format(label, imageurl)
        return "[{0}]({1})".format(label, url)
    elif elements[0] == "$":
        # math tex
        formula = " ".join(elements[1:])
        return " \\\\({0}\\\\) ".format(formula)
    elif elements[0] == "_":
        # underline
        formula = " ".join(elements[1:])
        return " __{0}__ ".format(formula)
    elif elements[0] == '**':
        return "＃＃ " + " ".join(elements[1:])
    elif elements[0] == '*':
        return "＃＃＃ " + " ".join(elements[1:])
    else:
        if not autolink:
            # It does not rely on the autolink
            # convert an empty link to an internal link
            # return "[{0}]({0}.md)".format(x)
            # or a hashtag
            return "#{0} ".format(x)
        # remove the bracket pointing an another page
        return "{0}".format(x)
    
    
def hashtag_proc(x):
    return "[{0}]({0}.md)".format(x[1:len(x)-1]) + x[-1]


def head_spaces(x):
    i = 0
    while x[i] in (" ","\t"):
        i+=1
    return i


basicConfig(level=INFO)


def scrapbox2md(title, lines, autolink=False):
    logger = getLogger()
    s = ""
    code = False
    indent = 0
    for i,line in enumerate(lines):

        # []
        if i == 0:
            # title line
            line = "# " + line

        if line[:5] == "code:":
            code = True
            print("")
            continue

        if code:
            if len(line) == 1:
                code = False
            else:
                line = "    "*indent + "   " + line
            s += line
            continue

        # bracket
        line = re.sub(r"\[[^\]]*\]", lambda x:bracket_proc(x.group(), autolink), line)

        # hashtag
        #line = re.sub(r"#[^#\s]+\s", lambda x:hashtag_proc(x.group()), line)

        # prefix spaces 
        spaces = head_spaces(line)
        if spaces > 0:
            logger.debug("INDENT:"+line)
            if indent == 0:
                # insert a new line
                s += "\n"
            if line[spaces] not in "0123456789":
                line = "  "*(spaces-1) + "* " + line[spaces:]
            else:
                line = "  "*(spaces-1) + line[spaces:]
        else:
            if indent > 0:
                # insert a NL when a list ends
                s += "\n"
            # in markdown, a paragraph ends with two NLs.
            line += "\n"
        indent = spaces

        # replace escaped letters
        line = re.sub("＃", "#", line)
        s += line
    return s
        
