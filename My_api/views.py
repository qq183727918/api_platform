import json
import requests

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
# Create your views here.
from icecream import ic

from My_api.models import *


@login_required
def welcome(request):
    return render(request, 'welcome.html')


def case_list(request):
    return render(request, 'case_list.html')


# 返回子页面
def child(request, eid, oid):
    ic(eid, oid)
    res = child_json(eid, oid)
    return render(request, eid, res)


# 控制不同页面返回不同的数据：数据分发器
def child_json(eid, oid=''):
    res = {}
    if eid == 'Home.html':
        date = DB_home_href.objects.all()

        res = {"hrefs": date}
    if eid == 'project_list.html':
        date = DB_project.objects.all()
        res = {"projects": date}

    if eid == 'P_apis.html':
        project = DB_project.objects.filter(id=oid)[0]
        apis = DB_apis.objects.filter(project_id=oid)
        res = {"project": project, 'apis': apis}
        ic(project)
    if eid == 'P_cases.html':
        project = DB_project.objects.filter(id=oid)[0]
        res = {"project": project}
        ic(project)
    if eid == 'P_project_set.html':
        project = DB_project.objects.filter(id=oid)[0]
        res = {"project": project}
        ic(project)

    return res


# 进入主页
@login_required
def home(request):
    return render(request, 'welcome.html', {"whichHTML": "Home.html", "oid": ""})


# 进入登录页面
def login(request):
    return render(request, 'login.html')


def login_action(request):
    u_name = request.GET['username']
    p_word = request.GET['password']
    ic(u_name, p_word)

    # 开始联通django用户库，查看用户密码是否正确
    from django.contrib import auth
    user = auth.authenticate(username=u_name, password=p_word)

    if user is not None:
        # 进行正确的动作
        auth.login(request, user)
        request.session['user'] = u_name
        # return HttpResponseRedirect('/home/')
        return HttpResponse('成功')
        # return redirect('/home/')
    else:
        # 返回前端告诉前端用户用户名或者密码不正确
        return HttpResponse('失败')


# 注册
def sign_action(request):
    u_name = request.GET['username']
    p_word = request.GET['password']
    ic(u_name, p_word)

    # 开始关联django用户表
    from django.contrib.auth.models import User
    try:
        user = User.objects.create_user(username=u_name, password=p_word)
        user.save()
        return HttpResponse('注册成功！')
    except Exception as e:
        ic(e)
        return HttpResponse('注册失败~用户名好像已经存在了~')


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


# 帮助
def api_help(request):
    return render(request, 'welcome.html', {"whichHTML": "help.html", "oid": ""})


# 进入项目列表
def project_list(request):
    return render(request, 'welcome.html', {"whichHTML": "project_list.html", "oid": ""})


# 删除项目
def delete_project(request):
    Id = request.GET['id']

    DB_project.objects.filter(id=Id).delete()
    DB_apis.objects.filter(project_id=Id).delete()
    return HttpResponse('')


# 新增项目
def add_project(request):
    project_name = request.GET['project_name']
    project_remark = request.GET['project_remark']
    DB_project.objects.create(name=project_name, remark=project_remark, user=request.user.username)
    return HttpResponse('')


# 进入接口库
def open_apis(request, id):
    project_id = id
    return render(request, 'welcome.html', {"whichHTML": "P_apis.html", "oid": project_id})


# 进入接口库
def open_cases(request, id):
    project_id = id
    return render(request, 'welcome.html', {"whichHTML": "P_cases.html", "oid": project_id})


# 进入接口库
def open_project_set(request, id):
    project_id = id
    return render(request, 'welcome.html', {"whichHTML": "P_project_set.html", "oid": project_id})


# 保存项目设置
def save_project_set(request, id):
    project_id = id
    name = request.GET['name']
    remark = request.GET['remark']
    other_user = request.GET['other_user']
    ic(project_id, name, remark, other_user)
    DB_project.objects.filter(id=project_id).update(name=name, remark=remark, other=other_user)

    return HttpResponse('')


# 新增接口
def project_api_add(request, Pid):
    project_id = Pid
    ic(project_id)
    DB_apis.objects.create(project_id=project_id)
    return HttpResponseRedirect('/apis/%s/'%project_id)


# 删除接口
def project_api_del(request, id):
    project_id = DB_apis.objects.filter(id=id)[0].project_id
    DB_apis.objects.filter(id=id).delete()
    return HttpResponseRedirect('/apis/%s/' % project_id)


# 备注保存接口
def save_bz(request):
    api_id = request.GET['api_id']
    bz_value = request.GET['bz_value']
    DB_apis.objects.filter(id=api_id).update(des=bz_value)
    return HttpResponse('')


