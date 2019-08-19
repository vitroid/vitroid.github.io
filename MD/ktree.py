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
    """
    if len(word) == 0:
        if "" in ktree:
            return 0
        return None
    if word[0] in ktree:
        result = keyword_find(word[1:], ktree[word[0]])
        if result is None:
            return None
        else:
            return result+1
    elif "" in ktree:
        return 0
    return None
