# -*- encoding:utf-8 -*-
# author: unclejimao
import re

from recursionRearch import search
from stanfordParse import parse_sentence, pos


def split_long_sentence_by_pos(text):
    '''
    去除句子中不需要词性的词，剩余词以字符串返回
    :param text:
    :return:
    '''
    del_flag = ['DEC', 'AD', 'DEG', 'DER', 'DEV', 'SP', 'AS', 'ETC', 'SP', 'MSP', 'IJ', 'ON', 'JJ', 'FW', 'LB', 'SB',
                'BA', 'AD', 'PN', 'RB']
    pos_tag = pos(text)
    new_str = ''
    for apos in pos_tag:
        if apos[1] not in del_flag:
            new_str += apos[0]
    return new_str


def extrat_parallel(text):
    parallel_text = []
    pattern = re.compile('[，,][\u4e00-\u9fa5]{2,4}[，,]')
    search_obj = pattern.search(text)
    if search_obj:
        start_start, end = search_obj.span()
        rep = text[start_start:end - 2]
        rep1 = text[start_start:end - 1]
        if '，' in rep1:
            rep1.repalce('，', '、')
        if ',' in rep1:
            rep1.repalce(',', '、')
        text.replace(rep1, text)
        parallel_text.append(rep[1:])
        text_leave = text.replace(rep, '')

        while pattern.search(text_leave):
            start, end = pattern.search(text_leave).span()
            rep = text_leave[start:end - 2]
            rep1 = text[start_start:end - 1]
            if '，' in rep1:
                rep1.repalce('，', '、')
            if ',' in rep1:
                rep1.repalce(',', '、')
            text.replace(rep1, text)
            text_leave = text_leave.replace(rep, '')
            parallel_text.append(rep[1:])

        return parallel_text, text
    else:
        return None, text


def split_long_sentence_by_sep(text):
    segment = []
    if '。' or '.' or '!' or '！' or '?' or '？' or ';' or '；' in text:
        text = re.split(r'[。.!！?？;；]', text)
        for seg in text:
            if seg == '' or seg == ' ':
                continue
            para, seg = extrat_parallel(seg)
            if len(seg) > 19:
                seg = split_long_sentence_by_pos(seg)
                if len(seg) > 19:
                    seg = re.split('[，,]', seg)
                    if isinstance(seg, list) and '' in seg:
                        seg.remove('')
                    if isinstance(seg, list) and ' ' in seg:
                        seg.remove(' ')
            segment.append(seg)
    return segment


def read_data(path):
    return open(path, 'r', encoding='utf8')


def get_np_words(t):
    noun_phrase_list = []
    for tree in t.subtrees(lambda t: t.height() == 3):
        if tree.label() == 'NP' and len(tree.leaves()) > 1:
            noun_phrase = ''.join(tree.leaves())
            noun_phrase_list.append(noun_phrase)
    return noun_phrase_list


def get_n_v_pair(t):
    pass


if __name__ == '__main__':
    with open('dependency.txt', 'w', encoding='utf8') as fout:
        itera = read_data('text.txt')
        for it in itera:
            s = parse_sentence(it)
            res = search(s)
            print(res)
            fout.write(res)
            fout.write('\n')
