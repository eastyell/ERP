# 模块名称：基本信息控制
# 创建日期：2020-4
# 最后修改日期：2020-6
# 作者：Jason

from django.contrib import admin
from baseinfo_manage.models import *
import xadmin
import datetime
from xadmin.views.base import CommAdminView


# 商品信息
# 自定义模型管理类，作用：告诉django在生成的管理页面上显示哪些内容。
# class ContactAdminCustomer(admin.ModelAdmin):
class ContactAdminShop(object):
    def save_models(self):
        obj = self.new_obj
        flag = self.org_obj is None and 'create' or 'change'
        request = self.request
        if flag == 'create':  # 新增默认回填操作员
            obj.author = str(request.user)
            obj.save()
        else:
            obj.save()

    # 设置作者字段只读
    # readonly_fields = ("author",'pub_date')

    # 过滤，只能查看操作登陆人自己创建的内容
    # def get_queryset(self, request):
    #     qs = super(ContactAdmin, self).get_queryset(request)
    #     if request.user.is_superuser:
    #         return qs
        # return qs.filter(author=request.user)

    # listdisplay设置要显示在列表中的字段（id字段是Django模型的默认主键）
    list_display = ('id','name','shop_type','shop_level','shop_brand','quantity_good','remark','author','update_time')  # list
    search_fields = ('name',)  # 如果只有一个值，结尾必须有一个逗号，证明是list或元组
    search_name = '名称'
    # list_per_page设置每页显示多少条记录，默认是100条
    list_per_page = 5
    # ordering设置默认排序字段，负号表示降序排序
    ordering = ('id',)
    # list_editable 设置默认可编辑字段,第一个字段不允许编辑
    # list_editable = ['location', ]
    # 设置过滤
    # list_filter = ('location',)
    # fk_fields 设置显示外键字段
    # fk_fields = ('machine_room_id',)
    # 详细时间分层筛选
    date_hierarchy = 'pub_date'
    # 添加和修改时那些界面不显示
    exclude = ('author','pub_date','shop_brand_childs','status','cost','useage','price')
    # 指定列表显示的哪列可以点击跳转到详情更新页
    list_display_links = ('id','name')
    model_icon = 'fa fa-user'  # 图标样式
    style_fields = {'csdevice': 'm2m_transfer', 'csservice': 'ueditor', }  # 字段显示样式


