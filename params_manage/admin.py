# 模块名称：参数设置业务处理模块
# 创建日期：2020-6
# 最后修改日期：2020-6
# 作者：Jason

from django.contrib import admin
from params_manage.models import *
# from reversion.admin import VersionAdmin
# import reversion
import xadmin

# 库存位置
class ContactAdminLocation(object):
    def save_models(self):
        obj = self.new_obj
        flag = self.org_obj is None and 'create' or 'change'
        request = self.request
        if flag == 'create':  # 新增默认回填操作员
            obj.author = str(request.user)
            obj.save()
        else:
            obj.save()
    list_display = ('code','name','level1','level2','level3','remark','author','update_time')
    model_icon = 'fa fa-pencil-square-o' # 图标样式
    # 添加和修改时那些界面不显示
    exclude = ('author',)
    list_editable = ('code','name')
    # list_per_page设置每页显示多少条记录，默认是100条
    list_per_page = 5

# 客户类型
class ContactAdminCustomer_type(object):
    def save_models(self):
        obj = self.new_obj
        flag = self.org_obj is None and 'create' or 'change'
        request = self.request
        if flag == 'create':  # 新增默认回填操作员
            obj.author = str(request.user)
            obj.save()
        else:
            obj.save()
    list_display = ('name','author','update_time')
    model_icon = 'fa fa-pencil-square-o'  # 图标样式
    # 添加和修改时那些界面不显示
    exclude = ('author',)
    list_editable = ('name')
    # list_per_page设置每页显示多少条记录，默认是100条
    list_per_page = 5

# 客户地址信息
class ContactAdminCustomer_address(object):
    def save_models(self):
        obj = self.new_obj
        flag = self.org_obj is None and 'create' or 'change'
        request = self.request
        if flag == 'create':  # 新增默认回填操作员
            obj.author = str(request.user)
            obj.save()
        else:
            obj.save()
    list_display = ('customer_id','name','address_type','address',
                    'people','tel','author','update_time')
    show_detail_fields = ['name']  # 在指定的字段后添加一个显示数据详情的一个按钮
    model_icon = 'fa fa-pencil-square-o'  # 图标样式
    # 添加和修改时那些界面不显示
    exclude = ('author',)
    # list_editable 设置默认可编辑字段,第一个字段不允许编辑
    list_editable = ['address_type','address','name', ]
    # list_display_links，列表时，定制列可以点击跳转。
    list_display_links = ('customer_id', 'name', 'address',)
    # list_per_page设置每页显示多少条记录，默认是100条
    list_per_page = 5

# 采购类型
class ContactAdminPurchase_type(object):
    def save_models(self):
        obj = self.new_obj
        flag = self.org_obj is None and 'create' or 'change'
        request = self.request
        if flag == 'create':  # 新增默认回填操作员
            obj.author = str(request.user)
            obj.save()
        else:
            obj.save()
    list_display = ('type','author','update_time')
    model_icon = 'fa fa-pencil-square-o'  # 图标样式
    # 添加和修改时那些界面不显示
    exclude = ('author',)
    list_editable = ('type')
    # list_per_page设置每页显示多少条记录，默认是100条
    list_per_page = 5

# 备件FRU
class ContactAdminDevice_FRU(object):
    def save_models(self):
        obj = self.new_obj
        flag = self.org_obj is None and 'create' or 'change'
        request = self.request
        if flag == 'create':  # 新增默认回填操作员
            obj.author = str(request.user)
            obj.save()
        else:
            obj.save()
    list_display = ('name','desc','author','update_time')
    model_icon = 'fa fa-pencil-square-o'  # 图标样式
    # 添加和修改时那些界面不显示
    exclude = ('author',)
    list_editable = ('name','desc')
    # list_per_page设置每页显示多少条记录，默认是100条
    list_per_page = 5
    search_fields = ('name', 'desc')

# 整机类型
class ContactAdminDevice_kind(object):
    def save_models(self):
        obj = self.new_obj
        flag = self.org_obj is None and 'create' or 'change'
        request = self.request
        if flag == 'create':  # 新增默认回填操作员
            obj.author = str(request.user)
            obj.save()
        else:
            obj.save()
    list_display = ('name','desc','author','update_time')
    model_icon = 'fa fa-pencil-square-o'  # 图标样式
    # 添加和修改时那些界面不显示
    exclude = ('author',)
    list_editable = ('name','desc')
    # list_per_page设置每页显示多少条记录，默认是100条
    list_per_page = 5

