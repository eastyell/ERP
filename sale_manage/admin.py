# 模块名称：销售管理业务处理模块
# 创建日期：2020-4
# 最后修改日期：2020-6
# 作者：Jason

from django.contrib import admin
import xadmin
from sale_manage.models import *
from xadmin.plugins.actions import BaseActionView
from django.contrib import messages
from django.shortcuts import redirect

# Register your models here.

# 提交所选的 销售下单
class Act_Device_sale(BaseActionView): # 定义一个动作
    action_name = "device_sale"  # 相当于这个 Action 的唯一标示, 尽量用比较针对性的名字
    description = "提交所选的 销售下单"  # 要显示的名字
    icon = 'fa fa-tasks'  # 图标
    model_perm = "change"   # 该动作所需权限

    def do_action(self, queryset):  # 重载do_action()方法
        # queryset 是包含了已经选择的数据的 queryset
        # 生成采购下单明细
        # queryset.update(status = 6)
        d1 = timezone.now()
        a = ()
        for i in range(0, queryset.count()):
            status = str(queryset.values_list('status')[i]).strip('(,)')
            parts = str(queryset.values_list('machineSelects')[i]).strip('(,)')
            print('parts: ' + parts)
            if (status == '0') and (parts != 'None') :
              # a = a + queryset.values_list('id')[i]
              saleid = queryset.values_list('id')[i]
              saleids = ''.join(saleid)
              saleids = saleids.strip('()')
              print(saleids)
              sql = 'select distinct SN,FRUSelect_id from report_manage_stock_detail where FRUSelect_id in ' \
                    '(select device_id  from baseinfo_manage_selectorderdetail where id in '\
                    '(select selectorderdetail_id from sale_manage_sales_out_machineSelects where sales_out_id = "%s")) and stock_type = 0 order by FRUSelect_id'  %queryset.values_list('id')[i]
              print(sql)
              cds = generic.query(sql)
              sn = ''
              fruSelectid = '0'
              if cds:
                  a = a + queryset.values_list('id')[i]
                  tempid = cds[0][1]
                  for i in range(0, len(cds)):
                    if cds[i][1] is not None:
                       # 遇见不同的备件新增
                       fruSelectid = cds[i][1]
                       if tempid != fruSelectid:
                          sql = 'insert into splitSN (bill,SN,FRUselectid) ' \
                                 'VALUES ("%s","%s","%s") ' % (saleids, sn, cds[i-1][1])
                          print(sql)
                          generic.update(sql)
                          sn = ''
                          tempid = fruSelectid
                    if cds[i][0] is not None:
                      if sn != '':
                        sn = sn + ',' + cds[i][0]
                      else: sn = cds[i][0]

                  sql = 'insert into splitSN (bill,SN,FRUselectid) ' \
                          'VALUES ("%s","%s","%s") ' % (saleids,sn,fruSelectid)
                  print(sql)
                  generic.update(sql)
                    # else:
                    #   if cds[i][0] is not None:
                    #     sn = sn + ',' +cds[i][0]
                    #   else: sn = '空'
        print(a)
        id = str(a).strip().rstrip(',)')
        id = id + ')'
        print(id)
        # 状态待提交   才能提交
        if a:
          sql = 'update sale_manage_sales_out set status = 6,update_time = "%s" where id in  %s' % (
              d1, id)
          print(sql)
          generic.update(sql)
          # 提交单据销售下单
          sql = 'insert into sale_manage_sales_out_stockout' \
              '(customer_id,ifsure,SN,saleid_id,desc,shopid_id,useage,price,quantity,remark,FRUSelect_id,status,customersSignid_id,fru,pn,machinemodel,replace,image,location_id,update_time) ' \
              'select distinct customer_id,0,g.SN,b.id,c.desc,d.shop_id,0,d.price,-c.quantity,b.remark,c.device_id,6,b.customersSignid_id,e.name,d.pn,f.name,d.replaces,d.image,1,date() ' \
              'from sale_manage_sales_out_machineSelects a,sale_manage_sales_out b,baseinfo_manage_selectorderdetail c,baseinfo_manage_devicestores d,params_manage_device_fru e, params_manage_device_kind f,splitSN g ' \
              'where a.sales_out_id = b.id and c.id=a.selectorderdetail_id and  c.device_id = d.id and d.FRUS_id = e.id and f.id = d.machineModels_id and c.device_id = g.fruSelectid and g.bill = b.id and b.id in %s' % id
          print(sql)
          generic.update(sql)

          # 插入单据流程
          sql = 'insert into report_manage_workflow_query ' \
                '(flowstatus1,name1,pid,FRUSelect_id,FRU,author1,update_time1,flowstatus2) ' \
                'select "销售下单" as status,b.id,a.id,a.FRUSelect_id,a.FRU,b.author,b.update_time,"销售出库" ' \
                'from sale_manage_sales_out_stockout a,' \
                'sale_manage_sales_out b ' \
                'where b.id = a.saleid_id and b.id in %s' % id
          generic.update(sql)

          messages.success(self.request, '提交销售下单成功！')
          # 返回 HttpResponse
          return redirect(self.request.get_full_path())


