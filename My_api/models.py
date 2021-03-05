# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class DbApis(models.Model):
    id = models.IntegerField(primary_key=True)
    project_id = models.CharField(max_length=10, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    api_models = models.CharField(max_length=10, blank=True, null=True)
    api_url = models.CharField(max_length=1000, blank=True, null=True)
    api_header = models.CharField(max_length=1000, blank=True, null=True)
    api_login = models.CharField(max_length=10, blank=True, null=True)
    api_host = models.CharField(max_length=100, blank=True, null=True)
    des = models.CharField(max_length=100, blank=True, null=True)
    api_body = models.CharField(max_length=1000, blank=True, null=True)
    result = models.TextField(blank=True, null=True)
    sign = models.CharField(max_length=10, blank=True, null=True)
    file_key = models.CharField(max_length=50, blank=True, null=True)
    file_name = models.CharField(max_length=50, blank=True, null=True)
    public_header = models.CharField(max_length=1000, blank=True, null=True)
    last_body_method = models.CharField(max_length=20, blank=True, null=True)
    last_api_body = models.CharField(max_length=1000, blank=True, null=True)
    body_method = models.CharField(max_length=50, blank=True, null=True)
    is_delete = models.IntegerField()

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
    is_delete = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'db_cases'


class DbGlobalData(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20, blank=True, null=True)
    user_id = models.CharField(max_length=10, blank=True, null=True)
    data = models.TextField(blank=True, null=True)
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
    id = models.IntegerField(primary_key=True)
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
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    remark = models.CharField(max_length=1000, blank=True, null=True)
    user = models.CharField(max_length=15, blank=True, null=True)
    other = models.CharField(max_length=200, blank=True, null=True)
    user_id = models.CharField(max_length=10, blank=True, null=True)
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
    is_delete = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'db_step'


class DbUser(models.Model):
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    is_active = models.IntegerField()
    is_delete = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'db_user'

    def __str__(self):
        return self.id
