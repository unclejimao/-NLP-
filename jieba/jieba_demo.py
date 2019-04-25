# encoding=utf-8
import jieba

print("\njieba分词全模式：")
seg_list = jieba.cut("我来到北京清华大学", cut_all=True)
print("Full mode: " + "/".join(seg_list))
print("分词后的结果seg_list本质是：", seg_list)
print("seg_list 数据类型：", type(seg_list))  # 分词后返回的是一个生成器而非list，防止数据太大时占用过多内存

print("\njieba分词精确模式（默认模式）：")
seg_list = jieba.cut("我来到北京清华大学", cut_all=False)
print("Default mode: " + "/".join(seg_list))
seg_list = jieba.cut("他来到了网易杭研大厦")  # 默认是精确模式
print("Default mode: " + "/".join(seg_list))
print("seg_list 数据类型：", type(seg_list))

print("\njieba分词搜索引擎模式：")
seg_list = jieba.cut_for_search("小明硕士毕业于中国科学院计算所，后在日本京都大学深造")
print("Search engine mode: " + "，".join(seg_list))
print("分词后的结果seg_list本质是：", seg_list)
print("seg_list 数据类型：", type(seg_list))
