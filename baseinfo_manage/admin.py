# 模块名称：基本信息控制
# 创建日期：2020-4
# 最后修改日期：2020-6
# 作者：Jason

from django.contrib import admin
from baseinfo_manage.models import *
import xadmin,win32ui
from xadmin.layout import Fieldset
from xadmin.views.base import CommAdminView
from xadmin.plugins.actions import BaseActionView
from django.contrib import messages
from common import generic
import  datetime

# 备件信息
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
    list_display = ('name','shop_type','shop_level','shop_brand','quantity_good','remark','author','update_time')  # list
    search_fields = ('name',)  # 如果只有一个值，结尾必须有一个逗号，证明是list或元组
    search_name = '名称'
    # list_per_page设置每页显示多少条记录，默认是100条
    list_per_page = 5
    # ordering设置默认排序字段，负号表示降序排序
    ordering = ('id',)
    # list_editable 设置默认可编辑字段,第一个字段不允许编辑
    # list_editable = ['location', ]
    # 设置过滤
    list_filter = ('name','shop_type','shop_brand')
    # fk_fields 设置显示外键字段
    # fk_fields = ('machine_room_id',)
    # 详细时间分层筛选
    date_hierarchy = 'pub_date'
    # 添加和修改时那些界面不显示
    exclude = ('author','shop_level','quantity_good','pub_date','shop_brand_childs','status','cost','useage','price')
    # 指定列表显示的哪列可以点击跳转到详情更新页
    list_display_links = ('shop_brand','shop_type')
    model_icon = 'fa fa-user'  # 图标样式

class ImportDeviceStore(BaseActionView): # 定义一个动作
    action_name = "import_DeviceStore"  # 相当于这个 Action 的唯一标示, 尽量用比较针对性的名字
    description = "Excel批量导入"  # 要显示的名字
    icon = 'fa fa-tasks'  # 图标
    model_perm = "change"   # 该动作所需权限

    def do_action(self, queryset):  # 重载do_action()方法
        # 过滤出文件结尾为 xlsx 与 xls
        bOpen = False
        filename_filter = "文件类型 (*.xlsx)|*.xlsx|文件类型 (*.xls)|*.xls||"
        dlg = win32ui.CreateFileDialog(1 if bOpen else 0, None, None, 1, filename_filter, None)  # 1表示打开文件对话框
        # dlg.SetOFNInitialDir('E:/Python')  # 设置打开文件对话框中的初始显示目录
        # 返回是否完成操作 1代表完成选取文件
        flag = dlg.DoModal()  # 成功选中文件地址 返回文件名,失败返回 None
        if 1 == flag:
            filename = dlg.GetPathName()  # 获取选择的文件名称
            print(filename)
            try:
                getValues = generic.readExcel(filename)
                for i in range(len(getValues)):
                   print(getValues[i])
                   model = getValues[i][2]
                   sql = 'select id from params_manage_device_kind where name = "%s"' % model
                   datas = generic.query(sql)
                   print(sql)
                   # users = self.request.user
                   if datas:
                      modelID =  datas[0][0]
                   else:
                      sql = 'insert into params_manage_device_kind  (name,desc,author,pub_date) ' \
                             ' values ("%s","","%s",date())' % model,self.request.user
                      print(sql)
                      generic.update(sql)
                      sql = 'select id from params_manage_device_kind where name = "%s"' % model
                      datas = generic.query(sql)
                      print(sql)
                      if datas:
                          modelID = datas[0][0]
                      else:  modelID = 0
                   queryset.create(typename = int(getValues[i][0]),
                                   machineModels = modelID,
                                   shop = 23,
                                   FRUS = 78,
                                   descs = getValues[i][3],
                                   price = 0,
                                   quantity = 0,
                                   quantityLock = 0,
                                   quantityLover = 0,
                                   type = 1,
                                   location = 1,
                                   suppliers = 1,
                                   ifmachine = 0,
                                   update_time = datetime.datetime.now(),
                                   author = self.request.user)
                messages.success(self.request, str(len(getValues)) + '条记录，导入成功！')
            except: messages.error(self.request, '文件格式不一致，导入失败！')

