# 模块名称：web地址路由
# 创建日期：2020-6
# 最后修改日期：2020-6
# 作者：Jason

""" crmURL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf.urls import url
from crm.settings import TEMPLATES_ROOT, TEMPLATES_RPT  # 导入项目设置文件 获得TEMPLATES定义的路径
from crm.settings import MEDIA_ROOT #导入项目设置文件 获得MEDIA_ROOT定义的路径
from django.urls import re_path #从原生urls类中导入重定向路径方法
from django.views.static import serve # server
from purchase_manage import views
from django.views import static
from django.conf import settings
# import notifications.urls #发送通知

import xadmin
from xadmin.plugins import xversion

xadmin.autodiscover()
xversion.register_models()

# 路由转发使用的是include()方法，需要提前导入，它的参数是转发目的地路径的字符串，路径以圆点分割。
urlpatterns = [
    # path(正则表达式, views视图函数，参数，别名),
    # path('admin/', xadmin.site.urls),
    # url(r'^admin/', xadmin.site.urls),
    path('', xadmin.site.urls),
    # 正则表达式  (?P<name>pattern)，其中name是组的名称，pattern是需要匹配的规则。
    # 重定向静态文件的读写路径(原来1.6的版本用的是url，坑苦我了，又去翻文档)
    re_path(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),
    # # 重定向静态文件的读写路径
    re_path(r'^device_manage/devices/(?P<path>.*)$', serve, {"document_root": TEMPLATES_ROOT}),
    re_path(r'^admin/report_manage/StockIn_view/(?P<path>.*)$', serve, {"document_root": TEMPLATES_RPT}),
    re_path(r'^admin/report_manage/StockOut_view/(?P<path>.*)$', serve, {"document_root": TEMPLATES_RPT}),
    re_path(r'^admin/report_manage/Repair_view/(?P<path>.*)$', serve, {"document_root": TEMPLATES_RPT}),
     ##　以下是新增
    url(r'^static/(?P<path>.*)$', static.serve,
       {'document_root': settings.STATIC_ROOT}, name='static'),
    #发送通知
    # path('inbox/notifications/', include(notifications.urls, namespace='notifications')),
]

