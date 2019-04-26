# encoding=utf8
import os

root_path = "D:\\Users\HY\hanlp"  # hanlp 文件夹在系统中的路径
dict_file = open(root_path + os.sep + "data" + os.sep + "dictionary" + os.sep + "custom" + os.sep + "resume_nouns.txt",
                 'r', encoding='utf8')
d = {}

[d.update({line: len(line.split(" ")[0])}) for line in dict_file]
f = sorted(d.items(), key=lambda x: x[1], reverse=True)
dict_file = open(root_path + os.sep + "data" + os.sep + "dictionary" + os.sep + "custom" + os.sep + "resume_nouns1.txt",
                 'w', encoding='utf8')
# 注意上述新用户词典生成后要重新配置hanlp文件夹下的hanlp.properties文件
[dict_file.write(item[0]) for item in f]
dict_file.close()
