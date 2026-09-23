#!/usr/bin/env python

# CLI でキーワード照合を試すためだけに残している。
# 被リンクの構築は make.py が毎ビルドで本文からやり直す。

from ktree import keyword_tree, keyword_find
import glob


if __name__ == "__main__":
    keywords = [fn[:-3] for fn in glob.glob("*.md")]
    kwtree = keyword_tree(keywords)
    for word in ("かもめだった", "LDAがいい", "ice T研究のため", "ice T3", "ice T"):
        print(word, keyword_find(word, kwtree))
