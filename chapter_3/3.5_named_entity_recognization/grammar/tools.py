# -*- encoding:utf-8 -*-
# author: unclejimao

import os, gc, re, sys
from itertools import chain
from stanfordcorenlp import StanfordCoreNLP

stanford_nlp = StanfordCoreNLP('D:\\Users\HY\stanfordnlp', lang='zh')


def to_string():  # 本节没有没有使用此函数，故pass掉
    pass


def to_string_hanlp():  # 本节没有没有使用此函数，故pass掉
    pass


def seg_sentences():  # 本节没有没有使用此函数，故pass掉
    pass


def ner_stanford(raw_sentence, return_list=True):
    if len(raw_sentence.strip()) > 0:
        return stanford_nlp.ner(raw_sentence) if return_list else iter(stanford_nlp.ner(raw_sentence))


def ner_hanlp():  # 本节没有没有使用此函数，故pass掉
    pass


def cut_stanford(raw_sentence, return_list=True):
    if len(raw_sentence.strip()) > 0:
        return stanford_nlp.pos_tag(raw_sentence) if return_list else iter(stanford_nlp.pos_tag(raw_sentence))
