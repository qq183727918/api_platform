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

from django.http import HttpResponse
# Create your views here.
from icecream import ic

from My_api.models import *
from My_api.static.params.return_params import RE
from django.core.paginator import Paginator


# Create your views here.
from My_api.static.public_method.public_method import decode_token


def project_list(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        ic(len(data))
        if len(data) == 3:
            queryset = DbProject.objects.filter(listName=data['listName'], is_delete=0).all()
        else:
            queryset = DbProject.objects.filter(is_delete=0).all()
        paginator = Paginator(queryset, data['pageSize'])
        page = paginator.get_page(data['pageNo'])
        ic(page.object_list.values())
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
            ic(others)
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


def project_Apis(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        ic(len(data))
        if len(data) == 3:
            if DbProject.objects.filter(listName=data['listName'], is_delete=0, is_active=0).values().count() == 0:
                dic = {
                    "code": 200,
                    "data": [],
                    "msg": "success",
                    "totalCount": 0
                }
                return HttpResponse(json.dumps(dic), content_type=RE.CONTENT_TYPE.value)
            else:
                list_id = DbProject.objects.filter(listName=data['listName'], is_delete=0, is_active=0).values()[0]['id']
                queryset = DbApis.objects.filter(project_id=list_id, is_delete=0).all()
        else:
            queryset = DbApis.objects.filter(is_delete=0).all()
        paginator = Paginator(queryset, data['pageSize'])
        page = paginator.get_page(data['pageNo'])
        ic(page.object_list.values())
        lists = []
        for project in page.object_list.values():
            listName = DbProject.objects.filter(id=project['project_id']).values()[0]['listName']
            ic(listName)
            project['listName'] = listName
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

