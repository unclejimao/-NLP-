# -*-encoding=utf-8-*-
from stanfordcorenlp import StanfordCoreNLP
import time

t_start = time.time()

nlp = StanfordCoreNLP(r'D:\Users\HY\stanfordnlp', lang='zh')

fin = open('news.txt', 'r', encoding='utf8')
fner = open('ner.txt', 'w', encoding='utf8')
ftag = open('pos_tag.txt', 'w', encoding='utf8')
for line in fin:
    line = line.strip()  # 去掉每行之后的换行符
    if len(line) < 1:  # 如果是空行则丢弃
        continue

    # ner==named entity recognize, 即命名实体识别
    fner.write(" ".join([each[0] + "/" + each[1] for each in nlp.ner(line) if len(each) == 2]) + "\n")
    ftag.write(" ".join([each[0] + "/" + each[1] for each in nlp.pos_tag(line) if len(each) == 2]) + "\n")
fner.close()
ftag.close()
t_end = time.time()
print("程序运行时间共 %.2f s" % (t_end - t_start))