# 备注获取接口
def get_bz(request):
    api_id = request.GET['api_id']
    bz_value = DB_apis.objects.filter(id=api_id)[0].des
    ic(bz_value)
    return HttpResponse(bz_value)


# 保存接口
def Api_save(request):
    api_id = request.GET['api_id']
    ts_method = request.GET['ts_method']
    ts_url = request.GET['ts_url']
    ts_host = request.GET['ts_host']
    ts_header = request.GET['ts_header']
    ts_body_method = request.GET['ts_body_method']
    api_name = request.GET['api_name']
    ic(api_id, ts_method, ts_url, ts_host, ts_header, ts_body_method, api_name)

    if ts_body_method == '返回体':
        api = DB_apis.objects.filter(id=api_id).values()[0]
        ic(api)
        # if
        ts_body_method = api['last_body_method']
        ts_api_body = api['last_api_body']
        ic(ts_body_method, ts_body_method)
    else:
        ts_api_body = request.GET['ts_api_body']
        ic(ts_api_body)

    # 保存数据
    DB_apis.objects.filter(id=api_id).update(
        api_models=ts_method,
        api_url=ts_url,
        api_host=ts_host,
        api_header=ts_header,
        body_method=ts_body_method,
        api_body=ts_api_body,
        name=api_name
    )

    return HttpResponse('success')


# 查询接口内容
def get_api_data(request):
    api_id = request.GET['api_id']
    api = DB_apis.objects.filter(id=api_id).values()[0]
    return HttpResponse(json.dumps(api), content_type='application/json')


# 调试层发送请求
def Api_send(request):
    api_id = request.GET['api_id']
    ts_method = request.GET['ts_method']
    ts_url = request.GET['ts_url']
    ts_host = request.GET['ts_host']
    ts_header = request.GET['ts_header']
    api_name = request.GET['api_name']
    ts_body_method = request.GET['ts_body_method']
    ic(api_id, ts_method, ts_url, ts_host, ts_header, ts_body_method, api_name)
    if ts_body_method == '返回体':
        api = DB_apis.objects.filter(id=api_id).values()[0]
        ic(api)
        ts_body_method = api['last_body_method']
        ts_api_body = api['last_api_body']
        if ts_header in ['', None]:
            return HttpResponse('请先选择好请求编码格式和请求体，在点击Send按钮发送请求！')
    else:
        ts_api_body = request.GET['ts_api_body']
        if ts_header in ['', {}, None]:
            return HttpResponse('请先选择好请求编码格式和请求体，在点击Send按钮发送请求！')
        else:
            api = DB_apis.objects.filter(id=api_id)
            api.update(last_body_method=ts_body_method, last_api_body=ts_api_body)
    ic(ts_api_body)
    # 发送请求获取返回值
    header = json.loads(ts_header)  # 处理header

    # 拼接完整的url
    if ts_host[-1] == '/' and ts_url[0] == '/':  # 都有/
        url = ts_host[:-1] + ts_url
    elif ts_host[-1] != '/' and ts_url[0] != '/':  # 都没有/
        url = ts_host + '/' + ts_url
    else:  # 肯定有一个有/
        url = ts_host + '/' + ts_url

    if ts_body_method == 'none':
        response = requests.request(ts_method.upper(), url, headers=header, data={})
    elif ts_body_method == 'form-data':
        files = []
        payload = {}
        for i in eval(ts_api_body):
            payload[0] = i[1]
            ic(payload[0], i[1])
        ic(payload)
        response = requests.request(ts_method.upper(), url, headers=header, data=payload, files=files)

    elif ts_body_method == 'x-www-form-urlencoded':
        header['Content-Type'] = 'application/x-www-form-urlencoded'
        payload = {}
        for i in eval(ts_api_body):
            payload[0] = i[1]
        response = requests.request(ts_method.upper(), url, headers=header, data=payload)
    else:
        if ts_body_method == 'Text':
            header['Content-Type'] = 'text/plain'
        if ts_body_method == 'Javascript':
            header['Content-Type'] = 'text/plain'
        if ts_body_method == 'Json':
            header['Content-Type'] = 'text/plain'
        if ts_body_method == 'Html':
            header['Content-Type'] = 'text/plain'
        if ts_body_method == 'Xml':
            header['Content-Type'] = 'text/plain'
        response = requests.request(ts_method.upper(), url, headers=header, data=ts_api_body.encode('utf-8'))
    # 把返回值传递给前端页面
    return HttpResponse(response.text)
