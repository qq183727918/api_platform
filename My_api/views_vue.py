"""
_*_ coding: UTF-8 _*_
@Time      : 2021/4/8 16:19
@Author    : LiuXiaoQiang
@Site      : https://github.com/qq183727918
@File      : views_vue.py
@Software  : PyCharm
"""
import json
import os
import re
import time

import requests
from django.core.paginator import Paginator
from django.forms import forms
from django.http import HttpResponse, JsonResponse
# Create your views here.
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from icecream import ic

from My_api.models import *
from My_api.static.params.return_params import RE
# Create your views here.
from My_api.static.public_method.public_method import decode_user, decode_time


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
        Authorization = request.headers['Accesstoken']
        user = decode_user(Authorization)
        ic(user)
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


# 项目列表查询
def project_list(request):
    method = "POST"
    if community(request, method) == RE.TRUE.value:
        data = json.loads(request.body)
        ic(data)
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
        return HttpResponse(json.dumps(dic), content_type=RE.CONTENT_TYPE.value)
    else:
        community(request, method)


# 项目编辑/新增
def project_edit(request):
    method = "POST"
    if community(request, method) == RE.TRUE.value:
        Authorization = request.headers['Accesstoken']
        user = decode_user(Authorization)
        ic(user)
        data = json.loads(request.body)
        ic(data)
        listName = data['listName']
        remark = data['remark']
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
        community(request, method)


# 项目删除
def project_del(request):
    method = "DELETE"
    if community(request, method) == RE.TRUE.value:
        data = json.loads(request.body)
        ic(data)
        Id = data['ids']
        if type(Id) == int:
            if DbApis.objects.filter(project_id=Id).values().count() == 0:
                DbProject.objects.filter(id=Id).update(is_delete=1)
            else:
                listName = DbProject.objects.filter(id=Id).values()[0]['listName']
                dic = json.dumps({"code": 20010, "data": "false", "msg": f"项目{listName}下存在接口不能删除！"})
                community(request, method)
        else:
            ids = Id.split(',')
            for i in ids:
                if DbApis.objects.filter(project_id=i).values().count() == 0:
                    DbProject.objects.filter(id=i).update(is_delete=1)
                else:
                    listName = DbProject.objects.filter(id=i).values()[0]['listName']
                    dic = json.dumps({"code": 20010, "data": "false", "msg": f"项目{listName}下存在接口不能删除！"})
                    community(request, method)
        return HttpResponse(json.dumps(RE.SUCCESS.value), content_type=RE.CONTENT_TYPE.value)
    else:
        community(request, method)


# 接口查询
def project_Apis(request):
    method = "POST"
    if community(request, method) == RE.TRUE.value:
        data = json.loads(request.body)
        ic(data)
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
                    queryset = DbApis.objects.filter(name=data['name'], project_id=data['listName'], is_delete=0).order_by('-id').all()
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
        community(request, method)


# 用户查询
def user_select(request):
    method = "POST"
    if community(request, method) == RE.TRUE.value:
        try:
            data = json.loads(request.body)
            ic(data)
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
            print(e)
            dic = {
                "code": 30010,
                "data": [],
                "msg": "服务不可用，请联系管理员！",
                "totalCount": 0
            }
            return HttpResponse(json.dumps(dic), content_type=RE.CONTENT_TYPE.value)
    else:
        community(request, method)


# 用户禁用
def userDisable(request):
    method = "PUT"
    if community(request, method) == RE.TRUE.value:
        data = json.loads(request.body)
        ic(data)
        DbUser.objects.filter(id=data['ids']).update(is_active=1)
        return HttpResponse(json.dumps(RE.SUCCESS.value), content_type=RE.CONTENT_TYPE.value)
    else:
        community(request, method)


# 新增用户
def NewUser(request):
    method = "POST"
    if community(request, method) == RE.TRUE.value:
        data = json.loads(request.body)
        ic(data)
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
        community(request, method)


# 退出登录
def logout(request):
    method = "POST"
    if community(request, method) == RE.TRUE.value:
        return HttpResponse(json.dumps(RE.SUCCESS.value), content_type=RE.CONTENT_TYPE.value)
    else:
        community(request, method)


