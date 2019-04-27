# 本节说明
本节讲解了jieba分词加载用户词典的方法和在用户词典仍无法很好的分词的情况下使用正则匹配对文本进行补充处理的方法。

比如：特殊符号和汉字组成的词语不应该被切分的情况、百分数不应该被切分等。
## cut_data.py
分词主程序，程序分别使用jieba和Hanlp对text.txt中的文本进行分词，并将输出结果写入result_cut.txt
## dict.txt
jieba分词用户词典
## tokenizer.py
Hanlp分词结果处理程序，将原本Hanlp分词结果（一个<class 'jpype._jclass.java.util.ArrayList'>对象）转换成str

**注意:**

chapter_3中所有需要

     from tokenizer import *
的地方都是从本文件import的，故不再将本文件copy至每个小节文件夹下。
## regex.md
正则匹配相关参考资料以及对主程序中所用到的正则匹配的解释。