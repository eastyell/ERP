# 模块名称：报表管理业务处理模块
# 创建日期：2020-6
# 最后修改日期：2020-6
# 作者：Jason

from django.contrib import admin
import xadmin
from report_manage.models import *

# 出入库明细
class ContactAdminStock_detail(object):
    def save_models(self):
        obj = self.new_obj
        flag = self.org_obj is None and 'create' or 'change'
        request = self.request
        obj.author = str(request.user)
        if flag == 'create':

            obj.save()
        else:
            obj.save()

    model_icon = 'fa fa-exchange'  # 图标样式
    list_display = ('bill_type', 'bill_id', 'shop', 'FRU', 'SN','PN','machineModel',
                    'machineSN','FRUSelect','desc','source','replace','useage','quantity','location','image',
                    'remark', 'pub_date', 'author', 'update_time')
    # 设置过滤
    list_filter = ('pub_date','FRU', 'PN', 'location',)
    search_fields = ('FRU', 'PN')
    aggregate_fields = {'quantity': 'sum', }


# Register your models here.
xadmin.site.register(Stock_detail, ContactAdminStock_detail)