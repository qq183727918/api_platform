"""
_*_ coding: UTF-8 _*_
@Time      : 2021/3/10 16:42
@Author    : LiuXiaoQiang
@Site      : https://github.com/qq183727918
@File      : log_setting.py
@Software  : PyCharm
"""


def log_set():
    import logging
    logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s] - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)

    return logger
