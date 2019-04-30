# TextRank算法解释
## jieba_text_rank.py
该文件详细分析了jieba内置的TextRank算法的代码，具体解读见注释，由于该算法依赖jieba外层文件，故此文件非执行文件，在pycharm中会提示 variable unresolved
## operator.itemgetter函数
operator模块提供的itemgetter函数用于获取对象的哪些维的数据，参数为一些序号。看下面的例子

    a = [1,2,3] 
    >>> b=operator.itemgetter(1)      //定义函数b，获取对象的第1个域的值
    >>> b(a) 

    2

    >>> b=operator.itemgetter(1,0)  //定义函数b，获取对象的第1个域和第0个的值
    >>> b(a) 
    (2, 1)

要注意，operator.itemgetter函数获取的不是值，而是定义了一个函数，通过该函数作用到对象上才能获取值。

sorted函数用来排序，
    
    sorted(iterable[, cmp[, key[, reverse]]])

其中key的参数为一个函数或者lambda函数。所以itemgetter可以用来当key的参数

    a = [('john', 'A', 15), ('jane', 'B', 12), ('dave', 'B', 10)]

根据第二个域和第三个域进行排序

    sorted(students, key=operator.itemgetter(1,2))
    

## from __future__ import unicode_literals
在Python中有些库的接口要求参数必须是str类型字符串，有些接口要求参数必须是unicode类型字符串。

对于str类型的字符串，调用len()和遍历时，其实都是以字节为单位的，这个太坑爹了，同一个字符使用不同的编码格式，长度往往是不同的。

对unicode类型的字符串调用len()和遍历才是以字符为单位，这是我们所要的。

另外，Django，Django REST framework的接口都是返回unicode类型的字符串。

为了统一，建议使用

    from __future__ import unicode_literals

将模块中显式出现的所有字符串转为unicode类型，不过，对于必须使用str字符串的地方要加以注意。

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
## values()和itervalues()
在Python2中，dict 对象有一个 values() 方法，这个方法把dict转换成一个包含所有value的list，这样，我们迭代的就是 dict的每一个 value：

    d = { 'Adam': 95, 'Lisa': 85, 'Bart': 59 }
    print d.values()
    # [85, 95, 59]
    for v in d.values():
        print v
    # 85
    # 95
    # 59
dict除了values()方法外，还有一个 itervalues() 方法，用 itervalues() 方法替代 values() 方法，迭代效果完全一样：

    d = { 'Adam': 95, 'Lisa': 85, 'Bart': 59 }
    print d.itervalues()
    # <dictionary-valueiterator object at 0x106adbb50>
    for v in d.itervalues():
        print v
    # 85
    # 95
    # 59

**两个方法区别：**
1. values() 方法实际上把一个 dict 转换成了包含 value 的list。
2. 但是 itervalues() 方法不会转换，它会在迭代过程中依次从 dict 中取出 value，所以 itervalues() 方法比 values() 方法节省了生成 list 所需的内存。
3. 打印 itervalues() 发现它返回一个 对象，这说明在Python中，for 循环可作用的迭代对象远不止 list，tuple，str，unicode，dict等，任何可迭代对象都可以作用于for循环，而内部如何迭代我们通常并不用关心。 

dict类似的方法对还有 keys()&&iterkeys、items()&&iteritems()

在Python3中，dict.iterkeys(), dict.itervalues(), dict.iteritems()被keys() and values() and items()所替代
，**他们的返回结果类似于集的可迭代对象，而不是键值对的列表。**从而在不进行键和值条目复制的情况下就能对其执行set操作。

## frozenset()
frozenset() 返回一个冻结的集合，冻结后集合不能再添加或删除任何元素。

frozenset() 函数语法：

    class frozenset([iterable])
    iterable – 可迭代的对象，比如列表、字典、元组等等
    返回新的 frozenset 对象，如果不提供任何参数，默认会生成空集合。

**与set()的区别：**
- set无序排序且不重复，是可变的，有add（），remove（）等方法。既然是可变的，所以它不存在哈希值。基本功能包括关系测试和消除重复元素. 集合对象还支持union(联合), intersection(交集),difference(差集)和sysmmetric difference(对称差集)等数学运算。不支持索引、切片等序列操作，但仍支持成员关系运算符in-not in、推导式等操作。

- frozenset是冻结的集合，它是不可变的，存在哈希值，好处是它可以作为字典的key，也可以作为其它集合的元素。缺点是一旦创建便不能更改，没有add，remove方法。
## tuple()
Python 元组 tuple() 函数将列表转换为元组。 

实例:

    >>>tuple([1,2,3,4])
 
    (1, 2, 3, 4)
 
    >>> tuple({1:2,3:4})    #针对字典 会返回字典的key组成的tuple
 
    (1, 3)
 
    >>> tuple((1,2,3,4))    #元组会返回元组自身
 
    (1, 2, 3, 4)
    
tuple() 函数不是改变值的类型，而是返回改变类型后的值，原值不会被改变：

    test_list1 = ('a','b','c')
    test_list2 = ['x','y','z']
    test_tuple = tuple(test_list2)
    # test_list2 可以修改，tuple() 函数不是改变值的类型，而是返回改变类型后的值，原值不会被改变
    test_list2[2] = '这是修改的'
    #下面这行报错，元组不可修改
    # test_list1[2]='这是修改的'
## enumerate()
enumerate() 函数用于将一个可遍历的数据对象(如列表、元组或字符串)组合为一个索引序列，同时列出数据和数据下标，一般用在 for 循环当中。

**语法**

    enumerate(sequence, [start=0])

**参数**

    sequence -- 一个序列、迭代器或其他支持迭代对象。
    start -- 下标起始位置。

**返回值**
>返回 enumerate(枚举) 对象。

**实例：**

    >>>seasons = ['Spring', 'Summer', 'Fall', 'Winter']
    >>>list(enumerate(seasons))
    [(0, 'Spring'), (1, 'Summer'), (2, 'Fall'), (3, 'Winter')]
    >>>list(enumerate(seasons, start=1))       # 小标从 1 开始
    [(1, 'Spring'), (2, 'Summer'), (3, 'Fall'), (4, 'Winter')]

**for 循环使用 enumerate()**

    >>>seq = ['one', 'two', 'three']
    >>>for i, element in enumerate(seq):
    ...    print(i, seq[i])
    ... 
    0 one
    1 two
    2 three
## xrange()和range()
在Python2中，xrange() 函数用法与 range 完全相同，所不同的是生成的不是一个数组，而是一个生成器。

python2中，range的返回值是list，这意味着内存将会分布相应的长度的空间给list。

    >>> a = range(0,100) 
    >>> print a 
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99] 
    >>> print type(a) 
    <type 'list'>
    
而xrange将返回一个生成器对象：

    >>> a = xrange(0,100)
    >>> print type(a)
    <type 'xrange'>
    >>> print a[0]
    0
    >>> list(a)
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99]
    
python3 中取消了 range 函数，而把 xrange 函数重命名为 range，所以现在直接用 range 函数。

python3中range() 返回的是一个对象，并没有将数据完全实例化，所以内存中只有一个对象的空间，对性能优化还是很有帮助的。

    >>> print(sys.version)
    3.5.3 (v3.5.3:1880cb95a742, Jan 16 2017, 16:02:32) [MSC v.1900 64 bit (AMD64)]
    >>> type(range(10))
    <class 'range'> 