# 接口删除
def APisdel(request):
    method = "DELETE"
    if community(request, method) == RE.TRUE.value:
        data = json.loads(request.body)
        ic(data, type(data['ids']))
        Id = data['ids']
        if type(Id) == int:
            DbApis.objects.filter(id=Id).update(is_delete=1)
        else:
            ids = Id.split(',')
            for i in ids:
                DbApis.objects.filter(id=i).update(is_delete=1)
        return HttpResponse(json.dumps(RE.SUCCESS.value), content_type=RE.CONTENT_TYPE.value)
    else:
        community(request, method)


# 接口复制接口
def copy_apis(request):
    method = "POST"
    if community(request, method) == RE.TRUE.value:
        data = json.loads(request.body)
        ic(data)
        api_id = data['ids']
        # 开始复制接口
        old_api = DbApis.objects.filter(id=api_id)[0]
        DbApis.objects.create(project_id=old_api.project_id,
                              name=old_api.name + '_副本',
                              api_models=old_api.api_models,
                              api_url=old_api.api_url,
                              api_header=old_api.api_header,
                              api_login=old_api.api_login,
                              api_host=old_api.api_host,
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
        # 返回
        dic = json.dumps({'code': 200, 'data': True, 'message': 'ok'})
        return HttpResponse(dic, content_type=RE.CONTENT_TYPE.value)
    else:
        community(request, method)


# 接口备注、名称修改
def DesEdit(request):
    method = "POST"
    if community(request, method) == RE.TRUE.value:
        data = json.loads(request.body)
        ic(data)
        Id = data['id']
        DbApis.objects.filter(id=Id).update(des=data['des'], name=data['name'])
        return HttpResponse(json.dumps(RE.SUCCESS.value), content_type=RE.CONTENT_TYPE.value)
    else:
        community(request, method)


# 新增接口
def SaveApis(request):
    method = "POST"
    if community(request, method) == RE.TRUE.value:
        data = json.loads(request.body)
        ic(data)
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
        DbApis.objects.create(
            project_id=project_id,
            name=api_name,
            api_models=method,
            api_url=url,
            api_header=json.dumps(dic_head),
            api_body=json.dumps(dic_body),
            api_tag=tag,
            result=result,
            body_method=body_method,
            is_delete=0,
        )
        return HttpResponse(json.dumps(RE.SUCCESS.value), content_type=RE.CONTENT_TYPE.value)
    else:
        community(request, method)


# 调试保存
def DebugApis(request):
    method = "POST"
    if community(request, method) == RE.TRUE.value:
        data = json.loads(request.body)
        ic(data)
        dic_head = {}
        dic_body = {}
        body_method = ''
        method = data['method']
        url = data['url']
        api_body = data['api_body']
        radio = data['radio']
        tag = data['tag']
        ic(type(data['result']))
        if tag == 'header' or tag == 'body':
            if radio == 1:
                body_method = "None"
            if radio == 2:
                body_method = "Form-data"
                for head in api_body:
                    dic_body[head['key']] = head['value']
                dic_body = json.loads(dic_body)
            if radio == 3:
                body_method = "X-www-form-urlencoded"
                for head in api_body:
                    dic_body[head['key']] = head['value']
                dic_body = json.loads(dic_body)
            if radio == 4:
                body_method = "Raw"
                ic(type(data['api_body']))
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
        if dic_body == {'': ''}:
            dic_body = {}
        else:
            pass
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
        return HttpResponse(json.dumps(RE.SUCCESS.value), content_type=RE.CONTENT_TYPE.value)
    else:
        community(request, method)


# 发送请求
def SendRequest(request):
    method = "POST"
    if community(request, method) == RE.TRUE.value:
        data = json.loads(request.body)
        ic(data)
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
                    dic_body[head['key']] = head['value']
            if radio == 3:
                api_body = data['api_body']
                for head in api_body:
                    dic_body[head['key']] = head['value']
            if radio == 4:
                if type(data['api_body']) == str:
                    dic_body = data['api_body']
                else:
                    dic_body = json.loads(data['api_body'])
        else:
            api_body = data['api_body']
            for head in api_body:
                dic_body[head['key']] = head['value']

        for head in data['header']:
            ic(head['value'])
            glo = re.findall("{{(.*?)}}", head['value'])
            if glo:
                a = DbGlobalData.objects.filter(name=glo[0]).values()[0]
                ic(a)
                dic_head[head['key']] = a['data']
            else:
                dic_head[head['key']] = head['value']
        if dic_head == {'': ''}:
            dic_head = {}
        else:
            pass
        try:
            if data['radio'] == 1:
                response = requests.request(data['method'].upper(), url=url, headers=dic_head, data={})
            elif data['radio'] == 2:
                files = []
                response = requests.request(data['method'].upper(), url=url, headers=dic_head, data=dic_body,
                                            files=files)
            elif data['radio'] == 3:
                dic_head['Content-Type'] = 'application/x-www-form-urlencoded'
                response = requests.request(data['method'].upper(), url=url, headers=dic_head, data=dic_body)
            elif data['radio'] == 4:
                ic(dic_body)
                response = requests.request(data['method'].upper(), url=url, headers=dic_head,
                                            data=json.dumps(dic_body).encode('utf-8'))
            else:
                response = requests.request(data['method'].upper(), url=url, headers=dic_head, data={})
        except Exception as e:
            ic(e)
            dic = {
                "code": 503001,
                "data": "false",
                "msg": "非法API请求地址：请检查是否正确填写URL以及URL是否允许访问"
            }
            return HttpResponse(json.dumps(dic), content_type=RE.CONTENT_TYPE.value)

        response.encoding = "utf-8"
        ic(type(response.text))
        dic = {
            "code": 200,
            "data": response.text,
            "message": "ok"
        }
        return HttpResponse(json.dumps(dic), content_type=RE.CONTENT_TYPE.value)
    else:
        community(request, method)


# 用例查询
def getCases(request):
    method = "POST"
    if community(request, method) == RE.TRUE.value:
        try:
            data = json.loads(request.body)
            ic(data)
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
                        queryset = DbCases.objects.filter(project_id=data['listName'], is_delete=0).order_by('-id').all()
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
            print(e)
            dic = {
                "code": 30010,
                "data": [],
                "msg": "服务不可用，请联系管理员！",
                "totalCount": 0
            }
            return HttpResponse(json.dumps(dic), content_type=RE.CONTENT_TYPE.value)
    else:
        community(request, method)


# 用例删除
def CaseDel(request):
    method = "DELETE"
    if community(request, method) == RE.TRUE.value:
        data = json.loads(request.body)
        ic(data, type(data['ids']))
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
        community(request, method)


# 新增用例
def InNewCase(request):
    method = "POST"
    if community(request, method) == RE.TRUE.value:
        try:
            data = json.loads(request.body)
            ic(data)
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
            print(e)
            dic = {
                "code": 30010,
                "data": [],
                "msg": "服务不可用，请联系管理员！",
                "totalCount": 0
            }
            return HttpResponse(json.dumps(dic), content_type=RE.CONTENT_TYPE.value)
    else:
        community(request, method)


# 复制用例
def CopyCase(request):
    method = "POST"
    if community(request, method) == RE.TRUE.value:
        try:
            data = json.loads(request.body)
            ic(data)
            old_case = DbCases.objects.filter(id=data['ids'])[0]
            ic(old_case)
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
            print(e)
            dic = {
                "code": 30010,
                "data": [],
                "msg": "服务不可用，请联系管理员！",
                "totalCount": 0
            }
            return HttpResponse(json.dumps(dic), content_type=RE.CONTENT_TYPE.value)
    else:
        community(request, method)


# 用例编辑
def CaseEdit(request):
    method = "PUT"
    if community(request, method) == RE.TRUE.value:
        data = json.loads(request.body)
        ic(data)
        project_id = DbProject.objects.filter(listName=data['project_id']).values()[0]['id']
        DbCases.objects.filter(id=data['id']).update(des=data['des'], name=data['name'], project_id=project_id)
        return HttpResponse(json.dumps(RE.SUCCESS.value), content_type=RE.CONTENT_TYPE.value)
    else:
        community(request, method)


# 新增小用例
def SmallCase(request):
    method = "POST"
    if community(request, method) == RE.TRUE.value:
        data = json.loads(request.body)
        ic(data)
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
        community(request, method)


# 查询小用例
def SmallList(request):
    method = "POST"
    if community(request, method) == RE.TRUE.value:
        data = json.loads(request.body)
        ic(data)
        smalls = DbStep.objects.filter(Case_id=data['id'], is_delete=0).order_by('index').values()
        small = []
        for s in smalls:
            small.append(s)
        dic = {
            "code": 200,
            "data": small,
            "msg": "success",
        }
        return HttpResponse(json.dumps(dic), content_type=RE.CONTENT_TYPE.value)
    else:
        community(request, method)


# 删除小用例
def SmallDel(request):
    method = "DELETE"
    if community(request, method) == RE.TRUE.value:
        data = json.loads(request.body)
        ic(data)
        DbStep.objects.filter(Case_id=data['case_id'], index=data['ids']).update(is_delete=1)
        length = DbStep.objects.filter(Case_id=data['case_id'], is_delete=0).values().count()
        cases = DbStep.objects.filter(Case_id=data['case_id'], is_delete=0).values()
        i = 0
        for case in cases:
            i += 1
            DbStep.objects.filter(id=case['id']).update(index=i)
        return HttpResponse(json.dumps(RE.SUCCESS.value), content_type=RE.CONTENT_TYPE.value)
    else:
        community(request, method)


# 小用例下拉框查询接口
def SmallGet(request):
    method = "POST"
    if community(request, method) == RE.TRUE.value:
        data = json.loads(request.body)
        ic(data)
        lists = DbApis.objects.filter(project_id=data['project_id'], is_delete=0).values()
        small = []
        for s in lists:
            small.append(s)
        dic = {
            "code": 200,
            "data": small,
            "msg": "success",
        }
        return HttpResponse(json.dumps(dic), content_type=RE.CONTENT_TYPE.value)
    else:
        community(request, method)


# 保存接口
def SmallOrder(request):
    method = "POST"
    if community(request, method) == RE.TRUE.value:
        data = json.loads(request.body)
        ic(data)
        small_list = data['case']
        for small in small_list:
            api = DbApis.objects.filter(id=small['apiid']).values()[0]
            ic(api)
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
                ic(f'url不正确{apis}')
                return HttpResponse(json.dumps(dic), content_type=RE.CONTENT_TYPE.value)
            DbStep.objects.filter(id=small['id']).update(
                api_id=small['apiid'],
                index=small['index'],
                api_method=api['api_models'],
                api_host=host,
                api_url=path,
                api_header=api['api_header'],
                api_body=api['api_body'],
                api_body_method=api['body_method']
            )
        cases = DbStep.objects.filter(Case_id=data['case_id'], is_delete=0).order_by('index').values()
        i = 0
        for case in cases:
            i += 1
            DbStep.objects.filter(id=case['id']).update(index=i)
        return HttpResponse(json.dumps(RE.SUCCESS.value), content_type=RE.CONTENT_TYPE.value)
    else:
        community(request, method)


# 查看报告
def LookReport(request):
    method = "POST"
    if community(request, method) == RE.TRUE.value:
        data = json.loads(request.body)
        ic(data)
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
        community(request, method)
    else:
        community(request, method)


# 报告路径
def Report(request):
    try:
        return render(request, f'Reports/{case_ids}.html')
    except Exception as e:
        ic(e)
        return "TemplateDoesNotExist"


# 运行用例
def RunCase(request):
    method = "POST"
    if community(request, method) == RE.TRUE.value:
        data = json.loads(request.body)
        ic(data)
        Case_id = data['case_id']
        Case_name = DbCases.objects.filter(id=Case_id).values()[0]['name']
        Case = DbStep.objects.filter(Case_id=Case_id)[0]
        steps = DbStep.objects.filter(Case_id=Case_id)
        ic(data, Case, Case.id, Case.name, steps)
        # from My_api.run_case import run
        from My_api.Run import run
        run(Case.Case_id, Case_name, steps)

        dic = json.dumps(RE.SUCCESS.value)
        return HttpResponse(dic, content_type=RE.CONTENT_TYPE.value)
    else:
        community(request, method)


# 全局变量查询
def Variable(request):
    method = "POST"
    if community(request, method) == RE.TRUE.value:
        try:
            data = json.loads(request.body)
            ic(data)
            if "name" in data:
                queryset = DbGlobalData.objects.filter(name=data['name'], is_delete=0).order_by('-id').all()
            else:
                queryset = DbGlobalData.objects.filter(is_delete=0).order_by('-id').all()
            paginator = Paginator(queryset, data['pageSize'])
            page = paginator.get_page(data['pageNo'])
            lists = []
            for project in page.object_list.values():
                times = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.mktime(project['created_time'].timetuple())))
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
            print(e)
            dic = {
                "code": 30010,
                "data": [],
                "msg": "服务不可用，请联系管理员！",
                "totalCount": 0
            }
            return HttpResponse(json.dumps(dic), content_type=RE.CONTENT_TYPE.value)
    else:
        community(request, method)


