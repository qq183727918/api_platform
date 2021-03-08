from django.contrib import admin

from My_api.models import *

# Register your models here.

# admin.site.register() 是注册用的函数

admin.site.register(DB_Roast)
admin.site.register(DB_home_href)
admin.site.register(DB_project)
admin.site.register(DB_apis)
admin.site.register(DB_apis_log)
admin.site.register(DB_cases)
admin.site.register(DB_step)
admin.site.register(DB_project_header)
admin.site.register(DB_host)
admin.site.register(DB_project_host)
admin.site.register(DB_login)
admin.site.register(DB_global_data)
# 使用mysql表
admin.site.register(DbUser)
admin.site.register(DbProject)
admin.site.register(DbApis)
admin.site.register(DbStep)
