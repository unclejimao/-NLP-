# Hanlp简介

HanLP是由一系列模型与算法组成的Java工具包，目标是普及自然语言处理在生产环境中的应用。HanLP具备功能完善、性能高效、架构清晰、语料时新、可自定义的特点。

功能：中文分词 词性标注 命名实体识别 依存句法分析 关键词提取 新词发现 短语提取 自动摘要 文本分类 拼音简繁

Hanlp是Java工具包，在Python环境下使用需要安装Jpype在Python环境中启动Java虚拟机以调用Hanlp的jar包

## Hanlp安装与配置

参考项目地址安装方法 https://github.com/hankcs/HanLP

# Jpype介绍

JPype是一个能够让 python 代码方便地调用 Java 代码的工具，从而克服了 python 在某些领域（如服务器端编程）中的不足。

## Jpype安装与测试
• 1、安装Java:我装的是Java 1.8

• 2、安裝Jpype,

> conda install -c conda-forge jpype1
  [或者]
>pip install jpype1

• 3、测试是否按照成功:

```
#-*- coding:utf-8 -*-
from jpype import *

startJVM(getDefaultJVMPath(), "-ea")
java.lang.System.out.println("Hello World")
shutdownJVM()
```

### Jpype启动Java虚拟机并调用Hanlp提供的jar包

1.启动JVM虚拟机

JPype 提供的 startJVM() 函数的作用是启动 JAVA 虚拟机，所以在后续的任何 JAVA 代码被调用前，必须先调用此方法启动 JAVA 虚拟机。

1) jpype.startJVM() 的定义:

startJVM(jvm, *args)

2) jpype.startJVM() 的参数
参数 1： jvm, 描述你系统中 jvm.dll 文件所在的路径，如“ C:\Program Files\IBM\Java50\jre\bin\j9vm\jvm.dll ”。
可以通过调用 jpype.getDefaultJVMPath() 得到默认的 JVM 路径。
参数 2： args, 为可选参数，会被 JPype 直接传递给 JVM 作为 Java 虚拟机的启动参数。此处适合所有合法的 JVM 启动参数，例如：
 -agentlib:libname[=options] 
 -classpath classpath 
 -verbose 
 -Xint

2.关闭JVM
当使用完 JVM 后，可以通过 jpype.shutdownJVM() 来关闭 JVM，该函数没有输入参数。当 python 程序退出时，JVM 会自动关闭。

3.引用第三方Java扩展包
python 项目中需要调用第三方的 Java 扩展包，这也是 JPype 的一个重要用途:。

通过在 JVM 启动参数增加：-Djava.class.path=ext_classpath，实现在 python 代码中调用已有的 Java 扩展包。

### 测试
```
#-*- coding:utf-8 -*-
from jpype import *

startJVM(getDefaultJVMPath(), "-Djava.class.path=D:\\Users\HY\hanlp\hanlp-1.7.3.jar;D:\\Users\HY\hanlp",
         "-Xms1g",
         "-Xmx1g")  # 启动JVM，Linux需替换分号;为冒号:

print("=" * 30 + "HanLP分词" + "=" * 30)
HanLP = JClass('com.hankcs.hanlp.HanLP')
# 中文分词
print(HanLP.segment('你好，欢迎在Python中调用HanLP的API'))
print("-" * 70)
```