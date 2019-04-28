# -*- encoding:utf-8 -*-
# author: unclejimao

import nltk, json
from .tools import ner_stanford, cut_stanford


def get_stanford_ner_nodes(parent):
    '''
    该函数对传入的语法树对象进行分析，取出标签为DATE/ORGANIZATION/LOCATION的子树（词块），并将每个子树下面的内容以空格' '拼接
    :param parent: nltk.Tree对象
    :return: 返回的是一个dict，键为预定义的标签类型，值为从词块中取出的所需标签的词（拼接后）
    '''
    date = ''
    # num = ''
    org = ''
    loc = ''
    for node in parent:
        if type(node) is nltk.Tree:
            if node.label() == 'DATE':  # 如果子树标签为DATE，则将该子树下的词取出来用空格拼接
                date = date + ' ' + ''.join([i[0] for i in node])
            # elif node.label() == 'NUMBER':
            #num = num + ' ' + ''.join([i[0] for i in node])
            elif node.label() == 'ORGANIZATION':
                org = org + ' ' + ''.join([i[0] for i in node])
            elif node.label() == 'LOCATION':
                loc = loc + ' ' + ''.join([i[0] for i in node])
    if len(date) > 0 or len(org) > 0 or len(loc) > 0:  # 如果子树中存在所需要的标签类型的词语，则将其存入dict并返回，否则返回一个空dict
        return {'date': date, 'org': org, 'loc': loc}
    else:
        return {}


def grammar_parse(raw_sentence=None, file_object=None):
    # assert grammar_type in set(['hanlp_keep','stanford_ner_drop','stanford_pos_drop'])
    if len(raw_sentence.strip()) < 1:  # 如果句子长度太短，默认没有我们需要识别的内容
        return False
    # 下面的dict的value是分块语法规则
    grammar_dict = \
        {
            'stanford_ner_drop': r"""
            DATE:{<DATE>+<MISC>?<DATE>*<O>{2}}
            {<DATE>+<MISC>?<DATE>*}
            {<DATE>+}
            {<TIME>+}
            ORGANIZATION:{<ORGANIZATION>+}
            LOCATION:{<LOCATION|STATE_OR_PROVRNCE|CITY|COUNTRY>+}
            """
        }

    stanford_ner_drop_rp = nltk.RegexpParser(grammar_dict['stanford_ner_drop'])  # 返回正则表达式分块器
    try:
        stanford_ner_drop_result = stanford_ner_drop_rp.parse(ner_stanford(raw_sentence))  # 对已添加命名实体标签的句子进行分块，返回一个树对象
    except:
        print("The error sentence is {}".format(raw_sentence))  # 出现异常则抛出有异常的句子
    else:

        stanford_keep_drop_dict = get_stanford_ner_nodes(
            stanford_ner_drop_result)  #遍历得到的语法树，将标签为DATE/ORGANIZATION/LOCATION的子树下的内容拼接，生成dict
        if len(stanford_keep_drop_dict) > 0:
            file_object.write(json.dumps(stanford_keep_drop_dict, skipkeys=False,
                                         ensure_ascii=False,
                                         check_circular=True,
                                         allow_nan=True,
                                         cls=None,
                                         indent=4,
                                         separators=None,
                                         default=None,
                                         sort_keys=False) + '\n')
