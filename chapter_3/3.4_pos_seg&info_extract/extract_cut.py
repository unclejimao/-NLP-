# -*- encoding:utf-8 -*-
# author: unclejimao

import jieba
import re
from tokenizer import seg_sentences  # 使用Hanlp的切分工具

fp = open("text.txt", 'r', encoding='utf8')
fout = open("out.txt", 'w', encoding='utf8')
for line in fp:
    line = line.strip()  # 丢弃行末换行符
    if len(line) > 0:  # 对非空行进行处理
        fout.write(' '.join(seg_sentences(line)) + "\n")
fout.close()
if __name__ == "__main__":
    pass
