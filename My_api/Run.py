"""
_*_ coding: UTF-8 _*_
@Time      : 2021/4/20 16:12
@Author    : LiuXiaoQiang
@Site      : https://github.com/qq183727918
@File      : Run.py
@Software  : PyCharm
"""
import json
import os
import re
import sys
import time
import unittest
from HTMLTestRunner1 import HTMLTestRunner

import django
from requests import request

path = "../platform"
sys.path.append(path)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "api_platform.setting")
django.setup()
from My_api.models import *
# from My_api.A_WQRFhtmlRunner import HTMLTestRunner
import requests


class Test(unittest.TestCase):
    """测试类"""
    def demo(self, step):  # 8
        time.sleep(3)
        # 提取所有请求数据
        api_method = step.api_method
        api_url = step.api_url
        api_host = step.api_host
        api_header = step.api_header
        api_body_method = step.api_body_method
        api_body = step.api_body
        url = api_host + api_url
        # 输出请求数据
        print('\n【host】：', api_host)
        print('【url】：', url)
        print('【header】：', api_header)
        print('【method】：', api_method)
        print('【body_method】：', api_body_method)
        print('【body】：', api_body)
        response = request(api_method.upper(), url=url, headers=api_header, data=api_body)

        response.encoding = "utf-8"
        res = response.text

        print('【返回体】：', res)


def make_defself(step):  # 6
    def tool(self):
        Test.demo(self, step)  # 7

    setattr(tool, "__doc__", u"%s" % step.name)
    return tool


def make_def(steps):  # 3
    for i in range(len(steps)):  # 4
        setattr(Test, 'test_' + str(steps[i].index).zfill(3), make_defself(steps[i]))  # 5


def run(Case_id, Case_name, steps):  # 1
    print(steps)
    make_def(steps)  # 2
    suit = unittest.makeSuite(Test)
    filename = 'My_api/templates/Reports/%s.html' % Case_id
    fp = open(filename, 'wb')
    runner = HTMLTestRunner(fp, title='接口测试平台测试报告：%s' % Case_name, description='用例描述')
    runner.run(suit)