# 库存信息
class ContactAdminDeviceStore(object):
    def save_models(self):
        obj = self.new_obj
        flag = self.org_obj is None and 'create' or 'change'
        request = self.request
        if flag == 'create':  # 新增默认回填操作员
            obj.author = str(request.user)
            obj.save()
        else:
            obj.save()

    # 设置作者字段只读
    # readonly_fields = ("authors",)

    # # 定制Action行为具体方法
    # def func(self, request, queryset):
    #     queryset.update(pub_date='2018-09-28')
    #     # 批量更新我们的created_time字段的值为2018-09-28
    #
    # func.short_description = "中文显示自定义Actions"
    # actions = [func,]
    # 定制Action行为具体方法
    # def func(self, request, queryset):
    #     print(self, request, queryset)
    #     print(request.POST.getlist('_selected_action'))
    #
    # func.short_description = "中文显示自定义Actions"
    # actions = [func, ]

    # Action选项都是在页面上方显示
    actions_on_top = True
    # Action选项都是在页面下方显示
    actions_on_bottom = False

    # 是否显示选择个数
    # actions_selection_counter = True

    # # 过滤，只能查看操作登陆人自己创建的内容
    # def get_queryset(self, request):
    #     # print('request111111' + request.GET['searchbar'])
    #     qs = super(ContactAdminDevices, self).get_queryset(request)
    #     if request.user.is_superuser:
    #         return qs
    #     return qs.filter(author=request.user)

    # listdisplay设置要显示在列表中的字段（id字段是Django模型的默认主键）
    list_display = ('shop','FRU','PN','machineModel','descs','replaces','type','quantity','quantityLock','quantityLover','price','image_data',
                    'location','source','suppliers','remark','author','update_time')  # list
    # list_display_links，列表时，定制列可以点击跳转。
    list_display_links = ('FRU','PN',)
    search_fields = ('FRU','PN')  # 如果只有一个值，结尾必须有一个逗号，证明是list或元组
    # search_name = {'FRU查询':'FRU','SN查询':'SN'}
    free_query_filter = ['FRU','PN']
    # list_per_page设置每页显示多少条记录，默认是100条
    list_per_page = 5
    # ordering设置默认排序字段，负号表示降序排序
    ordering = ['-update_time',]
    # list_editable 设置默认可编辑字段,第一个字段不允许编辑
    # list_editable = ['location', ]
    # 设置过滤
    list_filter = ('FRU','PN','location',)
    # fk_fields 设置显示外键字段
    # fk_fields = ('machine_room_id',)
    # 详细时间分层筛选
    date_hierarchy = ['pub_date']
    # fields，详细页面时，显示字段的字段
    #   fields = ('user',)
    # 添加和修改时那些界面不显示
    exclude = ('author','machineSN')
    # 详细页面时，M2M显示时，数据移动选择（方向：上下和左右）
    filter_horizontal = ('authors',)  # filter_horizontal 从‘多选框’的形式改变为‘过滤器’的方式，水平排列过滤器，必须是一个 ManyToManyField类型，且不能用于 ForeignKey字段，默认地，管理工具使用`` 下拉框`` 来展现`` 外键`` 字段
    filter_vertical = ("location",)  #同上filter_horizontal，垂直排列过滤器
    # 或filter_horizontal = ("m2m字段",)
    empty_value_display = '无'#"列数据为空时，默认显示"
    # advanced_filter_fields = ('name', ('product_lot__product__name', 'Product name'))
    show_detail_fields = ['desc','location'] #在指定的字段后添加一个显示数据详情的一个按钮
    free_query_filter = ['FRU', 'PN']
    aggregate_fields = {'quantity': 'sum',}  # 列聚合，在list表格下面会增加一行统计的数据，可用的值："count","min","max","avg",  "sum"
    # model_icon = 'fa fa-comment'  # 图标样式  # 图标样式
    model_icon = 'fa fa-user'  # 图标样式
    style_fields = {'csdevice': 'm2m_transfer', 'csservice': 'ueditor', }  # 字段显示样式
    list_bookmarks = [{
        'title': "今天库存",  # 书签的名称, 显示在书签菜单中
        # 'query': {'gender': True, 'postdate__gte': 20200327},  # 过滤参数, 是标准的 queryset 过滤

        # 'query': {'pub_date__exact': int(datetime.datetime.now().strftime('%Y%m%d'))},  # 过滤参数, 是标准的 queryset 过滤
        # 'query': {'pub_date__exact': '20200408'},  # 过滤参数, 是标准的 queryset
        'query': {"author":'root'},  # 过滤参数, 是标准的 queryset 过滤
        'order': ('FRU', 'PN' ),  # 排序参数
        'selected': True,
    },
        {
            'title': "近两天库存",  # 书签的名称, 显示在书签菜单中
            'query': {'pub_date__gte': (datetime.datetime.now() + datetime.timedelta(-1)).strftime('%Y%m%d')},
            # 过滤参数, 是标准的 queryset 过滤
            # 'order': ('FRU', 'PN' ),  # 排序参数
        },
    ]

    # data_charts = {
    #     "quantityOut_counts": {
    #         'title': '出库统计',
    #         'x-field': "pub_date",
    #         'y-field': ("quantityOut",),
    #         'option': {
    #             "series": {"bars": {"align": "center", "barWidth": 0.5, "show": True}},
    #             "xaxis": {"aggregate": "count", "mode": "categories"}
    #         }
    #     },
    #     "quantityIn_counts": {
    #         'title': '入库统计',
    #         'x-field': "pub_date",
    #         'y-field': ("quantityIn"),
    #         # 'option': {
    #         #     "series": {"bars": {"align": "center", "barWidth": 0.8, "show": True}},
    #         #     "xaxis": {"aggregate": "count", "mode": "categories"}
    #         # },
    #     },
    # }

