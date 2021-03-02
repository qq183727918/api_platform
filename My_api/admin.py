from django.contrib import admin
# Register your models here.
from django.utils.module_loading import import_string

from My_api import apps
from My_api.models import *

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