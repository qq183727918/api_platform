"""
_*_ coding: UTF-8 _*_
@Time      : 2021/2/19 11:08
@Author    : LiuXiaoQiang
@Site      : https://github.com/qq183727918
@File      : public_method.py
@Software  : PyCharm
"""
import datetime


def time_format():
    curr_time = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
    return f'[{curr_time}]|> '
