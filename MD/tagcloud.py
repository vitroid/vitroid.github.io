#!/usr/bin/env python

from logging import getLogger

logger = getLogger()


def tagcloud(graph, source_pages):
    """
    graph: {word: iterable of referring page titles}
    source_pages: set of titles that have MD/*.md
    """
    logger.info("Update tagcloud.")
    virtual = dict()
    MAX = 0
    for page, refs in graph.items():
        if page in source_pages:
            continue
        N = len(refs)
        if N >= 2:
            virtual[page] = N
            if N > MAX:
                MAX = N

    s = "<div class='tc'>\n"
    if MAX == 0:
        s += "</div>"
        return s

    for tag in sorted(virtual):
        N = virtual[tag]
        fontsize = 80 + 220 * N // MAX
        gray = 0 + 150 * (MAX - N) // MAX
        gray = "#{0:02x}{0:02x}{0:02x}".format(gray)
        s += "<span class='tag' style='font-size:{0}%;' ><a href='{2}' style='color:{1};'>{2}</a></span>\n".format(
            fontsize, gray, tag
        )

    s += "</div>"
    return s
