"""
_*_ coding: UTF-8 _*_
@Time      : 2021/4/13 19:39
@Author    : LiuXiaoQiang
@Site      : https://github.com/qq183727918
@File      : ccc.py
@Software  : PyCharm
"""
import codecs
import csv

data = [{'key0: AU', 'key1: eaby', 'key2: KU'},
               {'key0: AU', 'key1: Amazon', 'key2: SPU'},
               {'key0: AU', 'key1: Amazon', 'key2: 平台ID '},
               {'key0: AU', 'key1: eaby', 'key2: 平台ID '},
               {'key0: AU', 'key1: eaby', 'key2: SPU'},
               {'key0: AU', 'key1: Amazon', 'key2: SKU'}]
f = codecs.open('./222.csv', 'w', 'gbk')
writer = csv.writer(f)
for i in data:
    writer.writerow(i)
f.close()