# 客户
# 自定义模型管理类，作用：告诉django在生成的管理页面上显示哪些内容。
# class ContactAdminCustomer(admin.ModelAdmin):
class ContactAdminCustomer(object):
    def save_models(self):
        obj = self.new_obj
        flag = self.org_obj is None and 'create' or 'change'
        request = self.request
        if flag == 'create':  # 新增默认回填操作员
            obj.author = str(request.user)
            obj.save()
        else:
            obj.save()

    # 设置作者字段只读
    # readonly_fields = ("author",'pub_date')

    # 过滤，只能查看操作登陆人自己创建的内容
    # def get_queryset(self, request):
    #     qs = super(ContactAdmin, self).get_queryset(request)
    #     if request.user.is_superuser:
    #         return qs
        # return qs.filter(author=request.user)

    # listdisplay设置要显示在列表中的字段（id字段是Django模型的默认主键）
    list_display = ('name','customer_type','base_info','contract_info','clue','service',
                    'people','tel','address','remark','author','update_time')  # list
    search_fields = ('name',)  # 如果只有一个值，结尾必须有一个逗号，证明是list或元组
    search_name = '名称'
    # list_per_page设置每页显示多少条记录，默认是100条
    list_per_page = 5
    # ordering设置默认排序字段，负号表示降序排序
    ordering = ('-update_time',)
    # list_editable 设置默认可编辑字段,第一个字段不允许编辑
    # list_editable = ['location', ]
    # 设置过滤
    # list_filter = ('location',)
    # fk_fields 设置显示外键字段
    # fk_fields = ('machine_room_id',)
    # 详细时间分层筛选
    date_hierarchy = 'pub_date'
    # 添加和修改时那些界面不显示
    exclude = ('author','pub_date')
    # 指定列表显示的哪列可以点击跳转到详情更新页
    list_display_links = ('name', 'customer_type')
    model_icon = 'fa fa-user'  # 图标样式
    style_fields = {'csdevice': 'm2m_transfer', 'csservice': 'ueditor', }  # 字段显示样式

# 潜在客户
class ContactAdminCustomersLatent(object):
    def save_models(self):
        obj = self.new_obj
        flag = self.org_obj is None and 'create' or 'change'
        request = self.request
        if flag == 'create':  # 新增默认回填操作员
            obj.author = str(request.user)
            obj.save()
        else:
            obj.save()

    # listdisplay设置要显示在列表中的字段（id字段是Django模型的默认主键）
    list_display = ('pub_date','saler','customer','item','rate','status','remark','author','update_time')  # list
    search_fields = ('customer',)  # 如果只有一个值，结尾必须有一个逗号，证明是list或元组
    search_name = '潜在客户'
    # list_per_page设置每页显示多少条记录，默认是100条
    list_per_page = 5
    # ordering设置默认排序字段，负号表示降序排序
    ordering = ('-update_time',)
    # list_editable 设置默认可编辑字段,第一个字段不允许编辑
    # list_editable = ['location', ]
    # 设置过滤
    # list_filter = ('location',)
    # fk_fields 设置显示外键字段
    # fk_fields = ('machine_room_id',)
    # 详细时间分层筛选
    date_hierarchy = 'pub_date'
    # 添加和修改时那些界面不显示
    exclude = ('author','update_time')
    # 指定列表显示的哪列可以点击跳转到详情更新页
    list_display_links = ('saler', 'customer')
    model_icon = 'fa fa-user'  # 图标样式
    style_fields = {'csdevice': 'm2m_transfer', 'csservice': 'ueditor', }  # 字段显示样式

# 签约客户
class ContactAdminCustomersSign(object):
    def save_models(self):
        obj = self.new_obj
        flag = self.org_obj is None and 'create' or 'change'
        request = self.request
        if flag == 'create':  # 新增默认回填操作员
            obj.author = str(request.user)
            obj.save()
        else:
            obj.save()

    # listdisplay设置要显示在列表中的字段（id字段是Django模型的默认主键）
    list_display = ('contractid','pub_date','customer','type','item','saler',
                    'engineer','status','file_data','remark','author','update_time')  # list
    search_fields = ('customer',)  # 如果只有一个值，结尾必须有一个逗号，证明是list或元组
    search_name = '签约客户'
    # list_per_page设置每页显示多少条记录，默认是100条
    list_per_page = 5
    # ordering设置默认排序字段，负号表示降序排序
    ordering = ('-update_time',)
    # list_editable 设置默认可编辑字段,第一个字段不允许编辑
    # list_editable = ['location', ]
    # 设置过滤
    # list_filter = ('location',)
    # fk_fields 设置显示外键字段
    # fk_fields = ('machine_room_id',)
    # 详细时间分层筛选
    date_hierarchy = 'pub_date'
    # 添加和修改时那些界面不显示
    exclude = ('author','update_time')
    # 指定列表显示的哪列可以点击跳转到详情更新页
    list_display_links = ('contractid', 'customer')
    model_icon = 'fa fa-user'  # 图标样式
    style_fields = {'csdevice': 'm2m_transfer', 'csservice': 'ueditor', }  # 字段显示样式

