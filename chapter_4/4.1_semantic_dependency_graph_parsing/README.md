# 句法分析（Syntactic Parsing）
句法分析是NLP关键技术，非最终目标
## 基本任务
确定句子的 **句法结构（syntactic structure）** 或句子中词汇之间的依存关系。包括两种：
- 句法结构分析 syntactic structure parsing
- 依存关系分析 dependency parsing
### 句法结构分析
又称为 **成分结构分析（constituent structure parsi）** 或 **短语结构分析（phrase structure parsi）**

句法结构分析是对输入的单词序列（一般为句子）判断其结构是否合乎给定的语法，分析出合乎语法的句子的句法结构。

通常用树状数据结构表示，称为句法分析树（syntactic parsing tree），简称分析树（parsing tree）

完成这种分析过程的程序模块称为句法分析器（syntactic parser），简称分析器（parser）

- 以获取整个句子的句法结构为目的的句法分析称为 **完全句法分析（full syntactic parsing）** 或者 **完全短语结构分析（full phrase structure parsing）**，简称 **full parsing**
- 以获取局部成分，如基本名词短语（base NP）为目的的句法分析称为 **局部分析（particle parsing）** 或 **浅层分析（shallow parsing）**

#### 任务
1. 判断输入的字符串是否属于某种语言
2. 消除输入句子中此法和结构等方面的歧义
3. 分析输入句子的内部结构，如成分构成、上下文关系等

如果一个句子有多种结构表示，parser应该分析出最有可能的那种结构。实际应用中，一般不用考虑任务1，着重考虑任务2和3

#### 构建parser的重点
1. 语法的形式化表示和词条信息描述（构建parser知识库）
    - 构建语法规则库
    - 构建词典或词表
    
     语法形式化方法：
    - 上下文无关文法（CFG）
    - 基于约束的文法（constraint-based grammar）
2. 分析算法的设计

### 依存关系分析

又称为依存句法分析或者依存结构分析，简称依存分析