# 模块名称：其他出库业务处理模块
# 创建日期：2020-6
# 最后修改日期：2020-6
# 作者：Jason

from django.contrib import admin
from stockout_manage.models import *
import datetime
from xadmin import views
import xadmin

# 自定义模型管理类，作用：告诉django在生成的管理页面上显示哪些内容。
# class ContactAdminDevices(admin.ModelAdmin)
class ContactAdminDevices(object):
    # 增加内容时，将登陆人的账号存入指定的字段中，models中要预留这个字段，这里是author
    # def save_model(self, request, obj, form, change):
    #     if change:  # 更新操作返回true
    #         obj.save()
    #     else:  # 否则是新增
    #         obj.author = request.user
    #         obj.save()
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
    list_display = ('FRU','SN','PN','desc','image_data','quantityIn','quantityOut','TotalQuantity',
                    'location','source','replace','remark','pub_date','author','update_time')  # list
    # list_display_links，列表时，定制列可以点击跳转。
    list_display_links = ('FRU','SN','PN',)
    search_fields = ('FRU','SN')  # 如果只有一个值，结尾必须有一个逗号，证明是list或元组
    # search_name = {'FRU查询':'FRU','SN查询':'SN'}
    free_query_filter = ['FRU','SN','PN']
    # list_per_page设置每页显示多少条记录，默认是100条
    list_per_page = 5
    # ordering设置默认排序字段，负号表示降序排序
    ordering = ['-update_time',]
    # list_editable 设置默认可编辑字段,第一个字段不允许编辑
    # list_editable = ['location', ]
    # 设置过滤
    list_filter = ('FRU','SN','PN','location',)
    # fk_fields 设置显示外键字段
    # fk_fields = ('machine_room_id',)
    # 详细时间分层筛选
    date_hierarchy = ['pub_date']
    # fields，详细页面时，显示字段的字段
    #   fields = ('user',)
    # 添加和修改时那些界面不显示
    exclude = ('author','quantity')
    # 详细页面时，M2M显示时，数据移动选择（方向：上下和左右）
    filter_horizontal = ('authors',)  # filter_horizontal 从‘多选框’的形式改变为‘过滤器’的方式，水平排列过滤器，必须是一个 ManyToManyField类型，且不能用于 ForeignKey字段，默认地，管理工具使用`` 下拉框`` 来展现`` 外键`` 字段
    filter_vertical = ("location",)  #同上filter_horizontal，垂直排列过滤器
    # 或filter_horizontal = ("m2m字段",)
    empty_value_display = '无'#"列数据为空时，默认显示"
    # advanced_filter_fields = ('name', ('product_lot__product__name', 'Product name'))
    show_detail_fields = ['desc'] #在指定的字段后添加一个显示数据详情的一个按钮
    free_query_filter = ['FRU', 'PN']
    aggregate_fields = {'quantityIn': 'sum','quantityOut':'sum'}  # 列聚合，在list表格下面会增加一行统计的数据，可用的值："count","min","max","avg",  "sum"
    model_icon = 'fa fa-comment'  # 图标样式
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

class ContactAdminDeviceStore(object):
    # 增加内容时，将登陆人的账号存入指定的字段中，models中要预留这个字段，这里是author
    # def save_model(self, request, obj, form, change):
    #     if change:  # 更新操作返回true
    #         obj.save()
    #     else:  # 否则是新增
    #         obj.author = request.user
    #         obj.save()
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
    list_display = ('FRU','PN','desc','replace','type','quantity','price','image_data',
                    'location','source','remark','author','update_time')  # list
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
    exclude = ('author',)
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

# class ContactAdminInstock(admin.ModelAdmin):
class ContactAdminInstock(object):
    # 增加内容时，将登陆人的账号存入指定的字段中，models中要预留这个字段，这里是author
    # def save_model(self, request, obj, form, change):
    #     if change:  # 更新操作返回true
    #         obj.save()
    #     else:  # 否则是新增
    #         # obj.author = 'root'//request.user
    #         obj.save()

    # 设置作者字段只读
    # readonly_fields = ("authors",)

    # 过滤，只能查看操作登陆人自己创建的内容
    # def get_queryset(self, request):
    #     qs = super(ContactAdmin, self).get_queryset(request)
    #     if request.user.is_superuser:
    #         return qs
        # return qs.filter(author=request.user)

    # listdisplay设置要显示在列表中的字段（id字段是Django模型的默认主键）
    list_display = ('FRU','SN','PN','desc','image_data','quantity','source','replace',
                    'remark','pub_date','author','update_time')  # list
    search_fields = ('FRU',)  # 如果只有一个值，结尾必须有一个逗号，证明是list或元组
    search_name = 'FRU'
    free_query_filter = ['FRU','PN']
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
    # exclude = ('author',)

