# 命名实体识别和信息抽取
本节课程代码处理流程：

1. 使用StanfordCoreNLP.ner()对文本进行命名实体识别，获得带有命名实体标签（比如：LOCATION、DATE、NUMBER、O（代表others，非命名实体））的处理结果
2. 构造分块语法规则
3. 使用nltk.RegexpParser(grammar)解析分块语法，返回一个正则表达式分块器
4. 使用分块器对已经带有命名实体标签的句子（词语列表）进行分块，返回一个nltk.Tree对象
5. 遍历nltk.Tree对象，将根结点下的每个子树（期望获取的label，如：ORGANIZATION、DATE）的结点进行拼接，返回一个dict
6. 如果上一步返回不为空，则使用json.dumps()将dict写入文件

--------------------------------------------------------------------------------

## StanfordCoreNLP.ner()
命名实体识别方法，输出结果为list

     sentence = '合肥工业大学在屯溪路193号，李勇在这里上大学'
     StanfordCoreNLP.ner(sentence)
     
     output：
     [('合肥', 'ORGANIZATION'), ('工业', 'ORGANIZATION'), ('大学', 'ORGANIZATION'), ('在', 'O'), ('屯溪路', 'FACILITY'), ('193', 'FACILITY'), ('号', 'FACILITY'), ('，', 'O'), ('李勇', 'PERSON'), ('在', 'O'), ('这里', 'O'), ('上', 'O'), ('大学', 'O')]


## StanfordCoreNLP.pos_tag()
词性标注方法，输出结果为多个tuple

示例：

     sentence = '合肥工业大学在屯溪路193号，李勇在这里上大学'
     StanfordCoreNLP.pos_tag(sentence)
     
     output：
     ('合肥', 'NR'), ('工业', 'NN'), ('大学', 'NN'), ('在', 'P'), ('屯溪路', 'NR'), ('193', 'OD'), ('号', 'NN'), ('，', 'PU'), ('李勇', 'NR'), ('在', 'P'), ('这里', 'PN'), ('上', 'VV'), ('大学', 'NN')

--------------------------------------------------------------------------------

## nltk.RegexpParser(grammar)
一个句子在分成一个个词后，我们还可以将一个或多个连续的词分成一块。分成的块通常代表一个整体，例如在句子"We saw the yellow dog"中，"the yellow dog"可以看作是一个块，像这样的块我们一般称为名词短语块。分块是用于实体识别的基本技术。

NLTK提供了一个基于词性的正则解析器RegexpParser，可以通过正则表达式匹配特定标记的词块。每条正则表达式由一系列词性标签组成，标签以尖括号为单位用来匹配一个词性对应的词。例如<NN>用于匹配句子中出现的名词，由于名词还有细分的如NNP,NNS等，可以用<NN.*>来表示所有名词的匹配。

RegexpParser通过分析预先定义的分块语法grammar，得到多个语法规则，然后利用parser函数对句子分析，得到语法树。

### RegexpParser 名词短语分块示例
#### 正则表达式分块器
为了创建一个NP-块，我们需要定义NP-块的块语法。正则表达式分块器接受正则表达式规则定义的语法来对文本进行分块，我们先看一个例子：

     import nltk

     # 分词
     text = "the little yellow dog barked at the cat"
     sentence = nltk.word_tokenize(text)

     # 词性标注
     sentence_tag = nltk.pos_tag(sentence)
     print(sentence_tag)

     # 定义分块语法
     # 这个规则是说一个NP块由一个可选的限定词后面跟着任何数目的形容词然后是一个名词组成
     # NP(名词短语块) DT(限定词) JJ(形容词) NN(名词)
     grammar = "NP: {<DT>?<JJ>*<NN>}"

     # 进行分块
     cp = nltk.RegexpParser(grammar)
     tree = cp.parse(sentence_tag)
     tree.draw()

示例中我们先进行分词，词性标注，之后我们定义了一个分块语法"NP: {...}"，该语法中的NP就是代表我们的块名称，一对{}就是把大括号中语法匹配到的词做为一块，使用该语法构造出一个正则表达式分块器就可以对标注词性的文本进行分块，分块结果是一个Tree对象。

