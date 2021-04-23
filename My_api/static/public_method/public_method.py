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


def new_token(user):
    times = (datetime.datetime.now() + datetime.timedelta(hours=2)).strftime('%Y-%m-%d %H:%M:%S')
    test_str = user + ";" + times
    # 编码
    encode_str = base64.encodebytes(test_str.encode('utf8'))
    token = encode_str.decode().split('\n')[0]
    return token


def decode_user(word):
    test_str = bytes(word, encoding='utf-8')
    decode_str = base64.decodebytes(test_str)
    strings = str(decode_str, encoding='utf-8').split(';')[0]
    return strings


def decode_time(word):
    test_str = bytes(word, encoding='utf-8')
    decode_str = base64.decodebytes(test_str)
    strings = str(decode_str, encoding='utf-8').split(';')[1]
    print(strings)
    return compare_time(strings)


def compare_time(time2):
    curr_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    s_time = time.mktime(time.strptime(curr_time, "%Y-%m-%d %H:%M:%S"))
    e_time = time.mktime(time.strptime(time2, "%Y-%m-%d %H:%M:%S"))
    difference = int(e_time) - int(s_time)
    print(curr_time, difference)
    if difference > 0:
        return True
    else:
        return False


print(decode_time('YWRtaW47MjAyMS0wNC0yMiAxOToxNToyNg=='))
