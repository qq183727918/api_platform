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
def child(request, eid, oid, ooid):
    ic(eid, oid, ooid)
    res = child_json(eid, oid, ooid)
    return render(request, eid, res)


# 控制不同页面返回不同的数据：数据分发器
def child_json(eid, oid='', ooid=''):
    res = {}
    if eid == 'Home.html':
        date = DB_home_href.objects.all()
        home_log = DB_apis_log.objects.filter(user_id=oid)[::-1]
        hosts = DB_host.objects.all()
        from django.contrib.auth.models import User
        user_projects = DB_project.objects.filter(user=User.objects.filter(id=oid)[0].username)
        if ooid == '':
            res = {"hrefs": date, "home_log": home_log, "hosts": hosts, "user_projects": user_projects}
        else:
            log = DB_apis_log.objects.filter(id=ooid)[0]
            res = {"hrefs": date, "home_log": home_log, "log": log, hosts: "hosts", "user_projects": user_projects}

    if eid == 'project_list.html':
        date = DB_project.objects.all()
        res = {"projects": date}

    if eid == 'P_apis.html':
        project = DB_project.objects.filter(id=oid)[0]
        apis = DB_apis.objects.filter(project_id=oid)

        for i in apis:
            try:
                i.short_url = i.api_url.split('?')[0][:50]
            except:
                i.short_url = ''
        project_header = DB_project_header.objects.filter(project_id=oid)
        hosts = DB_host.objects.all()
        project_host = DB_project_host.objects.filter(project_id=oid)
        res = {"project": project, 'apis': apis, 'project_header': project_header, 'hosts': hosts,
               'project_host': project_host}
        ic(project)

    if eid == 'P_project_set.html':
        project = DB_project.objects.filter(id=oid)[0]
        res = {"project": project}
        ic(project)

    if eid == 'P_cases.html':
        # 这里应该是去数据库拿到这个项目的所有用例
        project = DB_project.objects.filter(id=oid)[0]
        Cases = DB_cases.objects.filter(project_id=oid)
        apis = DB_apis.objects.filter(project_id=oid)
        project_header = DB_project_header.objects.filter(project_id=oid)
        hosts = DB_host.objects.all()
        project_host = DB_project_host.objects.filter(project_id=oid)
        res = {"project": project, "Cases": Cases, "apis": apis, 'project_header': project_header, 'hosts': hosts,
               'project_host': project_host}

    return res


# 获取公共字典
def glodict(request):
    userimg = str(request.user.id) + '.png'  # 这里我们写死png后缀，因为上传时候我们也可以强行弄成这个png后缀
    res = {"username": request.user.username, "userimg": userimg}
    return res


# 上传用户头像
def user_upload(request):
    file = request.FILES.get("fileUpload", None)  # 靠name获取上传的文件，如果没有，避免报错，设置成None

    if not file:
        return HttpResponseRedirect('/home/')  # 如果没有则返回到首页

    new_name = str(request.user.id) + '.png'  # 设置好这个新图片的名字
    ic(new_name)
    destination = open("/My_api/static/img/" + new_name, 'wb')  # 打开特定的文件进行二进制的写操作
    for chunk in file.chunks():  # 分块写入文件
        destination.write(chunk)
    destination.close()

    return HttpResponseRedirect('/home/')  # 返回到首页


# 进入主页
@login_required
def home(request, log_id=''):
    ic(request.user.id, request.user.username)
    return render(request, 'welcome.html',
                  {"whichHTML": "Home.html", "oid": request.user.id, "ooid": log_id, **glodict(request)})


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
    return render(request, 'welcome.html', {"whichHTML": "help.html", "oid": "", **glodict(request)})


# 进入项目列表
def project_list(request):
    return render(request, 'welcome.html', {"whichHTML": "project_list.html", "oid": "", **glodict(request)})


# 删除项目
def delete_project(request):
    Id = request.GET['id']

    DB_project.objects.filter(id=Id).delete()
    DB_apis.objects.filter(project_id=Id).delete()  # 删除旗下接口

    all_Case = DB_cases.objects.filter(project_id=Id)
    for i in all_Case:
        DB_step.objects.filter(Case_id=i.id).delete()  # 删除步骤
        i.delete()  # 用例删除自己
    return HttpResponseRedirect('')


