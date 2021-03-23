"""
_*_ coding: UTF-8 _*_
@Time      : 2021/3/23 16:47
@Author    : LiuXiaoQiang
@Site      : https://github.com/qq183727918
@File      : views_api.py
@Software  : PyCharm
"""
import json
import re
import time

import requests
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
# Create your views here.
from icecream import ic

from My_api.models import *
from My_api.static.params.return_params import RE


# 返回子页面
def child(request, eid, oid, ooid):
    ic('child', eid, oid, ooid)
    res = child_json(eid, oid, ooid)
    return render(request, eid, res)


# 控制不同页面返回不同的数据：数据分发器
def child_json(eid, oid='', ooid=''):
    ic(eid, oid, ooid)
    res = {}
    if eid == 'home.html':
        date = DbHomeHref.objects.all()
        home_log = DbApisLog.objects.filter(user_id=oid)[::-1]
        hosts = DbHost.objects.all()
        user_projects = DbProject.objects.filter(user=DbUser.objects.filter(id=oid)[0].username)

        # 个人数据看板
        count_project = len(user_projects)
        count_api = sum([len(DbApis.objects.filter(project_id=i.id)) for i in user_projects])
        count_case = sum([len(DbCases.objects.filter(project_id=i.id)) for i in user_projects])

        ziyuan_all = len(DbProject.objects.all()) + len(DbApis.objects.all()) + len(DbCases.objects.all())
        ziyuan_user = count_project + count_api + count_case
        if ziyuan_all == 0:
            ziyuan = ziyuan_user * 100
        else:
            ziyuan = ziyuan_user / ziyuan_all * 100

        new_res = {
            "count_project": count_project,
            "count_api": count_api,
            "count_case": count_case,
            "count_report": '',
            "ziyuan": ziyuan,
        }
        if ooid == '':
            res = {"hrefs": date, "home_log": home_log, "hosts": hosts, "user_projects": user_projects}
        else:
            log = DbApisLog.objects.filter(id=ooid)[0]
            res = {"hrefs": date, "home_log": home_log, "log": log, hosts: "hosts", "user_projects": user_projects}
        res.update(new_res)

    if eid == 'project_list.html':
        date = DbProject.objects.filter(is_delete=0)
        res = {"projects": date}
        ic(date)

    if eid == 'P_apis.html':
        project = DbProject.objects.filter(id=oid)[0]
        apis = DbApis.objects.filter(project_id=oid, is_delete=0)

        for i in apis:
            try:
                i.short_url = i.api_url.split('?')[0][:50]
            except:
                i.short_url = ''
        project_header = DbProjectHeader.objects.filter(project_id=oid)
        hosts = DbHost.objects.all()
        project_host = DbProjectHost.objects.filter(project_id=oid)
        res = {"project": project, 'apis': apis, 'project_header': project_header, 'hosts': hosts,
               'project_host': project_host}
        ic(res)

    if eid == 'P_project_set.html':
        project = DbProject.objects.filter(id=oid)[0]
        res = {"project": project}
        ic(project)

    if eid == 'P_cases.html':
        # 这里应该是去数据库拿到这个项目的所有用例
        project = DbProject.objects.filter(id=oid)[0]
        Cases = DbCases.objects.filter(project_id=oid)
        apis = DbApis.objects.filter(project_id=oid)
        project_header = DbProjectHeader.objects.filter(project_id=oid)
        hosts = DbHost.objects.all()
        project_host = DbProjectHost.objects.filter(project_id=oid)
        res = {"project": project, "Cases": Cases, "apis": apis, 'project_header': project_header, 'hosts': hosts,
               'project_host': project_host}

    if eid == 'P_global_data.html':
        project = DbProject.objects.filter(id=oid)[0]
        global_data_s = DbGlobalData.objects.filter(user_id=project.user_id)
        res = {"project": project, "global_data": global_data_s}
        ic(res)

    if eid == 'user.html':
        add = []
        users = DbUser.objects.filter(is_delete=0).values()
        for i in users:
            i['is_active'] = '启用'
            add.append(i)
        ic(add)
        res = {"users": users}
        ic(users)

    return res


# 获取公共字典
def glodict(request):
    user_data = DbUser.objects.filter(id=1).values()[0]
    userimg = str(user_data['id']) + '.png'  # 这里我们写死png后缀，因为上传时候我们也可以强行弄成这个png后缀
    res = {"username": user_data['username'], "userimg": userimg}
    return res


# 上传用户头像
def user_upload(request):
    file = request.FILES.get("fileUpload", None)  # 靠name获取上传的文件，如果没有，避免报错，设置成None

    if not file:
        return HttpResponseRedirect('/home/')  # 如果没有则返回到首页

    new_name = str(request.user.id) + '.png'  # 设置好这个新图片的名字
    ic(new_name)
    destination = open(r"D:\platform\My_api\static\img\\" + new_name, 'wb')  # 打开特定的文件进行二进制的写操作
    for chunk in file.chunks():  # 分块写入文件
        destination.write(chunk)
    destination.close()

    return HttpResponseRedirect('/home/')  # 返回到首页


# 登录
def login_action(request):
    if request.method == "POST":
        data = json.loads(request.body)
        u_name = data['username']
        p_word = data['password']
        ic(u_name, p_word, data)
        if u_name == '':
            dic = json.dumps({"code": 30001, "data": "false", "message": "请输入账号"})
            return HttpResponse(dic, content_type=RE.CONTENT_TYPE.value)
        if p_word == '':
            dic = json.dumps({"code": 30002, "data": "false", "message": "请输入密码"})
            return HttpResponse(dic, content_type=RE.CONTENT_TYPE.value)
        # 开始联通用户库，查看用户密码是否正确
        username = DbUser.objects.filter(username=u_name).values()

        if username.count() == 0:
            dic = json.dumps({"code": 30003, "data": "false", "message": "用户名不存在请检查"})
            return HttpResponse(dic, content_type=RE.CONTENT_TYPE.value)
        else:
            for name in username:
                if u_name == name['username']:
                    if p_word == name['password']:
                        dic = json.dumps({"code": 200, "data": "false", "message": "成功"})
                        return HttpResponse(dic, content_type=RE.CONTENT_TYPE.value)
                    else:
                        dic = json.dumps({"code": 30004, "data": "false", "message": "密码错误，请重试！"})
                        return HttpResponse(dic, content_type=RE.CONTENT_TYPE.value)
    else:
        dic = json.dumps(RE.WRONG_REQUEST.value)
        return HttpResponse(dic, content_type=RE.CONTENT_TYPE.value)


