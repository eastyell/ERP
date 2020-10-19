# 模块名称：其他库业务处理模块
# 创建日期：2020-6
# 最后修改日期：2020-6
# 作者：Jason

from django.contrib import admin
from stockin_manage.models import *
import datetime
from xadmin import views
import xadmin
from xadmin.plugins.actions import BaseActionView
from django.contrib import messages
from django.shortcuts import redirect
from common import generic

# Register your models here.

# 提交所选的 回收申请
class ReturnPost(BaseActionView): # 定义一个动作
    action_name = "return_post"  # 相当于这个 Action 的唯一标示, 尽量用比较针对性的名字
    description = "提交所选的 回收申请"  # 要显示的名字
    icon = 'fa fa-tasks'  # 图标
    model_perm = "change"   # 该动作所需权限

    def do_action(self, queryset):  # 重载do_action()方法
        # queryset 是包含了已经选择的数据的 queryset
        # 生成采购下单明细
        d1 = timezone.now()
        # d1 = d1.strftime("%Y-%m-%d %H:%M")
        # queryset.update(update_time=d1.strftime("%Y-%m-%d %H:%M"))
        a = ()
        for i in range(0, queryset.count()):
            status = str(queryset.values_list('status')[i]).strip('(,)')
            parts = str(queryset.values_list('machineSelects')[i]).strip('(,)')
            print(parts)
            if status == '0':
              if parts != 'None':
                a =  a + queryset.values_list('id')[i]
                # 插入单据流程
        print(a)
        id = '("' + '","'.join(a) + '")'
        print(id)
        # 状态待提交   才能提交
        if a:
          sql = 'update stockin_manage_device_return set status = 4,update_time = "%s" where id in  %s' % (
          d1, id)
          print(sql)
          generic.update(sql)
          # 提交单据回收入库
          sql = 'insert into stockin_manage_device_return_stockin' \
              '(ifsure,returnid_id,desc,shopid_id,quantity,remark,FRUSelect_id,status,customer_id,fru,pn,machinemodel,replace,image,location_id,update_time) ' \
              'select distinct 0,b.id,c.desc,d.shop_id,c.quantity,b.remark,c.device_id,4,b.customer_id,e.name,d.pn,f.name,d.replaces,d.image,1,date() ' \
              'from stockin_manage_device_return_machineSelects a,stockin_manage_device_return b,baseinfo_manage_selectorderdetail c,baseinfo_manage_devicestores d,params_manage_device_fru e, params_manage_device_kind f ' \
              'where a.device_return_id = b.id and c.id=a.selectorderdetail_id and  c.device_id = d.id and d.FRUS_id = e.id and f.id= d.machineModels_id and b.id in %s' % id
          print(sql)
          generic.update(sql)
          # 插入单据流程
          sql = 'insert into report_manage_workflow_query ' \
                '(flowstatus1,name1,pid,FRUSelect_id,FRU,author1,update_time1,flowstatus2) ' \
                'select "回收下单" as status,b.id,a.id,a.FRUSelect_id,a.FRU,b.author,b.update_time,"回收入库" ' \
                'from stockin_manage_device_return_stockin a,' \
                'stockin_manage_device_return b ' \
                'where b.id = a.returnid_id and b.id in %s' % id
          generic.update(sql)
          messages.success(self.request, '提交回收申请成功！')
          # 返回 HttpResponse
          return redirect(self.request.get_full_path())

