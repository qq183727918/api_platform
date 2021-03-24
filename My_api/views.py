from django.contrib.auth.decorators import login_required
from django.shortcuts import render
# Create your views here.
from icecream import ic

from My_api.models import *
from My_api.views_api import glodict


@login_required
def welcome(request):
    return render(request, 'welcome.html')


# 用户管理页面
def user(request):
    return render(request, 'welcome.html', {"whichHTML": "user.html", **glodict(request)})


# 进入主页
def home(request, log_id=''):
    ic('home', request.user.id, request.user.username, log_id)
    return render(request, 'welcome.html',
                  {"whichHTML": "home.html", "oid": '1', "ooid": log_id, **glodict(request)})


# 进入登录页面
def login_user(request):
    return render(request, 'login.html')


# 帮助
def api_help(request):
    return render(request, 'welcome.html', {"whichHTML": "help.html", "oid": "", **glodict(request)})


# 进入项目列表
def project_list(request):
    return render(request, 'welcome.html', {"whichHTML": "project_list.html", "oid": "", **glodict(request)})


# 进入接口库
def open_apis(request, id):
    project_id = id
    return render(request, 'welcome.html', {"whichHTML": "P_apis.html", "oid": project_id, **glodict(request)})


# 进入用例设置库
def open_cases(request, id):
    project_id = id
    return render(request, 'welcome.html', {"whichHTML": "P_cases.html", "oid": project_id, **glodict(request)})


# 进入项目设置
def open_project_set(request, id):
    project_id = id
    return render(request, 'welcome.html', {"whichHTML": "P_project_set.html", "oid": project_id, **glodict(request)})


# 进入全局变量
def global_data(request, Id):
    project_id = Id
    return render(request, 'welcome.html', {"whichHTML": "P_global_data.html", "oid": project_id})


# home改版
def index(request):
    logs = DbApi.objects.all().order_by("-id")
    project = DbProject.objects.all()
    return render(request, 'index.html', {"logs": logs, "project": project})


# 按钮样式
def button(request):
    return render(request, 'button.html')