# 提交所选的 销售单出库
class Act_Device_sale_stockout(BaseActionView): # 定义一个动作
    action_name = "device_sale_stockout"  # 相当于这个 Action 的唯一标示, 尽量用比较针对性的名字
    description = "提交所选的 销售单出库"  # 要显示的名字
    icon = 'fa fa-tasks'  # 图标
    model_perm = "change"   # 该动作所需权限

    def do_action(self, queryset):  # 重载do_action()方法
        # queryset 是包含了已经选择的数据的 queryset
        # 生成采购下单明细
        author = self.request.user
        d1 = timezone.now()
        # d1 = d1.strftime("%Y-%m-%d %H:%M")
        a = ()
        b = ()
        for i in range(0, queryset.count()):
            status = str(queryset.values_list('status')[i]).strip('(,)')
            print(status)
            SN = str(queryset.values_list('SN')[i]).strip('(,)')
            print('SN:' + SN)
            if (status == '6') and (SN != 'None'):
              a = a + queryset.values_list('id')[i]
              b = b + queryset.values_list('saleid_id')[i]
        print(a)
        id = str(a).strip().rstrip(',)')
        id = id + ')'
        print(id)
        saleidid = str(b).strip().rstrip(',)')
        saleidid = saleidid + ')'
        # 状态待出库  才能提交
        if a:
          # SN码不等于空值，更新状态和出库单号
          billid = generic.getOrderMaxNO('XSDCK')
          sql = 'update sale_manage_sales_out_stockout set status = 7,billid = "%s",author = "%s"  where replace(sn," ","") <> "" and id in  %s' % (
              billid, author, id)
          print(sql)
          generic.update(sql)
          # 如果入库日期没选，默认系统日期
          sql = 'update sale_manage_sales_out_stockout set pub_date = "%s",author = "%s"  where pub_date is null and replace(sn," ","") <> "" and id in  %s' % (
              d1, author, id)
          print(sql)
          generic.update(sql)

          # 生成出入库报表数据，单个SN码
          sql = 'insert into report_manage_stock_detail' \
              ' (customer_id,stock_type,bill_type,bill_id,sn, FRU, PN, machineModel, machineSN, price,quantity, useage,source, desc, replace, image,FRUSelect_id, author, remark, location_id,shopid_id,pub_date,update_time) ' \
              'select customer_id,1,2,billid,sn, FRU, PN, machineModel, machineSN, price, -1, useage,source, desc, replace, image, FRUSelect_id, author, remark, location_id,shopid_id,pub_date,date() ' \
              'from sale_manage_sales_out_stockout where replace(sn," ","") <> "" and  (instr(sn, ",") <= 0  and sn is not null) and id in %s' % id
          print(sql)
          generic.update(sql)

          # 拆分SN码批量入库
          sql = 'select billid,sn,quantity,id ' \
                'from sale_manage_sales_out_stockout where instr(sn, ",") > 0 and id in %s' % id
          print(sql)
          cds = generic.query(sql)
          rksl = 0  # 拆分剩余数量的回收入库单
          if cds:
              for i in range(0, len(cds)):
                  billids = cds[i][0]
                  sn = cds[i][1]
                  quantity = -cds[i][2]
                  Fid = cds[i][3]
                  strlist = sn.split(',')  # 用逗号分割sn字符串，并保存到列表
                  for value in strlist:  # 循环输出列表值
                      sql = 'insert into splitSN (bill,SN) ' \
                            'VALUES ("%s","%s") ' % (billids, value)
                      print(sql)
                      generic.update(sql)
                      rksl = rksl + 1  #计算入库数量
                  # 拆分剩余数量的回收入库单
                  sysl = quantity - rksl
                  print('剩余数量：')
                  print(str(sysl))
                  if sysl > 0:
                          # 拆分单据，插入剩余数量的入库单据
                          sql = 'insert into sale_manage_sales_out_stockout' \
                                '(customer_id,ifsure,saleid_id,desc,shopid_id,useage,price,quantity,remark,FRUSelect_id,status,customersSignid_id,fru,pn,machinemodel,replace,image,location_id,update_time) ' \
                                'select customer_id,ifsure,saleid_id,desc,shopid_id,useage,price,%s,remark,FRUSelect_id,6,customersSignid_id,fru,pn,machinemodel,replace,image,location_id,date() from sale_manage_sales_out_stockout where id = %s' % (
                                -sysl, Fid)
                          print(sql)
                          generic.update(sql)
                          # 更新入库单据信息
                          sql = 'update sale_manage_sales_out_stockout set quantity =%s,billid = "%s" where id = %s' % (
                          -rksl, billid, Fid)
                          print(sql)
                          generic.update(sql)
              # 生成出入库报表数据，批量SN码
              sql = 'insert into report_manage_stock_detail' \
                    ' (customer_id,stock_type,bill_type,bill_id,sn, FRU, PN, machineModel, machineSN, price,quantity, useage,source, desc, replace, image,FRUSelect_id, author, remark, location_id,shopid_id,pub_date,update_time) ' \
                    'select a.customer_id,1,2,a.billid, b.sn, a.FRU, a.PN, a.machineModel, a.machineSN, a.price, -1, a.useage, a.source, a.desc, a.replace, a.image, a.FRUSelect_id, a.author, a.remark, a.location_id, a.shopid_id, a.pub_date,date()  ' \
                    'from sale_manage_sales_out_stockout a,splitSN b where instr(a.sn, ",") > 0 and a.billid = b.bill and a.id in %s' % id
              print(sql)
              generic.update(sql)
          else:  # 输入一个SN，拆分单据，插入剩余数量单据
              sql = 'insert into sale_manage_sales_out_stockout' \
                    '(customer_id,ifsure,saleid_id,desc,shopid_id,useage,price,quantity,remark,FRUSelect_id,status,customersSignid_id,fru,pn,machinemodel,replace,image,location_id,update_time) ' \
                    'select customer_id,ifsure,saleid_id,desc,shopid_id,useage,price,quantity+1,remark,FRUSelect_id,6,customersSignid_id,fru,pn,machinemodel,replace,image,location_id,date() from sale_manage_sales_out_stockout where -quantity > 1 and  replace(sn," ","") <> "" and id in %s' % id
              print(sql)
              generic.update(sql)
              # 更新单据信息
              sql = 'update sale_manage_sales_out_stockout set quantity = -1  where replace(sn," ","") <> "" and instr(sn, ",") <= 0  and -quantity >= 1 and id in  %s' % id
              print(sql)
              generic.update(sql)

          # 更新状态
          # sql = 'update stockout_manage_device_lend set status = 7  where id in %s' % lendidid
          # print(sql)
          # generic.update(sql)

          sql = 'select * from sale_manage_sales_out_stockout where status <> 7 and saleid_id in %s' % saleidid
          print(sql)
          datas = generic.query(sql)
          # 还有未入库的备件
          if datas:
              sql = 'update sale_manage_sales_out set status = 9  where id in %s' % saleidid
          else:
              sql = 'update sale_manage_sales_out set status = 7  where id in %s' % saleidid
          print(sql)
          generic.update(sql)

          # 更新单据流程
          sql = 'update report_manage_workflow_query ' \
                'set author2 = "%s",update_time2 = "%s",name2 = "%s" ' \
                'where pid in %s' % (author, d1, billid, id)
          generic.update(sql)

          messages.success(self.request, '提交销售单出库成功！')
          # 返回 HttpResponse
          return redirect(self.request.get_full_path())

