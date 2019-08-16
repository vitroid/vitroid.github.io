#!/usr/bin/env python

import sys
import re
from logging import getLogger, basicConfig, INFO, DEBUG


def bracket_proc(x):
    logger = getLogger()
    x = x[1:len(x)-1]
    elements = x.split(" ")
    if elements[0][:4] == "http":
        url   = elements[0]
        label = " ".join(elements[1:])
        return "[{0}]({1})".format(label, url)
    elif elements[-1][:4] == "http":
        url   = elements[-1]
        label = " ".join(elements[:-1])
        return "[{0}]({1})".format(label, url)
    elif elements[0] == '**':
        return "＃＃ " + " ".join(elements[1:])
    elif elements[0] == '*':
        return "＃＃＃ " + " ".join(elements[1:])
    else:
        return "[{0}]({0}.md)".format(x)
    
    
def hashtag_proc(x):
    return "[{0}]({0}.md)".format(x[1:len(x)-1]) + x[-1]


def head_spaces(x):
    i = 0
    while x[i] in (" ","\t"):
        i+=1
    return i


basicConfig(level=INFO)


def scrapbox2md(sbfile, mdfile):
    open(mdfile, "w").write(s2m_lines(open(sbfile).readlines()))


def s2m_lines(lines):
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
        line = re.sub(r"\[[^\]]*\]", lambda x:bracket_proc(x.group()), line)

        # hashtag
        line = re.sub(r"#[^#\s]+\s", lambda x:hashtag_proc(x.group()), line)

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
        
