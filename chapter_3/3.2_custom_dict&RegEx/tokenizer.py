# encoding=utf8
import os, gc, re, sys

from jpype import *

# 启动JVM，Linux需替换分号;为冒号:
root_path = "D:\\Users\HY\hanlp"  # hanlp 文件夹在系统中的路径
djclass_path = "-Djava.class.path=" + root_path + os.sep + "hanlp-1.7.3.jar;" + root_path
startJVM(getDefaultJVMPath(), djclass_path, "-Xms1g", "-Xmx1g")

Tokenizer = JClass('com.hankcs.hanlp.tokenizer.StandardTokenizer')  # 标准分词器

keep_pos = "q,qg,qt,qv,s,t,tg,g,gb,gbc,gc,gg,gm,gp,m,mg,Mg,mq,n,an,vn,ude1,nr,ns,nt,nz,nb,nba,nbc,nbp,nf,ng,nh,nhd,o,nz,nx,ntu,nts,nto,nth,ntch,ntcf,ntcb,ntc,nt,nsf,ns,nrj,nrf,nr2,nr1,nr,nnt,nnd,nn,nmc,nm,nl,nit,nis,nic,ni,nhm,nhd"
keep_pos_nouns = set(keep_pos.split(","))
keep_pos_v = "v,vd,vg,vf,vl,vshi,vyou,vx,vi"
keep_pos_v = set(keep_pos_v.split(","))
keep_pos_p = set(['p', 'pbei', 'pba'])

drop_pos_set = set(
    ['xu', 'xx', 'y', 'yg', 'wh', 'wky', 'wkz', 'wp', 'ws', 'wyy', 'wyz', 'wb', 'u', 'ud', 'ude1', 'ude2', 'ude3',
     'udeng', 'udh', 'p', 'rr', 'w'])
han_pattern = re.compile(r'[^\dA-Za-z\u3007\u4E00-\u9FCB\uE815-\uE864]+')
HanLP = JClass('com.hankcs.hanlp.HanLP')


def to_string(sentence, return_generator=False):
    if return_generator:
        return (word_pos_item.toString().split('/') for word_pos_item in Tokenizer.segment(sentence))  # 将分词结果作为生成器返回
    else:
        return " ".join([word_pos_item.toString().split('/')[0] for word_pos_item in Tokenizer.segment(sentence)])
        # 将分词结果拼接成以“ ”分开的词串，string格式，不包含词性标注
        # 这里的“”.split('/')可以将string拆分成list 如：'Python/nx'.split('/') => ['Python', 'nx']


def seg_sentences(sentence, with_filter=True, return_generator=False):
    segs = to_string(sentence, return_generator=return_generator)
    if with_filter:
        g = [word_pos_pair[0] for word_pos_pair in segs if
             len(word_pos_pair) == 2 and word_pos_pair[0] != ' ' and word_pos_pair[1] not in drop_pos_set]
    else:
        g = [word_pos_pair[0] for word_pos_pair in segs if len(word_pos_pair) == 2 and word_pos_pair[0] != ' ']
    return iter(g) if return_generator else g


def cut_hanlp(raw_sentence, return_list=True):
    if len(raw_sentence.strip()) > 0:
        return to_string(raw_sentence) if return_list else iter(to_string(raw_sentence))