# 合同信息
class ContactAdminContractInfo(object):
    def save_models(self):
        obj = self.new_obj
        flag = self.org_obj is None and 'create' or 'change'
        request = self.request
        if flag == 'create':  # 新增默认回填操作员
            obj.author = str(request.user)
            obj.save()
        else:
            obj.save()

    # listdisplay设置要显示在列表中的字段（id字段是Django模型的默认主键）
    list_display = ('contractid','amount','paydesc','rate','paydays','billdate',
                    'paystatus','file_data','remark','author','update_time')  # list
    search_fields = ('contractid',)  # 如果只有一个值，结尾必须有一个逗号，证明是list或元组
    search_name = '合同编号'
    # list_per_page设置每页显示多少条记录，默认是100条
    list_per_page = 5
    # ordering设置默认排序字段，负号表示降序排序
    ordering = ('-update_time',)
    # list_editable 设置默认可编辑字段,第一个字段不允许编辑
    # list_editable = ['location', ]
    # 设置过滤
    # list_filter = ('location',)
    # fk_fields 设置显示外键字段
    # fk_fields = ('machine_room_id',)
    # 详细时间分层筛选
    date_hierarchy = 'pub_date'
    # 添加和修改时那些界面不显示
    exclude = ('author','update_time')
    # 指定列表显示的哪列可以点击跳转到详情更新页
    list_display_links = ('contractid', 'paydesc')
    model_icon = 'fa fa-user'  # 图标样式
    style_fields = {'csdevice': 'm2m_transfer', 'csservice': 'ueditor', }  # 字段显示样式

# 合同服务内容
class ContactAdminContractContent(object):
    def save_models(self):
        obj = self.new_obj
        flag = self.org_obj is None and 'create' or 'change'
        request = self.request
        if flag == 'create':  # 新增默认回填操作员
            obj.author = str(request.user)
            obj.save()
        else:
            obj.save()

    # listdisplay设置要显示在列表中的字段（id字段是Django模型的默认主键）
    list_display = ('contractid','type','model','SN','level','begindate','enddate',
                    'address','deliverydate','setupdate','remark','author','update_time')  # list
    search_fields = ('SN',)  # 如果只有一个值，结尾必须有一个逗号，证明是list或元组
    search_name = '合同服务内容'
    # list_per_page设置每页显示多少条记录，默认是100条
    list_per_page = 5
    # ordering设置默认排序字段，负号表示降序排序
    ordering = ('-update_time',)
    # list_editable 设置默认可编辑字段,第一个字段不允许编辑
    list_editable = ['type','level','model', 'begindate','enddate','deliverydate','setupdate']
    # 设置过滤
    list_filter = ('type','level','begindate','enddate','deliverydate','setupdate')
    # fk_fields 设置显示外键字段
    # fk_fields = ('machine_room_id',)
    # 详细时间分层筛选
    # date_hierarchy = 'pub_date'
    # 添加和修改时那些界面不显示
    exclude = ('author','update_time')
    # 指定列表显示的哪列可以点击跳转到详情更新页
    list_display_links = ('contractid', 'type')
    model_icon = 'fa fa-user'  # 图标样式
    style_fields = {'csdevice': 'm2m_transfer', 'csservice': 'ueditor', }  # 字段显示样式
    refresh_times = (3, 5)  # 用户可以选择三秒或者5秒刷新一次

