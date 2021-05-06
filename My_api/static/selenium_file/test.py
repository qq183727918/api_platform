"""
_*_ coding: UTF-8 _*_
@Time      : 2021/5/6 17:06
@Author    : LiuXiaoQiang
@Site      : https://github.com/qq183727918
@File      : test.py
@Software  : PyCharm
"""
import time
import unittest
from HTMLTestRunner1 import HTMLTestRunner

from selenium import webdriver

# from My_api.static.selenium_file.public_selenium import *


class selenium_test(unittest.TestCase):

    def setUp(self) -> None:
        self.driver = webdriver.Chrome()

    def test(self):

        self.url = "http://www.baidu.com"

        self.driver.maximize_window()

        self.driver.get(self.url)

        # path_id_send('kw', '这只是个测试')

        time.sleep(3)

    def tearDown(self) -> None:
        self.driver.close()


def run():
    import unittest
    import HTMLTestRunner1

    file_path = r'..\\platform\\My_api\\templates\\Reports\\HtmlTest\\htmltesttrunner\\'

    # 自动生成测试套件
    suite = unittest.defaultTestLoader.discover("..\\platform\\My_api\\static\\selenium_file\\", pattern="test.py")

    # 定义测试报告文件对象
    file = open(fr'{file_path}\latest.html', 'wb')

    # 生成运行器
    runner = HTMLTestRunner1.HTMLTestRunner(file, title='TestReport', description='SEM_TestReport')

    # 运行
    runner.run(suite)

    # 关闭文件
    file.close()