# 注册
def sign_action(request):
    if request.method == "POST":
        data = json.loads(request.body)
        u_name = data["username"]
        p_word = data["password"]
        ic(u_name, p_word)
        if u_name in ['', None]:
            dic = json.dumps({"code": 30001, "data": "false", "message": "请输入账号"})
            return HttpResponse(dic, content_type=RE.CONTENT_TYPE.value)
        if p_word in ['', None]:
            dic = json.dumps({"code": 30002, "data": "false", "message": "请输入密码"})
            return HttpResponse(dic, content_type=RE.CONTENT_TYPE.value)
        username = DbUser.objects.filter(username=u_name).values().count()
        ic(username)
        if username == 0:
            # 开始关联django用户表
            DbUser.objects.create(username=u_name, password=p_word, is_delete=0, is_active=0)
            dic = json.dumps({"code": 200, "data": "false", "message": "注册成功！"})
            return HttpResponse(dic, content_type=RE.CONTENT_TYPE.value)
        else:
            dic = json.dumps({"code": 30005, "data": "false", "message": "注册失败~用户名好像已经存在了~"})
            return HttpResponse(dic, content_type=RE.CONTENT_TYPE.value)
    else:
        dic = json.dumps(RE.WRONG_REQUEST.value)
        return HttpResponse(dic, content_type=RE.CONTENT_TYPE.value)


# 退出
def logout(request):
    from django.contrib import auth

    auth.logout(request)

    return HttpResponseRedirect('/login/')


# 吐槽
def pei(request):
    Roast_input = request.GET['Roast_input']
    ic(Roast_input)

    DB_Roast.objects.create(user=request.user.username, text=Roast_input)

    return HttpResponse(Roast_input)