# 全局变量编辑/新增
def DoEdit(request):
    method = "POST"
    if community(request, method) == RE.TRUE.value:
        data = json.loads(request.body)
        ic(data)
        if "id" in data:
            DbGlobalData.objects.filter(id=data['id']).update(
                name=data['name'],
                data=data['data'],
            )
        else:
            Authorization = request.headers['Accesstoken']
            user = decode_user(Authorization)
            ic(user)
            DbGlobalData.objects.create(
                name=data['name'],
                data=data['data'],
                user=user,
                created_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                is_delete=0
            )
        return HttpResponse(json.dumps(RE.SUCCESS.value), content_type=RE.CONTENT_TYPE.value)
    else:
        community(request, method)


# 全局变量删除
def GloDel(request):
    method = "DELETE"
    if community(request, method) == RE.TRUE.value:
        data = json.loads(request.body)
        ic(data, type(data['ids']))
        Id = data['ids']
        if type(Id) == int:
            DbGlobalData.objects.filter(id=Id).update(is_delete=1)
        else:
            ids = Id.split(',')
            for i in ids:
                DbGlobalData.objects.filter(id=i).update(is_delete=1)
        return HttpResponse(json.dumps(RE.SUCCESS.value), content_type=RE.CONTENT_TYPE.value)
    else:
        community(request, method)