import qrcode
# 库存信息
class ContactAdminDeviceStore(object):
    def save_models(self):
        obj = self.new_obj
        flag = self.org_obj is None and 'create' or 'change'
        request = self.request
        if flag == 'create':  # 新增默认回填操作员
            obj.author = str(request.user)
            obj.save()
            # IP暂时固定写死
            url = 'http://192.168.2.123:8000/baseinfo_manage/devicestores/' + str(obj.id) + '/update/'
            img = qrcode.make(url)
            name = str(obj.id) + '.png'
            filename = 'upload\images\\' + name
            # 保存二维码图片
            img.save(filename)
            obj.qrcode = 'images/' + name
            obj.save()
            print(str(obj.id))
        else:
            obj.save()
            # 保存的时候把FRU的描述信息带入
        sql = 'select desc,name from params_manage_device_fru where id = %s' % obj.FRUS_id
        datas = generic.query(sql)
        print(sql)
        if datas:
            desc = datas[0][0]
            fru = datas[0][1]
            print(desc)
            print(fru)
            obj.descs = desc
            obj.FRU = fru
            obj.save()
        # id = obj.shop_id
        # sql = 'select b.name from baseinfo_manage_shop a,params_manage_device_type b where a.name_id = b.id and a.id  = "%s"' % id
        # print(sql)
        # cds = generic.query(sql)
        # if cds:
        #     if cds[0][0] != None:
        #         obj.typename = cds[0][0]
        #     else:
        #         obj.typename = '无'
        # obj.save()

    # Action选项都是在页面上方显示
    actions_on_top = True
    # Action选项都是在页面下方显示
    actions_on_bottom = True

    # 是否显示选择个数
    actions_selection_counter = True

    # listdisplay设置要显示在列表中的字段（id字段是Django模型的默认主键）
    list_display = ('typename','machineModels','shop','FRUS','PN','replaces','descs','quantitys','image_data',
                    'remark','author','update_time')  # list
    # list_display_links，列表时，定制列可以点击跳转。
    list_display_links = ('FRUS','PN',)
    search_fields = ('replaces','descs','FRU','PN',)  # 如果只有一个值，结尾必须有一个逗号，证明是list或元组
    # search_name = {'FRU查询':'FRU','SN查询':'SN'}
    free_query_filter = ['ifmachine','FRUS']
    # list_per_page设置每页显示多少条记录，默认是100条
    list_per_page = 5
    # ordering设置默认排序字段，负号表示降序排序
    ordering = ['shop','machineModels','FRUS']
    # list_editable 设置默认可编辑字段,第一个字段不允许编辑
    # list_editable = ['location', ]
    # 设置过滤
    list_filter = ('typename','ifmachine','machineModels','shop','location',)
    # fk_fields 设置显示外键字段
    # fk_fields = ('machine_room_id',)
    # 详细时间分层筛选
    date_hierarchy = ['pub_date']
    # fields，详细页面时，显示字段的字段
    #   fields = ('user',)
    # readonly_fields = ('descs',)
    # 添加和修改时那些界面不显示
    exclude = ('ifmachine','typename','qrcode_data','author','FRU','source','descs','suppliers','quantityLock','type','quantityLover','price','location','quantity','machineSN','machineModel')
    # 详细页面时，M2M显示时，数据移动选择（方向：上下和左右）
    filter_horizontal = ('authors',)  # filter_horizontal 从‘多选框’的形式改变为‘过滤器’的方式，水平排列过滤器，必须是一个 ManyToManyField类型，且不能用于 ForeignKey字段，默认地，管理工具使用`` 下拉框`` 来展现`` 外键`` 字段
    filter_vertical = ("location",)  #同上filter_horizontal，垂直排列过滤器
    # 或filter_horizontal = ("m2m字段",)
    empty_value_display = '无'#"列数据为空时，默认显示"
    # advanced_filter_fields = ('name', ('product_lot__product__name', 'Product name'))
    show_detail_fields = ['desc','location'] #在指定的字段后添加一个显示数据详情的一个按钮
    free_query_filter = ['FRUS', 'PN']
    aggregate_fields = {'quantity': 'sum',}  # 列聚合，在list表格下面会增加一行统计的数据，可用的值："count","min","max","avg",  "sum"
    # model_icon = 'fa fa-comment'  # 图标样式  # 图标样式
    model_icon = 'fa fa-user'  # 图标样式
    # actions = [ImportDeviceStore]
    # list_bookmarks = [{
    #     'title': "今天库存",  # 书签的名称, 显示在书签菜单中
    #     # 'query': {'gender': True, 'postdate__gte': 20200327},  # 过滤参数, 是标准的 queryset 过滤
    #
    #     # 'query': {'pub_date__exact': int(datetime.datetime.now().strftime('%Y%m%d'))},  # 过滤参数, 是标准的 queryset 过滤
    #     # 'query': {'pub_date__exact': '20200408'},  # 过滤参数, 是标准的 queryset
    #     'query': {"author":'root'},  # 过滤参数, 是标准的 queryset 过滤
    #     'order': ('FRU', 'PN' ),  # 排序参数
    #     'selected': True,
    # },
    #     {
    #         'title': "近两天库存",  # 书签的名称, 显示在书签菜单中
    #         'query': {'pub_date__gte': (datetime.datetime.now() + datetime.timedelta(-1)).strftime('%Y%m%d')},
    #         # 过滤参数, 是标准的 queryset 过滤
    #         # 'order': ('FRU', 'PN' ),  # 排序参数
    #     },
    # ]

