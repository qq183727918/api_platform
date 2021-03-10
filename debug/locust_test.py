"""
_*_ coding: UTF-8 _*_
@Time      : 2021/3/10 15:07
@Author    : LiuXiaoQiang
@Site      : https://github.com/qq183727918
@File      : locust_test.py
@Software  : PyCharm
"""
import logging

from locust import HttpUser, TaskSet, task

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


# 定义用户行为类
class UserBehavior(TaskSet):
    @task  # 任务项
    def test_login(self):
        url = ''
        data = {
            "username": "admin",
            "password": "admin"
        }
        res = self.client.post(url, json=data)
        if res.status_code == 200:
            logger.info(f'接口调用成功！结果为：{res.json()}')
        else:
            logger.error('接口调用失败！')


class WebSiteUser(HttpUser):
    tasks = [UserBehavior]
    max_wait = 5000
    min_wait = 1000


if __name__ == '__main__':
    import os

    os.system('locust -f ../debug/locust_test.py')