该示例的结果为：

     [('the', 'DT'), ('little', 'JJ'), ('yellow', 'JJ'), ('dog', 'NN'), ('barked', 'VBD'), ('at', 'IN'), ('the', 'DT'), ('cat', 'NN')] 

[示例生成Tree对象截图](http://www.coderjie.com/static/img/1487148599085NP.PNG)

从分块结果中我们可以看到"the little yellow dog"和"the cat"都被正确的分块为NP-块。

#### 多条规则的正则表达式分块器

上面的例子只有一条语法规则，如果面对复杂的情况就不太适用，我们可以定义多条分块规则。面对多条规则，分块器会轮流应用分块规则，依次更新块结构，所有的规则都被调用后才返回。我们先看一个示例：

    import nltk

    # 分词
    text = "Lucy let down her long golden hair"
    sentence = nltk.word_tokenize(text)

    # 词性标注
    sentence_tag = nltk.pos_tag(sentence)
    print(sentence_tag)

    # 定义分块语法
    # NNP(专有名词) PRP$(格代名词)
    # 第一条规则匹配可选的词（限定词或格代名词），零个或多个形容词，然后跟一个名词
    # 第二条规则匹配一个或多个专有名词
    # $符号是正则表达式中的一个特殊字符，必须使用转义符号\来匹配PP$
    grammar = r"""
        NP: {<DT|PRP\$>?<JJ>*<NN>}
            {<NNP>+}
    """

    # 进行分块
    cp = nltk.RegexpParser(grammar)
    tree = cp.parse(sentence_tag)
    tree.draw()

该示例的结果为：

    [('Lucy', 'NNP'), ('let', 'VBD'), ('down', 'RP'), ('her', 'PRP$'), ('long', 'JJ'), ('golden', 'JJ'), ('hair', 'NN')] 
    
[示例生成Tree对象截图](http://www.coderjie.com/static/img/1487150169688NP.PNG)

从分块结果可以看到"Lucy"和"her long golden hair"都符合我们的分块预期。
#### 加缝隙

上面两个例子我们都是根据定义的块规则来找到块，反过来想，我们可以定义非块结构的规则，然后把找到的非块给排除掉。以上的过程叫做加缝隙，加缝隙是从一大块中去除一个标识符序列的过程。如果匹配的标识符序列出现在块的中间，这些标识符会被去除，在以前只有一个块的地方留下两个块。如果序列在块的周边，这些标记被去除，留下一个较小的块。我们先看一个例子：

    import nltk
    
    # 分词
    text = "the little yellow dog barked at the cat"
    sentence = nltk.word_tokenize(text)

    # 词性标注
    sentence_tag = nltk.pos_tag(sentence)
    print(sentence_tag)

    # 定义缝隙语法
    # 第一个规则匹配整个句子
    # 第二个规则匹配一个或多个动词或介词
    # 一对}{就代表把其中语法匹配到的词作为缝隙
    grammar = r"""
        NP: {<.*>+}
            }<VBD|IN>+{
    """
    cp = nltk.RegexpParser(grammar)

    # 分块
    tree = cp.parse(sentence_tag)
    tree.draw()

该示例的结果为：

    [('the', 'DT'), ('little', 'JJ'), ('yellow', 'JJ'), ('dog', 'NN'), ('barked', 'VBD'), ('at', 'IN'), ('the', 'DT'), ('cat', 'NN')]
    
[示例生成Tree对象截图](http://www.coderjie.com/static/img/1487148599085NP.PNG) 

该示例的结果结果和第一个例子的结果一致。
### nltk.Tree
- 树继承自列表，树的孩子是以列表的方式进行存储的。
- 树的孩子可以是一个叶子结点或者子树结点，叶子结点没有孩子，子树结点有孩子，子树也是树。
- 树有一个标签属性，可以使用.label()方法进行查看。如下图就是
     
     
     [('the', 'DT'), ('little', 'JJ'), ('yellow', 'JJ'), ('dog', 'NN'), ('barked', 'VBD'), ('at', 'IN'), ('the', 'DT'), ('cat', 'NN')]
    
分块后的树结构： 

![Tree_Image](分块后的树结构.png)

树根的标签为'S'，它有4个孩子，4个孩子以列表的方式存储。树根的孩子0和孩子3是子树，它们的标签是'NP'。树根的孩子1和孩子2是叶子，它们是元组对象。

### nltk.RegexpParser总结

    RegexpParser(grammar)：构造函数，接受分块语法，返回一个正则表达式分块器
    RegexpParser::parse(tokens)：针对标注词性的列表进行分块，返回一个Tree对象
    Tree::draw()：绘制树形结构
    Tree::label()：返回树的标签
    Tree::subtrees()：返回所有的子树，包括子树的子树
    Tree::leaves()：返回所有的叶子，包括子树的叶子
### NLTK词性标注符号含义

|标记|描述|
|:------|:------|
|CC|连接词|
|CD|基数词|
|DT|限定词|
|EX|存在|
|FW|外来词|
|IN|介词或从属连词|
|JJ|形容词或序数词|
|JJR|形容词比较级|
|JJS|形容词最高级|
|LS|列表标示|
|MD|情态助动词|
|NN|常用名词 单数形式|
|NNS|常用名词 复数形式|
|NNP|专有名词 单数形式|
|NNPS|专有名词 复数形式|
|PDT|前位限定词|
|POS|所有格结束词|
|PRP|人称代词|
|PRP$|所有格代名词|
|RB|副词|
|RBR|副词比较级|
|RBS|副词最高级|
|RP|小品词|
|SYM|符号|
|TO|to 作为介词或不定式格式|
|UH|感叹词|
|VB|动词基本形式|
|VBD|动词过去式|
|VBG|动名词和现在分词|
|VBN|过去分词|
|VBP|动词非第三人称单数|
|VBZ|动词第三人称单数|
|WDT|限定词|
|WP|代词|
|WP$|所有格代词|
|WRB|疑问代词|

以上nltk.RegexpParser 相关内容参考自 http://www.coderjie.com/blog/24026f94f7e611e6841d00163e0c0e36

--------------------------------------------------------------------------------

## StanfordNLP各场景下词性标注符号含义
### 1. 词性标注解释

|标记|描述|
|:------|:------|
|CC|conjunction, coordinatin 表示连词|
|CD|numeral, cardinal 表示基数词|
|DT|determiner 表示限定词|
|EX|existential there 存在句|
|FW|foreign word 外来词|
|IN|preposition or conjunction, subordinating 介词或从属连词|
|JJ|adjective or numeral, ordinal 形容词或序数词|
|JJR|adjective, comparative 形容词比较级|
|JJS|adjective, superlative 形容词最高级|
|LS|list item marker 列表标识|
|MD|modal auxiliary 情态助动词|
|NN|noun, common, singular or mass|
|NNS|noun, common, plural|
|NNP|noun, proper, singular|
|NNPS|noun, proper, plural|
|PDT|pre-determiner 前位限定词|
|POS|genitive marker 所有格标记|
|PRP|pronoun, personal 人称代词|
|PRP$|pronoun, possessive 所有格代词|
|RB|adverb 副词|
|RBR|adverb, comparative 副词比较级|
|RBS|adverb, superlative 副词最高级|
|RP|particle 小品词|
|SYM|symbol 符号|
|TO|"to" as preposition or infinitive marker 作为介词或不定式标记|
|UH|interjection 插入语|
|VB|verb, base form|
|VBD|verb, past tense|
|VBG|verb, present participle or gerund|
|VBN|verb, past participle|
|VBP|verb, present tense, not 3rd person singular|
|VBZ|verb, present tense,3rd person singular|
|WDT|WH-determiner WH限定词|
|WP|WH-pronoun WH代词|
|WP$|WH-pronoun, possessive WH所有格代词|
|WRB|Wh-adverb WH副词|

### 2. 句法分析（句法树）标记解释

|标记|描述|
|:------|:------|
|ROOT|要处理文本的语句|
|IP|简单从句|
|NP|名词短语|
|VP|动词短语|
|PU|断句符，通常是句号、问号、感叹号等标点符号|
|LCP|方位词短语|
|PP|介词短语|
|CP|由‘的’构成的表示修饰性关系的短语|
|DNP|由‘的’构成的表示所属关系的短语|
|ADVP|副词短语|
|ADJP|形容词短语|
|DP|限定词短语|
|QP|量词短语|
|NN|常用名词|
|NR|固有名词:表示仅适用于该项事物的名词，含地名，人名，国名，书名，团体名称以及一事件的名称等。|
|NT|时间名词|
|PN|代词|
|VV|动词|
|VC|是|
|CC|表示连词|
|VE|有|
|VA|表语形容词|
|AS|内容标记（如:了）|
|VRD|动补复合词|
|CD|表示基数词|
|DT|determiner 表示限定词|
|EX|existential there 存在句|
|FW|foreign word 外来词|
|IN|preposition or conjunction, subordinating 介词或从属连词|
|JJ|adjective or numeral, ordinal 形容词或序数词|
|JJR|adjective, comparative 形容词比较级|
|JJS|adjective, superlative 形容词最高级|
|LS|list item marker 列表标识|
|MD|modal auxiliary 情态助动词|
|PDT|pre-determiner 前位限定词|
|POS|genitive marker 所有格标记|
|PRP|pronoun, personal 人称代词|
|RB|adverb 副词|
|RBR|adverb, comparative 副词比较级|
|RBS|adverb, superlative 副词最高级|
|RP|particle 小品词|
|SYM|symbol 符号|
|TO|”to” as preposition or infinitive marker 作为介词或不定式标记|
|WDT|WH-determiner WH限定词|
|WP|WH-pronoun WH代词|
|WP$|WH-pronoun, possessive WH所有格代词|
|WRB|Wh-adverb WH副词|

### 3. 关系表示标记解释

|标记|描述|
|:------|:------|
|abbrev|abbreviation modifier，缩写|
|acomp|adjectival complement，形容词的补充；|
|advcl |adverbial clause modifier，状语从句修饰词|
|advmod|adverbial modifier状语|
|agent|agent，代理，一般有by的时候会出现这个|
|amod|adjectival modifier形容词|
|appos|appositional modifier,同位词|
|attr|attributive，属性|
|aux|auxiliary，非主要动词和助词，如BE,HAVE SHOULD/COULD等到|
|auxpass|passive auxiliary 被动词|
|cc|coordination，并列关系，一般取第一个词|
|ccomp|clausal complement从句补充|
|complm|complementizer，引导从句的词好重聚中的主要动词|
|conj |conjunct，连接两个并列的词。|
|cop|copula。系动词（如be,seem,appear等），（命题主词与谓词间的）连系|
|csubj |clausal subject，从主关系|
|csubjpass|clausal passive subject 主从被动关系|
|dep|dependent依赖关系|
|det|determiner决定词，如冠词等|
|dobj |direct object直接宾语|
|expl|expletive，主要是抓取there|
|infmod|infinitival modifier，动词不定式|
|iobj |indirect object，非直接宾语，也就是所以的间接宾语；|
|mark|marker，主要出现在有“that” or “whether”“because”, “when”,|
|mwe|multi-word expression，多个词的表示|
|neg|negation modifier否定词|
|nn|noun compound modifier名词组合形式|
|npadvmod|noun phrase as adverbial modifier名词作状语|
|nsubj |nominal subject，名词主语|
|nsubjpass|passive nominal subject，被动的名词主语|
|num|numeric modifier，数值修饰|
|number|element of compound number，组合数字|
|parataxis|parataxis，并列关系|
|partmod|participial modifier动词形式的修饰|
|pcomp|prepositional complement，介词补充|
|pobj |object of a preposition，介词的宾语|
|poss|possession modifier，所有形式，所有格，所属|
|possessive|possessive modifier，这个表示所有者和那个’S的关系|
|preconj |preconjunct，常常是出现在 “either”, “both”, “neither”的情况下|
|predet|predeterminer，前缀决定，常常是表示所有|
|prep|prepositional modifier|
|prepc|prepositional clausal modifier|
|prt|phrasal verb particle，动词短语|
|punct|punctuation，这个很少见，但是保留下来了，结果当中不会出现这个|
|purpcl |purpose clause modifier，目的从句|
|quantmod|quantifier phrase modifier，数量短语|
|rcmod|relative clause modifier相关关系|
|ref |referent，指示物，指代|
|rel |relative|
|root|root，最重要的词，从它开始，根节点|
|tmod|temporal modifier|
|xcomp|open clausal complement|
|xsubj|controlling subject 掌控者|

--------------------------------------------------------------------------------

## str.format()

Python的一种格式化字符串的函数 str.format()，它增强了字符串格式化的功能。

基本语法是通过 {} 和 : 来代替以前的 % 。

format 函数可以接受不限个参数，位置可以不按顺序。

实例

    >>>"{} {}".format("hello", "world")    # 不设置指定位置，按默认顺序
    'hello world'
 
    >>> "{0} {1}".format("hello", "world")  # 设置指定位置
    'hello world'
 
    >>> "{1} {0} {1}".format("hello", "world")  # 设置指定位置
    'world hello world'
--------------------------------------------------------------------------------

## try...except...else

在执行的程序中，难免会碰到因为一些原因如输入输出导致致命性错误产生的情况（如因为输入的文件名错误而导致无法运行相关的代码。）。此时你不希望程序直接挂掉，而是通过显示一些信息，使其平稳的结束。此时，就可以使用try，except和else这三个关键字来组成一个包容性很好的程序。

>分别解释三个关键字：
>
>try：执行可能会出错的试探性语句，即这里面的语句是可以导致致命性错误使得程序无法继续执行下去
>
>except：如果try里面的语句无法正确执行，那么就执行except里面的语句，这里面可以是错误信息或者其他的可执行语句
>
>else：如果try里面的语句可以正常执行，那么就执行else里面的语句（相当于程序没有碰到致命性错误）

**try...except...else的使用格式**

    try:
        try block
        
    except ERROR1:
        except ERROR1 block
        
    except ERRPR2:
        except ERROR2 block
    
    ......
            
    except:
        except block

    else:
        else block

--------------------------------------------------------------------------------

# json

JSON(JavaScript Object Notation) 是一种轻量级的数据交换格式，易于人阅读和编写。

使用 JSON 函数需要导入 json 库：

    import json

|函数|	描述|
|:------|:------|
|json.dumps 	|将 Python 对象编码成 JSON 字符串|
|json.loads	|将已编码的 JSON 字符串解码为 Python 对象|

## 概念理解

1. json.dumps()和json.loads()是json格式处理函数（可以这么理解，json是字符串）

    - json.dumps()函数是将一个Python数据类型列表进行json格式的编码（可以这么理解，json.dumps()函数是将字典(python数据类型)转化为字符串）
　　

    - json.loads()函数是将json格式数据转换为字典（可以这么理解，json.loads()函数是将字符串转化为字典(python数据类型)）

2. json.dump()和json.load()主要用来读写json文件函数

## 示例
### json.dumps()

    import json

    # json.dumps()函数的使用，将字典转化为字符串
    dict1 = {"age": "12"}
    json_info = json.dumps(dict1)
    print("dict1的类型："+str(type(dict1)))
    print("通过json.dumps()函数处理：")
    print("json_info的类型："+str(type(json_info)))
    
输出结果：

    dict1的类型：<class 'dict'>
    通过json.dumps()函数处理：
    json_info的类型：<class 'str'>
    
### json.loads()

    import json

    # json.loads函数的使用，将字符串转化为字典
    json_info = '{"age": "12"}'
    dict1 = json.loads(json_info)
    print("json_info的类型："+str(type(json_info)))
    print("通过json.dumps()函数处理：")
    print("dict1的类型："+str(type(dict1)))    
    
输出结果：

    json_info的类型：<class 'str'>
    通过json.loads()函数处理：
    dict1的类型：<class 'dict'>
    
### json.dump()

    import json

    # json.dump()函数的使用，将json信息写进文件
    json_info = "{'age': '12'}"
    file = open('1.json','w',encoding='utf-8')
    json.dump(json_info,file)
    
输出结果（1.json文件内容）：

    “{'age': '12'}”
    
### json.load()

    import json

    # json.load()函数的使用，将读取json信息
    file = open('1.json','r',encoding='utf-8')
    info = json.load(file)
    print(info)
    
输出结果：

    {'age': '12'}