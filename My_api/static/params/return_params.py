"""
_*_ coding: UTF-8 _*_
@Time      : 2021/2/7 13:38
@Author    : LiuXiaoQiang
@Site      : https://github.com/qq183727918
@File      : return_params.py
@Software  : PyCharm
"""
from enum import Enum


class RE(Enum):
    # 请求参数为空
    PARAMETER_IS_EMPTY = {"code": 30010, "data": "false", "msg": "请求参数不能为空"}
    # 请求参数类型错误
    TYPE_ERROR = {"code": 30011, "data": "false", "msg": "请求参数类型错误"}
    # 200
    SUCCESS = {"code": 200, "data": "true", "message": "OK"}
    # 请注意空格
    PAY_ATTENTION_TO_SPACES = {"code": 30012, "data": "false", "msg": "请注意空格"}
    # 请求方式错误
    WRONG_REQUEST = {"code": 30013, "data": "false", "msg": "请求方式错误"}
    # 编码格式
    CONTENT_TYPE = 'application/json;charset=utf-8'
    # 返回值为真
    TRUE = "用户有使用权限"