# 备件类别
class ContactAdminDevice_type(object):
    def save_models(self):
        obj = self.new_obj
        flag = self.org_obj is None and 'create' or 'change'
        request = self.request
        if flag == 'create':  # 新增默认回填操作员
            obj.author = str(request.user)
            obj.save()
        else:
            obj.save()
    list_display = ('name','author','update_time')
    model_icon = 'fa fa-pencil-square-o'  # 图标样式
    # 添加和修改时那些界面不显示
    exclude = ('author',)
    list_editable = ('name')
    # list_per_page设置每页显示多少条记录，默认是100条
    list_per_page = 5

# 商品类别
class ContactAdminBase_type(object):
    def save_models(self):
        obj = self.new_obj
        flag = self.org_obj is None and 'create' or 'change'
        request = self.request
        if flag == 'create':  # 新增默认回填操作员
            obj.author = str(request.user)
            obj.save()
        else:
            obj.save()
    list_display = ('name','author','update_time')
    model_icon = 'fa fa-pencil-square-o'  # 图标样式
    # 添加和修改时那些界面不显示
    exclude = ('author',)
    list_editable = ('name')
    # list_per_page设置每页显示多少条记录，默认是100条
    list_per_page = 5

# 商品品牌
class ContactAdminBase_brand(object):
    def save_models(self):
        obj = self.new_obj
        flag = self.org_obj is None and 'create' or 'change'
        request = self.request
        if flag == 'create':  # 新增默认回填操作员
            obj.author = str(request.user)
            obj.save()
        else:
            obj.save()
    list_display = ('name','author','update_time')
    model_icon = 'fa fa-pencil-square-o'  # 图标样式
    # 添加和修改时那些界面不显示
    exclude = ('author',)
    list_editable = ('name')
    # list_per_page设置每页显示多少条记录，默认是100条
    list_per_page = 5

# 商品等级
class ContactAdminBase_level(object):
    def save_models(self):
        obj = self.new_obj
        flag = self.org_obj is None and 'create' or 'change'
        request = self.request
        if flag == 'create':  # 新增默认回填操作员
            obj.author = str(request.user)
            obj.save()
        else:
            obj.save()
    list_display = ('name','author','update_time')
    model_icon = 'fa fa-pencil-square-o'  # 图标样式
    # 添加和修改时那些界面不显示
    exclude = ('author',)
    list_editable = ('name')
    # list_per_page设置每页显示多少条记录，默认是100条
    list_per_page = 5

# 商品子品牌
class ContactAdminBase_brand_child(object):
    def save_models(self):
        obj = self.new_obj
        flag = self.org_obj is None and 'create' or 'change'
        request = self.request
        if flag == 'create':  # 新增默认回填操作员
            obj.author = str(request.user)
            obj.save()
        else:
            obj.save()
    list_display = ('name','author','update_time')
    model_icon = 'fa fa-pencil-square-o' # 图标样式
    # 添加和修改时那些界面不显示
    exclude = ('author',)
    list_editable = ('name')

# Register your models here.
xadmin.site.register(Customer_type, ContactAdminCustomer_type) # 客户类型
xadmin.site.register(Customer_address, ContactAdminCustomer_address) # 客户地址信息
xadmin.site.register(Location, ContactAdminLocation)  # 库存位置
xadmin.site.register(Purchase_type, ContactAdminPurchase_type)  # 采购类型
xadmin.site.register(Device_FRU, ContactAdminDevice_FRU)  # FRU信息
xadmin.site.register(Device_kind, ContactAdminDevice_kind) # 整机类型
xadmin.site.register(Device_type, ContactAdminDevice_type) # 备件类别
xadmin.site.register(Base_type, ContactAdminBase_type)  # 基础类别
xadmin.site.register(Base_brand, ContactAdminBase_brand) # 备件品牌
xadmin.site.register(Base_brand_child, ContactAdminBase_brand_child) # 备件子品牌
xadmin.site.register(Base_level, ContactAdminBase_level) # 备件等级
