# 模块名称：采购管理业务处理模块
# 创建日期：2020-4
# 最后修改日期：2020-6
# 作者：Jason

# from django.contrib import admin
from purchase_manage.models import *
import xadmin
from common import generic
from xadmin.views.base import CommAdminView
import time


# 自定义页面
class ContactAdminPurchase_order_self(object):
    # 指向自定义的页面
    # object_list_template = 'PurchaseOrder.html'
    # object_list_template = 'test_view'

    # 重写方法，把要展示的数据更新到 context
    def get_context(self):
        context = CommAdminView.get_context(self)

        # bill_message = bill_manage.objects.all()
        context.update(
            {
                'title': '采购下单',
            }
        )

        return context

#采购单
class ContactAdminPurchase_order(object):
    def save_models(self):
        obj = self.new_obj
        flag = self.org_obj is None and 'create' or 'change'
        request = self.request
        obj.author = str(request.user)
        if flag == 'create':  # 新增默认回填操作员
            # obj.author = str(request.user)
            id = 'CGD' + time.strftime("%Y%m%d", time.localtime()) + '%'
            sql = 'select max(id) from purchase_manage_purchase_order where id like "%s"' % id
            MaxOrderNO  = generic.getOrderNO(sql)
            # obj.remark = sql
            if not MaxOrderNO:
                 MaxOrderNO = '001'
            else:
              # 查找倒数三个字符串为订单数字，自动加1
              MaxOrderNO = int(MaxOrderNO[-3:]) + 1
              #不足三位补0
              if (len(str(MaxOrderNO)) == 1):
                  MaxOrderNO = '00' + str(MaxOrderNO)
              elif (len(MaxOrderNO) == 2):
                  MaxOrderNO = '0' + str(MaxOrderNO)
              else:
                  MaxOrderNO = str(MaxOrderNO)
            # OrderNO = 'CGD' + time.strftime("%Y%m%d", time.localtime()) + MaxOrderNO
            OrderNO = generic.getOrderMaxNO('CGD')
            obj.id =  OrderNO
            obj.save()
        else:
            obj.save()

    list_display = ('id','purchase_type','shopid','desc','quantity','amount','remark','author','update_time')
    model_icon = 'fa fa-exchange'  # 图标样式
    # 添加和修改时那些界面不显示
    exclude = ('author','price','suppliersid')
    readonly_fields = ('id','quantity','amount')
    # ordering设置默认排序字段，负号表示降序排序
    ordering = ['-id', ]
    add_form_template = 'PurchaseOrder_form.html'
    change_form_template = 'PurchaseOrder_form.html'