# 备件选择历史信息
class ContactAdminSelectOrderDetail(object):
    list_display = ('device', 'quantity')
    fieldsets = (
        (None, {'fields': ('device', 'desc')}),
    )
    # filter_horizontal = ('device', 'desc','quantity')
    filter_vertical = ('shopid','device', 'desc','quantity')
    exclude = ('shopid','desc' )
    ordering = ('device','quantity')
    # list_per_page设置每页显示多少条记录，默认是100条
    list_per_page = 5
    model_icon = 'fa fa-user'  # 图标样式

    def save_models(self):
        obj = self.new_obj
        flag = self.org_obj is None and 'create' or 'change'
        request = self.request
        if flag == 'create':  # 新增默认回填操作员
            # 新增回填默认的备件信息中描述信息
            sql = 'select descs from baseinfo_manage_devicestores where id = %s' % obj.device_id
            print(sql)
            datas = generic.query(sql)
            print(sql)
            if datas:
                desc = datas[0][0]
                print(desc)
                obj.desc = desc
                obj.save()
        else:
            obj.save()

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

    # listdisplay设置要显示在列表中的字段（id字段是Django模型的默认主键）
    list_display = ('name','customer_type','base_info','contract_info','clue','service',
                    'people','tel','address','remark','author','update_time')  # list
    search_fields = ('name','base_info','contract_info','clue','service','people','address')  # 如果只有一个值，结尾必须有一个逗号，证明是list或元组
    search_name = '名称'
    # list_per_page设置每页显示多少条记录，默认是100条
    list_per_page = 5
    # ordering设置默认排序字段，负号表示降序排序
    ordering = ('-update_time',)
    # list_editable 设置默认可编辑字段,第一个字段不允许编辑
    # list_editable = ['location', ]
    # 设置过滤
    list_filter = ('customer_type',)
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
    search_fields = ('contractid','item',)  # 如果只有一个值，结尾必须有一个逗号，证明是list或元组
    search_name = '签约客户'
    # list_per_page设置每页显示多少条记录，默认是100条
    list_per_page = 5
    # ordering设置默认排序字段，负号表示降序排序
    ordering = ('-update_time',)
    # list_editable 设置默认可编辑字段,第一个字段不允许编辑
    # list_editable = ['location', ]
    # 设置过滤
    list_filter = ('customer','pub_date','type','status')
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

    # listdisplay设置要显示在列表中的字段（id字段是Django模型的默认主键）
    list_display = ('name','adress','people','tel','remark','author','update_time')  # list
    search_fields = ('name','adress','people')  # 如果只有一个值，结尾必须有一个逗号，证明是list或元组
    search_name = '名称'
    # list_per_page设置每页显示多少条记录，默认是100条
    list_per_page = 5
    # ordering设置默认排序字段，负号表示降序排序
    ordering = ('-update_time',)
    # list_editable 设置默认可编辑字段,第一个字段不允许编辑
    # list_editable = ['location', ]
    # 设置过滤
    # list_filter = ('name','pub_date',)
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
    # def get_readonly_fields(self, obj=None):
    #     if self.user.is_superuser:
    #         self.readonly_fields = []
    #     else:
    #         self.readonly_fields = ['important','pub_date','solve','type','desc','image','image_data','author','answer']
    #     return self.readonly_fields

    # form_layout = (
    #     # Fieldset('测试',
    #     #          'solve','type','desc'
    #     #          ),
    #     Fieldset(None,
    #              'important','pub_date',**{"style":"display:None"} #隐藏前面两个字段
    #              ),
    # )
    def get_form_layout(self):
        if self.org_obj:
            self.form_layout = (
                    Fieldset('问题列表',
                             'solve','important','type','desc','image','image_data','author'
                             ),
                    Fieldset('解决方案',
                             'answer', 'pub_date'
                             ),
            )
        return super(ContactAdminRequirement, self).get_form_layout()

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
    exclude = ('author',)
    # 设置哪些字段可以点击进入编辑界面
    # 指定列表显示的哪列可以点击跳转到详情更新页
    list_display_links = ('pub_date', 'desc')
    # 这些字段可以点击显示详细信息
    show_detail_fields = ['desc']
    model_icon = 'fa fa-user'  # 图标样式


# 注册基本信息Model类
xadmin.site.register(Shop, ContactAdminShop) # 商品信息
xadmin.site.register(DeviceStores, ContactAdminDeviceStore)  # 备件信息
xadmin.site.register(SelectOrderDetail, ContactAdminSelectOrderDetail)  # 备件选择历史信息
xadmin.site.register(Suppliers, ContactAdminSupplier) # 供应商信息
xadmin.site.register(Customers, ContactAdminCustomer)  #客户信息
xadmin.site.register(CustomersLatent, ContactAdminCustomersLatent) # 潜在项目
xadmin.site.register(CustomersSign, ContactAdminCustomersSign) # 签约项目
xadmin.site.register(ContractContent, ContactAdminContractContent) # 项目服务内容
xadmin.site.register(ContractInfo, ContactAdminContractInfo) # 合同服务内容
xadmin.site.register(Requirement, ContactAdminRequirement) # 项目需求管理

