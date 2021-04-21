"""
_*_ coding: UTF-8 _*_
@Time      : 2021/4/13 19:39
@Author    : LiuXiaoQiang
@Site      : https://github.com/qq183727918
@File      : ccc.py
@Software  : PyCharm
"""
import re

a = '{{token}}'

s = re.findall("{{(.*?)}}", a)
if s:
    print(s[0])
