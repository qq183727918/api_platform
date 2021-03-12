"""api_platform URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from My_api.views import *
from My_api.views_tools import *

urlpatterns = [

    url(r'^$', login),
    url(r'^admin/', admin.site.urls),
    url(r'^user/', user),  # 用户管理页面
    url(r'^welcome/$', welcome),  # 获取菜单
    url(r'^home/$', home),  # 进入首页
    url(r"^child/(?P<eid>.+)/(?P<oid>.*)/(?P<ooid>.*)/$", child),  # 返回子页面
    url(r"^login/$", login),  # 登录页面

    url(r'^accounts/login/$', login),  # 非登录状态自动跳回登录页面
    url(r'^logout/$', logout),  # 退出
    url(r"^login_action/$", login_action),  # 登录
    url(r"^sign_action/$", sign_action),  # 注册
    url(r"^sign_change/$", sign_change),  # 修改密码
    url(r"^sign_select/$", sign_select),  # 查询账号信息
    url(r"^delete_user/$", delete_user),  # 删除用户信息

    url(r"^pei/$", pei),  # 匿名吐槽

    url(r"^help/$", api_help),  # 进入帮助页面
    url(r"^project_list/$", project_list),  # 进入项目列表
    url(r'^delete_project/$', delete_project),  # 删除项目
    url(r'^add_project/$', add_project),  # 新增项目

    url(r'^apis/(?P<id>.*)/$', open_apis),  # 进入接口库
    url(r'^cases/(?P<id>.*)/$', open_cases),  # 进入用例库
    url(r'^project_set/(?P<id>.*)/$', open_project_set),  # 进入项目设置
    url(r'^save_project_set/(?P<id>.*)/$', save_project_set),  # 保存项目设置
    url(r'^project_api_add/(?P<Pid>.*)/$', project_api_add),  # 新增接口
    url(r'^project_api_del/(?P<id>.*)/$', project_api_del),  # 删除接口
    url(r'^save_bz/$', save_bz),  # 保存备注
    url(r'^get_bz/$', get_bz),  # 获取备注
    url(r'^Api_save/$', Api_save),  # 保存接口

    url(r'^get_api_data/$', get_api_data),  # 查询接口内容

    url(r'^Api_send/$', Api_send),  # 调试层发送请求
    url(r'^copy_api/$', copy_api),  # 复制接口
    url(r'^error_request/$', error_request),  # 调用异常测试接口
    url(r'^Api_send_home/$', Api_send_home),  # 首页发送请求
    url(r'^get_home_log/$', get_home_log),  # 获取最新请求记录
    url(r'^get_api_log_home/$', get_api_log_home),  # 获取完整的单一的请求记录数据
    url(r'^home_log/(?P<log_id>.*)/$', home),  # 再次进入首页，这次要带着请求记录
    url(r'^add_case/(?P<eid>.*)/$', add_case),  # 增加用例
    url(r'^del_case/(?P<eid>.*)/(?P<oid>.*)/$', del_case),  # 删除用例
    url(r'^copy_case/(?P<eid>.*)/(?P<oid>.*)/$', copy_case),  # 复制用例
    url(r'^get_small/$', get_small),  # 获取小用例步骤的列表数据
    url(r'^user_upload/$', user_upload),  # 上传头像

    url(r'^add_new_step/$', add_new_step),  # 新增小步骤接口

    url(r'^delete_step/(?P<eid>.*)/$', delete_step),  # 删除小步骤接口
    url(r'^get_step/$', get_step),  # 获取小步骤
    url(r'^save_step/$', save_step),  # 保存小步骤
    url(r'^step_get_api/$', step_get_api),  # 步骤详情页获取接口数据
    url(r'^Run_Case/$', Run_Case),  # 运行大用例
    url(r'^look_report/(?P<eid>.*)/$', look_report),  # 查看报告
    url(r'^save_project_header/$', save_project_header),  # 保存项目公共请求头
    url(r'^save_case_name/$', save_case_name),  # 保存用例名称
    url(r'^save_project_host/$', save_project_host),  # 保存项目公域名

    url(r'^project_get_login/$', project_get_login),  # 获取项目登录态接口
    url(r'^project_login_save/$', project_login_save),  # 保存项目登录态接口
    url(r'^project_login_send/$', project_login_send),  # 调试请求登录态接口
    url(r'^Home_save_api/$', Home_save_api),  # 首页保存请求数据
    url(r'^search/$', search),  # 首页搜索功能
    url(r'^global_data/(?P<Id>.*)/$', global_data),  # 进入全局变量
    url(r'^global_data_new/$', global_data_new),  # 新增全局变量
    url(r'^delete_data/$', delete_data),  # 删除全局变量
    url(r'^show_data/$', show_data),  # 展示全局变量
    url(r'^save_data/$', save_data),  # 修改全局变量
    url(r'^new_home/$', new_home),  # 主要自改版
    url(r'^index/$', index),  # 主要自改版

    # --------------------小工具-------------------- #
    url(r'^tools_zhengjiao/$', zhengjiao),  # 进入小工具页面
    url(r'^zhengjiao_play/$', zhengjiao_play),  # 正交工具运行
    url(r'^zhengjiao_excel/$', zhengjiao_excel),  # 正交结果导出

]
