"""
_*_ coding: UTF-8 _*_
@Time      : 2021/4/30 11:33
@Author    : LiuXiaoQiang
@Site      : https://github.com/qq183727918
@File      : httprunner_file.py
@Software  : PyCharm
"""
import json
import os
import time

import yaml


def RunnerFileJson(file_name):
    file_path = f"..\\platform\\My_api\\static\\httprunner\\testcases\\{file_name}.har"
    # 解压成json文件
    os.system(f"har2case {file_path}")
    time.sleep(1.5)

    # 读取json文件
    files = f"..\\platform\\My_api\\static\\httprunner\\testcases\\{file_name}.json"
    with open(files, 'r', encoding="utf-8")as f:
        json_body = json.load(f)
    return json_body


def RunnerFileYml(file_name):
    file_path = f"..\\platform\\My_api\\static\\httprunner\\testcases\\{file_name}.har"
    # 解压成yml文件
    os.system(f"har2case {file_path} --to-yml")
    time.sleep(1.5)
    # 读取yml文件
    files = f"..\\platform\\My_api\\static\\httprunner\\testcases\\{file_name}.yml"
    with open(files, 'r', encoding="utf-8")as f:
        yml_body = yaml.safe_load(f)
    return yml_body


def RunApiFileYml(file_name):
    os.system(
        f"hrun ..\\platform\\My_api\\static\\httprunner\\testcases\\{file_name}.yml  --log-level info --html-report-name {file_name}")


def RunApiFileJson(file_name):
    os.system(
        f"hrun ..\\platform\\My_api\\static\\httprunner\\testcases\\{file_name}.json --log-level info --html-report-name {file_name}")


def RunApiFiles():
    os.system(f"hrun ..\\platform\\My_api\\static\\httprunner\\testcases")
