# -*- coding=utf8 -*-
import jieba
import re
from tokenizer import cut_hanlp

jieba.load_userdict("dict.txt")  # jieba加载用户词典


def merge_two_list(a, b):
    c = []
    len_a, len_b = len(a), len(b)
    minlen = min(len_a, len_b)
    for i in range(minlen):
        c.append(a[i])
        c.append(b[i])

    if len_a > len_b:
        for i in range(minlen, len_a):
            c.append(a[i])
    else:
        for i in range(minlen, len_b):
            c.append(b[i])
    return c


if __name__ == "__main__":
    fp = open("text.txt", "r", encoding="utf8")
    fout = open("result_cut.txt", "w", encoding="utf8")
    # regular expression matching用法参考当前路径下的regex.md
    # “？：”非获取匹配，匹配冒号后的内容但不获取匹配结果，不进行存储供以后使用,可以用来提高执行速度。单独的“？”：匹配前面的子表达式零次或一次。
    # 以u或U开头的字符串表示unicode字符串,因为字符串中含有中文，以u开头防止报错
    regex1 = u'(?:[^\u4e00-\u9fa5（）*&……%￥$，,。.@! ！]){1,5}期'  # 非汉字xxx期
    # 前面的一个 r 表示字符串为非转义的原始字符串，让编译器忽略反斜杠，也就是忽略转义字符。
    regex2 = r'(?:[0-9]{1,3}[.]?[0-9]{1,3})%'  # xx.xx%
    p1 = re.compile(regex1)
    p2 = re.compile(regex2)
    for line in fp.readlines():
        result1 = p1.findall(line)  # 返回匹配到的list
        if result1:
            regex_re1 = result1
            line = p1.sub("FLAG1", line)  # 将匹配到的替换成FLAG1
        result2 = p2.findall(line)
        if result2:
            line = p2.sub("FLAG2", line)

        words = jieba.cut(line)  # 结巴分词，返回一个generator object
        result = " ".join(words)  # 结巴分词结果 本身是一个generator object，所以使用 “ ”.join() 拼接起来

        words1 = cut_hanlp(line)  # hanlp分词结果，返回的是str
        if "FLAG1" in result:
            result = result.split("FLAG1")
            result = merge_two_list(result, result1)
            ss = result
            result = "".join(result)  # 本身是个list，我们需要的是str，所以使用 "".join() 拼接起来
        if "FLAG2" in result:
            result = result.split("FLAG2")
            result = merge_two_list(result, result2)
            result = "".join(result)
            # print(result)
        fout.write("jieba:" + result)
        fout.write("hanlp:" + words1)
    fout.close()
