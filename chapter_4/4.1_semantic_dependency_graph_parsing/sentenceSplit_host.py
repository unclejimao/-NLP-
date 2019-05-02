# -*- encoding:utf-8 -*-
# author: unclejimao

from recursionRearch import search
from stanfordParse import parse_sentence


def split_long_sentence_by_pos(text):
    pass


def extrat_parallel(text):
    pass


def split_long_sentence_by_sep(text):
    pass


def read_data(path):
    return open(path, 'r', encoding='utf8')


def get_np_words(t):
    pass


def get_n_v_pair(t):
    pass


if __name__ == '__main__':
    with open('dependency.txt', 'w', encoding='utf8') as fout:
        itera = read_data('text.txt')
        for it in itera:
            s = parse_sentence(it)
            res = search(s)
            print(res)
