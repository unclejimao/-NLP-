# TextRank算法解释
## jieba_text_rank.py
该文件详细分析了jieba内置的TextRank算法的代码，具体解读见注释，由于该算法依赖jieba外层文件，故此文件非执行文件，在pycharm中会提示 variable unresolved
## defaultdict类
### dict数据类型
python中的dict是一个重要的数据类型，不同于其他由数字索引的序列，字典是用”键”（key）来索引的。通常表示为dict(key: val, …)，有以下特征：
   - 键可以是任何不可变（immutable）数据类型（不可变数据类型：数字，字符串、元组）（也就是说key不能为列表和字典类型）
   - 每个键必须是唯一的
   - 字典中每一项的顺序是任意的
   
### collections.defaultdict类
defaultdict是Python内建dict类的一个子类，第一个参数为default_factory属性提供初始值，默认为None。它覆盖一个方法并添加一个可写实例变量。它的其他功能与dict相同，但会为一个不存在的键提供默认value值，从而避免KeyError异常。

### 一般的dict类型导致KeyError异常示例
当我们试图访问字典中不存在的键时，会抛出KeyError异常。

    bag = ['apple', 'orange', 'cherry', 'apple','apple', 'cherry', 'blueberry'] 
    count = {} 
    for fruit in bag: 
        count[fruit] += 1 
    
    错误： 
    KeyError: 'apple'
### defaultdict类避免KeyError异常示例
defaultdict接受一个工厂函数作为参数，如下来构造：

    dict =defaultdict( factory_function)

这个factory_function可以是list、set、str等等，作用是当key不存在时，返回的是工厂函数的默认值，比如list对应[ ]，str对应的是空字符串，set对应set( )，int对应0。

示例：

    import collections 
    bag = ['apple', 'orange', 'cherry', 'apple','apple', 'cherry', 'blueberry'] 
    count = collections.defaultdict(int) 
    for fruit in bag: 
        count[fruit] += 1 
    
    输出： 
    defaultdict(<class 'int'>, {'apple': 3, 'orange': 1, 'cherry': 2, 'blueberry': 1})
    
在第一次执行 count[fruit]+=1时，apple并不存在于字典中，defaultdict不抛出KeyError异常，而是给键apple赋予一个int类型的默认值，即0.

### collections.defaultdict类使用函数作为初始化函数参数

    import collections 
    def zero():
        return 0 
    dic = collections.defaultdict(zero) 
    dic['bbb'] 
    print(dic) 
    
    输出： 
    defaultdict(<function zero at 0x000001754EB4B488>, {'bbb': 0})
### dict.items()
以列表返回可遍历的(键, 值) 元组数组，返回对象是数组
### sorted()
Python内置的sorted()函数可以对list进行排序：

    >>> sorted([36, 5, -12, 9, -21])
    [-21, -12, 5, 9, 36]

此外，sorted()函数也是一个高阶函数，它还可以接收一个key函数来实现自定义的排序，例如按绝对值大小排序：

    >>> sorted([36, 5, -12, 9, -21], key=abs)
    [5, 9, -12, -21, 36]

key指定的函数将作用于list的每一个元素上，并根据key函数返回的结果进行排序。对比原始的list和经过key=abs处理过的list：

    list = [36, 5, -12, 9, -21]

    keys = [36, 5,  12, 9,  21]

然后sorted()函数按照keys进行排序，并按照对应关系返回list相应的元素：

> keys排序结果 => [5, 9,  12,  21, 36]
                  |  |    |    |   |
> 最终结果     => [5, 9, -12, -21, 36]

我们再看一个字符串排序的例子：

    >>> sorted(['bob', 'about', 'Zoo', 'Credit'])
    ['Credit', 'Zoo', 'about', 'bob']

默认情况下，对字符串排序，是按照ASCII的大小比较的，由于'Z' < 'a'，结果，大写字母Z会排在小写字母a的前面。

现在，我们提出排序应该忽略大小写，按照字母序排序。要实现这个算法，不必对现有代码大加改动，只要我们能用一个key函数把字符串映射为忽略大小写排序即可。忽略大小写来比较两个字符串，实际上就是先把字符串都变成大写（或者都变成小写），再比较。

这样，我们给sorted传入key函数，即可实现忽略大小写的排序：

    >>> sorted(['bob', 'about', 'Zoo', 'Credit'], key=str.lower)
    ['about', 'bob', 'Credit', 'Zoo']

要进行反向排序，不必改动key函数，可以传入第三个参数reverse=True：

    >>> sorted(['bob', 'about', 'Zoo', 'Credit'], key=str.lower, reverse=True)
    ['Zoo', 'Credit', 'bob', 'about']