# 提交所选的 回收入库
class Act_Return_stockin(BaseActionView):  # 定义一个动作
    action_name = "return_stockin"  # 相当于这个 Action 的唯一标示, 尽量用比较针对性的名字
    description = "提交所选的 回收入库"  # 要显示的名字
    icon = 'fa fa-tasks'  # 图标
    model_perm = "change"  # 该动作所需权限

    def do_action(self, queryset):  # 重载do_action()方法
        # queryset 是包含了已经选择的数据的 queryset
        # 生成采购下单明细
        d1 = timezone.now()
        # d1 = d1.strftime("%Y-%m-%d")
        request = self.request
        author = str(request.user)
        a = ()
        b = ()
        for i in range(0, queryset.count()):
            status = str(queryset.values_list('status')[i]).strip('(,)')
            SN = str(queryset.values_list('SN')[i]).strip('(,)')
            print('SN:' + SN)
            if (status == '4') and (SN != 'None'):
              a = a + queryset.values_list('id')[i]
              b = b + queryset.values_list('returnid_id')[i]
        print(a)
        id = str(a).strip().rstrip(',)')
        id = id + ')'
        print(id)
        returnid = str(b).strip().rstrip(',)')
        returnid = returnid + ')'
        print(returnid)
        # 状态待入库   才能提交
        if a:
          billid = generic.getOrderMaxNO('HSRK')
          sql = 'update stockin_manage_device_return_stockin set status = 5,billid = "%s",author = "%s"  where replace(sn," ","") <> "" and id in  %s' % (
          billid, author, id)
          print(sql)
          generic.update(sql)

          # 生成出入库报表数据
          sql = 'insert into report_manage_stock_detail' \
              ' (customer_id,stock_type,bill_type,bill_id,sn, FRU, PN, machineModel, machineSN, price,quantity, useage,source, desc, replace, image,FRUSelect_id, author, remark, location_id,shopid_id,pub_date,update_time) ' \
              'select a.customer_id,0,5,a.billid,a.sn, a.FRU, a.PN, a.machineModel, a.machineSN,0, 1, 0,a.source, a.desc, a.replace, a.image, a.FRUSelect_id, a.author, a.remark, a.location_id,b.shop_id,a.pub_date,date() ' \
              'from stockin_manage_device_return_stockin a,baseinfo_manage_devicestores b where replace(sn," ","") <> "" and (instr(a.sn, ",") <= 0 or  a.sn is null) and a.FRUSelect_id = b.id and a.id in %s' % id
          print(sql)
          generic.update(sql)
          # 拆分SN码批量入库
          sql = 'select billid,sn,quantity,id  ' \
                'from stockin_manage_device_return_stockin where instr(sn, ",") > 0 and id in %s' % id
          print(sql)
          cds = generic.query(sql)
          rksl = 0 # 拆分剩余数量的回收入库单
          if cds:
             for i in range(0, len(cds)):
                 billids = cds[i][0]
                 sn = cds[i][1]
                 quantity = cds[i][2]
                 Fid = cds[i][3]
                 strlist = sn.split(',')  # 用逗号分割sn字符串，并保存到列表
                 for value in strlist:  # 循环输出列表值
                    sql = 'insert into splitSN (bill,SN) ' \
                          'VALUES ("%s","%s") ' % (billids,value)
                    print(sql)
                    generic.update(sql)
                    rksl = rksl + 1
                 # 拆分剩余数量的回收入库单
                 sysl = quantity - rksl
                 print('剩余数量：')
                 print(str(sysl))
                 if sysl > 0:
                   sql = 'insert into stockin_manage_device_return_stockin' \
                         '(customer_id,ifsure,returnid_id,desc,shopid_id,quantity,remark,FRUSelect_id,status,customer_id,fru,pn,machinemodel,replace,image,location_id,update_time ) '\
                         'select customer_id,ifsure,returnid_id,desc,shopid_id,%s,remark,FRUSelect_id,4,customer_id,fru,pn,machinemodel,replace,image,location_id,date() from stockin_manage_device_return_stockin where id = %s' % (sysl,Fid)
                   print(sql)
                   generic.update(sql)
                   print(billid)
                   sql = 'update stockin_manage_device_return_stockin set quantity =%s,billid = "%s" where id = %s' % (rksl,billid,Fid)
                   print(sql)
                   generic.update(sql)

             sql = 'insert into report_manage_stock_detail' \
                   ' (customer_id,stock_type,bill_type,bill_id,sn, FRU, PN, machineModel, machineSN, price,quantity, useage,source, desc, replace, image,FRUSelect_id, author, remark, location_id,shopid_id,pub_date,update_time) ' \
                   'select a.customer_id,0,5,a.billid,c.sn, a.FRU, a.PN, a.machineModel, a.machineSN,0, 1, 0,a.source, a.desc, a.replace, a.image, a.FRUSelect_id, a.author, a.remark, a.location_id,b.shop_id,a.pub_date,date() ' \
                   'from stockin_manage_device_return_stockin a,baseinfo_manage_devicestores b,splitSN c where instr(a.sn, ",") > 0 and a.billid = c.bill and a.FRUSelect_id = b.id and a.id in %s' % id
             print(sql)
             generic.update(sql)
          else: # 输入一个SN
              sql = 'insert into stockin_manage_device_return_stockin' \
                    '(customer_id,ifsure,returnid_id,desc,shopid_id,quantity,remark,FRUSelect_id,status,customer_id,fru,pn,machinemodel,replace,image,location_id,update_time) ' \
                    'select customer_id,ifsure,returnid_id,desc,shopid_id,quantity-1,remark,FRUSelect_id,4,customer_id,fru,pn,machinemodel,replace,image,location_id,date() from stockin_manage_device_return_stockin where quantity > 1 and id in %s' % id
              print(sql)
              generic.update(sql)
              # 更新单据信息
              sql = 'update stockin_manage_device_return_stockin set quantity = 1  where replace(sn," ","") <> "" and instr(sn, ",") <= 0  and quantity >= 1 and id in  %s' % id
              print(sql)
              generic.update(sql)
          # 更新状态
          sql = 'select * from stockin_manage_device_return_stockin where status <> 5 and returnid_id in %s' % returnid
          print(sql)
          datas = generic.query(sql)
          # 还有未入库的备件
          if datas:
              sql = 'update stockin_manage_device_return set status = 8  where id in %s' % returnid
          else:
              sql = 'update stockin_manage_device_return set status = 5  where id in %s' % returnid
          print(sql)
          generic.update(sql)

          # 更新单据流程
          sql = 'update report_manage_workflow_query ' \
                'set author2 = "%s",update_time2 = "%s",name2 = "%s" ' \
                'where pid in %s' % (author, d1, billid, id)
          generic.update(sql)

          messages.success(self.request, '提交回收入库成功！')
          # 返回 HttpResponse
          return redirect(self.request.get_full_path())


