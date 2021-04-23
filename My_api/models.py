from django.db import models


# Create your models here.

class DB_Roast(models.Model):
    user = models.CharField(max_length=30, null=True)  # 吐槽人名称
    text = models.CharField(max_length=1000, null=True)  # 吐槽内容
    ctime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text + str(self.ctime)


class DB_home_href(models.Model):
    name = models.CharField(max_length=30, null=True)
    href = models.CharField(max_length=2000, null=True)

    def __str__(self):
        return self.name


class DB_project(models.Model):
    name = models.CharField(max_length=100, null=True)  # 项目名称
    remark = models.CharField(max_length=1000, null=True)  # 项目描述
    user = models.CharField(max_length=15, null=True)  # 项目创建者名字
    user_id = models.CharField(max_length=10, null=True)  # 项目创建者名id
    other = models.CharField(max_length=200, null=True)  # 项目其他创建者

    def __str__(self):
        return self.name


class DB_apis(models.Model):
    project_id = models.CharField(max_length=10, null=True)  # 项目ID
    name = models.CharField(max_length=100, null=True)  # 接口名称
    api_models = models.CharField(max_length=10, null=True)  # 请求方式
    api_url = models.CharField(max_length=1000, null=True)  # url
    api_header = models.CharField(max_length=1000, null=True)  # 请求头
    api_login = models.CharField(max_length=10, null=True)  # 是否带登录态
    api_host = models.CharField(max_length=100, null=True)  # 域名
    des = models.CharField(max_length=100, null=True)  # 描述
    body_method = models.CharField(max_length=50, null=True)  # 请求体编码格式
    api_body = models.CharField(max_length=1000, null=True)  # 请求体
    result = models.TextField(null=True)  # 返回体，因为长度巨大，所以用大文本方式存储
    sign = models.CharField(max_length=10, null=True)  # 是否验签
    file_key = models.CharField(max_length=50, null=True)  # 文件key
    file_name = models.CharField(max_length=50, null=True)  # 文件名称
    public_header = models.CharField(max_length=1000, null=True)  # 全局变量-请求头

    last_body_method = models.CharField(max_length=20, null=True)  # 上次请求体编码格式
    last_api_body = models.CharField(max_length=1000, null=True)  # 上次请求体

    def __str__(self):
        return self.name


class DB_apis_log(models.Model):
    user_id = models.CharField(max_length=10, null=True)  # 所属用户id

    api_method = models.CharField(max_length=10, null=True)  # 请求方式
    api_url = models.CharField(max_length=1000, null=True)  # url
    api_header = models.CharField(max_length=1000, null=True)  # 请求头
    api_login = models.CharField(max_length=10, null=True)  # 是否带登陆态
    api_host = models.CharField(max_length=100, null=True)  # 域名

    body_method = models.CharField(max_length=20, null=True)  # 请求体编码格式
    api_body = models.CharField(max_length=1000, null=True)  # 请求体
    sign = models.CharField(max_length=10, null=True)  # 是否验签
    file_key = models.CharField(max_length=50, null=True)  # 文件key
    file_name = models.CharField(max_length=50, null=True)  # 文件名

    def __str__(self):
        return self.api_url


class DB_cases(models.Model):
    project_id = models.CharField(max_length=10, null=True)
    name = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.name