# 供应商
# 自定义模型管理类，作用：告诉django在生成的管理页面上显示哪些内容。
# class ContactAdminSupplier(admin.ModelAdmin):
class ContactAdminSupplier(object):
    def save_models(self):
       obj = self.new_obj
       flag = self.org_obj is None and 'create' or 'change'
       request = self.request
       if flag == 'create':  # 新增默认回填操作员
          obj.author = str(request.user)
          obj.save()
       else:
          obj.save()

    # 设置作者字段只读
    # readonly_fields = ("author",'pub_date')

    # 过滤，只能查看操作登陆人自己创建的内容
    # def get_queryset(self, request):
    #     qs = super(ContactAdmin, self).get_queryset(request)
    #     if request.user.is_superuser:
    #         return qs
        # return qs.filter(author=request.user)

    # listdisplay设置要显示在列表中的字段（id字段是Django模型的默认主键）
    list_display = ('name','adress','people','tel','remark','author','update_time')  # list
    search_fields = ('name',)  # 如果只有一个值，结尾必须有一个逗号，证明是list或元组
    search_name = '名称'
    # list_per_page设置每页显示多少条记录，默认是100条
    list_per_page = 5
    # ordering设置默认排序字段，负号表示降序排序
    ordering = ('-update_time',)
    # list_editable 设置默认可编辑字段,第一个字段不允许编辑
    # list_editable = ['location', ]
    # 设置过滤
    list_filter = ('name','pub_date',)
    # fk_fields 设置显示外键字段
    # fk_fields = ('machine_room_id',)
    # 详细时间分层筛选
    date_hierarchy = 'pub_date'
    # 添加和修改时那些界面不显示
    exclude = ('author','pub_date')
    # 设置哪些字段可以点击进入编辑界面
    # 指定列表显示的哪列可以点击跳转到详情更新页
    list_display_links = ('name', 'adress')
    # 这些字段可以点击显示详细信息
    show_detail_fields = ['adress']
    model_icon = 'fa fa-user'  # 图标样式

# 需求信息
# 自定义模型管理类，作用：告诉django在生成的管理页面上显示哪些内容。
# class ContactAdminSupplier(admin.ModelAdmin):
class ContactAdminRequirement(object):
    def save_models(self):
       obj = self.new_obj
       flag = self.org_obj is None and 'create' or 'change'
       request = self.request
       if flag == 'create':  # 新增默认回填操作员
          # obj.author = str(request.user)
          obj.save()
       else:
          obj.save()

    # 设置作者字段只读
    # readonly_fields = ("author",'pub_date')

    # 过滤，只能查看操作登陆人自己创建的内容
    # def get_queryset(self, request):
    #     qs = super(ContactAdmin, self).get_queryset(request)
    #     if request.user.is_superuser:
    #         return qs
        # return qs.filter(author=request.user)

    # listdisplay设置要显示在列表中的字段（id字段是Django模型的默认主键）
    list_display = ('pub_date','solve','type','desc','image_data','author','answer')  # list
    search_fields = ('desc',)  # 如果只有一个值，结尾必须有一个逗号，证明是list或元组
    search_name = '内容'
    # list_per_page设置每页显示多少条记录，默认是100条
    list_per_page = 5
    # ordering设置默认排序字段，负号表示降序排序
    ordering = ('-pub_date',)
    # list_editable 设置默认可编辑字段,第一个字段不允许编辑
    list_editable = ('solve','type','desc','answer' )
    # 设置过滤
    list_filter = ('author','type','pub_date',)
    # fk_fields 设置显示外键字段
    # fk_fields = ('machine_room_id',)
    # 详细时间分层筛选
    # date_hierarchy = 'pub_date'
    # 添加和修改时那些界面不显示
    #exclude = ('author','pub_date')
    # 设置哪些字段可以点击进入编辑界面
    # 指定列表显示的哪列可以点击跳转到详情更新页
    list_display_links = ('pub_date', 'desc')
    # 这些字段可以点击显示详细信息
    show_detail_fields = ['desc']
    model_icon = 'fa fa-user'  # 图标样式


# 注册基本信息Model类
xadmin.site.register(Shop, ContactAdminShop) #商品信息
xadmin.site.register(DeviceStores, ContactAdminDeviceStore)  #库存信息
xadmin.site.register(Suppliers, ContactAdminSupplier) # 供应商信息
xadmin.site.register(Customers, ContactAdminCustomer)  #客户信息
xadmin.site.register(CustomersLatent, ContactAdminCustomersLatent) # 潜在项目
xadmin.site.register(CustomersSign, ContactAdminCustomersSign) # 签约项目
xadmin.site.register(ContractContent, ContactAdminContractContent) # 项目服务内容
xadmin.site.register(ContractInfo, ContactAdminContractInfo) # 合同服务内容
xadmin.site.register(Requirement, ContactAdminRequirement) # 项目需求管理


# # 设置登陆窗口的标题
# admin.site.site_header = '客户档案管理'
# # 设置页签标题
# admin.site.site_title = '客户档案'