#采购下单
class ContactAdminPurchase_order_detail(object):
    def save_models(self):
        obj = self.new_obj
        flag = self.org_obj is None and 'create' or 'change'
        request = self.request
        obj.author = str(request.user)
        # 新增默认回填备件库数据
        if flag == 'create':
            id = str(obj.FRUSelect_id)
            sql = 'select FRU,PN,machineSN,machineModel,price,image,descs,replaces,source,remark from baseinfo_manage_devicestores where id = %s' % id
            cds = generic.query(sql)
            obj.FRU = cds[0][0]
            obj.PN = cds[0][1]
            obj.machineSN = cds[0][2]
            obj.machineModel = cds[0][3]
            # obj.price = cds[0][4]
            obj.image = cds[0][5]
            obj.desc = cds[0][6]
            obj.replace = cds[0][7]
            obj.source = cds[0][8]
            obj.remark = cds[0][9]
            obj.save()
            # 新增默认回填待入库数据
            # sql = 'insert into purchase_manage_purchase_stockin_detail' \
            #       '(purchase_id_id,FRU,PN,useage,price,quantity,source,image,author,remark,location_id,shopid_id,FRUSelect_id)' \
            #       'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
            # sql = 'insert into purchase_manage_purchase_stockin_detail' \
            #       '(purchase_id_id,FRU,PN,price,quantity,source,author,useage,location_id,shopid_id,FRUSelect_id)' \
            #       'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s，%s, %s)'
            # params = [obj.id, obj.FRU, str(obj.PN), obj.price, obj.quantity, str(obj.source), str(obj.author),'0','1', obj.shopid_id, obj.FRUSelect_id]
            # # params = [obj.id,obj.FRU,obj.PN,obj.useage,obj.price,obj.quantity,obj.source,obj.image,obj.author,
            #           obj.remark,'1',obj.shopid_id,obj.FRUSelect_id]
            # generic.update(sql,params)
            # sql = 'insert into purchase_manage_purchase_stockin_detail (purchase_id_id,author,price,quantity,useage,location_id,shopid_id,FRUSelect_id)  VALUES(71, "root", 1, 1, 0, 1, 20200002, 4)'
            # generic.update(sql)
            # obj.remark = sql + '(' + str(obj.id)+ ','+ obj.FRU + ',' + obj.PN +','+ str(obj.price) + ',' + str(obj.quantity) + ','+obj.source+ ','+\
            #              obj.author+',1'+ ','+str(obj.shopid_id)+ ',' + str(obj.FRUSelect_id)
            # obj.save()
            # purchase_stockin = Purchase_stockin_detail()
            # purchase_stockin.purchase_id_id = obj.id
            # purchase_stockin.FRU = obj.FRU
            # purchase_stockin.PN = obj.PN
            # purchase_stockin.price = obj.price
            # purchase_stockin.quantity = obj.quantity
            # purchase_stockin.useage = 1
            # purchase_stockin.source = obj.source
            # purchase_stockin.author = obj.author
            # purchase_stockin.location_id = 1
            # purchase_stockin.shopid_id = obj.shopid_id
            # purchase_stockin.FRUSelect_id = obj.FRUSelect_id
            # purchase_stockin.save()
        else:
            obj.save()
    list_display = ('bill_id','shopid','FRUSelect','desc','source','replace','useage',
                    'quantity','price','image_data','remark','author','update_time')
    model_icon = 'fa fa-exchange'  # 图标样式
    # 添加和修改时那些界面不显示
    exclude = ('SN','PN','author',)
    # readonly_fields = ('bill_id', )
    ordering = ['-id', ]

    # def get_readonly_fields(request, obj=None):
    #     if obj.bill_id:
    #         return ('bill_id')
    #     else:
    #         return super(ContactAdminPurchase_order_detail).get_readonly_fields(request, obj)

    # def get_readonly_fields(self, request, obj=None):
    #     fields = []
    #     if request.user.is_superuser:
    #         return fields
    #     else:
    #         fields = ['boss_verified', 'deliver_during']
    #         return fields
    #
    # def get_readonly_fields(self, obj=None):
    #     # objs = object
    #     if obj.bill_id == '':
    #         self.readonly_fields = []
    #     else:
    #         self.readonly_fields = ['bill_id']
    #     return self.readonly_fields

    # def get_readonly_fields(self, obj=None):
    #     return ('FRU', 'desc', 'source', 'replace', 'price', 'image_data')
    # def get_readonly_fields(self, obj=None):
    #     if object.id:
    #        return ('FRU', 'desc','source','replace','price','image_data')
    #     else:
    #         return []

       # if obj.certainfield == something:
       #          return ('field1', 'field2')
       #      else:
       #          return super(TranslationAdmin, self).get_readonly_fields(request, obj)

    def get_changeform_initial_data(self, request):
        # import datetime
        # begin = datetime.date.today()
        # end = begin + datetime.timedelta(30)
        # return {'order_date': begin, 'arrive_date': end}
        obj = self.new_obj
        flag = self.org_obj is None and 'create' or 'change'
        # request = self.request
        # obj.author = str(request.user)
        if flag == 'create':  # 新增默认回填操作员
            obj.remark = 'test'
            # exclude = ('SN', 'PN', 'author','desc')

