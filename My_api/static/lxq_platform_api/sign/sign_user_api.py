"""
_*_ coding: UTF-8 _*_
@Time      : 2021/3/5 15:46
@Author    : LiuXiaoQiang
@Site      : https://github.com/qq183727918
@File      : sign_user_api.py
@Software  : PyCharm
"""
import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from icecream import ic

from My_api.static.lxq_automate_service.login.login import service_login
from My_api.static.params.magicalValue import magicalValue
from My_api.static.params.return_params import RE
from My_api.static.public_method.public_method import time_format


@csrf_exempt
# 新增接口
def R_login(request):
    """
    登录
    :param request:
    :return:
    """
    ic.configureOutput(prefix=time_format)
    blank = magicalValue.BLANK.value
    NULL = magicalValue.NULL.value
    if request.method == "POST":
        data = json.loads(request.body)
        name = data['name']
        pwd = data['pwd']
        ic(data)
        insert = {
            'user': name,
            'pwd': pwd
        }
        if name == NULL or pwd == NULL:
            dic = json.dumps(RE.PARAMETER_IS_EMPTY.value)
            return HttpResponse(dic, content_type=RE.CONTENT_TYPE.value)
        elif blank in name or blank in pwd:
            dic = json.dumps(RE.PAY_ATTENTION_TO_SPACES.value)
            return HttpResponse(dic, content_type=RE.CONTENT_TYPE.value)
        else:
            num = service_login(insert)
            if num['code'] == RE.SUCCESS.value['code']:
                dic = json.dumps(num)
                return HttpResponse(dic, content_type=RE.CONTENT_TYPE.value)
            else:
                dic = json.dumps({"code": 30030, "data": "false", "message": f"{num}"})
                return HttpResponse(dic, content_type=RE.CONTENT_TYPE.value)
    else:
        dic = json.dumps(RE.WRONG_REQUEST.value)
        return HttpResponse(dic, content_type=RE.CONTENT_TYPE.value)
