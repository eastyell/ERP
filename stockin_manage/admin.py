# 模块名称：其他库业务处理模块
# 创建日期：2020-6
# 最后修改日期：2020-6
# 作者：Jason

from django.contrib import admin
from stockin_manage.models import *
import datetime
from xadmin import views
import xadmin

# Register your models here.

# 回收下单
class ContactAdminDevice_return(object):
    def save_models(self):
        obj = self.new_obj
        flag = self.org_obj is None and 'create' or 'change'
        request = self.request
        if flag == 'create':  # 新增默认回填操作员
            obj.author = str(request.user)
            obj.save()
        else:
            obj.save()

    list_display = ('id', 'shopid', 'quantity', 'price', 'remark', 'pub_date', 'author', 'update_time')

# 回收入库
class ContactAdminDevice_return_stockin(object):
    def save_models(self):
        obj = self.new_obj
        flag = self.org_obj is None and 'create' or 'change'
        request = self.request
        if flag == 'create':  # 新增默认回填操作员
            obj.author = str(request.user)
            obj.save()
        else:
            obj.save()

    list_display = ('id', 'shopid', 'quantity',  'remark', 'pub_date', 'author', 'update_time')


xadmin.site.register(Device_return, ContactAdminDevice_return) # 回收下单
xadmin.site.register(Device_return_stockin, ContactAdminDevice_return_stockin)# 回收入库
