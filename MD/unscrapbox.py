#!/usr/bin/env python

import json
import sys
import re
with open(sys.argv[1]) as file:
    scrapbox=json.load(file)
    for page in scrapbox["pages"]:
        title = page["title"].replace("/", "_")
        with open(title + ".sb", "w") as outfile:
            outfile.write("\n".join(page["lines"]) + "\n")

