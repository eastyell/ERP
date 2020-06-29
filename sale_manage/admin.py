# 模块名称：销售管理业务处理模块
# 创建日期：2020-4
# 最后修改日期：2020-6
# 作者：Jason

from django.contrib import admin
import xadmin
from sale_manage.models import *
# Register your models here.

# 销售下单
class ContactAdminSales_out(object):
    def save_models(self):
        obj = self.new_obj
        flag = self.org_obj is None and 'create' or 'change'
        request = self.request
        if flag == 'create':  # 新增默认回填操作员
            obj.author = str(request.user)
            obj.save()
        else:
            obj.save()

    model_icon = 'fa fa-cog'  # 图标样式
    list_display = ('id', 'shopid', 'quantity', 'price', 'remark', 'pub_date', 'author', 'update_time')

# 销售下单出库
class ContactAdminSales_out_stockout_out(object):
    def save_models(self):
        obj = self.new_obj
        flag = self.org_obj is None and 'create' or 'change'
        request = self.request
        if flag == 'create':  # 新增默认回填操作员
            obj.author = str(request.user)
            obj.save()
        else:
            obj.save()

    model_icon = 'fa fa-cog'  # 图标样式
    list_display = ('id', 'shopid', 'quantity', 'price', 'remark', 'pub_date', 'author', 'update_time')

# 销售退单
class ContactAdminSales_return(object):
    def save_models(self):
        obj = self.new_obj
        flag = self.org_obj is None and 'create' or 'change'
        request = self.request
        if flag == 'create':  # 新增默认回填操作员
            obj.author = str(request.user)
            obj.save()
        else:
            obj.save()

    model_icon = 'fa fa-cog'  # 图标样式
    list_display = ('id', 'shopid', 'quantity', 'price', 'remark', 'pub_date', 'author', 'update_time')

# 销售退单入库
class ContactAdminSales_return_stockin(object):
    def save_models(self):
        obj = self.new_obj
        flag = self.org_obj is None and 'create' or 'change'
        request = self.request
        if flag == 'create':  # 新增默认回填操作员
            obj.author = str(request.user)
            obj.save()
        else:
            obj.save()

    model_icon = 'fa fa-cog'  # 图标样式
    list_display = ('id', 'shopid', 'quantity', 'price', 'remark', 'pub_date', 'author', 'update_time')

xadmin.site.register(Sales_out, ContactAdminSales_out)
xadmin.site.register(Sales_out_stockout, ContactAdminSales_out_stockout_out)
xadmin.site.register(Sales_return, ContactAdminSales_return)
xadmin.site.register(Sales_return_stockin, ContactAdminSales_return_stockin)