# 提交所选的 维修返回入库
class Act_Repair_use_stockin(BaseActionView): # 定义一个动作
    action_name = "repair_use_stockin"  # 相当于这个 Action 的唯一标示, 尽量用比较针对性的名字
    description = "提交所选的 维修返回入库"  # 要显示的名字
    icon = 'fa fa-tasks'  # 图标
    model_perm = "change"   # 该动作所需权限

    def do_action(self, queryset):  # 重载do_action()方法
        # queryset 是包含了已经选择的数据的 queryset
        # 生成采购下单明细
        author = self.request.user
        d1 = timezone.now()
        d1 = d1.strftime("%Y-%m-%d %H:%M")
        # queryset.update(pub_date=d1.strftime("%Y-%m-%d"))
        a = ()
        wxlyid = ()
        for i in range(0, queryset.count()):
            status = str(queryset.values_list('status')[i]).strip('(,)')
            SN = str(queryset.values_list('SN')[i]).strip('(,)')
            print('SN:' + SN)
            if (status == '4') and (SN != 'None'):
                a = a + queryset.values_list('id')[i]
                wxlyid = wxlyid + queryset.values_list('stockouid_id')[i]
        print(a)
        id = str(a).strip().rstrip(',)')
        id = id + ')'
        print(id)
        wxlyid = str(wxlyid).strip().rstrip(',)')
        wxlyid = wxlyid + ')'
        # 状态待入库   才能提交
        if a:
          billid = generic.getOrderMaxNO('WXFHRK')
          sql = 'update stockin_manage_repair_use_stockin set status = 5,billid = "%s"  where id in  %s' % (
               billid, id)
          print(sql)
          generic.update(sql)
          # 如果入库日期没选，默认系统日期
          sql = 'update stockin_manage_repair_use_stockin set pub_date = "%s",author = "%s"  where pub_date is null  and id in  %s' % (
              d1, author, id)
          print(sql)
          generic.update(sql)
          # 生成出入库报表数据
          sql = 'insert into report_manage_stock_detail' \
              ' (customer_id,stock_type,bill_type,bill_id,sn, FRU, PN, machineModel, machineSN, price,quantity, useage,source, desc, replace, image,FRUSelect_id, author, remark, location_id,shopid_id,pub_date)' \
              'select a.customer_id,0,7,a.billid,a.sn, a.FRU, a.PN, a.machineModel, a.machineSN, a.price, 1, a.useage,a.source, a.desc, a.replace, a.image, a.FRUSelect_id, a.author, a.remark, a.location_id,b.shop_id,a.pub_date ' \
              'from stockin_manage_repair_use_stockin a,baseinfo_manage_devicestores b where (instr(a.sn, ",") <= 0  or a.sn is null) and a.FRUSelect_id = b.id and a.id in %s' % id
          print(sql)
          generic.update(sql)
          # 拆分SN码批量入库
          sql = 'select billid,sn ' \
                'from stockin_manage_repair_use_stockin where instr(sn, ",") > 0 and id in %s' % id
          print(sql)
          cds = generic.query(sql)
          if cds:
              for i in range(0, len(cds)):
                  billids = cds[i][0]
                  sn = cds[i][1]
                  strlist = sn.split(',')  # 用逗号分割sn字符串，并保存到列表
                  for value in strlist:  # 循环输出列表值
                      sql = 'insert into splitSN (bill,SN) ' \
                            'VALUES ("%s","%s") ' % (billids, value)
                      print(sql)
                      generic.update(sql)
              sql = 'insert into report_manage_stock_detail' \
                    ' (customer_id,stock_type,bill_type,bill_id,sn, FRU, PN, machineModel, machineSN, price,quantity, useage,source, desc, replace, image,FRUSelect_id, author, remark, location_id,shopid_id,pub_date)' \
                    'select a.customer_id,0,7,a.billid,c.sn, a.FRU, a.PN, a.machineModel, a.machineSN, a.price, 1, a.useage,a.source, a.desc, a.replace, a.image, a.FRUSelect_id, a.author, a.remark, a.location_id,b.shop_id,a.pub_date ' \
                    'from stockin_manage_repair_use_stockin a,baseinfo_manage_devicestores b,splitSN c where instr(a.sn, ",") > 0 and a.billid = c.bill and a.FRUSelect_id = b.id and a.id in %s' % id
              print(sql)
              generic.update(sql)

          # 更新单据流程
          sql = 'update report_manage_workflow_query ' \
                'set author3 = "%s",update_time3 = "%s",name3 = "%s" ' \
                'where pid in %s' % (author, d1, billid, wxlyid)
          generic.update(sql)

          messages.success(self.request, '提交维修返回入库成功！')
          # 返回 HttpResponse
          return redirect(self.request.get_full_path())

