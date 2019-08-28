#!/usr/bin/env python

import urllib.request
import sys
import os
import re
from logging import getLogger, basicConfig, INFO, DEBUG




def wiki2md(file, title):
    footnotes = []
    logger = getLogger()
    
    def proc_func(x, storage=""):
        elem = x.split(" ", 1)
        logger.info(elem)
        if elem[0] in ("category", "alias", "redirect"):
            return "#" + " ".join(elem[1:])
        elif elem[0] == "ref":
            linklabel = [x.strip() for x in elem[1].split(",")]
            linklabel.append("")
            return "［{2}］({0}{1})".format(storage, *linklabel) #protected with double-sized char
        elif elem[0] == "ref_image":
            linklabel = [x.strip() for x in elem[1].split(",")]
            linklabel.append("")
            return "！［{2}］({0}{1})".format(storage, *linklabel)
        elif elem[0] in ("thumbnail2",):
            thumb,actual = [x.strip() for x in elem[1].split(",")]
            return "！［！［XXX］({0})］({2}{1})".format(thumb, actual, storage)
        #elif elem[0] == "include":
        #    return "{{% include ../{0} %}}".format(elem[1]+".md")
        elif elem[0] == "publish":
            if len(elem) == 1:
                return ""
            elif elem[1] in ("any",):
                return ""
            else:
                assert False
        elif elem[0] == "fn":
            footnotes.append(" ".join(elem[1:]))
            return "[^{0}]".format(len(footnotes))
        elif elem[0] == "footnote_list":
            s = ""
            for i,footnote in enumerate(footnotes):
                s += "[^{0}]: {1}\n".format(i+1, footnote)
            return s
        elif elem[0] in ("comment", "timestamp", "accessdays", "access", "accomment", "asciicaptchacomment", "actives", "attach", "buglist", "bugstate", "bugtrack", "calendar", "category_list", "datetime", "files", "edit", "history", "lastedit", "outline", "pagelinkref", "palmbasket", "recall", "recentcalendar", "recentdays", "rss", "search", "todayslink", "todoadd", "todolist", "trackback", "thumbnail"):
            return ""
        elif elem[0] == "youtube":
            # interwikiname-like
            return "[youtube:{0}]".format(elem[1])
        elif elem[0] == "amazon":
            # interwikiname-like
            return "[amazon:{0}]".format(elem[1])
        else:
            logger.error("Unknown func: {0}".format(x))
            return x
        # include

        
    def proc_head(line, env):
        s = ""
        
        def terminate(lastenv, newenv):
            if lastenv == newenv:
                return ""
            ss = ""
            if lastenv == "dl":
                ss += "</dl>\n"
            elif lastenv == "code":
                ss += "```\n"
            if newenv == "dl":
                ss += "<dl>\n"
            elif newenv == "code":
                ss += "```\n"
            return ss

        if len(line) == 0:
            return s, env
        if line[0] == ":":
            # dd
            dt,dd = line[1:].split(":",1)
            s += terminate(env, "dl")
            env = "dl"
            if dt == "":
                dt, dd = dd, ""
            s += "  <dt>{0}</dt><dd>{1}</dd>\n".format(dt,dd)
        else:
            if line[0] == " ":
                # code block
                s += terminate(env, "code")
                env = "code"
                s += line[1:]
            elif line[0] == ",":
                # table
                s += terminate(env, "table")
                if env == "tablehead":
                    env = "table"
                elif env != "table":
                    env = "tablehead"
                c = line.count(",")
                p = re.sub(r",", "|", line)
                s += p.replace("\n", " |\n")
                if env == "tablehead":
                    s += "|-----" * c + "|\n"
            else:
                s += terminate(env, "normal")
                env = "normal"
                if line[0] == "!":
                    # heading
                    h = 0
                    while line[h] == '!':
                        h += 1
                    s += "\n" + "#" * (4-h) + " " + line[h:] + "\n"
                elif line[0] == "*":
                    # ul
                    h = 0
                    while line[h] == '*':
                        h += 1
                    s += " " * (h*3-3) + "* " + line[h:]
                elif line[0] == "+":
                    # ol
                    h = 0
                    while line[h] == '+':
                        h += 1
                    s += "  " * (h-1) + "1. " + line[h:]
                elif len(line)>=2  and line[0:2] == '""':
                    s += "> " + line[2:]
                elif len(line)>=2  and line[0:2] == '//':
                    s += "<!-- " + line[2:][:-1] + " -->\n"
                else:
                    s += line + "\n"
                # , ---- // 
        return s, env

    def proc_span(line, env):

        def proc_link(x):
            a, b = x.group(1), x.group(2)
            internal = False
            if a[0] == "[":
                logger.info("Double kakko <<{0}>> <<{1}>>".format(a,b))
                a = a[1:]
                internal = ":" not in a
                # InterWikiName is  an external link
            if b == "":
                a, b = a, a
            else:
                b = b[1:] # remove "|"
            if internal:
                return "[{0}](/{1})".format(a,b)
            return "[{0}]({1})".format(a,b)
            
        if env == "code":
            return line
        # strike
        line = re.sub(r"==([^=]+)==", lambda x: "~~{0}~~".format(x.group(1)), line)
        line = re.sub(r"__([^_]+)__", lambda x: "_{0}_".format(x.group(1)), line)
        line = re.sub(r"'''([^']+)'''", lambda x: "**{0}**".format(x.group(1)), line)
        line = re.sub(r"''([^']+)''", lambda x: "*{0}*".format(x.group(1)), line)
        line = re.sub(r"\[([^\]\|]+)(\|[^\]]+|)\]\]*", lambda x: proc_link(x), line)
        return line
        
    env = "normal"
    body = ""
    for line in file:
        #logger.info(line)
        line = re.sub(r'{{([^}]+)}}', lambda x: proc_func(x.group(1), storage="storage:{0}/".format(title)), line)
        #logger.info(line)
        # 行先頭文字の処理
        line, env = proc_head(line, env)
        #logger.info(line)
        # 行中の処理
        line = proc_span(line, env)
        line = line.replace("［","[").replace("］","]").replace("！","!")
        #logger.info(line)
        body += line
    return body


def main():    
    basicConfig(level=INFO)
    wikifile = sys.argv[1]
    assert wikifile[-5:] == ".wiki"
    title = urllib.request.unquote(os.path.basename(wikifile), 'euc-jp')[:-5]
    print(title)
    print(wiki2md(open(wikifile, encoding='euc-jp'), title=title))

if __name__ == "__main__":
    main()
