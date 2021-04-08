"""
_*_ coding: UTF-8 _*_
@Time      : 2021/2/19 11:08
@Author    : LiuXiaoQiang
@Site      : https://github.com/qq183727918
@File      : public_method.py
@Software  : PyCharm
"""
import base64
import datetime
import time


def time_format():
    curr_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    return curr_time


print(time_format())


def new_token(user):
    times = (datetime.datetime.now() + datetime.timedelta(hours=2)).strftime('%Y-%m-%d %H:%M:%S')
    test_str = user + ";" + times
    print(test_str)
    # 编码
    encode_str = base64.encodebytes(test_str.encode('utf8'))
    token = encode_str.decode().split('\n')[0]
    return token


def decode_token(word):
    test_str = bytes(word, encoding='utf-8')
    decode_str = base64.decodebytes(test_str)
    strings = str(decode_str, encoding='utf-8').split(';')[0]
    return strings


print(decode_token('YWRtaW47MjAyMS0wNC0wOCAyMjoyOTowNA=='))
