#!/usr/bin/env python

import glob
import os
import scrapbox2md as s2m

for file in glob.glob("*.sb"):
    md = file[:-2] + "md"
    if not os.path.exists(md) or os.path.getmtime(md) < os.path.getmtime(file):
        print(md)
        s2m.scrapbox2md(file, md)

