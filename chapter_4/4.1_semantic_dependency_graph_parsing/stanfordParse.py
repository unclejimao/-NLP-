# -*- encoding:utf-8 -*-
# author: unclejimao

from stanfordcorenlp import StanfordCoreNLP
from nltk import Tree, ProbabilisticTree
import nltk, re
from nltk.chunk.regexp import *

nlp = StanfordCoreNLP(r'D:\Users\HY\stanfordnlp', lang='zh')

grammar = "NP:{<DT>?<JJ>*<NN>}"
cp = nltk.RegexpParser(grammar)
pattern = re.compile(u'[^a-zA-Z\u4E00-\u9FA5]')
pattern_del = re.compile('(\a-zA-Z0-9+)')


def _replace_c(text):
    '''
    把英文标点替换成中文标点，去除HTML语言的一些标志灯噪音
    :param text: 待处理文本
    :return:
    '''
    intab = ',?!()'
    outtab = '，？！（）'
    deltab = '\n<li>< li>+_-.><li \U0010fc01 _'
    trantab = text.maketrans(intab, outtab, deltab)
    return text.translate(trantab)


def parse_sentence(text):
    text = _replace_c(text)  # 文本去噪音
    try:
        if len(text.strip()) > 6:  # 把小于6个字的文本不当做句子处理
            return Tree.formstring(nlp.parse(text.strip()))  # 返回nltk.tree()对象
    except:
        pass


def pos(text):
    text = _replace_c(text)
    if len(text.strip()) > 6:
        return nlp.pos_tag(text)
    else:
        return False


def depency_parse(text):
    return nlp.dependency_parse(text)
