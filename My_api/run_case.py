"""
_*_ coding: UTF-8 _*_
@Time      : 2021/3/1 8:44
@Author    : LiuXiaoQiang
@Site      : https://github.com/qq183727918
@File      : run_case.py
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

path = "../api_platform"
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
        get_path = step.get_path
        get_zz = step.get_zz
        assert_zz = step.assert_zz
        assert_qz = step.assert_qz
        assert_path = step.assert_path
        mock_res = step.mock_res

        ts_project_headers = step.public_header.split(',')  # 公共请求头
        if mock_res not in ['', None, 'None']:
            res = mock_res
        else:
            ## 检查是否需要进行替换占位符的
            rlist_url = re.findall(r"##(.*?)##", api_url)
            for i in rlist_url:
                api_url = api_url.replace("##" + i + "##", str(eval(i)))

            rlist_header = re.findall(r"##(.*?)##", api_header)
            for i in rlist_header:
                api_header = api_header.replace("##" + i + "##", repr(str(eval(i))))

            if api_body_method == 'none':
                pass
            elif api_body_method == 'form-data' or api_body_method == 'x-www-form-urlencoded':
                rlist_body = re.findall(r"##(.*?)##", api_body)
                for i in rlist_body:
                    api_body = api_body.replace("##" + i + "##", str(eval(i)))

            elif api_body_method == 'Json':
                rlist_body = re.findall(r"##(.*?)##", api_body)
                for i in rlist_body:
                    api_body = api_body.replace("##" + i + "##", repr(eval(i)))

            else:
                rlist_body = re.findall(r"##(.*?)##", api_body)
                for i in rlist_body:
                    api_body = api_body.replace("##" + i + "##", str(eval(i)))

            ## 实际发送请求
            try:
                header = json.loads(api_header)  # 处理header
            except:
                header = eval(api_header)

            # 在这遍历公共请求头，并把其加入到header的字典中
            for i in ts_project_headers:
                project_header = DB_project_header.objects.filter(id=i)[0]
                header[project_header.key] = project_header.value

            ## 输出请求数据
            print('\n【host】：', api_host)
            print('【url】：', api_url)
            print('【header】：', header)
            print('【method】：', api_method)
            print('【body_method】：', api_body_method)
            print('【body】：', api_body)

            # 拼接完整url
            if api_host[-1] == '/' and api_url[0] == '/':  # 都有/
                url = api_host[:-1] + api_url
            elif api_host[-1] != '/' and api_url[0] != '/':  # 都没有/
                url = api_host + '/' + api_url
            else:  # 肯定有一个有/
                url = api_host + api_url

            if api_body_method == 'none' or api_body_method == 'null':
                response = requests.request(api_method.upper(), url, headers=header, data={})

            elif api_body_method == 'form-data':
                files = []
                payload = {}
                for i in eval(api_body):
                    payload[i[0]] = i[1]
                response = requests.request(api_method.upper(), url, headers=header, data=payload, files=files)

            elif api_body_method == 'x-www-form-urlencoded':
                header['Content-Type'] = 'application/x-www-form-urlencoded'
                payload = {}
                for i in eval(api_body):
                    payload[i[0]] = i[1]
                response = requests.request(api_method.upper(), url, headers=header, data=payload)
            elif api_body_method == 'GraphQL':
                header['Content-Type'] = 'application/json'
                query = api_body.split('*WQRF*')[0]
                graphql = api_body.split('*WQRF*')[1]
                try:
                    eval(graphql)
                except:
                    graphql = {}
                payload = f'{"query":{query},"variables":{graphql}}'

                response = requests.request(api_method.upper(), url, headers=header, data=payload)

            else:  # 这时肯定是raw的五个子选项：
                if api_body_method == 'Text':
                    header['Content-Type'] = 'text/plain'

                if api_body_method == 'JavaScript':
                    header['Content-Type'] = 'text/plain'

                if api_body_method == 'Json':
                    header['Content-Type'] = 'text/plain'

                if api_body_method == 'Html':
                    header['Content-Type'] = 'text/plain'

                if api_body_method == 'Xml':
                    header['Content-Type'] = 'text/plain'
                response = requests.request(api_method.upper(), url, headers=header, data=api_body.encode('utf-8'))

            response.encoding = "utf-8"
            DB_host.objects.update_or_create(host=api_host)
            res = response.text
        print('【返回体】：', res)
        # 对返回值res进行提取：
        # # 路径法提取：
        if get_path != '':  # 说明有设置
            for i in get_path.split('\n'):
                key = i.split('=')[0].rstrip()
                path = i.split('=')[1].lstrip()

                py_path = ""
                for j in path.split('/'):
                    if j != '':
                        if j[0] != '[':
                            py_path += '["%s"]' % j
                        else:
                            py_path += j
                value = eval("%s%s" % (json.loads(res), py_path))
                exec('global %s\n%s = value ' % (key, key))

        # # 正则法提取：
        if get_zz != '':  # 说明有设置
            for i in get_zz.split('\n'):
                key = i.split('=')[0].rstrip()
                zz = i.split('=')[1].lstrip()
                value = re.findall(zz, res)[0]
                exec('global %s\n%s = "%s" ' % (key, key, value))

        # 对返回值res进行断言：
        ## 断言-路径法
        if assert_path != '':  # 说明有设置
            for i in assert_path.split('\n'):
                path = i.split('=')[0].rstrip()
                want = eval(i.split('=')[1].lstrip())
                py_path = ""
                for j in path.split('/'):
                    if j != '':
                        if j[0] != '[':
                            py_path += '["%s"]' % j
                        else:
                            py_path += j
                value = eval("%s%s" % (json.loads(res), py_path))
                self.assertEqual(want, value, '值不等')

        ## 断言-正则
        if assert_zz != '':
            for i in assert_zz.split('\n'):
                zz = i.split('=')[0].rstrip()
                want = i.split('=')[1].lstrip()
                value = re.findall(zz, res)[0]
                self.assertEqual(want, value, '值不等')

        ## 断言-全值
        if assert_qz != '':
            for i in assert_qz.split('\n'):
                if i not in res:
                    raise AssertionError('字符串不存在：%s' % i)


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
    filename = 'My_Api/templates/Reports/%s.html' % Case_id
    fp = open(filename, 'wb')
    runner = HTMLTestRunner(fp, title='接口测试平台测试报告：%s' % Case_name, description='用例描述')
    runner.run(suit)
