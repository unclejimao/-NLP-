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
    '''
    使用Stanfordnlp.ner()方法进行命名实体识别
    :param raw_sentence:
    :param return_list:
    :return: 默认返回list，也可以返回生成器
    '''
    if len(raw_sentence.strip()) > 0:
        return stanford_nlp.ner(raw_sentence) if return_list else iter(stanford_nlp.ner(raw_sentence))


def ner_hanlp():  # 本节没有没有使用此函数，故pass掉
    pass


def cut_stanford(raw_sentence, return_list=True):
    '''
    使用Stanfordnlp.pos_tag进行词性标注
    :param raw_sentence:
    :param return_list:
    :return: 默认返回list，也可以返回生成器
    '''
    if len(raw_sentence.strip()) > 0:
        return stanford_nlp.pos_tag(raw_sentence) if return_list else iter(stanford_nlp.pos_tag(raw_sentence))