class DB_step(models.Model):
    Case_id = models.CharField(max_length=10, null=True)  # 所属大用例id
    name = models.CharField(max_length=50, null=True)  # 步骤名字
    index = models.IntegerField(null=True)  # 执行步骤
    api_method = models.CharField(max_length=10, null=True)  # 请求方式
    api_url = models.CharField(max_length=1000, null=True)  # url
    api_host = models.CharField(max_length=100, null=True)  # host
    api_header = models.CharField(max_length=1000, null=True)  # 请求头
    api_body_method = models.CharField(max_length=10, null=True)  # 请求体编码类型
    api_body = models.CharField(max_length=10, null=True)  # 请求体
    get_path = models.CharField(max_length=500, null=True)  # 提取返回值-路径法
    get_zz = models.CharField(max_length=500, null=True)  # 提取返回值-正则
    assert_zz = models.CharField(max_length=500, null=True)  # 断言返回值-正则
    assert_qz = models.CharField(max_length=500, null=True)  # 断言返回值-全文检索存在
    assert_path = models.CharField(max_length=500, null=True)  # 断言返回值-路径法
    mock_res = models.CharField(max_length=1000, null=True)  # mock返回值
    public_header = models.CharField(max_length=1000, null=True)  # 全局变量-请求头
    api_login = models.CharField(max_length=10, null=True)  # 是否带登录态

    def __str__(self):
        return self.name


class DB_project_header(models.Model):
    project_id = models.CharField(max_length=10, null=True)  # 所属项目id
    name = models.CharField(max_length=20, null=True)  # 请求头变量名字
    key = models.CharField(max_length=20, null=True)  # 请求头header的 key
    value = models.TextField(null=True)  # 请求头的value，因为有可能cookie较大，达到几千字符，所以采用大文本方式存储

    def __str__(self):
        return self.name


class DB_host(models.Model):
    host = models.CharField(max_length=100, null=True)
    des = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.host


class DB_project_host(models.Model):
    project_id = models.CharField(max_length=10, null=True)
    name = models.CharField(max_length=20, null=True)
    host = models.TextField(null=True)

    def __str__(self):
        return self.name


class DB_login(models.Model):
    project_id = models.CharField(max_length=10, null=True)  # 项目id
    api_method = models.CharField(max_length=10, null=True)  # 请求方式
    api_url = models.CharField(max_length=1000, null=True)  # url
    api_header = models.CharField(max_length=1000, null=True)  # 请求头
    api_host = models.CharField(max_length=100, null=True)  # 域名
    body_method = models.CharField(max_length=20, null=True)  # 请求体编码格式
    api_body = models.CharField(max_length=1000, null=True)  # 请求体
    sign = models.CharField(max_length=10, null=True)  # 是否验签
    set = models.CharField(max_length=300, null=True)  # 提取设置

    def __str__(self):
        return self.project_id


class DB_global_data(models.Model):
    name = models.CharField(max_length=20, null=True)  # 名字
    user_id = models.CharField(max_length=10, null=True)  # 所属用户id
    data = models.TextField(null=True)  # 存储的所有数据

    def __str__(self):
        return self.name


# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class DbApis(models.Model):
    id = models.IntegerField(primary_key=True)
    project_id = models.CharField(max_length=10, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    api_models = models.CharField(max_length=10, blank=True, null=True)
    api_url = models.CharField(max_length=1000, blank=True, null=True)
    api_header = models.CharField(max_length=1000, blank=True, null=True)
    api_login = models.CharField(max_length=10, blank=True, null=True)
    api_tag = models.CharField(max_length=100, blank=True, null=True)
    des = models.CharField(max_length=100, blank=True, null=True)
    api_body = models.CharField(max_length=1000, blank=True, null=True)
    result = models.TextField(blank=True, null=True)
    sign = models.CharField(max_length=10, blank=True, null=True)
    file_key = models.CharField(max_length=50, blank=True, null=True)
    file_name = models.CharField(max_length=50, blank=True, null=True)
    public_header = models.CharField(max_length=1000, blank=True, null=True)
    last_body_method = models.CharField(max_length=200, blank=True, null=True)
    last_api_body = models.CharField(max_length=1000, blank=True, null=True)
    body_method = models.CharField(max_length=50, blank=True, null=True)
    is_delete = models.IntegerField()

    def __str__(self):
        return self.id

    class Meta:
        managed = False
        db_table = 'db_apis'


class DbApisLog(models.Model):
    id = models.IntegerField(primary_key=True)
    user_id = models.CharField(max_length=10, blank=True, null=True)
    api_method = models.CharField(max_length=10, blank=True, null=True)
    api_url = models.CharField(max_length=1000, blank=True, null=True)
    api_header = models.CharField(max_length=1000, blank=True, null=True)
    api_login = models.CharField(max_length=10, blank=True, null=True)
    api_host = models.CharField(max_length=100, blank=True, null=True)
    body_method = models.CharField(max_length=20, blank=True, null=True)
    api_body = models.CharField(max_length=1000, blank=True, null=True)
    sign = models.CharField(max_length=10, blank=True, null=True)
    file_key = models.CharField(max_length=50, blank=True, null=True)
    file_name = models.CharField(max_length=50, blank=True, null=True)
    is_delete = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'db_apis_log'


class DbCases(models.Model):
    id = models.IntegerField(primary_key=True)
    project_id = models.CharField(max_length=10, blank=True, null=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    des = models.CharField(max_length=255, blank=True, null=True)
    created_time = models.DateTimeField()
    is_delete = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'db_cases'


class DbGlobalData(models.Model):
    name = models.CharField(max_length=20, blank=True, null=True)
    user = models.CharField(max_length=20, blank=True, null=True)
    data = models.TextField(blank=True, null=True)
    created_time = models.DateTimeField()
    is_delete = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'db_global_data'


class DbHomeHref(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30, blank=True, null=True)
    href = models.CharField(max_length=2000, blank=True, null=True)
    is_delete = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'db_home_href'


class DbHost(models.Model):
    host = models.CharField(max_length=100, blank=True, null=True)
    des = models.CharField(max_length=100, blank=True, null=True)
    is_delete = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'db_host'


class DbLogin(models.Model):
    id = models.IntegerField(primary_key=True)
    project_id = models.CharField(max_length=10, blank=True, null=True)
    api_method = models.CharField(max_length=10, blank=True, null=True)
    api_url = models.CharField(max_length=1000, blank=True, null=True)
    api_header = models.CharField(max_length=1000, blank=True, null=True)
    api_host = models.CharField(max_length=100, blank=True, null=True)
    body_method = models.CharField(max_length=20, blank=True, null=True)
    api_body = models.CharField(max_length=1000, blank=True, null=True)
    sign = models.CharField(max_length=10, blank=True, null=True)
    set = models.CharField(max_length=300, blank=True, null=True)
    is_delete = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'db_login'


class DbProject(models.Model):
    listName = models.CharField(max_length=100, blank=True, null=True)
    remark = models.CharField(max_length=1000, blank=True, null=True)
    user = models.CharField(max_length=15, blank=True, null=True)
    other = models.CharField(max_length=200, blank=True, null=True)
    user_id = models.CharField(max_length=10, blank=True, null=True)
    created_time = models.DateTimeField()
    is_active = models.IntegerField(blank=True, null=True)
    is_delete = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'db_project'


class DbProjectHeader(models.Model):
    id = models.IntegerField(primary_key=True)
    project_id = models.CharField(max_length=10, blank=True, null=True)
    name = models.CharField(max_length=20, blank=True, null=True)
    key = models.CharField(max_length=20, blank=True, null=True)
    value = models.TextField(blank=True, null=True)
    is_delete = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'db_project_header'


class DbProjectHost(models.Model):
    id = models.IntegerField(primary_key=True)
    project_id = models.CharField(max_length=10, blank=True, null=True)
    name = models.CharField(max_length=20, blank=True, null=True)
    host = models.TextField(blank=True, null=True)
    is_delete = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'db_project_host'


class DbRoast(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.CharField(max_length=30, blank=True, null=True)
    text = models.CharField(max_length=1000, blank=True, null=True)
    ctime = models.DateTimeField()
    is_delete = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'db_roast'


class DbStep(models.Model):
    id = models.IntegerField(primary_key=True)
    Case_id = models.CharField(max_length=10, blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(max_length=50, blank=True, null=True)
    index = models.IntegerField(blank=True, null=True)
    api_id = models.IntegerField(blank=True, null=True)
    api_method = models.CharField(max_length=10, blank=True, null=True)
    api_url = models.CharField(max_length=1000, blank=True, null=True)
    api_host = models.CharField(max_length=100, blank=True, null=True)
    api_header = models.CharField(max_length=1000, blank=True, null=True)
    api_body_method = models.CharField(max_length=10, blank=True, null=True)
    api_body = models.CharField(max_length=10, blank=True, null=True)
    get_path = models.CharField(max_length=500, blank=True, null=True)
    get_zz = models.CharField(max_length=500, blank=True, null=True)
    assert_zz = models.CharField(max_length=500, blank=True, null=True)
    assert_qz = models.CharField(max_length=500, blank=True, null=True)
    assert_path = models.CharField(max_length=500, blank=True, null=True)
    mock_res = models.CharField(max_length=1000, blank=True, null=True)
    public_header = models.CharField(max_length=1000, blank=True, null=True)
    api_login = models.CharField(max_length=10, blank=True, null=True)
    is_delete = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'db_step'


class DbUser(models.Model):
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_time = models.DateTimeField()
    is_active = models.IntegerField()
    is_delete = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'db_user'


class DbApi(models.Model):
    ts_method = models.CharField(max_length=255)
    ts_url = models.CharField(max_length=255)
    ts_header = models.CharField(max_length=255)
    ts_body_method = models.CharField(max_length=255)
    ts_api_body = models.CharField(max_length=255)
    ts_api_method = models.CharField(max_length=255)
    result = models.TextField(blank=True)
    head = models.TextField(blank=True)
    api_time = models.CharField(max_length=255)
    all_time = models.CharField(max_length=255)
    status_code = models.CharField(max_length=255)
    is_delete = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'db_api'


class UserToken(models.Model):
    user_id = models.IntegerField()
    user_name = models.CharField(max_length=255)
    token = models.CharField(max_length=255)
    failure_time = models.DateTimeField()
    is_failure = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'user_token'


class MyApiDbApis(models.Model):
    project_id = models.CharField(max_length=10, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    api_models = models.CharField(max_length=10, blank=True, null=True)
    api_url = models.CharField(max_length=1000, blank=True, null=True)
    api_header = models.CharField(max_length=1000, blank=True, null=True)
    api_login = models.CharField(max_length=10, blank=True, null=True)
    api_host = models.CharField(max_length=100, blank=True, null=True)
    des = models.CharField(max_length=100, blank=True, null=True)
    body_method = models.CharField(max_length=50, blank=True, null=True)
    api_body = models.CharField(max_length=1000, blank=True, null=True)
    result = models.TextField(blank=True, null=True)
    sign = models.CharField(max_length=10, blank=True, null=True)
    file_key = models.CharField(max_length=50, blank=True, null=True)
    file_name = models.CharField(max_length=50, blank=True, null=True)
    public_header = models.CharField(max_length=1000, blank=True, null=True)
    last_body_method = models.CharField(max_length=20, blank=True, null=True)
    last_api_body = models.CharField(max_length=1000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'my_api_db_apis'


class MyApiDbApisLog(models.Model):
    user_id = models.CharField(max_length=10, blank=True, null=True)
    api_method = models.CharField(max_length=10, blank=True, null=True)
    api_url = models.CharField(max_length=1000, blank=True, null=True)
    api_header = models.CharField(max_length=1000, blank=True, null=True)
    api_login = models.CharField(max_length=10, blank=True, null=True)
    api_host = models.CharField(max_length=100, blank=True, null=True)
    body_method = models.CharField(max_length=20, blank=True, null=True)
    api_body = models.CharField(max_length=1000, blank=True, null=True)
    sign = models.CharField(max_length=10, blank=True, null=True)
    file_key = models.CharField(max_length=50, blank=True, null=True)
    file_name = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'my_api_db_apis_log'


class MyApiDbCases(models.Model):
    project_id = models.CharField(max_length=10, blank=True, null=True)
    name = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'my_api_db_cases'


class MyApiDbGlobalData(models.Model):
    name = models.CharField(max_length=20, blank=True, null=True)
    user_id = models.CharField(max_length=10, blank=True, null=True)
    data = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'my_api_db_global_data'


class MyApiDbHomeHref(models.Model):
    name = models.CharField(max_length=30, blank=True, null=True)
    href = models.CharField(max_length=2000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'my_api_db_home_href'


class MyApiDbHost(models.Model):
    host = models.CharField(max_length=100, blank=True, null=True)
    des = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'my_api_db_host'


class MyApiDbLogin(models.Model):
    project_id = models.CharField(max_length=10, blank=True, null=True)
    api_method = models.CharField(max_length=10, blank=True, null=True)
    api_url = models.CharField(max_length=1000, blank=True, null=True)
    api_header = models.CharField(max_length=1000, blank=True, null=True)
    api_host = models.CharField(max_length=100, blank=True, null=True)
    body_method = models.CharField(max_length=20, blank=True, null=True)
    api_body = models.CharField(max_length=1000, blank=True, null=True)
    sign = models.CharField(max_length=10, blank=True, null=True)
    set = models.CharField(max_length=300, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'my_api_db_login'


class MyApiDbProject(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    remark = models.CharField(max_length=1000, blank=True, null=True)
    user = models.CharField(max_length=15, blank=True, null=True)
    user_id = models.CharField(max_length=10, blank=True, null=True)
    other = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'my_api_db_project'


class MyApiDbProjectHeader(models.Model):
    project_id = models.CharField(max_length=10, blank=True, null=True)
    name = models.CharField(max_length=20, blank=True, null=True)
    key = models.CharField(max_length=20, blank=True, null=True)
    value = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'my_api_db_project_header'


class MyApiDbProjectHost(models.Model):
    project_id = models.CharField(max_length=10, blank=True, null=True)
    name = models.CharField(max_length=20, blank=True, null=True)
    host = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'my_api_db_project_host'


class MyApiDbRoast(models.Model):
    user = models.CharField(max_length=30, blank=True, null=True)
    text = models.CharField(max_length=1000, blank=True, null=True)
    ctime = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'my_api_db_roast'


class MyApiDbStep(models.Model):
    case_id = models.CharField(db_column='Case_id', max_length=10, blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(max_length=50, blank=True, null=True)
    index = models.IntegerField(blank=True, null=True)
    api_method = models.CharField(max_length=10, blank=True, null=True)
    api_url = models.CharField(max_length=1000, blank=True, null=True)
    api_host = models.CharField(max_length=100, blank=True, null=True)
    api_header = models.CharField(max_length=1000, blank=True, null=True)
    api_body_method = models.CharField(max_length=10, blank=True, null=True)
    api_body = models.CharField(max_length=10, blank=True, null=True)
    get_path = models.CharField(max_length=500, blank=True, null=True)
    get_zz = models.CharField(max_length=500, blank=True, null=True)
    assert_zz = models.CharField(max_length=500, blank=True, null=True)
    assert_qz = models.CharField(max_length=500, blank=True, null=True)
    assert_path = models.CharField(max_length=500, blank=True, null=True)
    mock_res = models.CharField(max_length=1000, blank=True, null=True)
    public_header = models.CharField(max_length=1000, blank=True, null=True)
    api_login = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'my_api_db_step'


class DbSession(models.Model):
    name = models.CharField(max_length=255)
    pwd = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'db_session'


class Returned(models.Model):
    apis_id = models.IntegerField(blank=True, max_length=11)
    extract_path = models.TextField(blank=True)  # 提取返回值-路径法
    extract_re = models.TextField(blank=True)  # 提取返回值-正则
    expected = models.TextField(blank=True)  # 断言返回值-全文检索存在
    assert_re = models.TextField(blank=True)  # 断言返回值-正则
    assert_path = models.TextField(blank=True)  # 断言返回值-路径法
    mock_res = models.TextField(blank=True)  # mock返回值
    is_delete = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'returned'
