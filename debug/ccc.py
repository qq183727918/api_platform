"""
_*_ coding: UTF-8 _*_
@Time      : 2021/4/13 19:39
@Author    : LiuXiaoQiang
@Site      : https://github.com/qq183727918
@File      : ccc.py
@Software  : PyCharm
"""
import re

dic = "{'code': 401, 'data': 'true', 'message': 'token为空'}"

pa = re.findall('code(.*?),', dic)
print(pa)