# 新增项目
def add_project(request):
    project_name = request.GET['project_name']
    project_remark = request.GET['project_remark']
    DB_project.objects.create(name=project_name, remark=project_remark, user=request.user.username)
    return HttpResponse('')


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
    DB_apis.objects.create(project_id=project_id, api_models='none', api_url='')
    return HttpResponseRedirect('/apis/%s/' % project_id)


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
    ts_project_headers = request.GET['ts_project_headers']
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
    print(ts_project_headers)
    # 保存数据
    DB_apis.objects.filter(id=api_id).update(
        api_models=ts_method,
        api_url=ts_url,
        api_host=ts_host,
        api_header=ts_header,
        body_method=ts_body_method,
        api_body=ts_api_body,
        name=api_name,
        public_header=ts_project_headers
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
    ts_project_headers = request.GET['ts_project_headers'].split(',')
    ic(api_id, ts_method, ts_url, ts_host, ts_header, ts_body_method, api_name, ts_project_headers)
    # 处理域名host
    if ts_host[:4] == '全局域名':
        project_host_id = ts_host.split('-')[1]
        ic(DB_project_host.objects.filter(id=project_host_id)[0])
        ts_host = DB_project_host.objects.filter(id=project_host_id)[0].host

    if ts_body_method == '返回体':
        api = DB_apis.objects.filter(id=api_id).values()[0]
        ic(api)
        ts_body_method = api['last_body_method']
        ts_api_body = api['last_api_body']
        if ts_body_method in ['', None]:
            return HttpResponse('请先选择好请求编码格式和请求体，在点击Send按钮发送请求！')
    else:
        ts_api_body = request.GET['ts_api_body']
        api = DB_apis.objects.filter(id=api_id)
        api.update(last_body_method=ts_body_method, last_api_body=ts_api_body)
    ic(ts_api_body)
    try:
        # 发送请求获取返回值
        header = json.loads(ts_header)  # 处理header
    except Exception as e:
        return HttpResponse(f'请求头不符合json格式！原因：{e}')

    for i in ts_project_headers:
        if i != '':
            project_header = DB_project_header.objects.filter(id=i)[0]
            header[project_header.key] = project_header.value

    ic(f'这是header{header}')

    # 拼接完整的url
    if ts_host[-1] == '/' and ts_url[0] == '/':  # 都有/
        url = ts_host[:-1] + ts_url
    elif ts_host[-1] != '/' and ts_url[0] != '/':  # 都没有/
        url = ts_host + '/' + ts_url
    else:  # 肯定有一个有/
        url = ts_host + '/' + ts_url
    try:
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
        response.encoding = 'utf-8'
        DB_host.objects.update_or_create(host=ts_host)
        return HttpResponse(response.text)
    except Exception as e:
        return HttpResponse(str(e))


# 复制接口
def copy_api(request):
    api_id = request.GET['api_id']
    # 开始复制接口
    old_api = DB_apis.objects.filter(id=api_id)[0]
    ic(DB_apis.objects.filter(id=api_id).values()[0])

    DB_apis.objects.create(project_id=old_api.project_id,
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
                           last_api_body=old_api.last_api_body
                           )
    # 返回
    return HttpResponse('')


# 异常值发送请求
def error_request(request):
    ic(request)
    api_id = request.GET['api_id']
    ic(api_id)
    new_body = request.GET['new_body']
    ic(new_body)
    span_text = request.GET['span_text']
    # 验证下请求体是不是新的替换过
    ic(api_id)

    api = DB_apis.objects.filter(id=api_id)[0]
    method = api.api_models
    url = api.api_url
    host = api.api_host
    header = api.api_header
    body_method = api.body_method
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

    try:
        if body_method == 'form-data':
            files = []
            payload = {}
            for i in eval(new_body):
                payload[i[0]] = i[1]
            response = requests.request(method.upper(), url, headers=header, data=payload, files=files)
        elif body_method == 'x-www-form-urlencoded':
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
        ic(f'报错{res_json}')
        return HttpResponse(json.dumps(res_json), content_type='application/json')


# 首页发送请求
def Api_send_home(request):
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
    try:
        header = json.loads(ts_header)  # 处理header
    except Exception as e:
        return HttpResponse(f'请求头不符合json格式！,原因为：{e}')
    # 写入到数据库请求记录中
    DB_apis_log.objects.create(
        user_id=request.user.id,
        api_method=ts_method,
        api_url=ts_url,
        api_header=ts_header,
        api_host=ts_host,
        body_method=ts_body_method,
        api_body=ts_api_body,
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
        DB_host.objects.update_or_create(host=ts_host)
        return HttpResponse(response.text)
    except Exception as e:
        return HttpResponse(str(e))


# 首页获取请求记录
def get_home_log(request):
    user_id = request.user.id
    all_logs = DB_apis_log.objects.filter(user_id=user_id).values()
    ret = {"all_log": list(all_logs.values("id", "api_method", 'api_host', "api_url"))[::-1]}
    return HttpResponse(json.dumps(ret), content_type='application/json')


# 获取完整的单一的请求记录数据
def get_api_log_home(request):
    log_id = request.GET['log_id']
    log = DB_apis_log.objects.filter(id=log_id)
    ret = {"log": list(log.values())[0]}
    ic(ret)
    return HttpResponse(json.dumps(ret), content_type='application/json')


# 增加用例
def add_case(request, eid):
    DB_cases.objects.create(project_id=eid, name='')
    return HttpResponseRedirect('/cases/%s/' % eid)


# 删除用例
def del_case(request, eid, oid):
    DB_cases.objects.filter(id=oid).delete()
    return HttpResponseRedirect('/cases/%s/' % eid)


# 复制用例
def copy_case(request, eid, oid):
    old_case = DB_cases.objects.filter(id=oid)[0]
    DB_cases.objects.create(project_id=old_case.project_id, name=old_case.name + '_副本')
    return HttpResponseRedirect('/cases/%s/' % eid)


# 获取小用例步骤的数据
def get_small(request):
    case_id = request.GET['case_id']
    steps = DB_step.objects.filter(Case_id=case_id).order_by('index')
    ret = {"all_steps": list(steps.values("index", "id", "name"))}
    return HttpResponse(json.dumps(ret), content_type='application/json')


# 新增小步骤
def add_new_step(request):
    Case_id = request.GET['Case_id']
    all_len = len(DB_step.objects.filter(Case_id=Case_id))
    DB_step.objects.create(Case_id=Case_id, name='我是新步骤', index=all_len + 1)
    return HttpResponse('')


# 删除小步骤
def delete_step(request, eid):
    ic(eid)
    step = DB_step.objects.filter(id=eid)[0]  # 获取待删除的step
    ic(step)
    index = step.index  # 获取目标index
    Case_id = step.Case_id  # 获取目标所属大用例id
    step.delete()  # 删除目标step
    # 遍历所有该大用例下的步骤中 顺序号大于目标index的步骤
    for i in DB_step.objects.filter(Case_id=Case_id).filter(index=index):
        i.index -= 1  # 执行顺序自减1
        i.save()

    return HttpResponse('')


# 获取小步骤数据
def get_step(request):
    step_id = request.GET['step_id']
    step = DB_step.objects.filter(id=step_id)
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

    DB_step.objects.filter(id=step_id).update(name=name,
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
                                              )
    return HttpResponse('')


# 步骤详情页获取接口数据
def step_get_api(request):
    api_id = request.GET['api_id']
    api = DB_apis.objects.filter(id=api_id).values()[0]
    return HttpResponse(json.dumps(api), content_type="application/json")


# 运行大用例
def Run_Case(request):
    Case_id = request.GET['Case_id']
    Case = DB_cases.objects.filter(id=Case_id)[0]
    steps = DB_step.objects.filter(Case_id=Case_id)
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
                DB_project_header.objects.create(project_id=project_id, name=names[i], key=keys[i], value=values[i])
            else:
                DB_project_header.objects.filter(id=ids[i]).update(name=names[i], key=keys[i], value=values[i])
        else:
            try:
                DB_project_header.objects.filter(id=ids[i]).delete()
            except:
                pass
    return HttpResponse('')


# 保存用例名称
def save_case_name(request):
    Id = request.GET['id']
    name = request.GET['name']
    ic(Id, name)
    DB_cases.objects.filter(id=Id).update(name=name)
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
                DB_project_host.objects.create(project_id=project_id, name=names[i], host=hosts[i])
            else:
                DB_project_host.objects.filter(id=ids[i]).update(name=names[i], host=hosts[i])
        else:
            try:
                DB_project_host.objects.filter(id=ids[i]).delete()
            except:
                pass
    return HttpResponse('')


# 获取项目登录态
def project_get_login(request):
    project_id = request.GET['project_id']
    try:
        login = DB_login.objects.filter(project_id=project_id).values()[0]
    except:
        login = {}
    return HttpResponse(json.dumps(login), content_type='application/json')


# 保存登陆态接口
def project_login_save(request):
    # 提取所有数据
    project_id = request.GET['project_id']
    login_method = request.GET['login_method']
    login_url = request.GET['login_url']
    login_host = request.GET['login_host']
    login_header = request.GET['login_header']
    login_body_method = request.GET['login_body_method']
    login_api_body = request.GET['login_api_body']
    login_response_set = request.GET['login_response_set']
    # 保存数据
    DB_login.objects.filter(project_id=project_id).update(
        api_method=login_method,
        api_url=login_url,
        api_header=login_header,
        api_host=login_host,
        body_method=login_body_method,
        api_body=login_api_body,
        set=login_response_set
    )
    # 返回
    return HttpResponse('success')
