# -*- encoding:utf-8 -*-
# author: unclejimao

import jieba
import re
from grammar.rules import grammar_parse

with open('text.txt', 'r', encoding='utf8') as fp:
    with open('out.txt', 'w', encoding='utf8') as fout:
        [grammar_parse(line.strip(), fout) for line in fp if len(line.strip()) > 0]

if __name__ == '__main__':
    pass
