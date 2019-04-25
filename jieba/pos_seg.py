# encoding=utf-8
import jieba
import jieba.posseg as pseg

string = "4月24日，期待已久的《复仇者联盟4》终于在各大院线上映跟观众见面"
print(string)
words = pseg.cut(string)
print("\n标注返回结果的数据类型: ", type(words))
print("\njieba词性标注结果：")
for word, flag in words:
    print('%s %s' % (word, flag), )