# 删除项目
def delete_project(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        Id = data['id']
        ic(Id)
        DbProject.objects.filter(id=Id).update(is_delete=1)
        DbApis.objects.filter(project_id=Id).update(is_delete=1)  # 删除旗下接口

        all_Case = DbCases.objects.filter(project_id=Id)
        for i in all_Case:
            DbStep.objects.filter(Case_id=i.id).update(is_delete=1)  # 删除步骤
            i.update(is_delete=1)  # 用例删除自己
        return HttpResponseRedirect('')
    else:
        dic = json.dumps(RE.WRONG_REQUEST.value)
        return HttpResponse(dic, content_type=RE.CONTENT_TYPE.value)


# 新增项目
def add_project(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        list_po = data['list_po']
        project_name = data['project_name']
        project_remark = data['project_remark']
        ic(list_po, project_name, project_remark)
        username = DbUser.objects.filter(username=list_po, is_delete=0, is_active=0).values().count()
        if username == 0:
            return HttpResponse('输入管理员不存在或未启用，请重新输入！')
        else:
            others = DbUser.objects.filter(username=list_po, is_delete=0, is_active=0).values()[0]
            ic(others)
            DbProject.objects.create(name=project_name,
                                     remark=project_remark,
                                     user=others['username'],
                                     user_id=others['id'],
                                     other=list_po,
                                     is_delete=0)
            return HttpResponse('成功')


# 保存项目设置
def save_project_set(request, id):
    if request.method == 'POST':
        data = json.loads(request.body)
        project_id = id
        ic(project_id)
        name = data['name']
        remark = data['remark']
        other_user = data['other_user']
        ic(project_id, name, remark, other_user)
        username = DbUser.objects.filter(username=other_user, is_delete=0, is_active=0).values().count()
        if username == 0:
            dic = json.dumps({'code': 31002, 'data': True, 'message': '输入管理员不存在或未启用，请重新输入!'})
            return HttpResponse(dic, content_type=RE.CONTENT_TYPE.value)
        else:
            others = DbUser.objects.filter(username=other_user, is_delete=0, is_active=0).values()[0]
            ic(others)
            DbProject.objects.filter(id=project_id).update(name=name, remark=remark, other=other_user)
            dic = json.dumps({'code': 200, 'data': True, 'message': 'ok'})
            return HttpResponse(dic, content_type=RE.CONTENT_TYPE.value)
    else:
        dic = json.dumps(RE.WRONG_REQUEST.value)
        return HttpResponse(dic, content_type=RE.CONTENT_TYPE.value)


# 新增接口
def project_api_add(request, Pid):
    project_id = Pid
    ic(project_id)
    DbApis.objects.create(project_id=project_id,
                          name='',
                          api_models='',
                          api_url='',
                          api_header='',
                          is_delete=0)
    return HttpResponseRedirect('/apis/%s/' % project_id)


# 删除接口
def project_api_del(request, id):
    project_id = DbApis.objects.filter(id=id)[0].project_id
    DbApis.objects.filter(id=id).update(is_delete=1)
    return HttpResponseRedirect('/apis/%s/' % project_id)


# 备注保存接口
def save_bz(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        api_id = data['api_id']
        bz_value = data['bz_value']
        ic(bz_value)
        DbApis.objects.filter(id=api_id).update(des=bz_value)
        dic = json.dumps({'code': 200, 'data': True, 'message': '成功'})
        return HttpResponse(dic, content_type=RE.CONTENT_TYPE.value)
    else:
        dic = json.dumps(RE.WRONG_REQUEST.value)
        return HttpResponse(dic, content_type=RE.CONTENT_TYPE.value)


# 备注获取接口
def get_bz(request):
    if request.method == 'GET':
        api_id = request.GET['api_id']
        bz_value = DbApis.objects.filter(id=api_id)[0].des
        ic(bz_value)
        dic = json.dumps({"code": 200, "data": "true", "message": {"bz_value": f"{bz_value}"}})
        return HttpResponse(dic, content_type=RE.CONTENT_TYPE.value)
    else:
        dic = json.dumps(RE.WRONG_REQUEST.value)
        return HttpResponse(dic, content_type=RE.CONTENT_TYPE.value)


# 保存接口
def Api_save(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        api_id = data['api_id']
        ts_method = data['ts_method']
        ts_url = data['ts_url']
        ts_host = data['ts_host']
        ts_login = data['ts_login']
        ts_header = data['ts_header']
        ts_body_method = data['ts_body_method']
        api_name = data['api_name']
        ts_project_headers = data['ts_project_headers']
        ic(api_id, ts_method, ts_url, ts_host, ts_header, ts_body_method, api_name)

        if ts_body_method == '返回体':
            api = DbApis.objects.filter(id=api_id).values()[0]
            ic(api)
            ts_body_method = api['last_body_method']
            ts_api_body = api['last_api_body']
            ic(ts_body_method, ts_body_method)
        else:
            ts_api_body = data['ts_api_body']
            ic(ts_api_body)
        print(ts_project_headers)
        # 保存数据
        DbApis.objects.filter(id=api_id).update(
            api_models=ts_method,
            api_url=ts_url,
            api_login=ts_login,
            api_host=ts_host,
            api_header=ts_header,
            body_method=ts_body_method,
            api_body=ts_api_body,
            name=api_name,
            public_header=ts_project_headers
        )

        dic = json.dumps({"code": 200, "data": "true", "message": "success"})
        return HttpResponse(dic, content_type=RE.CONTENT_TYPE.value)
    else:
        dic = json.dumps(RE.WRONG_REQUEST.value)
        return HttpResponse(dic, content_type=RE.CONTENT_TYPE.value)


# 查询接口内容
def get_api_data(request):
    if request.method == 'GET':
        api_id = request.GET['api_id']
        api = DbApis.objects.filter(id=api_id).values()[0]
        return HttpResponse(json.dumps(api), content_type='application/json')
    else:
        dic = json.dumps(RE.WRONG_REQUEST.value)
        return HttpResponse(dic, content_type=RE.CONTENT_TYPE.value)


# 调试层发送请求
def Api_send(request):
    if request.method == 'POST':
        datas = json.loads(request.body)
        ic(datas)
        # 提取所有数据
        api_id = datas['api_id']
        ts_method = datas['ts_method']
        ts_url = datas['ts_url']
        ts_host = datas['ts_host']
        ts_header = datas['ts_header']
        api_name = datas['api_name']
        ts_body_method = datas['ts_body_method']
        ts_project_headers = datas['ts_project_headers'].split(',')
        ts_login = datas['ts_login']
        if ts_login == 'yes':  # 说明要调用登陆态了
            login_res = project_login_send_for_other(project_id=DbApis.objects.filter(id=api_id)[0].project_id)
        else:
            login_res = {}
        # 处理域名host
        if ts_host[:4] == '全局域名':
            project_host_id = ts_host.split('-')[1]
            ts_host = DbProjectHost.objects.filter(id=project_host_id)[0].host
        if ts_body_method == '返回体':
            api = DbApis.objects.filter(id=api_id)[0]
            ts_body_method = api.last_body_method
            ts_api_body = api.last_api_body
            if ts_body_method in ['', None]:
                return HttpResponse('请先选择好请求体编码格式和请求体，再点击Send按钮发送请求！')
        else:
            ts_api_body = datas['ts_api_body']
            api = DbApis.objects.filter(id=api_id)
            api.update(last_body_method=ts_body_method, last_api_body=ts_api_body)
        # 发送请求获取返回值
        if ts_header == '':
            ts_header = '{}'
        try:
            header = json.loads(ts_header)  # 处理header
        except:
            return HttpResponse('请求头不符合json格式！')

        for i in ts_project_headers:
            if i != '':
                project_header = DbProjectHeader.objects.filter(id=i)[0]
                header[project_header.key] = project_header.value
        # 拼接完整url
        if ts_host[-1] == '/' and ts_url[0] == '/':  # 都有/
            url = ts_host[:-1] + ts_url
        elif ts_host[-1] != '/' and ts_url[0] != '/':  # 都没有/
            url = ts_host + '/' + ts_url
        else:  # 肯定有一个有/
            url = ts_host + ts_url
        # 插入登陆态字段
        ## url插入
        if '?' not in url:
            url += '?'
            if type(login_res) == dict:
                for i in login_res.keys():
                    url += i + '=' + login_res[i] + '&'
        else:  # 证明已经有参数了
            if type(login_res) == dict:
                for i in login_res.keys():
                    url += '&' + i + '=' + login_res[i]

        ## header插入
        if type(login_res) == dict:
            header.update(login_res)

        try:
            if ts_body_method == 'none':
                if type(login_res) == dict:
                    response = requests.request(ts_method.upper(), url, headers=header, data={})
                else:
                    response = login_res.request(ts_method.upper(), url, headers=header, data={})

            elif ts_body_method == 'form-data':
                files = []
                payload = {}
                for i in eval(ts_api_body):
                    payload[i[0]] = i[1]
                if type(login_res) == dict:
                    for i in login_res.keys():
                        payload[i] = login_res[i]
                    response = requests.request(ts_method.upper(), url, headers=header, data=payload, files=files)
                else:
                    response = login_res.request(ts_method.upper(), url, headers=header, data=payload, files=files)

            elif ts_body_method == 'x-www-form-urlencoded':
                header['Content-Type'] = 'application/x-www-form-urlencoded'
                payload = {}
                for i in eval(ts_api_body):
                    payload[i[0]] = i[1]
                if type(login_res) == dict:
                    for i in login_res.keys():
                        payload[i] = login_res[i]
                        ic(url, i)
                    response = requests.request(ts_method.upper(), url, headers=header, data=payload)
                else:
                    response = login_res.request(ts_method.upper(), url, headers=header, data=payload)

            elif ts_body_method == 'GraphQL':
                header['Content-Type'] = 'application/json'
                query = ts_api_body.split('*WQRF*')[0]
                graphql = ts_api_body.split('*WQRF*')[1]
                try:
                    eval(graphql)
                except:
                    graphql = '{}'
                payload = '{"query":"%s","variables":%s}' % (query, graphql)
                if type(login_res) == dict:
                    response = requests.request(ts_method.upper(), url, headers=header, data=payload)
                else:
                    response = login_res.request(ts_method.upper(), url, headers=header, data=payload)

            else:  # 这时肯定是raw的五个子选项：
                if ts_body_method == 'Text':
                    header['Content-Type'] = 'text/plain'

                if ts_body_method == 'JavaScript':
                    header['Content-Type'] = 'text/plain'

                if ts_body_method == 'Json':
                    ts_api_body = json.loads(ts_api_body)
                    for i in login_res.keys():
                        ts_api_body[i] = login_res[i]
                    ts_api_body = json.dumps(ts_api_body)
                    header['Content-Type'] = 'text/plain'

                if ts_body_method == 'Html':
                    header['Content-Type'] = 'text/plain'

                if ts_body_method == 'Xml':
                    header['Content-Type'] = 'text/plain'
                if type(login_res) == dict:
                    response = requests.request(ts_method.upper(), url, headers=header,
                                                data=ts_api_body.encode('utf-8'))
                else:
                    response = login_res.request(ts_method.upper(), url, headers=header,
                                                 data=ts_api_body.encode('utf-8'))
            # 把返回值传递给前端页面
            response.encoding = "utf-8"

            DbHost.objects.update_or_create(host=ts_host, is_delete=0)
            ic(response.json())
            dic = json.dumps({"code": 200, "data": True, "massage": f"{response.text}"})
            return HttpResponse(dic, content_type=RE.CONTENT_TYPE.value)
        except Exception as e:
            dic = json.dumps({'code': 10010, 'data': False, 'massage': f'{e}'})
            return HttpResponse(dic, content_type=RE.CONTENT_TYPE.value)
    else:
        dic = json.dumps(RE.WRONG_REQUEST.value)
        return HttpResponse(dic, content_type=RE.CONTENT_TYPE.value)


# 复制接口
def copy_api(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        api_id = data['api_id']
        # 开始复制接口
        old_api = DbApis.objects.filter(id=api_id)[0]
        ic(old_api)
        ic(DbApis.objects.filter(id=api_id).values()[0])

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


# 异常值发送请求
def error_request(request):
    # ic(request)
    api_id = request.GET['api_id']
    # ic(api_id)
    new_body = request.GET['new_body']
    ic(new_body)
    span_text = request.GET['span_text']
    # 验证下请求体是不是新的替换过
    # ic(api_id)

    api = DbApis.objects.filter(id=api_id)[0]
    method = api.api_models
    url = api.api_url
    host = api.api_host
    header = api.api_header
    body_method = api.body_method

    if header == '':
        header = '{}'

    # 处理域名host
    if host[:4] == '全局域名':
        project_host_id = host.split('-')[1]
        ic(DbProjectHost.objects.filter(id=project_host_id)[0])
        host = DbProjectHost.objects.filter(id=project_host_id)[0].host

    try:
        # 发送请求获取返回值
        header = json.loads(header)  # 处理header
    except Exception as e:
        return HttpResponse(f'请求头不符合json格式！原因：{e}')

    if host[-1] == '/' and url[0] == '/':  # 都有/
        url = host[:-1] + url
    elif host[-1] != '/' and url[0] != '/':  # 都没有/
        url = host + '/' + url
    else:  # 肯定有一个有/
        url = host + url
    ic(host)
    try:
        if body_method == 'form-data':
            files = []
            payload = {}
            for i in eval(new_body):
                payload[i[0]] = i[1]
            response = requests.request(method.upper(), url, headers=header, data=payload, files=files)

        elif body_method == 'x-www-form-urlencoded':
            ic('x-www-form-urlencoded')
            ic('url', url)
            header['Content-Type'] = 'application/x-www-form-urlencoded'
            payload = {}
            for i in eval(new_body):
                payload[i[0]] = i[1]
            response = requests.request(method.upper(), url, headers=header, data=payload)
        elif body_method == 'Json':
            header['Content-Type'] = 'text/plain'
            response = requests.request(method.upper(), url, headers=header, data=new_body.encode('utf-8'))
        else:
            return HttpResponse('非法的请求体类型')
        # 把返回值传递给前端页面
        response.encoding = "utf-8"
        res_json = {"response": response.text, "span_text": span_text}
        ic(f'正常{res_json}')
        return HttpResponse(json.dumps(res_json), content_type='application/json')
    except Exception as e:
        res_json = {"response": "对不起，接口未通！", "span_text": span_text, "原因是": e}
        return HttpResponse(json.dumps(res_json), content_type='application/json')


# 首页发送请求
def Api_send_home(request):
    ic(request)
    # 提取所有数据
    ts_method = request.GET['ts_method']
    ic(ts_method)
    ts_url = request.GET['ts_url']
    ts_host = request.GET['ts_host']
    ts_header = request.GET['ts_header']
    ts_body_method = request.GET['ts_body_method']
    ts_api_body = request.GET['ts_api_body']
    ic(ts_api_body)
    # 发送请求获取返回值

    if ts_header == '':
        ts_header = '{}'
    try:
        header = json.loads(ts_header)  # 处理header
    except Exception as e:
        return HttpResponse(f'请求头不符合json格式！,原因为：{e}')
    # 写入到数据库请求记录中
    DbApisLog.objects.create(
        user_id=1,
        api_method=ts_method,
        api_url=ts_url,
        api_header=ts_header,
        api_host=ts_host,
        body_method=ts_body_method,
        api_body=ts_api_body,
        is_delete=0
    )

    # 拼接完整url
    if ts_host[-1] == '/' and ts_url[0] == '/':  # 都有/
        url = ts_host[:-1] + ts_url
    elif ts_host[-1] != '/' and ts_url[0] != '/':  # 都没有/
        url = ts_host + '/' + ts_url
    else:  # 肯定有一个有/
        url = ts_host + ts_url
    try:
        if ts_body_method == 'none':
            response = requests.request(ts_method.upper(), url, headers=header, data={})

        elif ts_body_method == 'form-data':
            files = []
            payload = {}
            for i in eval(ts_api_body):
                payload[i[0]] = i[1]
            response = requests.request(ts_method.upper(), url, headers=header, data=payload, files=files)

        elif ts_body_method == 'x-www-form-urlencoded':
            header['Content-Type'] = 'application/x-www-form-urlencoded'
            payload = {}
            for i in eval(ts_api_body):
                payload[i[0]] = i[1]
            response = requests.request(ts_method.upper(), url, headers=header, data=payload)

        elif ts_body_method == 'GraphQL':
            header['Content-Type'] = 'application/x-www-form-urlencoded'
            query = ts_api_body.split('*WQRF*')[0]
            graphql = ts_api_body.split('*WQRF*')[1]
            try:
                eval(graphql)
            except:
                graphql = {}
            payload = f'{"query": {query}, "variables": {graphql}}'
            response = requests.request(ts_method.upper(), url, headers=header, data=payload)

        else:  # 这时肯定是raw的五个子选项：
            if ts_body_method == 'Text':
                header['Content-Type'] = 'text/plain'

            if ts_body_method == 'JavaScript':
                header['Content-Type'] = 'text/plain'

            if ts_body_method == 'Json':
                header['Content-Type'] = 'text/plain'

            if ts_body_method == 'Html':
                header['Content-Type'] = 'text/plain'

            if ts_body_method == 'Xml':
                header['Content-Type'] = 'text/plain'
            response = requests.request(ts_method.upper(), url, headers=header, data=ts_api_body.encode('utf-8'))

        # 把返回值传递给前端页面
        response.encoding = "utf-8"
        DbHost.objects.update_or_create(host=ts_host, is_delete=0)
        return HttpResponse(response.text)
    except Exception as e:
        return HttpResponse(str(e))


# 首页获取请求记录
def get_home_log(request):
    user_id = request.user.id
    all_logs = DbApisLog.objects.filter(user_id=1).values()
    ret = {"all_log": list(all_logs.values("id", "api_method", 'api_host', "api_url"))[::-1]}
    return HttpResponse(json.dumps(ret), content_type='application/json')


# 获取完整的单一的请求记录数据
def get_api_log_home(request):
    log_id = request.GET['log_id']
    log = DbApisLog.objects.filter(id=log_id)
    ret = {"log": list(log.values())[0]}
    ic(ret)
    return HttpResponse(json.dumps(ret), content_type='application/json')


# 增加用例
def add_case(request, eid):
    DbCases.objects.create(project_id=eid, name='', is_delete=0)
    return HttpResponseRedirect('/cases/%s/' % eid)


# 删除用例
def del_case(request, eid, oid):
    DbCases.objects.filter(id=oid).delete()
    return HttpResponseRedirect('/cases/%s/' % eid)


# 复制用例
def copy_case(request, eid, oid):
    old_case = DbCases.objects.filter(id=oid)[0]
    DbCases.objects.create(project_id=old_case.project_id, name=old_case.name + '_副本')
    return HttpResponseRedirect('/cases/%s/' % eid)


# 获取小用例步骤的数据
def get_small(request):
    case_id = request.GET['case_id']
    ic(case_id)
    steps = DbStep.objects.filter(Case_id=case_id).order_by('index')
    ret = {"all_steps": list(steps.values("index", "id", "name"))}
    return HttpResponse(json.dumps(ret), content_type='application/json')


# 新增小步骤
def add_new_step(request):
    Case_id = request.GET['Case_id']
    ic('add', Case_id)
    a = DbStep.objects.filter(Case_id=Case_id)
    ic(a)
    all_len = len(DbStep.objects.filter(Case_id=Case_id))
    DbStep.objects.create(Case_id=Case_id, name='我是新步骤', index=all_len + 1, is_delete=0)
    return HttpResponse('')


# 删除小步骤
def delete_step(request, eid):
    ic(eid)
    step = DbStep.objects.filter(id=eid)[0]  # 获取待删除的step
    ic(step)
    index = step.index  # 获取目标index
    Case_id = step.Case_id  # 获取目标所属大用例id
    step.delete()  # 删除目标step
    # 遍历所有该大用例下的步骤中 顺序号大于目标index的步骤
    for i in DbStep.objects.filter(Case_id=Case_id).filter(index=index):
        i.index -= 1  # 执行顺序自减1
        i.save()

    return HttpResponse('')


# 获取小步骤数据
def get_step(request):
    step_id = request.GET['step_id']
    step = DbStep.objects.filter(id=step_id)
    steplist = list(step.values())[0]

    return HttpResponse(json.dumps(steplist), content_type="application/json")


# 保存小步骤
def save_step(request):
    step_id = request.GET['step_id']
    name = request.GET['name']
    index = request.GET['index']
    step_method = request.GET['step_method']
    step_url = request.GET['step_url']
    step_host = request.GET['step_host']
    step_header = request.GET['step_header']
    ts_project_headers = request.GET['ts_project_headers']
    ic(ts_project_headers)
    mock_res = request.GET['mock_res']
    step_body_method = request.GET['step_body_method']
    step_api_body = request.GET['step_api_body']
    get_path = request.GET['get_path']
    get_zz = request.GET['get_zz']
    assert_zz = request.GET['assert_zz']
    assert_qz = request.GET['assert_qz']
    assert_path = request.GET['assert_path']
    step_login = request.GET['step_login']

    DbStep.objects.filter(id=step_id).update(name=name,
                                             index=index,
                                             api_method=step_method,
                                             api_url=step_url,
                                             api_host=step_host,
                                             api_header=step_header,
                                             public_header=ts_project_headers,
                                             mock_res=mock_res,
                                             api_body_method=step_body_method,
                                             api_body=step_api_body,
                                             get_path=get_path,
                                             get_zz=get_zz,
                                             assert_zz=assert_zz,
                                             assert_qz=assert_qz,
                                             assert_path=assert_path,
                                             api_login=step_login,
                                             )
    return HttpResponse('')


# 步骤详情页获取接口数据
def step_get_api(request):
    api_id = request.GET['api_id']
    api = DbApis.objects.filter(id=api_id).values()[0]
    return HttpResponse(json.dumps(api), content_type="application/json")


# 运行大用例
def Run_Case(request):
    Case_id = request.GET['Case_id']
    Case = DbCases.objects.filter(id=Case_id)[0]
    steps = DbStep.objects.filter(Case_id=Case_id)
    ic(steps)
    from My_api.run_case import run
    run(Case.id, Case.name, steps)

    return HttpResponse('')


# 查看报告
def look_report(request, eid):
    Case_id = eid

    return render(request, 'Reports/%s.html' % Case_id)


# 保存项目公共请求头
def save_project_header(request):
    project_id = request.GET['project_id']
    req_names = request.GET['req_names']
    req_keys = request.GET['req_keys']
    req_values = request.GET['req_values']
    req_ids = request.GET['req_ids']

    ic(project_id, req_names, req_keys, req_values, req_ids)

    names = req_names.split(',')
    keys = req_keys.split(',')
    values = req_values.split(',')
    ids = req_ids.split(',')
    ic(names, keys, values, ids)
    for i in range(len(ids)):
        if names[i] != '':
            if ids[i] == 'new':
                DbProjectHeader.objects.create(project_id=project_id, name=names[i], key=keys[i], value=values[i],
                                               is_delete=0)
            else:
                DbProjectHeader.objects.filter(id=ids[i]).update(name=names[i], key=keys[i], value=values[i],
                                                                 is_delete=0)
        else:
            try:
                DbProjectHeader.objects.filter(id=ids[i]).delete()
            except:
                pass
    return HttpResponse('')


# 保存用例名称
def save_case_name(request):
    Id = request.GET['id']
    name = request.GET['name']
    ic(Id, name)
    DbCases.objects.filter(id=Id).update(name=name)
    return HttpResponse('')


# 保存项目公共域名
def save_project_host(request):
    project_id = request.GET['project_id']
    req_names = request.GET['req_names']
    req_hosts = request.GET['req_hosts']
    req_ids = request.GET['req_ids']
    names = req_names.split(',')
    hosts = req_hosts.split(',')
    ids = req_ids.split(',')
    for i in range(len(ids)):
        if names[i] != '':
            if ids[i] == 'new':
                DbProjectHost.objects.create(project_id=project_id, name=names[i], host=hosts[i], is_delete=0)
            else:
                DbProjectHost.objects.filter(id=ids[i]).update(name=names[i], host=hosts[i])
        else:
            try:
                DbProjectHost.objects.filter(id=ids[i]).delete()
            except:
                pass
    return HttpResponse('')


# 获取项目登录态
def project_get_login(request):
    if request.method == 'GET':
        project_id = request.GET['project_id']
        ic(project_id)
        try:
            login = DbLogin.objects.filter(project_id=project_id).values()[0]
        except:
            login = {}
        return HttpResponse(json.dumps(login), content_type='application/json')
    else:
        dic = json.dumps(RE.WRONG_REQUEST.value)
        return HttpResponse(dic, content_type=RE.CONTENT_TYPE.value)


# 保存登陆态接口
def project_login_save(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        # 提取所有数据
        project_id = data['project_id']
        login_method = data['login_method']
        login_url = data['login_url']
        login_host = data['login_host']
        login_header = data['login_header']
        login_body_method = data['login_body_method']
        login_api_body = data['login_api_body']
        login_response_set = data['login_response_set']
        # 保存数据
        ic(project_id,
           login_method,
           login_url,
           login_host,
           login_header,
           login_body_method,
           login_api_body,
           login_response_set)
        if DbLogin.objects.filter(project_id=project_id).values().count() == 0:
            DbLogin.objects.create(
                project_id=project_id,
                api_method=login_method,
                api_url=login_url,
                api_header=login_header,
                api_host=login_host,
                body_method=login_body_method,
                api_body=login_api_body,
                set=login_response_set,
                is_delete=0
            )
        else:
            DbLogin.objects.filter(project_id=project_id).update(
                api_method=login_method,
                api_url=login_url,
                api_header=login_header,
                api_host=login_host,
                body_method=login_body_method,
                api_body=login_api_body,
                set=login_response_set,
                is_delete=0
            )
        # 返回
        dic = json.dumps({'code': 200, 'data': True, 'massage': 'success'})
        return HttpResponse(dic, content_type=RE.CONTENT_TYPE.value)
    else:
        dic = json.dumps(RE.WRONG_REQUEST.value)
        return HttpResponse(dic, content_type=RE.CONTENT_TYPE.value)


# 调试登陆态接口
def project_login_send(request):
    # 第一步，获取前端数据
    login_method = request.GET['login_method']
    login_url = request.GET['login_url']
    login_host = request.GET['login_host']
    login_header = request.GET['login_header']
    login_body_method = request.GET['login_body_method']
    login_api_body = request.GET['login_api_body']
    login_response_set = request.GET['login_response_set']

    if login_header == '':
        login_header = '{}'

    ic(login_method,
       login_url,
       login_host,
       login_header,
       login_body_method,
       login_api_body,
       login_response_set)
    # 第二步，发送请求
    try:
        header = json.loads(login_header)  # 处理header
    except:
        return HttpResponse('请求头不符合json格式！')

        # 处理域名host
    if login_host[:4] == '全局域名':
        project_host_id = login_host.split('-')[1]
        ic(DbProjectHost.objects.filter(id=project_host_id)[0])
        login_host = DbProjectHost.objects.filter(id=project_host_id)[0].host

    # 拼接完整url
    if login_host[-1] == '/' and login_url[0] == '/':  # 都有/
        url = login_host[:-1] + login_url
        ic(url)
    elif login_host[-1] != '/' and login_url[0] != '/':  # 都没有/
        url = login_host + '/' + login_url
        ic(url)
    else:  # 肯定有一个有/
        url = login_host + login_url
        ic(url)
    try:
        if login_body_method == 'none':
            response = requests.request(login_method.upper(), url, headers=header, data={})
        elif login_body_method == 'form-data':
            files = []
            payload = {}
            for i in eval(login_api_body):
                payload[i[0]] = i[1]
            response = requests.request(login_method.upper(), url, headers=header, data=payload, files=files)

        elif login_body_method == 'x-www-form-urlencoded':
            header['Content-Type'] = 'application/x-www-form-urlencoded'
            payload = {}
            for i in eval(login_api_body):
                payload[i[0]] = i[1]
            response = requests.request(login_method.upper(), url, headers=header, data=payload)

        elif login_body_method == 'GraphQL':
            header['Content-Type'] = 'application/json'
            query = login_api_body.split('*WQRF*')[0]
            graphql = login_api_body.split('*WQRF*')[1]
            try:
                eval(graphql)
            except:
                graphql = '{}'
            payload = '{"query":"%s","variables":%s}' % (query, graphql)
            response = requests.request(login_method.upper(), url, headers=header, data=payload)


        else:  # 这时肯定是raw的五个子选项：
            if login_body_method == 'Text':
                header['Content-Type'] = 'text/plain'

            if login_body_method == 'JavaScript':
                header['Content-Type'] = 'text/plain'

            if login_body_method == 'Json':
                header['Content-Type'] = 'text/plain'

            if login_body_method == 'Html':
                header['Content-Type'] = 'text/plain'

            if login_body_method == 'Xml':
                header['Content-Type'] = 'text/plain'
            response = requests.request(login_method.upper(), url, headers=header, data=login_api_body.encode('utf-8'))

        # 把返回值传递给前端页面
        response.encoding = "utf-8"
        DbHost.objects.update_or_create(host=login_host)
        res = response.json()

        # 第三步，对返回值进行提取
        get_res = ''  # 声明提取结果存放
        for i in login_response_set.split('\n'):
            if i == "":
                continue
            else:
                i = i.replace(' ', '')
                key = i.split('=')[0]  # 拿出key
                path = i.split('=')[1]  # 拿出路径
                value = res
                for j in path.split('/')[1:]:
                    value = value[j]
                get_res += key + '="' + value + '"\n'
        # 第四步，返回前端
        end_res = {"response": response.text, "get_res": get_res}
        return HttpResponse(json.dumps(end_res), content_type='application/json')

    except Exception as e:
        end_res = {"response": str(e), "get_res": ''}
        return HttpResponse(json.dumps(end_res), content_type='application/json')


# 调用登陆态接口
def project_login_send_for_other(project_id):
    # 第一步，获取数据
    login_api = DbLogin.objects.filter(project_id=project_id)[0]
    login_method = login_api.api_method
    login_url = login_api.api_url
    login_host = login_api.api_host
    login_header = login_api.api_header
    login_body_method = login_api.body_method
    login_api_body = login_api.api_body
    login_response_set = login_api.set

    if login_header == '':
        login_header = '{}'
    # 第二步，发送请求
    try:
        header = json.loads(login_header)  # 处理header
    except:
        return HttpResponse('请求头不符合json格式！')

    # 拼接完整url
    if login_host[-1] == '/' and login_url[0] == '/':  # 都有/
        url = login_host[:-1] + login_url
    elif login_host[-1] != '/' and login_url[0] != '/':  # 都没有/
        url = login_host + '/' + login_url
    else:  # 肯定有一个有/
        url = login_host + login_url
    try:
        if login_body_method == 'none':
            # 先判断是否是cookie持久化，若是，则不处理
            if login_response_set == 'cookie':
                a = requests.session()
                a.request(login_method.upper(), url, headers=header, data={})
                return a
            else:
                response = requests.request(login_method.upper(), url, headers=header, data={})
        elif login_body_method == 'form-data':
            files = []
            payload = {}
            for i in eval(login_api_body):
                payload[i[0]] = i[1]
            # 先判断是否是cookie持久化，若是，则不处理
            if login_response_set == 'cookie':
                a = requests.session()
                a.request(login_method.upper(), url, headers=header, data={})
                return a
            else:
                response = requests.request(login_method.upper(), url, headers=header, data=payload, files=files)

        elif login_body_method == 'x-www-form-urlencoded':
            header['Content-Type'] = 'application/x-www-form-urlencoded'
            payload = {}
            for i in eval(login_api_body):
                payload[i[0]] = i[1]
            # 先判断是否是cookie持久化，若是，则不处理
            if login_response_set == 'cookie':
                a = requests.session()
                a.request(login_method.upper(), url, headers=header, data={})
                return a
            else:
                response = requests.request(login_method.upper(), url, headers=header, data=payload)

        elif login_body_method == 'GraphQL':
            header['Content-Type'] = 'application/json'
            query = login_api_body.split('*WQRF*')[0]
            graphql = login_api_body.split('*WQRF*')[1]
            try:
                eval(graphql)
            except:
                graphql = '{}'
            payload = '{"query":"%s","variables":%s}' % (query, graphql)
            # 先判断是否是cookie持久化，若是，则不处理
            if login_response_set == 'cookie':
                a = requests.session()
                a.request(login_method.upper(), url, headers=header, data={})
                return a
            else:
                response = requests.request(login_method.upper(), url, headers=header, data=payload)

        else:  # 这时肯定是raw的五个子选项：
            if login_body_method == 'Text':
                header['Content-Type'] = 'text/plain'

            if login_body_method == 'JavaScript':
                header['Content-Type'] = 'text/plain'

            if login_body_method == 'Json':
                header['Content-Type'] = 'text/plain'

            if login_body_method == 'Html':
                header['Content-Type'] = 'text/plain'

            if login_body_method == 'Xml':
                header['Content-Type'] = 'text/plain'
            # 先判断是否是cookie持久化，若是，则不处理
            if login_response_set == 'cookie':
                a = requests.session()
                a.request(login_method.upper(), url, headers=header, data={})
                return a
            else:
                response = requests.request(login_method.upper(), url, headers=header,
                                            data=login_api_body.encode('utf-8'))
        # 把返回值传递给前端页面
        response.encoding = "utf-8"
        DbHost.objects.update_or_create(host=login_host)
        res = response.json()

        # 先判断是否是cookie持久化，若是，则不处理
        if login_response_set == 'cookie':
            end_res = {"response": response.text, "get_res": 'cookie保持会话无需提取返回值'}
        else:
            get_res = ''  # 声明提取结果存放
            for i in login_response_set.split('\n'):
                if i == "":
                    continue
                else:
                    i = i.replace(' ', '')
                    key = i.split('=')[0]  # 拿出key
                    path = i.split('=')[1]  # 拿出路径
                    value = res
                    for j in path.split('/')[1:]:
                        value = value[j]
                    get_res += key + '="' + value + '"\n'
            end_res = {"response": response.text, "get_res": get_res}
        return HttpResponse(json.dumps(end_res), content_type='application/json')
    except Exception as e:
        return {}


# 首页保存请求数据
def Home_save_api(request):
    project_id = request.GET['project_id']
    ts_method = request.GET['ts_method']
    ts_url = request.GET['ts_url']
    ts_host = request.GET['ts_host']
    ts_header = request.GET['ts_header']
    ts_body_method = request.GET['ts_body_method']
    ts_api_body = request.GET['ts_api_body']
    ic(project_id,
       ts_method,
       ts_url,
       ts_host,
       ts_header,
       ts_body_method,
       ts_api_body)
    DbApis.objects.create(project_id=project_id,
                          name='首页保存接口',
                          api_models=ts_method,
                          api_url=ts_url,
                          api_header=ts_header,
                          api_host=ts_host,
                          body_method=ts_body_method,
                          api_body=ts_api_body,
                          is_delete=0
                          )

    return HttpResponse('')


# 首页搜索功能
def search(request):
    key = request.GET['key']

    # 项目名搜哦所
    projects = DbProject.objects.filter(name__contains=key)  # 获取name包含key的所有项目
    plist = [{"url": "/apis/%s/" % i.id, "text": i.name, "type": "project"} for i in projects]
    # 接口名搜索
    apis = DbApis.objects.filter(name__contains=key)  # 获取name包含key的所有接口
    alist = [{"url": "/apis/%s/" % i.project_id, "text": i.name, "type": "api"} for i in apis]

    res = {"results": plist + alist}
    return HttpResponse(json.dumps(res), content_type='application/json')


# 账号修改
def sign_change(request):
    if request.method == "POST":
        data = json.loads(request.body)
        u_name = data["username"]
        p_word = data["password"]
        ic(u_name, p_word)
        if p_word in ['', None]:
            dic = json.dumps({"code": 30002, "data": "false", "message": "请输入密码"})
            return HttpResponse(dic, content_type=RE.CONTENT_TYPE.value)

        DbUser.objects.filter(username=u_name).update(password=p_word)
        dic = json.dumps({"code": 200, "data": "false", "message": "修改成功！"})
        return HttpResponse(dic, content_type=RE.CONTENT_TYPE.value)
    else:
        dic = json.dumps(RE.WRONG_REQUEST.value)
        return HttpResponse(dic, content_type=RE.CONTENT_TYPE.value)


# 查询账号信息
def sign_select(request):
    if request.method == 'GET':
        Id = request.GET['id']
        user_s = DbUser.objects.filter(id=Id).values()[0]
        ic(user_s)
        dic = json.dumps(user_s)
        # dic = json.dumps({'code': 200, 'data': True, 'massage': f'{user_s}'})
        return HttpResponse(dic, content_type=RE.CONTENT_TYPE.value)
    else:
        dic = json.dumps(RE.WRONG_REQUEST.value)
        return HttpResponse(dic, content_type=RE.CONTENT_TYPE.value)


# 删除用户
def delete_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        ic(data)
        Id = data['id']
        DbUser.objects.filter(id=Id).update(is_delete=1)
        dic = json.dumps({'code': 200, 'data': True, 'message': '删除成功！'})
        return HttpResponse(dic, content_type=RE.CONTENT_TYPE.value)
    else:
        dic = json.dumps(RE.WRONG_REQUEST.value)
        return HttpResponse(dic, content_type=RE.CONTENT_TYPE.value)


# 新增全局变量
def global_data_new(request):
    name = request.GET['name']
    data = request.GET['data']
    user_a_id = request.GET['user_a_id']
    ic(name,
       data,
       user_a_id)
    DbGlobalData.objects.create(name=name, data=data, user_id=user_a_id, is_delete=0)

    return HttpResponse(json.dumps({'code': 200, 'data': True, 'message': '新增成功'}), content_type='application/json')


# 删除全局变量
def delete_data(request):
    Id = request.GET['id']
    DbGlobalData.objects.filter(id=Id).delete()

    return HttpResponse('删除成功！')


# 查询全局变量
def show_data(request):
    Id = request.GET['id']

    dic = DbGlobalData.objects.filter(id=Id).values()[0]
    ic(dic)
    return HttpResponse(json.dumps(dic), content_type='application/json')


def save_data(request):
    name = request.GET['name']
    data = request.GET['data']
    data_id = request.GET['data_id']

    DbGlobalData.objects.filter(id=data_id).update(name=name, data=data)

    return HttpResponse(json.dumps({'code': 200, 'data': True, 'message': '修改成功'}))


def Api_send_index(request):
    start_time = time.time()
    if request.method == 'POST':
        data = json.loads(request.body)
        ic(data)
        # 提取所有数据
        ts_method = data['ts_method']  # post
        ts_url = data['ts_url']  # url
        ts_header = data['ts_api_header']  # header
        ts_body_method = data['ts_body_method']  # 请求体
        ts_api_body = data['ts_api_body']
        ts_api_method = data['ts_api_method']  # 请求参数
        content_type = data['content_type']
        url = ts_url

        # # 拼接完整url
        # if ts_body_method == 'Query参数':
        #     ts_api_body = 'Query参数'  # form-data
        #     url = ts_url
        # else:
        #     ts_api_body = data['ts_api_body']  # form-data
        #     url = ts_url

        ic(ts_method,
           ts_url,
           ts_header,
           ts_body_method,
           ts_api_body,
           ts_api_method,
           content_type)
        # 发送请求获取返回值
        ts_headers = {}
        for i in ts_header:
            if i[0] == '':
                ts_header.remove(i)
            else:
                pass
        if ts_header == [['', '']]:
            ts_header = '{}'
        else:
            for i in ts_header:
                ts_headers[i[0]] = i[1]

        if content_type != '':
            ts_headers['content-type'] = content_type
        ic(ts_headers)

        try:
            if ts_api_method == 'none':
                response = requests.request(ts_method.upper(), url, headers=ts_headers, data={})

            elif ts_api_method == 'form-data':
                files = []
                payload = {}
                for i in eval(ts_api_body):
                    payload[i[0]] = i[1]
                response = requests.request(ts_method.upper(), url, headers=ts_headers, data=payload, files=files)

            elif ts_api_method == 'x-www-form-urlencoded':
                ts_headers['Content-Type'] = 'application/x-www-form-urlencoded'
                payload = {}
                for i in eval(ts_api_body):
                    payload[i[0]] = i[1]
                response = requests.request(ts_method.upper(), url, headers=ts_headers, data=payload)

            else:  # 这时肯定是raw的五个子选项：
                if ts_api_method == 'raw':
                    ts_headers['Content-Type'] = 'text/plain'
                response = requests.request(ts_method.upper(), url, headers=ts_headers,
                                            data=ts_api_body.encode('utf-8'))
            times = response.elapsed.total_seconds()  # 获取实际的响应时间
            ic(times)
            end_time = time.time()
            all_time = end_time - start_time
            heada = response.headers
            head1 = dict(heada)
            if head1.get('Transfer-Encoding'):
                pass
            else:
                head1['Transfer-Encoding'] = ''
            ic(head1)
            head = json.dumps(head1)
            ic(response.status_code)
            DbApi.objects.create(ts_method=ts_method,
                                 ts_url=ts_url,
                                 ts_header=ts_headers,
                                 ts_body_method=ts_body_method,
                                 ts_api_body=ts_api_body,
                                 ts_api_method=ts_api_method,
                                 result=response.text,
                                 head=head,
                                 api_time=times,
                                 all_time=all_time,
                                 status_code=response.status_code,
                                 is_delete=0)

            # 把返回值传递给前端页面
            if response.json()['code'] != 200:
                TE = ''
                heads = {
                    "head1": f"{heada['Server']}",
                    "head2": f"{heada['Date']}",
                    "head3": f"{heada['Content-Type']}",
                    "head4": f"{TE}",
                    "head5": f"{heada['Connection']}",
                    "head6": f"{heada['X-Content-Type-Options']}",
                    "head7": f"{heada['X-XSS-Protection']}",
                    "head8": f"{heada['Cache-Control']}",
                    "head9": f"{heada['Pragma']}",
                    "head10": f"{heada['Expires']}"
                }
            else:
                heads = {
                    "head1": f"{heada['Server']}",
                    "head2": f"{heada['Date']}",
                    "head3": f"{heada['Content-Type']}",
                    "head4": f"{heada['Transfer-Encoding']}",
                    "head5": f"{heada['Connection']}",
                    "head6": f"{heada['X-Content-Type-Options']}",
                    "head7": f"{heada['X-XSS-Protection']}",
                    "head8": f"{heada['Cache-Control']}",
                    "head9": f"{heada['Pragma']}",
                    "head10": f"{heada['Expires']}"
                }
            response.encoding = "utf-8"
            send_id = DbApi.objects.all().order_by("-id").values()[0]['id']
            return HttpResponse(json.dumps({
                "re": response.text,
                "head": f"{json.dumps(heads)}",
                "times": f"{times}",
                "timea": f"{all_time}",
                "send_id": f"{send_id}",
            }))
        except Exception as e:
            ic(e)
            return HttpResponse(json.dumps({"re": f"{e}"}))
    else:
        dic = json.dumps(RE.WRONG_REQUEST.value)
        return HttpResponse(dic, content_type=RE.CONTENT_TYPE.value)


# 新主页保存接口
def Api_new_save(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        api_name = data["api_name"]
        project_name = data["project_name"]
        ic(data)
        try:
            logs = DbApi.objects.all().order_by("-id").values()[0]
            ts_method = logs['ts_method'].lower()
            urls = re.findall(r"http://(.+?)/", logs['ts_url'])
            host_api = f'http://{urls[0]}'
            url = logs['ts_url'].replace(host_api, '')
            DbApis.objects.create(
                project_id=project_name,
                name=api_name,
                result=logs["result"],
                api_body=logs["ts_api_body"],
                body_method=logs["ts_api_method"],
                api_header=logs["ts_header"],
                api_models=ts_method,
                api_host=host_api,
                api_url=url,
                is_delete=0
            )
        except Exception as e:
            ic(e)
            return HttpResponse(json.dumps({"re": f"{e}"}))
        else:
            return HttpResponse(json.dumps({'code': 200, 'data': True, 'message': '保存成功'}))
    else:
        dic = json.dumps(RE.WRONG_REQUEST.value)
        return HttpResponse(dic, content_type=RE.CONTENT_TYPE.value)


# 查询接口
def select_api(request):
    if request.method == 'GET':
        Id = request.GET['Id']
        log = DbApi.objects.filter(id=Id).values()[0]
        head = eval(log['head'])
        print(type(head))
        heads = {
            "head1": f"{head['Server']}",
            "head2": f"{head['Date']}",
            "head3": f"{head['Content-Type']}",
            "head4": f"{head['Transfer-Encoding']}",
            "head5": f"{head['Connection']}",
            "head6": f"{head['X-Content-Type-Options']}",
            "head7": f"{head['X-XSS-Protection']}",
            "head8": f"{head['Cache-Control']}",
            "head9": f"{head['Pragma']}",
            "head10": f"{head['Expires']}"
        }
        ic(log)
        return HttpResponse(json.dumps({'message': log, "head": json.dumps(heads)}))
    else:
        dic = json.dumps(RE.WRONG_REQUEST.value)
        return HttpResponse(dic, content_type=RE.CONTENT_TYPE.value)
