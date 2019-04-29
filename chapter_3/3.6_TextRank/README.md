# TextRank算法解释
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
