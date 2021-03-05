from django.contrib import admin

from My_api.models import *

# Register your models here.

# admin.site.register() 是注册用的函数

admin.site.register(DbApis)
admin.site.register(DbApisLog)
admin.site.register(DbCases)
admin.site.register(DbStep)
admin.site.register(DbGlobalData)
admin.site.register(DbHomeHref)
admin.site.register(DbHost)
admin.site.register(DbLogin)
admin.site.register(DbProject)
admin.site.register(DbProjectHeader)
admin.site.register(DbProjectHost)
admin.site.register(DbRoast)
admin.site.register(DbUser)
