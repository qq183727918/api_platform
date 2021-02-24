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
