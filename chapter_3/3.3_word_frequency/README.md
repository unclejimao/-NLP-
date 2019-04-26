# 调整词典中的词频
有时候将词条添加至用户词典中，分词工具仍无法正确切分词语，此时可以通过调整词典中的词频和词条顺序改善。

## jieba.suggest_freq('台中',tune=True)
使用 suggest_freq(segment, tune=True) 可调节单个词语的词频，使其（或不能 tune=False）被分出来。

对于用户词典中的每一个词都调整词频可使用for循环：

    fp=open("dict.txt",'r',encoding='utf8')
    for line in fp:
        line=line.strip()   # 注意一定要去掉每行后面的换行符
        jieba.suggest_freq(line, tune=True)

或者

    [jieba.suggest_freq(line.strip(), tune=True) for line in open("dict.txt",'r',encoding='utf8')]
    
# Hanlp用户词典排序
我们一般希望在切词时遵循最大匹配原则，如

    算法工程师
    期望切分结果：算法工程师/n
    不期望结果：  算法/n 工程师/n

因此在使用用户词典时，我们应该先对用户词典中的词条按照词条长度进行排序（切词时遍历用户词典以先匹配到的词条为准）

## Hanlp用户自定义词典
对于词典，直接加载文本会很慢，所以HanLP对于文本文件做了一些预处理，生成了后缀名为.txt.bin的二进制文件。
这些二进制文件相当于缓存，避免了每次加载去读取多个文件。
通过这种txt和bin结合的方式，HanLP一方面方便用户编辑查看词典，另一方面bin方便加载，这种方式可谓是兼二者之长，设计上堪称典范。
### 建立自定义词典步骤

1. 打开hanlp的data目录data\dictionary\custom，删除所有的.txt.bin文件，这样一来，HanLP下次加载词典时会自动构建.txt.bin，这样一来，你对文本文件所做的更改才会生效。
    - 对于HanLP中的字典，**每次更改之后，都必须重新生成bin才可以**，否则不会生效。
2. 在该路径下添加自己的词典文件例如 mine.txt
3. 更改hanlp.properties配置，在properties文件里的CustomDictionaryPath下面添加mine.txt.

        自定义词典路径，用;隔开多个自定义词典，空格开头表示在同一个目录，使用“文件名 词性”形式则表示这个词典的词性默认是该词性。优先级递减。
        另外data/dictionary/custom/CustomDictionary.txt是个高质量的词库，请不要删除
        CustomDictionaryPath=data/dictionary/custom/mine.txt; CustomDictionary.txt; 现代汉语补充词库.txt; 全国地名大全.txt ns; 人名词典.txt; 机构名词典.txt; 上海地名.txt ns;data/dictionary/person/nrf.txt nrf
     
## sort_dict_by_lenth.py
该程序对已有的用户词典（Hanlp词典格式）按照词条长度排序

- 按行读取用户词典文件
- 以词条内容为key、词条长度为value构造Python dict{}
- dict{}按value逆向排序
- 提取排序后的dict{}的key写入文件，形成新的排好序的用户词典
