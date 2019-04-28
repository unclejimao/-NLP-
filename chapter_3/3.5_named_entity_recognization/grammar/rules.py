# -*- encoding:utf-8 -*-
# author: unclejimao

import nltk, json
from .tools import ner_stanford, cut_stanford


def get_stanford_ner_nodes(parent):
    date = ''
    org = ''
    loc = ''
    for node in parent:
        if type(node) is nltk.Tree:
            if node.label() == 'DATE':
                date = date + ' ' + ''.join([i[0] for i in node])
            elif node.label() == 'ORGANIZATION':
                org = org + ' ' + ''.join([i[0] for i in node])
            elif node.label() == 'LOCATION':
                loc = loc + ' ' + ''.join([i[0] for i in node])
    if len(date) > 0 or len(org) > 0 or len(loc) > 0:
        return {'date': date, 'org': org, 'loc': loc}
    else:
        return {}


def grammar_parse(raw_sentence=None, file_object=None):
    # assert grammar_type in set(['hanlp_keep','stanford_ner_drop','stanford_pos_drop'])
    if len(raw_sentence.strip()) < 1:
        return False
    grammar_dict = \
        {
            'stanford_ner_drop': r"""
            DATE:{<DATE>+<MISC>?<DATE>*<0>{2}}
            {<DATE>+<MISC>?<DATE>*}
            {<DATE>+}
            {<TIME>+}
            ORGANIZATION:{<ORGANIZATION>+}
            LOCATION:{<LOCATION|STATE_OR_PROVRNCE|CITY|COUNTRY>+}
            """
        }

    stanford_ner_drop_rp = nltk.RegexpParser(grammar_dict['stanford_ner_drop'])
    try:
        stanford_ner_drop_result = stanford_ner_drop_rp.parse(ner_stanford(raw_sentence))
    except:
        print("The error sentence is {}".format(raw_sentence))
    else:

        stanford_keep_drop_dict = get_stanford_ner_nodes(stanford_ner_drop_result)
        if len(stanford_keep_drop_dict) > 0:
            file_object.write(json.dumps(stanford_keep_drop_dict, skipkeys=False,
                                         ensure_ascii=False,
                                         check_circular=True,
                                         allow_nan=True,
                                         cls=None,
                                         indent=4,
                                         separators=None,
                                         default=None,
                                         sort_keys=False))
