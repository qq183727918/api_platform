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

# class DefaultAdminSite(LazyObject):
#     def _setup(self):
#         AdminSiteClass = import_string(apps.get_app_config('admin').default_site)
#         self._wrapped = AdminSiteClass()
#
#
# # This global object represents the default admin site, for the
# # You Adminsite using the (Simple)Adminconfig default site
# # attribute。You
# # also instantiate Adminsite in your own code to create a
#
# site = DefaultAdminSite()