#出入库明细
class ContactAdminDevice_stockinout_detail(object):
    def save_models(self):
        obj = self.new_obj
        flag = self.org_obj is None and 'create' or 'change'
        request = self.request
        if flag == 'create':  # 新增默认回填操作员
            obj.author = str(request.user)
            obj.save()
        else:
            obj.save()

    list_display = ('bill_id', 'shopid', 'trade_type','stockinout_type','type','SN', 'FRU', 'PN',
                    'desc', 'source', 'replace', 'useage','price', 'quantity', 'location',
                    'image_data', 'remark', 'pub_date', 'author')
    # model_icon = 'fa fa-user'  # 图标样式
    # 添加和修改时那些界面不显示
    exclude = ('author',)
    search_fields = ('FRU', 'SN', 'PN', 'replace')
    free_query_filter = ['FRU', 'SN', 'PN']
    # list_editable = ['location', ]
    show_detail_fields = ['desc', 'location']
    list_filter = ('stockinout_type','FRU', 'SN', 'PN', 'location', 'replace')
    date_hierarchy = ['pub_date']
    # 列聚合，在list表格下面会增加一行统计的数据，可用的值："count","min","max","avg",  "sum"
    aggregate_fields = {'quantity': 'sum',
                        }

class BaseSetting(object):
    enable_themes = True #开启主题选择
    use_bootswatch = True

class GlobalSettings(object):
    # 设置左上角title名字
    site_title = "备件库存管理系统"
    # 设置底部关于版权信息
    site_footer = "腾孝网络科技"
    #设置菜单缩放
    menu_style = "accordion"     #左侧导航条修改可折叠
    global_models_icon = {
         # Devices: "glyphicon glyphicon-user", #UserDistrict: "fa fa-cloud"
      }  # 设置models的全局图标

    # 自定义菜单
    # def get_site_menu(self):  # 名称不能改
    #     return [
    #         {
    #             'title': '自定义采购模块',
    #             'icon': 'fa fa-bar-chart-o',
    #             'menus': (
    #                 {
    #                     'title': '采购下单',  # 这里是你菜单的名称
    #                     'url': '/admin/purchase_manage/test_view',  # 这里填写你将要跳转url
    #                     'icon': 'fa fa-cny'  # 这里是bootstrap的icon类名，要换icon只要登录bootstrap官网找到icon的对应类名换上即可
    #                 },
    #                 {
    #                     'title': '采购入库',
    #                     'url': 'http://www.taobao.com',
    #                     'icon': 'fa fa-cny'
    #                 }
    #             )
    #         }
    #     ]

#注册你上面填写的url
from purchase_manage.views import TestView    #从你的app的view里引入你将要写的view，你也可以另外写一个py文件，把后台的view集中在一起方便管理
xadmin.site.register_view(r'test_view/$', TestView, name='for_test')

# 租用下单
class ContactAdminDevice_lend(object):
    def save_models(self):
        obj = self.new_obj
        flag = self.org_obj is None and 'create' or 'change'
        request = self.request
        if flag == 'create':  # 新增默认回填操作员
            obj.author = str(request.user)
            obj.save()
        else:
            obj.save()

    list_display = ('id', 'shopid', 'quantity', 'date_begin' ,'date_end','remark', 'pub_date', 'author', 'update_time')

# 租用出库
class ContactAdminDevice_lend_stockout(object):
    def save_models(self):
        obj = self.new_obj
        flag = self.org_obj is None and 'create' or 'change'
        request = self.request
        if flag == 'create':  # 新增默认回填操作员
            obj.author = str(request.user)
            obj.save()
        else:
            obj.save()

    list_display = ('id', 'shopid', 'quantity', 'date_begin' ,'date_end','remark', 'pub_date', 'author', 'update_time')

# 维修领用下单
class ContactAdminRepair_usel(object):
    def save_models(self):
        obj = self.new_obj
        flag = self.org_obj is None and 'create' or 'change'
        request = self.request
        if flag == 'create':  # 新增默认回填操作员
            obj.author = str(request.user)
            obj.save()
        else:
            obj.save()

    list_display = ('id', 'shopid', 'quantity', 'price','remark', 'pub_date', 'author', 'update_time')

# 维修领用出库
class ContactAdminRepair_use_stockout(object):
    def save_models(self):
        obj = self.new_obj
        flag = self.org_obj is None and 'create' or 'change'
        request = self.request
        if flag == 'create':  # 新增默认回填操作员
            obj.author = str(request.user)
            obj.save()
        else:
            obj.save()

    list_display = ('id', 'shopid', 'quantity', 'remark', 'pub_date', 'author', 'update_time')

# Register your models here.

# 注册备件Model类
# xadmin.site.register(Devices, ContactAdminDevices)
# xadmin.site.register(DeviceStore, ContactAdminDeviceStore)
xadmin.site.register(Device_lend, ContactAdminDevice_lend)# 租用下单
xadmin.site.register(Device_lend_stockout, ContactAdminDevice_lend_stockout)# 租用出库
# xadmin.site.register(Device_stockinout_detail, ContactAdminDevice_stockinout_detail)# 备件出入库明细
xadmin.site.register(Repair_use, ContactAdminRepair_usel)# 维修领用下单
xadmin.site.register(Repair_use_stockout, ContactAdminRepair_use_stockout)# 维修领用出库

# xadmin.site.register(Devices, ContactAdminInstock)
# 设置登陆窗口的标题
xadmin.site.site_header = '备件库存管理系统 V1.0'
# 设置页签标题
xadmin.site.site_title = '备件库存管理系统'
# 界面主题、基本信息设置
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)


