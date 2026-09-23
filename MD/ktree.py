# キーワードのおきかえはうまい方法がなさそう。treeを作っておいて、一文字ずつマッチさせるしかないのかもしれない。

def tree_add(tree, word):
    if word == "":
        # terminator
        tree[""] = None
        return
    letter = word[0]
    if letter not in tree:
        tree[letter] = dict()
    tree_add(tree[letter], word[1:])


def keyword_tree(keywords):
    tree = dict()
    for word in keywords:
        tree_add(tree, word)
    return tree


def keyword_find(word, ktree):
    """
    1文字目から照合し、何文字目まで一致したかを返す。
    途中までしか伸びない長い語があっても、最後に完成した語の長さを返す（最長一致）。
    """
    node = ktree
    last = None
    i = 0
    n = len(word)
    while i < n and word[i] in node:
        node = node[word[i]]
        i += 1
        if "" in node:
            last = i
    return last
