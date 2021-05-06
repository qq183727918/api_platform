"""
_*_ coding: UTF-8 _*_
@Time      : 2021/4/8 16:19
@Author    : LiuXiaoQiang
@Site      : https://github.com/qq183727918
@File      : views_vue.py
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
from config.httprunner_file import *

logger = logging.getLogger('log')


def publicKey(request):
    if request.method == "POST":
        dic = {
            "code": 200,
            "data": {
                "mockServer": "true",
                "publicKey": "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDBT2vr+dhZElF73FJ6xiP181txKWUSNLPQQlid6DUJhGAOZblluafIdLmnUyKE8mMHhT3R+Ib3ssZcJku6Hn72yHYj/qPkCGFv0eFo7G+GJfDIUeDyalBN0QsuiE/XzPHJBuJDfRArOiWvH0BXOv5kpeXSXM8yTt5Na1jAYSiQ/wIDAQAB",
                "msg": "success"
            }
        }
        return HttpResponse(json.dumps(dic), content_type=RE.CONTENT_TYPE.value)
    else:
        dic = json.dumps(RE.WRONG_REQUEST.value)
        return HttpResponse(dic, content_type=RE.CONTENT_TYPE.value)


def userInfo(request):
    method = "POST"
    if community(request, method) == RE.TRUE.value:
        Authorization = request.headers['Authorization']
        user = decode_user(Authorization)
        logger.info('登录用户：{}'.format(user))
        dic = {
            "code": 200,
            "data": {
                "avatar": "https://i.gtimg.cn/club/item/face/img/8/15918_100.gif",
                "permissions": [f"{user}"],
                "username": f"{user}",
            },
            "msg": "success"
        }
        return HttpResponse(json.dumps(dic), content_type=RE.CONTENT_TYPE.value)
    else:
        return community(request, method)


# 登录
def login_action(request):
    if request.method == "POST":
        data = json.loads(request.body)
        logger.info('请求参数：{}'.format(data))
        # Authorization = request.headers['Authorization']
        # Authorization_ = 'Basic YzU5Mzg3ZmMzMQ=='
        if 'Authorization' == 'Authorization':
            u_name = data['username']
            p_word = data['password']
            logger.info('请求参数：{}'.format(data))
            if u_name == '':
                dic = json.dumps({"code": 30001, "data": "false", "message": "请输入账号"})
                return HttpResponse(dic, content_type=RE.CONTENT_TYPE.value)
            if p_word == '':
                dic = json.dumps({"code": 30002, "data": "false", "message": "请输入密码"})
                return HttpResponse(dic, content_type=RE.CONTENT_TYPE.value)
            # 开始联通用户库，查看用户密码是否正确
            username = DbUser.objects.filter(username=u_name, is_active=0).values()

            if username.count() == 0:
                dic = json.dumps({"code": 30003, "data": "false", "msg": "用户名不存在或未请启用！"})
                return HttpResponse(dic, content_type=RE.CONTENT_TYPE.value)
            else:
                for name in username:
                    if u_name == name['username']:
                        if p_word == name['password']:
                            token = new_token(name['username'])
                            dic = json.dumps({"code": 200, "data": {"Authorization": token}, "message": "success"})
                            return HttpResponse(dic, content_type=RE.CONTENT_TYPE.value)

                        else:
                            dic = json.dumps({"code": 30004, "data": "false", "message": "密码错误，请重试！"})
                            return HttpResponse(dic, content_type=RE.CONTENT_TYPE.value)
        else:
            res = HttpResponse(json.dumps({"code": 401, "data": False, "message": "凭证错误！"}))
            res.status_code = 401
            return res
    else:
        dic = json.dumps(RE.WRONG_REQUEST.value)
        return HttpResponse(dic, content_type=RE.CONTENT_TYPE.value)


# 项目列表查询
def project_list(request):
    method = "POST"
    if community(request, method) == RE.TRUE.value:
        data = json.loads(request.body)
        logger.info('请求参数：{}'.format(data))
        if "listName" in data:
            project_name = DbProject.objects.filter(id=data['listName']).order_by('-id').values()[0]['listName']
            queryset = DbProject.objects.filter(listName=project_name, is_delete=0).order_by('-id').all()
        else:
            queryset = DbProject.objects.filter(is_delete=0).order_by('-id').all()
        paginator = Paginator(queryset, data['pageSize'])
        page = paginator.get_page(data['pageNo'])
        lists = []
        for project in page.object_list.values():
            if project['is_active'] == 0:
                project['is_active'] = '启用'
            else:
                project['is_active'] = '未启用'
            times = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.mktime(project['created_time'].timetuple())))
            project['created_time'] = times
            lists.append(project)
        dic = {
            "code": 200,
            "data": lists,
            "msg": "success",
            "totalCount": queryset.count()
        }
        logger.info('请求成功：{}'.format(dic))
        return HttpResponse(json.dumps(dic), content_type=RE.CONTENT_TYPE.value)
    else:
        return community(request, method)


# 项目列表查询
def GetProList(request):
    method = "POST"
    if community(request, method) == RE.TRUE.value:
        queryset = DbProject.objects.filter(is_delete=0).order_by('-id').all()
        lists = []
        for project in queryset.values():
            if project['is_active'] == 0:
                project['is_active'] = '启用'
            else:
                project['is_active'] = '未启用'
            times = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.mktime(project['created_time'].timetuple())))
            project['created_time'] = times
            lists.append(project)
        dic = {
            "code": 200,
            "data": lists,
            "msg": "success",
            "totalCount": queryset.count()
        }
        logger.info('请求成功：{}'.format(dic))
        return HttpResponse(json.dumps(dic), content_type=RE.CONTENT_TYPE.value)
    else:
        return community(request, method)


# 项目编辑/新增
def project_edit(request):
    method = "POST"
    if community(request, method) == RE.TRUE.value:
        Authorization = request.headers['Authorization']
        user = decode_user(Authorization)
        data = json.loads(request.body)
        listName = data['listName']
        remark = data['remark']
        logger.info('请求参数：{}'.format(data))
        if len(data) == 3:
            Id = data['id']
            DbProject.objects.filter(id=Id).update(listName=listName, remark=remark)
        else:
            others = DbUser.objects.filter(username=user, is_delete=0, is_active=0).values()[0]
            DbProject.objects.create(
                listName=listName,
                remark=remark,
                is_delete=0,
                user=others['username'],
                user_id=others['id'],
                is_active=0,
                created_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

        return HttpResponse(json.dumps(RE.SUCCESS.value), content_type=RE.CONTENT_TYPE.value)
    else:
        return community(request, method)


# 项目删除
def project_del(request):
    method = "DELETE"
    if community(request, method) == RE.TRUE.value:
        data = json.loads(request.body)
        logger.info('请求参数：{}'.format(data))
        Id = data['ids']
        if type(Id) == int:
            if DbApis.objects.filter(project_id=Id).values().count() == 0:
                DbProject.objects.filter(id=Id).update(is_delete=1)
            else:
                listName = DbProject.objects.filter(id=Id).values()[0]['listName']
                dic = json.dumps({"code": 20010, "data": "false", "msg": f"项目{listName}下存在接口不能删除！"})
                return HttpResponse(dic, content_type=RE.CONTENT_TYPE.value)
        else:
            ids = Id.split(',')
            for i in ids:
                if DbApis.objects.filter(project_id=i).values().count() == 0:
                    DbProject.objects.filter(id=i).update(is_delete=1)
                else:
                    listName = DbProject.objects.filter(id=i).values()[0]['listName']
                    dic = json.dumps({"code": 20010, "data": "false", "msg": f"项目{listName}下存在接口不能删除！"})
                    return HttpResponse(dic, content_type=RE.CONTENT_TYPE.value)
        return HttpResponse(json.dumps(RE.SUCCESS.value), content_type=RE.CONTENT_TYPE.value)
    else:
        return community(request, method)


# 接口查询
def project_Apis(request):
    method = "POST"
    if community(request, method) == RE.TRUE.value:
        data = json.loads(request.body)
        logger.info('请求参数：{}'.format(data))
        if "listName" in data:
            if DbProject.objects.filter(id=data['listName'], is_delete=0, is_active=0).values().count() == 0:
                dic = {
                    "code": 200,
                    "data": [],
                    "msg": "success",
                    "totalCount": 0
                }
                return HttpResponse(json.dumps(dic), content_type=RE.CONTENT_TYPE.value)
            else:
                if "name" in data:
                    queryset = DbApis.objects.filter(name=data['name'], project_id=data['listName'],
                                                     is_delete=0).order_by('-id').all()
                else:
                    queryset = DbApis.objects.filter(project_id=data['listName'], is_delete=0).order_by('-id').all()
        else:
            if "name" in data:
                queryset = DbApis.objects.filter(name=data['name'], is_delete=0).order_by('-id').all()
            else:
                queryset = DbApis.objects.filter(is_delete=0).order_by('-id').all()
        paginator = Paginator(queryset, data['pageSize'])
        page = paginator.get_page(data['pageNo'])
        lists = []
        # ic(paginator, page.object_list.values())
        for project in page.object_list.values():
            listName = DbProject.objects.filter(id=project['project_id']).values()[0]['listName']
            project['listName'] = listName
            project['api_header'] = json.loads(project['api_header'])
            project['api_body'] = json.loads(project['api_body'])
            lists.append(project)
        dic = {
            "code": 200,
            "data": lists,
            "msg": "success",
            "totalCount": queryset.count()
        }
        return HttpResponse(json.dumps(dic), content_type=RE.CONTENT_TYPE.value)
    else:
        return community(request, method)


# 用户查询
def user_select(request):
    method = "POST"
    if community(request, method) == RE.TRUE.value:
        try:
            data = json.loads(request.body)
            logger.info('请求参数：{}'.format(data))
            queryset = DbUser.objects.filter(is_delete=0).order_by('-id').all()
            paginator = Paginator(queryset, data['pageSize'])
            page = paginator.get_page(data['pageNo'])
            lists = []
            for project in page.object_list.values():
                if project['is_active'] == 0:
                    project['is_active'] = '启用'
                else:
                    project['is_active'] = '未启用'
                times = time.strftime("%Y-%m-%d %H:%M:%S",
                                      time.localtime(time.mktime(project['created_time'].timetuple())))
                project['created_time'] = times
                lists.append(project)
            dic = {
                "code": 200,
                "data": lists,
                "msg": "success",
                "totalCount": queryset.count()
            }
            return HttpResponse(json.dumps(dic), content_type=RE.CONTENT_TYPE.value)
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
        return community(request, method)


# 用户禁用
def userDisable(request):
    method = "PUT"
    if community(request, method) == RE.TRUE.value:
        data = json.loads(request.body)
        logger.info('请求参数：{}'.format(data))
        DbUser.objects.filter(id=data['ids']).update(is_active=1)
        return HttpResponse(json.dumps(RE.SUCCESS.value), content_type=RE.CONTENT_TYPE.value)
    else:
        return community(request, method)


# 新增用户
def NewUser(request):
    if request.method == "POST":
        data = json.loads(request.body)
        logger.info('请求参数：{}'.format(data))
        username = DbUser.objects.filter(username=data['username']).values().count()
        curr_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        if username == 0:
            DbUser.objects.create(username=data['username'], password=data['password'], created_time=curr_time,
                                  is_delete=0, is_active=0)
            dic = json.dumps({"code": 200, "data": "false", "msg": "注册成功！"})
            return HttpResponse(dic, content_type=RE.CONTENT_TYPE.value)
        else:
            dic = json.dumps({"code": 30005, "data": "false", "msg": "注册失败~用户名好像已经存在了~"})
            return HttpResponse(dic, content_type=RE.CONTENT_TYPE.value)
    else:
        return HttpResponse(json.dumps(RE.WRONG_REQUEST.value), content_type=RE.CONTENT_TYPE.value)


# 退出登录
def logout(request):
    method = "POST"
    if community(request, method) == RE.TRUE.value:
        return HttpResponse(json.dumps(RE.SUCCESS.value), content_type=RE.CONTENT_TYPE.value)
    else:
        return community(request, method)


# 接口删除
def APisdel(request):
    method = "DELETE"
    if community(request, method) == RE.TRUE.value:
        data = json.loads(request.body)
        logger.info('请求参数：{}'.format(data))
        Id = data['ids']
        if type(Id) == int:
            DbApis.objects.filter(id=Id).update(is_delete=1)
            Returned.objects.filter(apis_id=Id).update(is_delete=1)
        else:
            ids = Id.split(',')
            for i in ids:
                DbApis.objects.filter(id=i).update(is_delete=1)
                Returned.objects.filter(apis_id=i).update(is_delete=1)
        return HttpResponse(json.dumps(RE.SUCCESS.value), content_type=RE.CONTENT_TYPE.value)
    else:
        return community(request, method)


# 接口复制接口
def copy_apis(request):
    method = "POST"
    if community(request, method) == RE.TRUE.value:
        data = json.loads(request.body)
        logger.info('请求参数：{}'.format(data))
        api_id = data['ids']
        # 开始复制接口
        old_api = DbApis.objects.filter(id=api_id)[0]
        names = old_api.name
        apis_num = DbApis.objects.filter(name__contains=names).values().count()

        for i in range(apis_num):
            names += '_副本'
        DbApis.objects.create(project_id=old_api.project_id,
                              name=names,
                              api_models=old_api.api_models,
                              api_url=old_api.api_url,
                              api_header=old_api.api_header,
                              api_login=old_api.api_login,
                              api_tag=old_api.api_tag,
                              # api_host=old_api.api_host,
                              des=old_api.des,
                              body_method=old_api.body_method,
                              api_body=old_api.api_body,
                              result=old_api.result,
                              sign=old_api.sign,
                              file_key=old_api.file_key,
                              file_name=old_api.file_name,
                              public_header=old_api.public_header,
                              last_body_method=old_api.last_body_method,
                              last_api_body=old_api.last_api_body,
                              is_delete=0
                              )
        api_name = names
        apisIds = DbApis.objects.filter(name=api_name).values()[0]['id']
        apisId = Returned.objects.filter(apis_id=api_id).values()[0]
        Returned.objects.create(
            apis_id=apisIds,
            extract_path=apisId['extract_path'],
            extract_re=apisId['extract_re'],
            expected=apisId['expected'],
            assert_re=apisId['assert_re'],
            assert_path=apisId['assert_path'],
            mock_res=apisId['mock_res'],
            is_delete=0,
        )
        logger.info('请求参数：{}'.format(apisId))
        # 返回
        dic = json.dumps({"code": 200, "data": True, "msg": "ok"})
        return HttpResponse(dic, content_type=RE.CONTENT_TYPE.value)
    else:
        return community(request, method)


# 接口备注、名称修改
def DesEdit(request):
    method = "POST"
    if community(request, method) == RE.TRUE.value:
        data = json.loads(request.body)
        logger.info('请求参数：{}'.format(data))
        Id = data['id']
        DbApis.objects.filter(id=Id).update(des=data['des'], name=data['name'])
        return HttpResponse(json.dumps(RE.SUCCESS.value), content_type=RE.CONTENT_TYPE.value)
    else:
        return community(request, method)


# 新增接口
def SaveApis(request):
    method = "POST"
    if community(request, method) == RE.TRUE.value:
        data = json.loads(request.body)
        logger.info('请求参数：{}'.format(data))
        dic_head = {}
        dic_body = {}
        body_method = ''
        api_name = data['api_name']
        method = data['method']
        url = data['url']
        api_body = data['api_body']
        radio = data['radio']
        tag = data['tag']
        project_id = data['project_id']
        if tag == 'header' or 'body':
            if radio == 1:
                body_method = "None"
            if radio == 2:
                body_method = "Form-data"
                for head in api_body:
                    dic_body[head['key']] = head['value']
            if radio == 3:
                body_method = "X-www-form-urlencoded"
                for head in api_body:
                    dic_body[head['key']] = head['value']
            if radio == 4:
                body_method = "Raw"
                dic_body = json.loads(data['api_body'])
            if radio == 5:
                body_method = "Binary"
        else:
            body_method = "query"
            for head in api_body:
                dic_body[head['key']] = head['value']
        headers = data['header']
        for head in headers:
            dic_head[head['key']] = head['value']
        if dic_head == {'': ''}:
            dic_head = {}
        else:
            pass
        result = data['result']
        if type(result) == dict:
            results = json.dumps(result)
        else:
            results = result
        if "AssertRe" in data:
            AssertRe = data['AssertRe']
        else:
            AssertRe = ""
        if "AssertPath" in data:
            AssertPath = data['AssertPath']
        else:
            AssertPath = ""
        if "ExpectedResult" in data:
            ExpectedResult = data['ExpectedResult']
        else:
            ExpectedResult = ""
        if "ExtractPath" in data:
            ExtractPath = data['ExtractPath']
        else:
            ExtractPath = ""
        if "ExtractRe" in data:
            ExtractRe = data['ExtractRe']
        else:
            ExtractRe = ""
        if "mock" in data:
            mock = data['mock']
        else:
            mock = ""

        if DbApis.objects.filter(name=api_name).values().count() == 0:
            DbApis.objects.create(
                project_id=project_id,
                name=api_name,
                api_models=method,
                api_url=url,
                api_header=json.dumps(dic_head),
                api_body=json.dumps(dic_body),
                api_tag=tag,
                result=results,
                body_method=body_method,
                is_delete=0,
            )
            api_id = DbApis.objects.filter(name=api_name).values()[0]['id']
            Returned.objects.create(
                apis_id=api_id,
                extract_path=ExtractPath,
                extract_re=ExtractRe,
                expected=ExpectedResult,  # 预期结果
                assert_re=AssertRe,  # 断言全文检索
                assert_path=AssertPath,  # 断言路径
                mock_res=mock,
                is_delete=0
            )
        else:
            dic = {
                "code": 230010,
                "data": False,
                "msg": "接口名称已存在请重新输入"
            }
            return HttpResponse(json.dumps(dic), content_type=RE.CONTENT_TYPE.value)
        return HttpResponse(json.dumps(RE.SUCCESS.value), content_type=RE.CONTENT_TYPE.value)
    else:
        return community(request, method)


# 调试保存
def DebugApis(request):
    method = "POST"
    if community(request, method) == RE.TRUE.value:
        data = json.loads(request.body)
        logger.info('请求参数：{}'.format(data))
        dic_head = {}
        dic_body = {}
        body_method = ''
        method = data['method']
        url = data['url']
        radio = data['radio']
        tag = data['tag']
        if "api_body" in data:
            api_body = data['api_body']
        else:
            api_body = {}
        if tag == 'header' or tag == 'body':
            if radio == 1:
                body_method = "None"
            if radio == 2:
                body_method = "Form-data"
                for head in api_body:
                    dic_body[head["key"]] = head["value"]
                dic_body = json.dumps(dic_body)
            if radio == 3:
                body_method = "X-www-form-urlencoded"
                for head in api_body:
                    dic_body[head['key']] = head['value']
                dic_body = json.dumps(dic_body)
            if radio == 4:
                body_method = "Raw"
                if type(data['api_body']) == str:
                    dic_body = data['api_body']
                else:
                    dic_body = json.dumps(data['api_body'])
            if radio == 5:
                body_method = "Binary"
        else:
            body_method = "query"
            for head in api_body:
                dic_body[head['key']] = head['value']
        headers = data['header']
        for head in headers:
            dic_head[head['key']] = head['value']
        if dic_head == {'': ''}:
            dic_head = {}

        if dic_body == {"": ""}:
            dic_body = {}
        result = data['result']
        if type(result) == dict:
            results = json.dumps(result)
        else:
            results = result
        DbApis.objects.filter(id=data['project_id']).update(
            api_models=method,
            api_url=url,
            api_header=json.dumps(dic_head),
            api_body=dic_body,
            api_tag=tag,
            result=results,
            body_method=body_method,
        )
        if "AssertRe" in data:
            AssertRe = data['AssertRe']
        else:
            AssertRe = ""
        if "AssertPath" in data:
            AssertPath = data['AssertPath']
        else:
            AssertPath = ""
        if "ExpectedResult" in data:
            ExpectedResult = data['ExpectedResult']
        else:
            ExpectedResult = ""
        if "ExtractPath" in data:
            ExtractPath = data['ExtractPath']
        else:
            ExtractPath = ""
        if "ExtractRe" in data:
            ExtractRe = data['ExtractRe']
        else:
            ExtractRe = ""
        if "mock" in data:
            mock = data['mock']
        else:
            mock = ""
        Returned.objects.filter(apis_id=data['project_id']).update(
            extract_path=ExtractPath,
            extract_re=ExtractRe,
            expected=ExpectedResult,  # 预期结果
            assert_re=AssertRe,  # 断言全文检索
            assert_path=AssertPath,  # 断言路径
            mock_res=mock,
            is_delete=0
        )
        return HttpResponse(json.dumps(RE.SUCCESS.value), content_type=RE.CONTENT_TYPE.value)
    else:
        return community(request, method)


# 发送请求
def SendRequest(request):
    method = "POST"
    if community(request, method) == RE.TRUE.value:
        data = json.loads(request.body)
        logger.info('请求参数：{}'.format(data))
        dic_head = {}
        dic_body = {}
        response = ''
        url = data['url']
        radio = data['radio']
        tag = data['tag']
        if url[0:7] != 'http://' and url[0:8] != 'https://':
            dic = {
                "code": 20020,
                "data": "false",
                "msg": "非法请求地址！"
            }
            return HttpResponse(json.dumps(dic), content_type=RE.CONTENT_TYPE.value)
        if tag == 'header' or tag == 'body':
            if radio == 1:
                api_body = {}
            if radio == 2:
                api_body = data['api_body']
                for head in api_body:
                    glos = re.findall("{{(.*?)}}", head['value'])
                    if glos:
                        aw = DbGlobalData.objects.filter(name=glos[0]).values()[0]
                        dic_body[head['key']] = aw['data']
                    else:
                        dic_body[head['key']] = head['value']
            if radio == 3:
                api_body = data['api_body']
                for head in api_body:
                    glos = re.findall("{{(.*?)}}", head['value'])
                    if glos:
                        aw = DbGlobalData.objects.filter(name=glos[0]).values()[0]
                        dic_body[head['key']] = aw['data']
                    else:
                        dic_body[head['key']] = head['value']
            if radio == 4:
                dic_head['Content-Type'] = 'application/json'
                dic_body = data['api_body']
        else:
            api_body = data['api_body']
            for head in api_body:
                glos = re.findall("{{(.*?)}}", head['value'])
                if glos:
                    aw = DbGlobalData.objects.filter(name=glos[0]).values()[0]
                    dic_body[head['key']] = aw['data']
                else:
                    dic_body[head['key']] = head['value']

        for head in data['header']:
            glo = re.findall("{{(.*?)}}", head['value'])
            if glo:
                a = DbGlobalData.objects.filter(name=glo[0]).values()[0]
                dic_head[head['key']] = a['data']
            else:
                if head['key'] != "":
                    dic_head[head['key']] = head['value']
        if dic_head == {'': ''}:
            dic_head = {}
        else:
            pass
        try:
            if data['radio'] == 1:
                response = requests.request(data['method'].upper(), url=url, headers=dic_head, data={}, verify=False)
            elif data['radio'] == 2:
                files = []
                response = requests.request(data['method'].upper(), url=url, headers=dic_head, data=dic_body,
                                            files=files, verify=False)
            elif data['radio'] == 3:
                dic_head['Content-Type'] = 'application/x-www-form-urlencoded'
                response = requests.request(data['method'].upper(), url=url, headers=dic_head, data=dic_body,
                                            verify=False)
            elif data['radio'] == 4:
                response = requests.request(data['method'].upper(), url=url, headers=dic_head,
                                            data=dic_body, verify=False)
            else:
                response = requests.request(data['method'].upper(), url=url, headers=dic_head, data={}, verify=False)
        except Exception as e:
            logger.error('错误信息：{}'.format(e))
            dic = {
                "code": 503001,
                "data": "false",
                "msg": "非法API请求地址：请检查是否正确填写URL以及URL是否允许访问"
            }
            return HttpResponse(json.dumps(dic), content_type=RE.CONTENT_TYPE.value)
        response.encoding = "gbk"
        res = response.text
        head = response.headers
        if re.findall("{(.*?)}", res):
            res = response.json()
        else:
            res = response.text
        # 将头信息转为可以进行json序列化的
        logger.info('API返回头部：{}'.format(head))
        logger.info('请求参数：{}'.format(res))
        if 'Content-Disposition' in head:
            head_file = head['Content-Disposition'].split(";")[1].strip().split("=")[1]
            ic(head_file)
            file_path = ''
            with open(f"/My_api/static/selenium_file\\{head_file}", "wb") as code:
                code.write(response.content)
        else:
            file_path = False
        tractpath = ""
        tractre = ""
        ReAssert = ""
        PathAssert = ""
        ResultExpected = ""
        if "mock" in data:
            res = data['mock']
            logger.info('请求参数：{}'.format(res))
        if "ExtractPath" in data:
            ExtractPath = data['ExtractPath']
            try:
                datas = ExtractPath.split('\n')
                for i in datas:
                    if i == '':
                        continue
                    extract = i.split('=')
                    path = extract[1].split('/')
                    values = res
                    for a in path:
                        if a == '':
                            continue
                        try:
                            a = int(a)
                        except Exception as e:
                            logger.error('错误信息：{}'.format(e))
                            a = a
                        py_path = values[a]
                        values = py_path
                    tractpath += f"{i} ==> {values}\n"
            except Exception as e:
                logger.error('错误信息：{}'.format(e))
                dic = {
                    "code": 35010,
                    "data": "false",
                    "msg": "提取路径输入有误请仔细检查！"
                }
                return HttpResponse(json.dumps(dic), content_type=RE.CONTENT_TYPE.value)
        if "ExtractRe" in data:
            ExtractRe = data['ExtractRe']
            try:
                datas = ExtractRe.split('\n')
                for i in datas:
                    if i == '':
                        continue
                    extract = i.split('=')
                    path = extract[1]
                    pa = re.findall(path, str(res))
                    tractre += f"{i} ==> {pa[0]}\n"
            except Exception as e:
                logger.error('错误信息：{}'.format(e))
                dic = {
                    "code": 35010,
                    "data": "false",
                    "msg": "提取正则输入有误请仔细检查！"
                }
                return HttpResponse(json.dumps(dic), content_type=RE.CONTENT_TYPE.value)
        if "AssertRe" in data:
            try:
                AssertRe = data['AssertRe']
                datas = AssertRe.split('\n')
                for i in datas:
                    if i in str(res):
                        ReAssert += f"{i} ==> True\n"
                    else:
                        ReAssert += f"{i} ==> False\n"
            except Exception as e:
                logger.error('错误信息：{}'.format(e))
                dic = {
                    "code": 35010,
                    "data": "false",
                    "msg": "断言正则输入有误请仔细检查！"
                }
                logger.info('请求参数：{}'.format(dic))
                return HttpResponse(json.dumps(dic), content_type=RE.CONTENT_TYPE.value)
        if "AssertPath" in data:
            AssertPath = data['AssertPath']
            try:
                datas = AssertPath.split('\n')
                for i in datas:
                    if i == '':
                        continue
                    extract = i.split('=')
                    path = extract[0].split('/')
                    extract_value = extract[1]
                    values = res
                    for a in path:
                        if a == '':
                            continue
                        try:
                            a = int(a)
                        except Exception as e:
                            logger.error('错误信息：{}'.format(e))
                            a = a
                        py_path = values[a]
                        values = py_path
                    if str(values) == eval(extract_value):
                        PathAssert += f"{i} ==> True\n"
                    else:
                        PathAssert += f"{i} ==> False\n"
            except Exception as e:
                logger.error('错误信息：{}'.format(e))
                dic = {
                    "code": 35010,
                    "data": "false",
                    "msg": "断言路径输入有误请仔细检查！"
                }
                return HttpResponse(json.dumps(dic), content_type=RE.CONTENT_TYPE.value)
        if "ExpectedResult" in data:
            ExpectedResult = data['ExpectedResult']
            try:
                datas = ExpectedResult.split('\n')
                for i in datas:
                    if i == '':
                        continue
                    extract = i.split('=')
                    path = extract[0]
                    path_value = extract[1]
                    if len(re.findall(path, str(res))) == 0:
                        ResultExpected += f"{i} ==> 该正则未匹配到数据！\n"
                    else:
                        pa = re.findall(path, str(res))[0]
                        if pa == eval(path_value):
                            ResultExpected += f"{i} ==> True\n"
                        else:
                            ResultExpected += f"{i} ==> False\n"
            except Exception as e:
                logger.error('错误信息：{}'.format(e))
                dic = {
                    "code": 35010,
                    "data": "false",
                    "msg": "全文检索输入有误请仔细检查！"
                }
                return HttpResponse(json.dumps(dic), content_type=RE.CONTENT_TYPE.value)

        dic = {
            "code": 200,
            "data": res,
            "ExtractPath": f'{tractpath}',
            "ExtractRe": f'{tractre}',
            "AssertRe": f"{ReAssert}",
            "AssertPath": f"{PathAssert}",
            "ResultExpected": f"{ResultExpected}",
            "file_path": f"{file_path}",
            "message": "ok"
        }
        logger.info('返回结果：{}'.format(dic))
        return HttpResponse(json.dumps(dic), content_type=RE.CONTENT_TYPE.value)
    else:
        return community(request, method)


# 用例查询
def getCases(request):
    method = "POST"
    if community(request, method) == RE.TRUE.value:
        try:
            data = json.loads(request.body)
            logger.info('请求参数：{}'.format(data))
            if "listName" in data:
                if DbProject.objects.filter(id=data['listName'], is_delete=0, is_active=0).values().count() == 0:
                    dic = {
                        "code": 200,
                        "data": [],
                        "msg": "success",
                        "totalCount": 0
                    }
                    return HttpResponse(json.dumps(dic), content_type=RE.CONTENT_TYPE.value)
                else:
                    if "name" in data:
                        queryset = DbCases.objects.filter(name=data['name'], project_id=data['listName'],
                                                          is_delete=0).order_by('-id').all()
                    else:
                        queryset = DbCases.objects.filter(project_id=data['listName'], is_delete=0).order_by(
                            '-id').all()
            else:
                if "name" in data:
                    queryset = DbCases.objects.filter(name=data['name'], is_delete=0).order_by('-id').all()
                else:
                    queryset = DbCases.objects.filter(is_delete=0).order_by('-id').all()
            paginator = Paginator(queryset, data['pageSize'])
            page = paginator.get_page(data['pageNo'])
            lists = []
            for project in page.object_list.values():
                listName = DbProject.objects.filter(id=project['project_id']).values()[0]['listName']
                project['listName'] = listName
                times = time.strftime("%Y-%m-%d %H:%M:%S",
                                      time.localtime(time.mktime(project['created_time'].timetuple())))
                project['created_time'] = times
                lists.append(project)
            dic = {
                "code": 200,
                "data": lists,
                "msg": "success",
                "totalCount": queryset.count()
            }
            return HttpResponse(json.dumps(dic), content_type=RE.CONTENT_TYPE.value)
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
        return community(request, method)


# 用例删除
def CaseDel(request):
    method = "DELETE"
    if community(request, method) == RE.TRUE.value:
        data = json.loads(request.body)
        logger.info('请求参数：{}'.format(data))
        Id = data['ids']
        if type(Id) == int:
            DbCases.objects.filter(id=Id).update(is_delete=1)
            DbStep.objects.filter(Case_id=Id).update(is_delete=1)
        else:
            ids = Id.split(',')
            for i in ids:
                DbCases.objects.filter(id=i).update(is_delete=1)
                DbStep.objects.filter(Case_id=i).update(is_delete=1)
        return HttpResponse(json.dumps(RE.SUCCESS.value), content_type=RE.CONTENT_TYPE.value)
    else:
        return community(request, method)


# 新增用例
def InNewCase(request):
    method = "POST"
    if community(request, method) == RE.TRUE.value:
        try:
            data = json.loads(request.body)
            logger.info('请求参数：{}'.format(data))
            curr_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            print(curr_time)
            DbCases.objects.create(
                project_id=data['project_id'],
                name=data['name'],
                des=data['des'],
                created_time=curr_time,
                is_delete=0
            )
            dic = json.dumps(RE.SUCCESS.value)
            return HttpResponse(dic, content_type=RE.CONTENT_TYPE.value)
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
        return community(request, method)


# 复制用例
def CopyCase(request):
    method = "POST"
    if community(request, method) == RE.TRUE.value:
        try:
            data = json.loads(request.body)
            logger.info('请求参数：{}'.format(data))
            old_case = DbCases.objects.filter(id=data['ids'])[0]
            curr_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            DbCases.objects.create(
                project_id=old_case.project_id,
                name=old_case.name + '_副本',
                des=old_case.des,
                created_time=curr_time,
                is_delete=0)
            dic = json.dumps(RE.SUCCESS.value)
            return HttpResponse(dic, content_type=RE.CONTENT_TYPE.value)
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
        return community(request, method)


# 用例编辑
def CaseEdit(request):
    method = "PUT"
    if community(request, method) == RE.TRUE.value:
        data = json.loads(request.body)
        logger.info('请求参数：{}'.format(data))
        project_id = DbProject.objects.filter(listName=data['project_id']).values()[0]['id']
        DbCases.objects.filter(id=data['id']).update(des=data['des'], name=data['name'], project_id=project_id)
        return HttpResponse(json.dumps(RE.SUCCESS.value), content_type=RE.CONTENT_TYPE.value)
    else:
        return community(request, method)


# 新增小用例
def SmallCase(request):
    method = "POST"
    if community(request, method) == RE.TRUE.value:
        data = json.loads(request.body)
        logger.info('请求参数：{}'.format(data))
        if DbStep.objects.filter(Case_id=data['case_id'], name=data['name'], is_delete=0).values().count() == 0:
            DbStep.objects.create(
                Case_id=data['case_id'],
                name=data['name'],
                index=data['index'],
                is_delete=0
            )
        else:
            dic = {
                "code": 30012,
                "data": "false",
                "msg": "小用例名称已经存在"
            }
            return HttpResponse(json.dumps(dic), content_type=RE.CONTENT_TYPE.value)
        return HttpResponse(json.dumps(RE.SUCCESS.value), content_type=RE.CONTENT_TYPE.value)
    else:
        return community(request, method)


# 查询小用例
def SmallList(request):
    method = "POST"
    if community(request, method) == RE.TRUE.value:
        data = json.loads(request.body)
        logger.info('请求参数：{}'.format(data))
        smalls = DbStep.objects.filter(Case_id=data['id'], is_delete=0).order_by('index').values()
        a = smalls.count()
        small = []
        for s in smalls:
            small.append(s)
        dic = {
            "code": 200,
            "data": small,
            "msg": "success",
        }
        logger.info('请求参数：{}'.format(dic))
        return HttpResponse(json.dumps(dic), content_type=RE.CONTENT_TYPE.value)
    else:
        return community(request, method)


# 删除小用例
def SmallDel(request):
    method = "DELETE"
    if community(request, method) == RE.TRUE.value:
        data = json.loads(request.body)
        logger.info('请求参数：{}'.format(data))
        DbStep.objects.filter(Case_id=data['case_id'], index=data['ids']).update(is_delete=1)
        cases = DbStep.objects.filter(Case_id=data['case_id'], is_delete=0).values()
        i = 0
        for case in cases:
            i += 1
            DbStep.objects.filter(id=case['id']).update(index=i)
        return HttpResponse(json.dumps(RE.SUCCESS.value), content_type=RE.CONTENT_TYPE.value)
    else:
        return community(request, method)


# 小用例下拉框查询接口
def SmallGet(request):
    method = "POST"
    if community(request, method) == RE.TRUE.value:
        data = json.loads(request.body)
        logger.info('请求参数：{}'.format(data))
        lists = DbApis.objects.filter(project_id=data['project_id'], is_delete=0).values()
        small = []
        for s in lists:
            small.append(s)
        dic = {
            "code": 200,
            "data": small,
            "msg": "success",
        }
        logger.info('请求参数：{}'.format(dic))
        return HttpResponse(json.dumps(dic), content_type=RE.CONTENT_TYPE.value)
    else:
        return community(request, method)


# 保存接口
def SmallOrder(request):
    method = "POST"
    if community(request, method) == RE.TRUE.value:
        data = json.loads(request.body)
        logger.info('请求参数：{}'.format(data))
        small_list = data['case']
        for small in small_list:
            api = DbApis.objects.filter(id=small['apiid']).values()[0]
            returned = Returned.objects.filter(apis_id=small['apiid']).values()[0]
            apis = api['api_url']
            if apis[0:7] == 'http://':
                paths = apis[7:]
                s = paths.split('/')[0]
                path = paths.replace(s, '')
                host = 'http://' + s
            elif apis[0:8] == 'https://':
                paths = apis[8:]
                s = paths.split('/')[0]
                path = paths.replace(s, '')
                host = 'https://' + s
            else:
                dic = json.dumps({
                    "code": 30225,
                    "data": "false",
                    "msg": f"url不正确:{apis}"
                })
                return HttpResponse(json.dumps(dic), content_type=RE.CONTENT_TYPE.value)
            DbStep.objects.filter(id=small['id']).update(
                api_id=small['apiid'],
                index=small['index'],
                api_method=api['api_models'],
                api_host=host,
                api_url=path,
                api_header=api['api_header'],
                api_body=api['api_body'],
                api_body_method=api['body_method'],
                get_path=returned['extract_path'],
                get_zz=returned['extract_re'],
                assert_path=returned['assert_path'],
                assert_zz=returned['assert_re'],
                assert_qz=returned['expected'],
                mock_res=returned['mock_res'],
            )
        cases = DbStep.objects.filter(Case_id=data['case_id'], is_delete=0).order_by('index').values()
        i = 0
        for case in cases:
            i += 1
            DbStep.objects.filter(id=case['id']).update(index=i)
        return HttpResponse(json.dumps(RE.SUCCESS.value), content_type=RE.CONTENT_TYPE.value)
    else:
        return community(request, method)


# 查看报告
def LookReport(request):
    method = "POST"
    if community(request, method) == RE.TRUE.value:
        data = json.loads(request.body)
        logger.info('请求参数：{}'.format(data))
        global case_ids
        case_ids = data['id']
        asz = Report(request)
        if asz == "TemplateDoesNotExist":
            dic = json.dumps({
                "code": 30215,
                "data": "false",
                "msg": "测试报告还未生成，请检查！"
            })
        else:
            dic = json.dumps({
                "code": 200,
                "data": "true",
                "message": "http://192.168.1.42:8080/project/Report"
            })
        return HttpResponse(dic, content_type=RE.CONTENT_TYPE.value)
    else:
        return community(request, method)


# 报告路径
def Report(request):
    try:
        return render(request, f'Reports/HtmlTest/{case_ids}.html')
    except Exception as e:
        logger.error('错误信息：{}'.format(e))
        return "TemplateDoesNotExist"


# 运行用例
def RunCase(request):
    method = "POST"
    if community(request, method) == RE.TRUE.value:
        data = json.loads(request.body)
        logger.info('请求参数：{}'.format(data))
        Case_id = data['case_id']
        if DbStep.objects.filter(Case_id=Case_id).count() == 0:
            dic = json.dumps({
                "code": 32100,
                "daya": False,
                "msg": "该用例下没有接口存在"
            })
            return HttpResponse(dic, content_type=RE.CONTENT_TYPE.value)
        Case_name = DbCases.objects.filter(id=Case_id).values()[0]['name']
        Case = DbStep.objects.filter(Case_id=Case_id)[0]
        steps = DbStep.objects.filter(Case_id=Case_id)
        logger.info('请求参数data, Case, Case.id, Case.name, steps：{}'.format(data, Case, Case.id, Case.name, steps))
        # from My_api.run_case import run
        from My_api.Run import run
        run(Case.Case_id, Case_name, steps)

        dic = json.dumps(RE.SUCCESS.value)
        return HttpResponse(dic, content_type=RE.CONTENT_TYPE.value)
    else:
        return community(request, method)


# 全局变量查询
def Variable(request):
    method = "POST"
    if community(request, method) == RE.TRUE.value:
        try:
            data = json.loads(request.body)
            logger.info('请求参数：{}'.format(data))
            if "name" in data:
                queryset = DbGlobalData.objects.filter(name=data['name'], is_delete=0).order_by('-id').all()
            else:
                queryset = DbGlobalData.objects.filter(is_delete=0).order_by('-id').all()
            paginator = Paginator(queryset, data['pageSize'])
            page = paginator.get_page(data['pageNo'])
            lists = []
            for project in page.object_list.values():
                times = time.strftime("%Y-%m-%d %H:%M:%S",
                                      time.localtime(time.mktime(project['created_time'].timetuple())))
                project['created_time'] = times
                lists.append(project)
            dic = {
                "code": 200,
                "data": lists,
                "msg": "success",
                "totalCount": queryset.count()
            }
            return HttpResponse(json.dumps(dic), content_type=RE.CONTENT_TYPE.value)
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
        return community(request, method)


# 全局变量编辑/新增
def DoEdit(request):
    method = "POST"
    if community(request, method) == RE.TRUE.value:
        data = json.loads(request.body)
        logger.info('请求参数：{}'.format(data))
        if "id" in data:
            DbGlobalData.objects.filter(id=data['id']).update(
                name=data['name'],
                data=data['data'],
            )
        else:
            Authorization = request.headers['Authorization']
            user = decode_user(Authorization)
            DbGlobalData.objects.create(
                name=data['name'],
                data=data['data'],
                user=user,
                created_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                is_delete=0
            )
        return HttpResponse(json.dumps(RE.SUCCESS.value), content_type=RE.CONTENT_TYPE.value)
    else:
        return community(request, method)


# 全局变量删除
def GloDel(request):
    method = "DELETE"
    if community(request, method) == RE.TRUE.value:
        data = json.loads(request.body)
        logger.info('请求参数：{}'.format(data))
        Id = data['ids']
        if type(Id) == int:
            DbGlobalData.objects.filter(id=Id).update(is_delete=1)
        else:
            ids = Id.split(',')
            for i in ids:
                DbGlobalData.objects.filter(id=i).update(is_delete=1)
        return HttpResponse(json.dumps(RE.SUCCESS.value), content_type=RE.CONTENT_TYPE.value)
    else:
        return community(request, method)


class UserForm(forms.Form):
    filename = forms.FileField()


# 文件上传
@csrf_exempt
def Runner(request):
    method = "POST"
    try:
        if community(request, method) == RE.TRUE.value:
            myFile = request.FILES.get("file", None)  # 获取上传的文件，如果没有文件，则默认为None
            logger.info('请求参数：{}'.format(myFile))
            names = myFile.name
            a = "." + names.split('.')[-1]
            fname = names.replace(a, '')
            filename = HttpRunner.objects.filter(file_name=fname).values().count()
            if filename != 0:
                dic = {"code": 20110, "data": "false", "msg": "文件名称已存在请重新导入!"}
                return HttpResponse(json.dumps(dic), content_type=RE.CONTENT_TYPE.value)
            if not myFile:
                dic = {"code": 70010, "data": "false", "msg": "no files for upload!"}
                return HttpResponse(dic, content_type=RE.CONTENT_TYPE.value)
            destination = open(os.path.join("D:\\platform\\My_api\\static\\httprunner\\testcases\\", myFile.name),
                               'wb+')  # 打开特定的文件进行二进制的写操作
            for chunk in myFile.chunks():  # 分块写入文件
                destination.write(chunk)
            destination.close()
            Authorization = request.headers['Authorization']
            user = decode_user(Authorization)
            HttpRunner.objects.create(
                file_name=fname,
                is_zip=0,
                user_name=user,
                is_json=0,
                created_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                is_delete=0
            )
            dic = {"code": 200, "data": "true", "msg": "上传成功！"}
            return HttpResponse(json.dumps(dic), content_type=RE.CONTENT_TYPE.value)
        else:
            return community(request, method)
    except Exception as e:
        logger.error('错误信息：{}'.format(e))
        dic = {
            "code": 30010,
            "data": [],
            "msg": "服务不可用，请联系管理员！",
            "totalCount": 0
        }
        return HttpResponse(json.dumps(dic), content_type=RE.CONTENT_TYPE.value)


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


# 查询
def GetReturned(request):
    method = "POST"
    if community(request, method) == RE.TRUE.value:
        data = json.loads(request.body)
        logger.info('请求参数！{}'.format(data))
        Id = data['id']
        if Returned.objects.filter(apis_id=Id).values().count() == 0:
            dic = {"code": 32001, "data": False, "msg": "查询结果为空"}
        else:
            relist = Returned.objects.filter(apis_id=Id).values()[0]
            dic = {
                "code": 200,
                "data": relist,
                "msg": "OK"
            }
            logger.info('请求成功！{}'.format(dic))
        return HttpResponse(json.dumps(dic), content_type=RE.CONTENT_TYPE.value)
    else:
        return community(request, method)


# 异常值测试
def ErrorPlay(request):
    method = "POST"
    if community(request, method) == RE.TRUE.value:
        data = json.loads(request.body)
        logger.info('请求参数！{}'.format(data))
        apis = DbApis.objects.filter(id=data['id']).values()[0]
        url = apis['api_url']
        dic_body = data['abody']
        dic_head = eval(apis['api_header'])
        try:
            response = requests.request(apis['api_models'].upper(), url=url, headers=dic_head, data=dic_body,
                                        verify=False)
        except Exception as e:
            logger.error('请求出错：{}'.format(e))
            dic = {
                "code": 503001,
                "data": "false",
                "msg": "非法API请求地址：请检查是否正确填写URL以及URL是否允许访问"
            }
            return HttpResponse(json.dumps(dic), content_type=RE.CONTENT_TYPE.value)
        res = response.text
        logger.info('请求参数！{}'.format(res))
        return HttpResponse(json.dumps({"code": 200, "data": res, "msg": "OK"}), content_type=RE.CONTENT_TYPE.value)
    else:
        return community(request, method)


# 正交运行
def Orthogonal(request):
    method = "POST"
    if community(request, method) == RE.TRUE.value:
        data = json.loads(request.body)
        logger.info('请求参数！{}'.format(data))
        end_values = data['end_values']
        new_values = [i['value'].split('/') for i in end_values]
        res = []
        if new_values == [['']]:
            dic = {"code": 200, "res": [], "msg": "OK"}
        elif len(new_values) == 1:
            for k in range(len(new_values[0])):
                a = {f"key0": new_values[0][k]}
                res.append(a)
            dic = {"code": 200, "res": res, "msg": "OK"}
        else:
            for s in AllPairs(new_values):
                res.append(s)
            response = []
            for i in res:
                hj = {}
                for j in range(len(i)):
                    a = f"key{j}: {i[j]}"
                    hj[f"key{j}"] = i[j]
                response.append(hj)
                hj = {}
            dic = {"code": 200, "res": response, "msg": "OK"}
            logger.info('请求结果！{}'.format(dic))
        return HttpResponse(json.dumps(dic), content_type=RE.CONTENT_TYPE.value)
    else:
        return community(request, method)


# 正交导出
def OrthogonalDrive(request):
    method = "POST"
    if community(request, method) == RE.TRUE.value:
        data = json.loads(request.body)
        ic(data)
        logger.info('请求参数！{}'.format(data))
        end_values = data['end_values']
        new_values = [i['value'].split('/') for i in end_values]
        ic(new_values)
        res = []
        if new_values == [['']] or new_values == []:
            res = {"code": 13201, "data": "false", "msg": "没有可导出的数据"}
            return HttpResponse(json.dumps(res), content_type=RE.CONTENT_TYPE.value)
        elif len(new_values) == 1:
            for k in range(len(new_values[0])):
                a = {f"key0": new_values[0][k]}
                res.append(a)
        else:
            for s in AllPairs(new_values):
                res.append(s)
            response = []
            x = 1
            for i in res:
                hj = [f"用例编号{x}"]
                for j in range(len(i)):
                    a = f"{end_values[j]['key']}: {i[j]}"
                    hj.append(a)
                response.append(hj)
                hj = []
                x += 1
            f = codecs.open('D:\\platform\\My_api\\static\\driverfile\\driverFile.csv', 'w', 'gbk')
            writer = csv.writer(f)
            for i in response:
                writer.writerow(i)
            f.close()
            file_path = 'D:\\platform\\My_api\\static\\driverfile\\driverFile.csv'
            with open(file_path, "rb") as f:
                res = HttpResponse(f)
                res["Content-Type"] = "application/octet-stream;charset=UTF-8"  # 注意格式
                res["Content-Disposition"] = 'attachment; filename="OrthogonalDrive.csv"'
        return res

    else:
        return community(request, method)


# HttpRunner列表查询
def RunnerSee(request):
    method = "POST"
    if community(request, method) == RE.TRUE.value:
        try:
            data = json.loads(request.body)
            logger.info('请求参数：{}'.format(data))
            if "file_name" in data:
                queryset = HttpRunner.objects.filter(file_name=data['file_name'], is_delete=0).order_by('-id').all()
            else:
                queryset = HttpRunner.objects.filter(is_delete=0).order_by('-id').all()
            paginator = Paginator(queryset, data['pageSize'])
            page = paginator.get_page(data['pageNo'])
            lists = []
            for project in page.object_list.values():
                if project['is_zip'] == 0:
                    project['is_zip'] = "未解压"
                else:
                    project['is_zip'] = "已解压"
                times = time.strftime("%Y-%m-%d %H:%M:%S",
                                      time.localtime(time.mktime(project['created_time'].timetuple())))
                project['created_time'] = times
                lists.append(project)
            dic = {
                "code": 200,
                "data": lists,
                "msg": "success",
                "totalCount": queryset.count()
            }
            return HttpResponse(json.dumps(dic), content_type=RE.CONTENT_TYPE.value)
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
        return community(request, method)


# HttpRunner文件解压
def Uncompress(request):
    method = "PUT"
    if community(request, method) == RE.TRUE.value:
        try:
            data = json.loads(request.body)
            logger.info('请求参数：{}'.format(data))
            is_json = HttpRunner.objects.filter(id=data['id']).values()[0]
            if is_json['is_json'] == 0:
                # json解压
                runner_text = RunnerFileJson(is_json['file_name'])
            else:
                # yml解压
                runner_text = RunnerFileYml(is_json['file_name'])
            HttpRunner.objects.filter(id=data['id']).update(is_zip=1, runner_text=runner_text)
            return HttpResponse(json.dumps(RE.SUCCESS.value), content_type=RE.CONTENT_TYPE.value)
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
        return community(request, method)


# HttpRunner文件解压方式
def IsJSon(request):
    method = "PUT"
    if community(request, method) == RE.TRUE.value:
        try:
            data = json.loads(request.body)
            logger.info('请求参数：{}'.format(data))
            if 'is_json' not in data:
                data['is_json'] = 0
            HttpRunner.objects.filter(id=data['id']).update(is_json=data['is_json'])
            return HttpResponse(json.dumps(RE.SUCCESS.value), content_type=RE.CONTENT_TYPE.value)
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
        return community(request, method)


# HttpRunner删除
def RunnerDel(request):
    method = "DELETE"
    if community(request, method) == RE.TRUE.value:
        data = json.loads(request.body)
        logger.info('请求参数：{}'.format(data))
        Id = data['ids']
        if type(Id) == int:
            HttpRunner.objects.filter(id=Id).update(is_delete=1)
        else:
            ids = Id.split(',')
            for i in ids:
                HttpRunner.objects.filter(id=i).update(is_delete=1)
        return HttpResponse(json.dumps(RE.SUCCESS.value), content_type=RE.CONTENT_TYPE.value)
    else:
        return community(request, method)


# httpRunner查看报告
def RunnerLook(request):
    method = "POST"
    if community(request, method) == RE.TRUE.value:
        data = json.loads(request.body)
        logger.info('请求参数：{}'.format(data))
        global file_name
        file_name = data['file_name']
        asz = HttpReport(request)
        if asz == "TemplateDoesNotExist":
            dic = json.dumps({
                "code": 30215,
                "data": "false",
                "msg": "测试报告还未生成，请检查！"
            })
        else:
            dic = json.dumps({
                "code": 200,
                "data": "true",
                "message": "http://192.168.1.42:8080/httprunner/HttpReport"
            })
        return HttpResponse(dic, content_type=RE.CONTENT_TYPE.value)
    else:
        return community(request, method)


# HttpRunner报告路径
def HttpReport(request):
    try:
        return render(request, f'Reports/runner/{file_name}.html')
    except Exception as e:
        logger.error('错误信息：{}'.format(e))
        return "TemplateDoesNotExist"


# 运行
def HttpRunnerReport(request):
    method = "POST"
    if community(request, method) == RE.TRUE.value:
        data = json.loads(request.body)
        logger.info('请求参数：{}'.format(data))
        RunnerValue = HttpRunner.objects.filter(id=data['id']).values()[0]
        if RunnerValue['is_json'] == 0:
            RunApiFileJson(RunnerValue['file_name'])
        else:
            RunApiFileYml(RunnerValue['file_name'])
        return HttpResponse(json.dumps(RE.SUCCESS.value), content_type=RE.CONTENT_TYPE.value)
    else:
        return community(request, method)
