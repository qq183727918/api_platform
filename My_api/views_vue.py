"""
_*_ coding: UTF-8 _*_
@Time      : 2021/4/8 16:19
@Author    : LiuXiaoQiang
@Site      : https://github.com/qq183727918
@File      : views_vue.py
@Software  : PyCharm
"""
import json
import time

import requests
from django.core.paginator import Paginator
from django.http import HttpResponse
# Create your views here.
from icecream import ic

from My_api.models import *
from My_api.static.params.return_params import RE
# Create your views here.
from My_api.static.public_method.public_method import decode_token


# 项目列表查询
def project_list(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        ic(data)
        if len(data) == 3:
            queryset = DbProject.objects.filter(listName=data['listName'], is_delete=0).all()
        else:
            queryset = DbProject.objects.filter(is_delete=0).all()
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
        dic = json.dumps(RE.WRONG_REQUEST.value)
        return HttpResponse(dic, content_type=RE.CONTENT_TYPE.value)


# 项目编辑
def project_edit(request):
    if request.method == 'POST':
        Authorization = request.headers['Accesstoken']
        user = decode_token(Authorization)
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
        dic = json.dumps(RE.WRONG_REQUEST.value)
        return HttpResponse(dic, content_type=RE.CONTENT_TYPE.value)


# 项目删除
def project_del(request):
    if request.method == 'DELETE':
        data = json.loads(request.body)
        ic(data)
        Id = data['ids']
        if type(Id) == int:
            DbProject.objects.filter(id=Id).update(is_delete=1)
        else:
            ids = Id.split(',')
            for i in ids:
                DbProject.objects.filter(id=i).update(is_delete=1)
        return HttpResponse(json.dumps(RE.SUCCESS.value), content_type=RE.CONTENT_TYPE.value)
    else:
        dic = json.dumps(RE.WRONG_REQUEST.value)
        return HttpResponse(dic, content_type=RE.CONTENT_TYPE.value)


# 接口查询
def project_Apis(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        ic(data)
        if "listName" in data:
            if DbProject.objects.filter(listName=data['listName'], is_delete=0, is_active=0).values().count() == 0:
                dic = {
                    "code": 200,
                    "data": [],
                    "msg": "success",
                    "totalCount": 0
                }
                return HttpResponse(json.dumps(dic), content_type=RE.CONTENT_TYPE.value)
            else:
                if "name" in data:
                    list_id = DbProject.objects.filter(listName=data['listName'], is_delete=0, is_active=0).values()[0][
                        'id']
                    queryset = DbApis.objects.filter(name=data['name'], project_id=list_id, is_delete=0).all()
                else:
                    list_id = DbProject.objects.filter(listName=data['listName'], is_delete=0, is_active=0).values()[0][
                        'id']
                    queryset = DbApis.objects.filter(project_id=list_id, is_delete=0).all()
        else:
            if "name" in data:
                queryset = DbApis.objects.filter(name=data['name'], is_delete=0).all()
            else:
                queryset = DbApis.objects.filter(is_delete=0).all()
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
        dic = json.dumps(RE.WRONG_REQUEST.value)
        return HttpResponse(dic, content_type=RE.CONTENT_TYPE.value)


# 用户查询
def user_select(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            ic(data)
            queryset = DbUser.objects.filter(is_delete=0).all()
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
        dic = json.dumps(RE.WRONG_REQUEST.value)
        return HttpResponse(dic, content_type=RE.CONTENT_TYPE.value)


# 用户禁用
def userDisable(request):
    if request.method == 'PUT':
        data = json.loads(request.body)
        ic(data)
        DbUser.objects.filter(id=data['ids']).update(is_active=1)
        return HttpResponse(json.dumps(RE.SUCCESS.value), content_type=RE.CONTENT_TYPE.value)
    else:
        dic = json.dumps(RE.WRONG_REQUEST.value)
        return HttpResponse(dic, content_type=RE.CONTENT_TYPE.value)


# 新增用户
def NewUser(request):
    if request.method == 'POST':
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
        dic = json.dumps(RE.WRONG_REQUEST.value)
        return HttpResponse(dic, content_type=RE.CONTENT_TYPE.value)


# 接口删除
def APisdel(request):
    if request.method == 'DELETE':
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
        dic = json.dumps(RE.WRONG_REQUEST.value)
        return HttpResponse(dic, content_type=RE.CONTENT_TYPE.value)


# 接口复制接口
def copy_apis(request):
    if request.method == 'POST':
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
        dic = json.dumps(RE.WRONG_REQUEST.value)
        return HttpResponse(dic, content_type=RE.CONTENT_TYPE.value)


# 接口备注、名称修改
def DesEdit(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        ic(data)
        Id = data['id']
        DbApis.objects.filter(id=Id).update(des=data['des'], name=data['name'])
        return HttpResponse(json.dumps(RE.SUCCESS.value), content_type=RE.CONTENT_TYPE.value)
    else:
        dic = json.dumps(RE.WRONG_REQUEST.value)
        return HttpResponse(dic, content_type=RE.CONTENT_TYPE.value)


# 新增接口
def SaveApis(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        ic(data)
        dic_head = {}
        dic_body = {}
        body_method = ''
        if DbProject.objects.filter(listName=data['project_name'], is_active=0, is_delete=0).values().count() == 0:
            return HttpResponse(json.dumps({"code": 10032, "data": "false", "msg": "输入的项目名称不存在"}),
                                content_type=RE.CONTENT_TYPE.value)
        name = DbProject.objects.filter(listName=data['project_name'], is_active=0, is_delete=0).values()[0]['id']
        api_name = data['api_name']
        method = data['method']
        url = data['url']
        api_body = data['api_body']
        radio = data['radio']
        tag = data['tag']
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
            project_id=name,
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
        dic = json.dumps(RE.WRONG_REQUEST.value)
        return HttpResponse(dic, content_type=RE.CONTENT_TYPE.value)


# 调试保存
def DebugApis(request):
    if request.method == 'POST':
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
        DbApis.objects.filter(id=data['project_id']).update(
            api_models=method,
            api_url=url,
            api_header=json.dumps(dic_head),
            api_body=json.dumps(dic_body),
            api_tag=tag,
            result=results,
            body_method=body_method,
        )
        return HttpResponse(json.dumps(RE.SUCCESS.value), content_type=RE.CONTENT_TYPE.value)
    else:
        dic = json.dumps(RE.WRONG_REQUEST.value)
        return HttpResponse(dic, content_type=RE.CONTENT_TYPE.value)


# 发送请求
def SendRequest(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        ic(data)
        dic_head = {}
        dic_body = {}
        response = ''
        url = data['url']
        radio = data['radio']
        tag = data['tag']
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
                dic_body = json.loads(data['api_body'])
        else:
            api_body = data['api_body']
            for head in api_body:
                dic_body[head['key']] = head['value']
        for head in data['header']:
            dic_head[head['key']] = head['value']
        if dic_head == {'': ''}:
            dic_head = {}
        else:
            pass
        if data['radio'] == 1:
            response = requests.request(data['method'].upper(), data['url'], headers=dic_head, data={})
        elif data['radio'] == 2:
            files = []
            response = requests.request(data['method'].upper(), data['url'], headers=dic_head, data=dic_body,
                                        files=files)
        elif data['radio'] == 3:
            dic_head['Content-Type'] = 'application/x-www-form-urlencoded'
            response = requests.request(data['method'].upper(), data['url'], headers=dic_head, data=dic_body)
        elif data['radio'] == 4:
            ic(dic_body)
            response = requests.request(data['method'].upper(), url, headers=dic_body,
                                        data=json.dumps(dic_body).encode('utf-8'))
        response.encoding = "utf-8"
        ic(type(response.text))
        dic = {
            "code": 200,
            "data": response.text,
            "message": "ok"
        }
        return HttpResponse(json.dumps(dic), content_type=RE.CONTENT_TYPE.value)
    else:
        dic = json.dumps(RE.WRONG_REQUEST.value)
        return HttpResponse(dic, content_type=RE.CONTENT_TYPE.value)


# 用例查询
def getCases(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            ic(data)
            if "listName" in data:
                if DbProject.objects.filter(listName=data['listName'], is_delete=0, is_active=0).values().count() == 0:
                    dic = {
                        "code": 200,
                        "data": [],
                        "msg": "success",
                        "totalCount": 0
                    }
                    return HttpResponse(json.dumps(dic), content_type=RE.CONTENT_TYPE.value)
                else:
                    if "name" in data:
                        list_id = DbProject.objects.filter(listName=data['listName'], is_delete=0, is_active=0).values()[0][
                            'id']
                        queryset = DbCases.objects.filter(name=data['name'], project_id=list_id, is_delete=0).all()
                    else:
                        list_id = DbProject.objects.filter(listName=data['listName'], is_delete=0, is_active=0).values()[0][
                            'id']
                        queryset = DbCases.objects.filter(project_id=list_id, is_delete=0).all()
            else:
                if "name" in data:
                    queryset = DbCases.objects.filter(name=data['name'], is_delete=0).all()
                else:
                    queryset = DbCases.objects.filter(is_delete=0).all()
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
        dic = json.dumps(RE.WRONG_REQUEST.value)
        return HttpResponse(dic, content_type=RE.CONTENT_TYPE.value)


# 用例删除
def CaseDel(request):
    if request.method == 'DELETE':
        data = json.loads(request.body)
        ic(data, type(data['ids']))
        Id = data['ids']
        if type(Id) == int:
            DbCases.objects.filter(id=Id).update(is_delete=1)
        else:
            ids = Id.split(',')
            for i in ids:
                DbCases.objects.filter(id=i).update(is_delete=1)
        return HttpResponse(json.dumps(RE.SUCCESS.value), content_type=RE.CONTENT_TYPE.value)
    else:
        dic = json.dumps(RE.WRONG_REQUEST.value)
        return HttpResponse(dic, content_type=RE.CONTENT_TYPE.value)


# 新增用例
def InNewCase(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            ic(data)
            if DbProject.objects.filter(listName=data['listName'], is_active=0, is_delete=0).values().count() == 0:
                return HttpResponse(json.dumps({"code": 10032, "data": "false", "msg": "输入的项目名称不存在"}),
                                    content_type=RE.CONTENT_TYPE.value)
            name = DbProject.objects.filter(listName=data['listName'], is_active=0, is_delete=0).values()[0]['id']
            curr_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            DbCases.objects.create(
                project_id=name,
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
        dic = json.dumps(RE.WRONG_REQUEST.value)
        return HttpResponse(dic, content_type=RE.CONTENT_TYPE.value)


# 复制用例
def CopyCase(request):
    if request.method == 'POST':
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
        dic = json.dumps(RE.WRONG_REQUEST.value)
        return HttpResponse(dic, content_type=RE.CONTENT_TYPE.value)


# 用例编辑
def CaseEdit(request):
    if request.method == 'PUT':
        data = json.loads(request.body)
        ic(data)
        if DbProject.objects.filter(listName=data['listName'], is_active=0, is_delete=0).values().count() == 0:
            return HttpResponse(json.dumps({"code": 10032, "data": "false", "msg": "输入的项目名称不存在"}),
                                content_type=RE.CONTENT_TYPE.value)
        name = DbProject.objects.filter(listName=data['listName'], is_active=0, is_delete=0).values()[0]['id']
        DbCases.objects.filter(id=data['id']).update(des=data['des'], name=data['name'], project_id=name)
        return HttpResponse(json.dumps(RE.SUCCESS.value), content_type=RE.CONTENT_TYPE.value)
    else:
        dic = json.dumps(RE.WRONG_REQUEST.value)
        return HttpResponse(dic, content_type=RE.CONTENT_TYPE.value)