#采购入库
class ContactAdminPurchase_stockin(object):
    def save_models(self):
        obj = self.new_obj
        flag = self.org_obj is None and 'create' or 'change'
        request = self.request
        obj.author = str(request.user)
        if flag == 'create':  # 新增默认回填操作员
            id = 'CGRK' + time.strftime("%Y%m%d", time.localtime()) + '%'
            sql = 'select max(id) from purchase_manage_purchase_stockin where id like "%s"' % id
            MaxOrderNO = generic.getOrderNO(sql)
            if not MaxOrderNO:
                MaxOrderNO = '001'
            else:
                # 查找倒数三个字符串为订单数字，自动加1
                MaxOrderNO = int(MaxOrderNO[-3:]) + 1
                # 不足三位补0
                if (len(str(MaxOrderNO)) == 1):
                    MaxOrderNO = '00' + str(MaxOrderNO)
                elif (len(MaxOrderNO) == 2):
                    MaxOrderNO = '0' + str(MaxOrderNO)
                else:
                    MaxOrderNO = str(MaxOrderNO)
            OrderNO = 'CGRK' + time.strftime("%Y%m%d", time.localtime()) + MaxOrderNO
            obj.id = OrderNO
            # 获取采购数量和金额
            id = obj.purchase_id_id
            sql = 'select quantity,amount from purchase_manage_purchase_order where id = "%s"' % id
            cds = generic.query(sql)
            # purchase_info = Purchase_order.objects.filter(id=obj.purchase_id_id)
            if cds:
               obj.quantity = cds[0][0]
               obj.price =  cds[0][1]
            obj.save()
            # 保存采购入库单后，采购入库自动生成采购下单明细
            #通过采购单号获取采购信息
            id = obj.purchase_id_id
            sql = 'insert into purchase_manage_purchase_stockin_detail' \
                  ' (purchase_id_id, sn, FRU, PN, useage, price, quantity, source, image, author, remark, location_id, shopid_id,FRUSelect_id)' \
                  'select id, sn, FRU, PN, useage, price, quantity, source, image, author, remark, 1, shopid_id, FRUSelect_id ' \
                  'from purchase_manage_purchase_order_detail where bill_id_id="%s"' % id
            generic.update(sql)
            obj.remark = sql
            obj.save()
        else:
            obj.save()
    list_display = ('id','purchase_id','shopid','quantity','price','suppliersid','remark','author','update_time')
    model_icon = 'fa fa-exchange'  # 图标样式
    readonly_fields = ('id', 'price','quantity')
    # 添加和修改时那些界面不显示
    exclude = ('author',)


    # def queryset(self):
    #     """函数作用：使当前登录的用户只能看到自己负责的设备"""
    #     qs = super(ContactAdminPurchase_stockin, self).queryset()
    #     return qs.filter(author='ljh')
    # 过滤，只能查看操作登陆人自己创建的内容
    # def get_queryset(self, request):
    #     # return super(ContactAdminPurchase_stockin, self).get_queryset(request).filter(user='ljh')
    #     # return super(ContactAdminPurchase_stockin, self).get_queryset(request).filter(partner_type='S')
    #     qs = super(ContactAdminPurchase_stockin, self).get_queryset(request)
    #     if request.user.is_superuser:
    #         return qs
    #     return qs.filter(author='ljh')
    # select  a.FRUSelect_id
    # from purchase_manage_purchase_order_detail a, purchase_manage_purchase_stockin b
    # where a.bill_id_id = b.purchase_id_id and b.id = 'cgrk20200001'

#采购入库明细
class ContactAdminPurchase_stockin_detail(object):
    def save_models(self):
        obj = self.new_obj
        flag = self.org_obj is None and 'create' or 'change'
        request = self.request
        obj.author = str(request.user)
        if flag == 'create':  # 新增默认回填操作员
            obj.save()
        else:
            id = 'CGRK' + time.strftime("%Y%m%d", time.localtime()) + '%'
            sql = 'select max(bill_id) from purchase_manage_purchase_stockin_detail where bill_id like "%s"' % id
            MaxOrderNO = generic.getOrderNO(sql)
            if not MaxOrderNO:
                MaxOrderNO = '001'
            else:
                # 查找倒数三个字符串为订单数字，自动加1
                MaxOrderNO = int(MaxOrderNO[-3:]) + 1
                # 不足三位补0
                if (len(str(MaxOrderNO)) == 1):
                    MaxOrderNO = '00' + str(MaxOrderNO)
                elif (len(MaxOrderNO) == 2):
                    MaxOrderNO = '0' + str(MaxOrderNO)
                else:
                    MaxOrderNO = str(MaxOrderNO)
            OrderNO = 'CGRK' + time.strftime("%Y%m%d", time.localtime()) + MaxOrderNO
            obj.bill_id = OrderNO
            # obj.remark = 'test'
            obj.save()
            # 更新库存数量
            if (obj.quantity > 0) and (obj.bill_id):
                sql = "UPDATE baseinfo_manage_devicestores SET quantity = quantity + %s where (FRU=%s or PN=%s) or (machineSN=%s)"
                params = [obj.quantity, obj.FRU, obj.PN, 'test']
                generic.update(sql, params)
            # 拆分采购入库单
            # 获取采购单号中采购数量
            id = obj.purchase_id_id
            sql1 = 'select quantity from purchase_manage_purchase_order_detail where id= "%s"' % id
            cds1 = generic.query(sql1)
            FRUSelectID = obj.FRUSelect_id
            sql2 = 'select sum(quantity) from purchase_manage_purchase_stockin_detail where FRUSelect_id = "%s"' % FRUSelectID
            obj.remark = sql1 + '  ，  ' + sql2
            obj.save()
            cds2 = generic.query(sql2)
            quantity = 0
            if cds1 and cds2:
               quantity1 = cds1[0][0]
               quantity2 = cds2[0][0]
               quantity = quantity1 - quantity2 # 剩余数量
            if  quantity > 0:
               purchase_stockin = Purchase_stockin_detail()
               purchase_stockin.purchase_id_id = obj.purchase_id_id
               purchase_stockin.FRU = obj.FRU
               purchase_stockin.PN = obj.PN
               purchase_stockin.price = obj.price
               purchase_stockin.quantity = quantity
               purchase_stockin.useage = 1
               purchase_stockin.source = obj.source
               purchase_stockin.image = obj.image
               purchase_stockin.author = obj.author
               purchase_stockin.location_id = 1
               purchase_stockin.shopid_id = obj.shopid_id
               purchase_stockin.FRUSelect_id = obj.FRUSelect_id
               purchase_stockin.save()

    list_display = ('bill_id','purchase_id','shopid','FRUSelect','SN','FRU','PN','desc','source','replace','useage',
                    'price','quantity','location','image_data','remark','author','pub_date')
    model_icon = 'fa fa-exchange'  # 图标样式
    # 添加和修改时那些界面不显示
    exclude = ('author',)
    search_fields = ('FRU', 'SN','PN','replace')
    free_query_filter = ['FRU', 'SN', 'PN']
    list_editable = ['location', ]
    list_filter = ('FRU', 'SN', 'PN', 'location','replace')
    # show_detail_fields = ['bill_id', 'purchase_id']  # 在指定的字段后添加一个显示数据详情的一个按钮
    list_display_links = ('bill_id', 'purchase_id',)
    date_hierarchy = ['pub_date']

    # def get_readonly_fields(self, request, obj=None):
    #     if obj:
    #         self.readonly_fields = ['bill_id']
    #     else:
    #         self.readonly_fields = ['bill_id']
    #     return self.readonly_fields
    # def queryset(self):
    #     #"""函数作用：使当前登录的用户只能看到自己
    #    qs = super(ContactAdminPurchase_stockin_detail, self).queryset()
    #    return qs.filter(FRUSelect_id=5)

    # def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
    #     if object_id:
    #         extra_context = extra_context or {}
    #         obj = Purchase_stockin_detail.objects.get(id=object_id)
    #         # if obj.status == '99':
    #         #     extra_context.update(dict(readonly=True))
    #     return super(ContactAdminPurchase_stockin_detail, self).changeform_view(request, object_id, form_url, extra_context)

    # def formfield_for_dbfield(self, db_field, **kwargs):
    #     # 对FRUSelect这个表项的下拉框选择进行过滤
    #     if db_field.name == "SN":
    #         kwargs["queryset"] = Purchase_stockin_detail.objects.filter(SN=12)#.order_by('id')
    # def formfield_for_foreignkey(self, db_field, request, **kwargs):
    #     if db_field.name == "FRUSelect_id":
    #         kwargs["queryset"] = DeviceStores.objects.filter(id=4)
    #     return super(ContactAdminPurchase_stockin_detail, self).formfield_for_foreignkey(db_field, request, **kwargs)