# 回收下单
class ContactAdminDevice_return(object):
    def save_models(self):
        obj = self.new_obj
        flag = self.org_obj is None and 'create' or 'change'
        request = self.request
        obj.author = str(request.user)
        if flag == 'create':  # 新增默认回填操作员
            OrderNO = generic.getOrderMaxNO('HSD')
            obj.id = OrderNO
            obj.save()
        else:
            obj.save()

    list_display = ('id', 'status', 'machineSelects', 'desc', 'customer', 'remark', 'author', 'update_time','pub_date')
    # list_per_page设置每页显示多少条记录，默认是100条
    list_per_page = 5
    # 添加和修改时那些界面不显示
    exclude = ('id','status', 'price','quantity','update_time')
    readonly_fields = ('author',)
    # 多选样式
    # style_fields = {'machineSelects': 'm2m_dropdown'}
    style_fields = {'machineSelects': 'm2m_transfer', }
    filter_horizontal = ['machineSelects']
    actions = [ReturnPost]
    refresh_times = (10, 60)  # 指定列表页的数据定时刷新
    # 设置过滤
    list_filter = ('status', 'customer', 'update_time')
    # search_fields = ('desc')
    list_display_links = ('id', 'machineSelects')
    model_icon = 'fa fa-sign-in'  # 图标样式
    # 过滤，只能查看自己下的工单
    def queryset(self):
        # 取出当前Courses表单的所有对象
        qs = super().queryset()
        # 如果不是超级管理员,就对qs进行过滤
        if not self.request.user.is_superuser:
            qs = qs.filter(author=self.request.user)
        return qs

