"""
_*_ coding: UTF-8 _*_
@Time      : 2021/5/6 16:47
@Author    : LiuXiaoQiang
@Site      : https://github.com/qq183727918
@File      : views_selenium.py
@Software  : PyCharm
"""
import codecs
import csv
import logging
import re

import requests
from allpairspy import AllPairs
from django.core.paginator import Paginator
from django.forms import forms
from django.http import HttpResponse
# Create your views here.
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from icecream import ic

from My_api.models import *
from My_api.static.params.return_params import RE
# Create your views here.
from My_api.static.public_method.public_method import decode_user, decode_time, new_token
# from My_api.static.selenium_file.test import run
from config.httprunner_file import *

logger = logging.getLogger('log')


# 公共方法
def community(request, method):
    if request.method == method:
        try:
            if "Authorization" in request.headers:
                Authorization = request.headers['Authorization']
                try:
                    if decode_time(Authorization):
                        return RE.TRUE.value
                except Exception as e:
                    logger.error('请求出错：{}'.format(e))
                    res = HttpResponse(json.dumps({"code": 403, "data": False, "msg": "token错误"}))
                    res.status_code = 403
                    return res
                else:
                    res = HttpResponse(json.dumps({"code": 402, "data": False, "msg": "token失效"}))
                    res.status_code = 402
                    logger.error('请求出错：{}'.format(res))
                    return res
            else:
                res = HttpResponse(json.dumps({"code": 401, "data": False, "msg": "token为空"}))
                res.status_code = 401
                logger.error('请求出错：{}'.format(res))
                return res
        except Exception as e:
            logger.error('错误信息：{}'.format(e))
            dic = {
                "code": 30010,
                "data": [],
                "msg": "服务不可用，请联系管理员！",
                "totalCount": 0
            }
            return HttpResponse(json.dumps(dic), content_type=RE.CONTENT_TYPE.value)
    else:
        dic = json.dumps(RE.WRONG_REQUEST.value)
        logger.error('请求出错：{}'.format(dic))
        return HttpResponse(dic, content_type=RE.CONTENT_TYPE.value)


# 测试接口
def TestMethod(request):
    method = "POST"
    if community(request, method) == RE.TRUE.value:
        # run()
        return HttpResponse(json.dumps(RE.SUCCESS.value), content_type=RE.CONTENT_TYPE.value)
    else:
        return community(request, method)
