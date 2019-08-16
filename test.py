import re
from logging import getLogger, basicConfig, INFO, DEBUG



line = "test [string] in #hash\n"

def bracket_proc(x):
    logger = getLogger()
    x = x[1:len(x)-1]
    logger.info(x)
    elements = x.split(" ")
    if elements[0][:4] == "http":
        url   = elements[0]
        label = " ".join(elements[1:])
        return "[{0}]({1})".format(label, url)
    elif elements[-1][:4] == "http":
        url   = elements[-1]
        label = " ".join(elements[:-1])
        return "[{0}]({1})".format(label, url)
    elif elements[0] == '*':
        return "## " + " ".join(elements[1:])
    else:
        logger.info("Unknown bracket syntax: {0}".format(x))
        return "[{0}]({0}.md)".format(x)
    
    
def hashtag_proc(x):
    x = x[1:len(x)-1]
    return "[{0}]({0}.md)".format(x)
    
basicConfig(level=INFO)
print(re.sub(r"\[.*\]", lambda x: bracket_proc(x.group()), line))
print(re.sub(r"#.*[\n\t ]", lambda x: hashtag_proc(x.group()), line))