# 销售下单
class ContactAdminSales_out(object):
    def save_models(self):
        obj = self.new_obj
        flag = self.org_obj is None and 'create' or 'change'
        request = self.request
        obj.author = str(request.user)
        if flag == 'create':  # 新增默认回填操作员
            OrderNO = generic.getOrderMaxNO('XSD')
            obj.id = OrderNO
            obj.save()
        else:
            obj.save()

    # 过滤，只能查看自己下的工单
    def queryset(self):
        # 取出当前Courses表单的所有对象
        qs = super().queryset()
        # 如果不是超级管理员,就对qs进行过滤
        if not self.request.user.is_superuser:
            qs = qs.filter(author=self.request.user)
        return qs
    model_icon = 'fa fa-cog'  # 图标样式
    list_display = ('id', 'status', 'machineSelects', 'customer','remark','author', 'update_time','pub_date')
    exclude = ('id', 'status', 'customersSignid', 'update_time')
    readonly_fields = ('author',)
    # 多选样式
    style_fields = {'machineSelects': 'm2m_transfer', }
    actions = [Act_Device_sale]
    # 设置过滤
    list_filter = ('status', 'customer', 'update_time')
    list_display_links = ('id', 'machineSelects', )

# 销售下单出库
class ContactAdminSales_out_stockout_out(object):
    def save_models(self):
        obj = self.new_obj
        flag = self.org_obj is None and 'create' or 'change'
        request = self.request
        # obj.author = str(request.user)
        if obj.quantity > 0:
            obj.quantity = -obj.quantity
        if flag == 'create':  # 新增默认回填操作员
            obj.save()
        else:
            obj.save()

    model_icon = 'fa fa-cog'  # 图标样式
    list_display = ('billid', 'saleid', 'status', 'ifsure', 'customer','shopid', 'FRUSelect', 'quantity', 'SN', 'FRU', 'PN', 'desc', 'replace',
    'location',  'image_data', 'remark', 'pub_date', 'author','update_time')
    list_display_links = ('billid', 'saleid',)
    exclude = ('billid', 'saleid', 'status', 'FRU', 'PN', 'machineModel', 'machineSN', 'customersSignid', 'update_time', 'price', 'useage')
    readonly_fields = ('author',)
    # list_per_page设置每页显示多少条记录，默认是100条
    list_per_page = 5
    refresh_times = (10, 60)  # 指定列表页的数据定时刷新
    # 设置过滤
    list_filter = ('status', 'ifsure', 'shopid', 'location', 'pub_date')
    search_fields = ('SN', 'FRU', 'PN', 'machineSN', 'replace')
    aggregate_fields = {'quantity': 'sum', }
    ordering = ('status',  '-billid','-saleid', '-ifsure')
    # 多选样式
    style_fields = {'machineSelects': 'm2m_transfer', }
    actions = [Act_Device_sale_stockout]
    list_editable = ['SN','location' ]
    list_display_links = ('saleid', 'FRUSelect', 'billid')

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
