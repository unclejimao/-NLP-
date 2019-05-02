# -*- encoding:utf-8 -*-
# author: unclejimao

import nltk


def get_vn_pair():
    pass


def get_noun_chunk(tree):
    noun_chunk = []
    if tree.lable() == "NP":
        nouns_phrase = ''.join(tree.leaves())
        noun_chunk.append(nouns_phrase)
    return noun_chunk


def get_ip_recursion_noun(tree):
    np_list = []

    if len(tree) == 1:
        tr = tree[0]
        get_ip_recursion_noun(tr)

    if len(tree) == 2:
        tr = tree[0]
        get_ip_recursion_noun(tr)
        tr = tree[1]
        get_ip_recursion_noun(tr)

    if len(tree) == 3:
        tr = tree[0]
        get_ip_recursion_noun(tr)
        tr = tree[1]
        get_ip_recursion_noun(tr)
        tr = tree[2]
        get_ip_recursion_noun(tr)

    '''
    这几个if难道不能写成：
    
    for i in range(len(tree)):
        tr=tree[i]
        get_ip_recursion_noun(tr)
    
    这种形式？
    '''

    if tree.label() == 'NP':
        np_list.append(get_noun_chunk(tree))

    return np_list  # 返回的是一个tree对象的列表


def get_vv_loss_np(tree):
    if not isinstance(tree, nltk.tree.Tree):
        return False

    stack = []
    np = []
    stack.append(tree)
    current_tree = ''
    while stack:
        current_tree = stack.pop()
        if isinstance(current_tree, nltk.tree.Tree) and current_tree.label() == 'VP':
            continue
        elif isinstance(current_tree, nltk.tree.Tree) and current_tree.label() != 'NP':
            for i in range(len(current_tree)):
                stack.append(current_tree[i])
        elif isinstance(current_tree, nltk.tree.Tree) and current_tree.label() == 'NP':
            np.append(get_noun_chunk(current_tree))

    if np:
        return np
    else:
        return False


def search(tree_in):
    if not isinstance(tree_in, nltk.tree.Tree):
        return False

    vp_pair = []
    stack = []
    stack.append(tree_in)
    current_tree = ''

    while stack:
        current_tree = stack.pop()
        if isinstance(current_tree, nltk.tree.Tree) and current_tree.label() == 'ROOT':
            for i in range(len(current_tree)):
                stack.append(current_tree[i])
        if isinstance(current_tree, nltk.tree.Tree) and current_tree.label() == 'IP':
            for i in range(len(current_tree)):
                stack.append(current_tree[i])
        if isinstance(current_tree, nltk.tree.Tree) and current_tree.label() == 'VP':
            duplicate = []
            if len(current_tree) >= 2:
                for i in range(1, len(current_tree)):
                    if current_tree[0].label() == 'VV' and current_tree[1].label() == 'NP':
                        verb = ''.join(current_tree[0].leaves())
                        noun = get_noun_chunk(current_tree[i])
                        if verb and noun:
                            vp_pair.append((verb, noun))
                            duplicate.append(noun)
                    elif current_tree[0].label() == 'VV' and current_tree[1].label() != 'NP':
                        noun = get_vv_loss_np(current_tree)
                        verb = ''.join(current_tree[0].leaves())
                        if verb and noun and noun not in duplicate:
                            duplicate.append(noun)
                            vp_pair.append((verb, noun))
    if vp_pair:
        return vp_pair
    else:
        return False

    '''
    if tree.label()=='NP':
        noun_phrase=''.join(tree.leaves())
        noun_chunk.append(noun_phrase)
    '''
