# -*- encoding:utf-8 -*-
# author: unclejimao

# jieba内置TextRank算法代码解读

import sys
from __future__ import absolute_import, unicode_literals
from operator import itemgetter
from collections import defaultdict
import jieba.posseg
from .tfidf import KeywordExtractor
from .._compat import *


class UndirectWeightGraph:
    '''
    定义无向有权图类，包含一个graph属性和两个方法：
    addEdge（）：添加边方法
    rank（）：rank值计算方法
    '''
    d = 0.85  # TextRank算法公式中的阻尼系数，是一个超参数， 0.85 是经验值

    def __init__(self):
        '''
        无向有权图类的graph属性，本质是一个dict，value默认类型是list[]
        '''
        self.graph = defaultdict(list)

    def addEdge(self, start, end, weight):
        '''
        增加边的方法。由于是无向图，故一条边的始端和末端可以轮流做起始点，因此轮流将始端和末端作为起始点加入graph
        :param start: 边的始端
        :param end: 边的末端
        :param weight:
        :return:
        '''
        self.graph[start].append((start, end, weight))
        self.graph[end].append((start, end, weight))
        '''
        graph本质是一个dict，value值类型默认为list[]
        即 graph={key:[]}
        例如依次执行下列语句：
        
            addEdge('a','b',0.1)
            addEdge('a','c',0.2)
            addEdge('d','a',0.3)
            
        则得到的结果为：
        
        graph={
            'a':[('a','b',0.1),('a','c',0.2),('a','d',0.3)],
            'b':[('b','a',0.1)],
            'c':[('c','a',0.2)],
            'd':[('d','a',0.3)]
        }
        '''

    def rank(self):
        ws = defaultdict(float)  # 结点权重dict：key为各个结点，valve为各个结点rank值
        outSum = defaultdict(float)  # 结点出边权重之和dict：key为各个结点，value为每个结点出边权重之和

        wsdef = 1.0 / (len(self.graph) or 1.0)  # 初始化各个结点rank值均为 图中边数分之一

        for n, out in self.graph.items():  # 遍历图中的结点，初始化各结点rank值和出边权重和
            ws[n] = wsdef
            outSum[n] = sum((e[2] for e in out), 0.0)
        '''
        经过for循环后，得到了两个dict，其中ws包含了各个结点及其rank值，outSum包含了各个结点及其出边权重之和
        对于上述例子中的graph：
        ws={
            'a':0.25,
            'b':0.25,
            'c':0.25,
            'd':0.25
        }
        outSum={
            'a':0.6,
            'b':0.1,
            'c':0.2,
            'd':0.3
        }
        '''

        # this line for build stable iteration
        sorted_keys = sorted(self.graph.keys())  # 取出graph中的key（即结点）并排好序
        for x in range(10):  # 遍历10次
            for n in sorted_keys:  # 对于每一个结点，根据TextRank算法公式计算其rank值
                s = 0
                for e in self.graph[
                    n]:  # self.graph[n]的value是一个list，里面存了结点n的所有出边。公式中是计算结点n所有入边对结点权值贡献的加和，由于是无向图，入边就是出边，所以此处没有问题。
                    s += e[2] / outSum[e[1]] * ws[e[1]]  # 此处+=计算的就是公式中最外层的加和符号（计算结点n所有入边的权值贡献）
                ws[n] = (1 - self.d) + self.d * s  # 最后根据公式计算得到结点n的rank值

        (min_rank, max_rank) = (sys.float_info[0], sys.float_info[3])

        for w in itervalues(ws):  # 获取最小和最大rank值
            if w < min_rank:
                min_rank = w
            if w > max_rank:
                max_rank = w

        for n, w in ws.items():  # ws.items()的key和value分别赋给n,w
            ws[n] = (w - min_rank / 10) / (max_rank - min_rank / 10)  # 对每个结点的rank值进行归一化处理

        return ws