# 回收入库
class ContactAdminDevice_return_stockin(object):
    def save_models(self):
        obj = self.new_obj
        flag = self.org_obj is None and 'create' or 'change'
        request = self.request
        # obj.author = str(request.user)
        if flag == 'create':  # 新增默认回填操作员

            obj.save()
        else:
            obj.save()

    list_display = ('billid', 'status', 'ifsure','returnid','customer','shopid', 'FRUSelect','quantity','SN','FRU','PN',
                    'replace','location','desc','source','image_data','remark', 'author','pub_date','update_time')
    # list_per_page设置每页显示多少条记录，默认是100条
    list_per_page = 5
    refresh_times = (10, 60)  # 指定列表页的数据定时刷新
    exclude = ('returnid', 'billid', 'status', 'FRU', 'PN','machineModel','machineSN','update_time')
    readonly_fields = ('author',)
    actions = [Act_Return_stockin]
    list_display_links = ('billid', 'returnid','FRUSelect')
    list_editable = ['location']
    aggregate_fields = {'quantity': 'sum', }
    # 设置过滤
    list_filter = ('status', 'ifsure','location','customer','pub_date')
    search_fields = ('SN','PN', 'FRU','replace')
    ordering = ('status', '-billid', '-ifsure')
    model_icon = 'fa fa-sign-in'   # 图标样式

# 维修返回入库
class ContactAdminRepair_use_stockin(object):
    def save_models(self):
        obj = self.new_obj
        flag = self.org_obj is None and 'create' or 'change'
        request = self.request
        obj.author = str(request.user)
        if flag == 'create':
            obj.save()
        else:
            obj.save()
            # 更新库存数量
            # if (obj.quantity != 0) and (obj.billid):
            #     if (obj.machineModel and obj.machineModel.strip() != ''):
            #       sql = "UPDATE baseinfo_manage_devicestores SET quantity = quantity + %s where machineModel = %s"
            #       params = [obj.quantity, obj.machineModel]
            #     else:
            #       sql = "UPDATE baseinfo_manage_devicestores SET quantity = quantity + %s where FRU = %s or PN = %s"
            #       params = [obj.quantity, obj.FRU, obj.PN]
            #     print(params)
            #     print(sql)
            #     generic.update(sql, params)
            #     print(sql)
            #     print(params)
                # # 插入出入库报表数据
                # id = obj.id
                # sql = 'insert into report_manage_stock_detail' \
                #       ' (bill_type,bill_id,sn, FRU, PN, price,quantity, useage,source, image,FRUSelect_id, author, remark, location_id,pub_date)' \
                #       'select 6,billid,sn, FRU, PN, price, quantity, useage,source, image, FRUSelect_id, author, remark, location_id,pub_date ' \
                #       'from stockout_manage_repair_use_stockout where id="%s"' % id
                # generic.update(sql)
                # print(sql)

    list_display = ('billid','stockouid', 'status','ifsure','customer','FRUSelect', 'SN', 'desc', 'replace',
                    'quantity', 'location','image_data', 'remark', 'author','pub_date', 'update_time')
    # 添加和修改时那些界面不显示
    exclude = ('billid','status','source','FRU','PN','price','useage','customersSignid',
               'machineSN', 'machineModel','update_time')
    readonly_fields = ('author',)
    list_display_links = ('bill_id','stockouid','FRUSelect' )
    actions = [Act_Repair_use_stockin]
    # list_per_page设置每页显示多少条记录，默认是100条
    list_per_page = 5
    # 设置过滤
    list_filter = ('status', 'ifsure','customer','location','pub_date')
    search_fields = ('SN','machineSN','FRU','PN','replace' )
    aggregate_fields = {'quantity': 'sum', }
    ordering = ('status','billid','-ifsure')
    model_icon = 'fa fa-sign-in'   # 图标样式


xadmin.site.register(Device_return, ContactAdminDevice_return) # 回收下单
xadmin.site.register(Device_return_stockin, ContactAdminDevice_return_stockin)# 回收入库
xadmin.site.register(Repair_use_stockin, ContactAdminRepair_use_stockin)# 维修返回入库