class UserForm(forms.Form):
    filename = forms.FileField()


@csrf_exempt
def Runner(request):
    method = "POST"
    if community(request, method) == RE.TRUE.value:
        myFile = request.FILES.get("file", None)  # 获取上传的文件，如果没有文件，则默认为None
        ic(myFile)
        if not myFile:
            dic = {"code": 70010, "data": "true", "msg": "no files for upload!"}
            return HttpResponse(dic, content_type=RE.CONTENT_TYPE.value)
        destination = open(os.path.join("D:\\platform\\My_api\\static\\httprunner\\", myFile.name), 'wb+')  # 打开特定的文件进行二进制的写操作
        for chunk in myFile.chunks():  # 分块写入文件
            destination.write(chunk)
        destination.close()
        dic = {"code": 200, "data": "true", "msg": "上传成功！"}
        return HttpResponse(dic, content_type=RE.CONTENT_TYPE.value)
    else:
        community(request, method)


# 公共方法
def community(request, method):
    if request.method == method:
        if "Accesstoken" in request.headers:
            Authorization = request.headers['Accesstoken']
            if decode_time(Authorization):
                return RE.TRUE.value
            else:
                res = HttpResponse(json.dumps({"code": 402, "data": False, "msg": "token失效"}))
                res.status_code = 402
                return res
        else:
            res = HttpResponse(json.dumps({"code": 401, "data": False, "msg": "token为空"}))
            res.status_code = 401
            return res
    else:

        community(request, method)


# 测试接口
def testmetod(request):
    method = "GET"
    if community(request, method) == RE.TRUE.value:
        pass
    else:
        return community(request, method)