# 采购退货下单
class ContactAdminPurchase_return(object):
    def save_models(self):
        obj = self.new_obj
        flag = self.org_obj is None and 'create' or 'change'
        request = self.request
        if flag == 'create':  # 新增默认回填操作员
            obj.author = str(request.user)
            obj.save()
        else:
            obj.save()

    model_icon = 'fa fa-exchange'  # 图标样式
    list_display = ('id', 'purchase_id', 'shopid', 'quantity', 'price', 'reason','pub_date', 'author', 'update_time')

# 采购退货出库
class ContactAdminPurchase_returnout(object):
    def save_models(self):
        obj = self.new_obj
        flag = self.org_obj is None and 'create' or 'change'
        request = self.request
        if flag == 'create':  # 新增默认回填操作员
            obj.author = str(request.user)
            obj.save()
        else:
            obj.save()

    model_icon = 'fa fa-exchange'  # 图标样式
    list_display = ('id', 'purchase_id', 'shopid', 'quantity', 'price', 'remark', 'pub_date', 'author', 'update_time')

xadmin.site.register(Purchase_order, ContactAdminPurchase_order)
xadmin.site.register(Purchase_order_detail, ContactAdminPurchase_order_detail)
xadmin.site.register(Purchase_stockin, ContactAdminPurchase_stockin)
xadmin.site.register(Purchase_stockin_detail, ContactAdminPurchase_stockin_detail)
xadmin.site.register(Purchase_return, ContactAdminPurchase_return)
xadmin.site.register(Purchase_returnout, ContactAdminPurchase_returnout)

#
# from purchase_manage.views import TestView
# xadmin.site.register_view(r'purchase_manage/purchase_order_self/$', TestView, name='for_test')
#
# from purchase_manage.views import TestView    #从你的app的view里引入你将要写的view，你也可以另外写一个py文件，把后台的view集中在一起方便管理
# xadmin.site.register_view(r'purchase_manage/purchase_order/cgdj2020002/update/ShowDetail/$', TestView, name='for_test')
# # xadmin.site.register_modelview(r'purchase_manage/purchase_order/cgdj2020002/update/ShowDetail/$', TestView, name='for_test')
