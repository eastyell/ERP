# 模块名称：其他出库业务处理模块
# 创建日期：2020-6
# 最后修改日期：2020-6
# 作者：Jason

from django.contrib import admin
from stockout_manage.models import *
import datetime
import xadmin
from common import generic
from xadmin.plugins.actions import BaseActionView
from django.contrib import messages
from django.shortcuts import redirect

# 提交所选的 维修领用下单
class Act_Repair_use(BaseActionView): # 定义一个动作
    action_name = "repair_use"  # 相当于这个 Action 的唯一标示, 尽量用比较针对性的名字
    description = "提交所选的 维修领用下单"  # 要显示的名字
    icon = 'fa fa-tasks'  # 图标
    model_perm = "change"   # 该动作所需权限

    def do_action(self, queryset):  # 重载do_action()方法
        # queryset 是包含了已经选择的数据的 queryset
        # 生成采购下单明细
        d1 = timezone.now()
        # d1 = d1.strftime("%Y-%m-%d %H:%M")
        a = ()
        for i in range(0, queryset.count()):
            status = str(queryset.values_list('status')[i]).strip('(,)')
            parts = str(queryset.values_list('machineSelects')[i]).strip('(,)')
            if (status == '0') and (parts != 'None'):
              # a = a + queryset.values_list('id')[i]
              repairid = queryset.values_list('id')[i]
              repairids = ''.join(repairid)
              repairids = repairids.strip('()')
              print(repairids)
              sql = 'select distinct SN,FRUSelect_id from report_manage_stock_detail where FRUSelect_id in ' \
                    '(select device_id  from baseinfo_manage_selectorderdetail where id in ' \
                    '(select selectorderdetail_id from stockout_manage_repair_use_machineSelects where repair_use_id = "%s")) and stock_type = 0 ' % \
                    queryset.values_list('id')[i]
              print(sql)
              cds = generic.query(sql)
              sn = ''
              fruSelectid = '0'
              if cds:
                  a = a + queryset.values_list('id')[i]
                  tempid = cds[0][1]
                  for i in range(0, len(cds)):
                      # 遇见不同的备件新增
                      if cds[i][1] is not None:
                          fruSelectid = cds[i][1]
                          if tempid != fruSelectid:
                             sql = 'insert into splitSN (bill,SN,FRUselectid) ' \
                                  'VALUES ("%s","%s","%s") ' % (repairids, sn, cds[i-1][1])
                             print(sql)
                             generic.update(sql)
                             sn = ''
                             tempid = fruSelectid
                      if cds[i][0] is not None:
                         if sn != '':
                           sn = sn + ',' + cds[i][0]
                         else:
                           sn = cds[i][0]

                  sql = 'insert into splitSN (bill,SN,FRUselectid) ' \
                        'VALUES ("%s","%s","%s") ' % (repairids, sn, fruSelectid)
                  print(sql)
                  generic.update(sql)
        print(a)
        id = str(a).strip().rstrip(',)')
        id = id + ')'
        print(id)
        # 状态待提交   才能提交
        if a:
          # 提交单据维修领料出库
          # sql = 'insert into stockout_manage_repair_use_stockout' \
          #     ' (repairid_id, status, ifsure, sn, FRU, PN, machineModel,useage, price, quantity, source, desc, replace, customersSignid_id, image, author, remark, location_id, shopid_id,FRUSelect_id,pub_date) ' \
          #     'select id, 6, 0, sn, FRU, PN, machineModel,useage, price, quantity, source, desc, replace, customersSignid_id, image, author, remark||"\n下单人:"||author , 1, shopid_id, FRUSelect_id, date() ' \
          #     'from stockout_manage_repair_use where id in %s' % id
          # print(sql)
          # 提交单据租用下单
          # 'select b.id,6,0,g.SN,c.desc,c.shopid_id,0,d.price,-c.quantity,b.author,b.remark,c.device_id,6,d.machineModels_id,e.name,d.pn,f.name,d.replaces,d.image,date(),1 ' \
          # sql = 'insert into stockout_manage_device_lend_stockout' \
          #       '(ifsure,SN,lendid_id,desc,shopid_id,useage,price,quantity,author,remark,FRUSelect_id,status,customersSignid_id,fru,pn,machinemodel,replace,image,pub_date,location_id) ' \
          #       'select 0,g.SN,b.id,c.desc,c.shopid_id,0,d.price,-c.quantity,b.author,b.remark,c.device_id,6,d.machineModels_id,e.name,d.pn,f.name,d.replaces,d.image,date(),1 ' \
          #       'from stockout_manage_device_lend_machineSelects a,stockout_manage_device_lend b,baseinfo_manage_selectorderdetail c,baseinfo_manage_devicestores d,params_manage_device_fru e, params_manage_device_kind f,splitSN g ' \
          #       'where a.device_lend_id = b.id and c.id=a.selectorderdetail_id and  c.device_id = d.id and d.FRUS_id = e.id and f.id= d.machineModels_id and b.id=g.bill  and b.id in %s' % id
          # print(sql)

          sql = 'insert into stockout_manage_repair_use_stockout' \
                ' (customer_id,repairid_id, status, ifsure, sn, FRU, PN, machineModel,useage, price, quantity, source, desc, replace, customersSignid_id, image, remark, location_id, shopid_id,FRUSelect_id,update_time) ' \
                'select distinct b.customer_id,b.id, 6, 0, g.sn, e.name, d.pn, f.name,b.useage, d.price, -c.quantity, d.source, c.desc, d.replaces, b.customersSignid_id, d.image, b.remark||"\n下单人:"||b.author , 1, d.shop_id, c.device_id,date()  ' \
                'from stockout_manage_repair_use_machineSelects a,stockout_manage_repair_use b,baseinfo_manage_selectorderdetail c,baseinfo_manage_devicestores d,params_manage_device_fru e, params_manage_device_kind f,splitSN g ' \
                'where a.repair_use_id = b.id and c.id=a.selectorderdetail_id and  c.device_id = d.id and d.FRUS_id = e.id and f.id= d.machineModels_id and c.device_id = g.fruSelectid and g.bill = b.id and b.id in %s' % id
          print(sql)
          generic.update(sql)

          sql = 'update stockout_manage_repair_use set status = 6,update_time = "%s" where id in  %s' % (
              d1, id)
          print(sql)
          generic.update(sql)

          # 插入单据流程
          sql = 'insert into report_manage_workflow_query ' \
                '(flowstatus1,name1,pid,FRUSelect_id,FRU,author1,update_time1,flowstatus2) ' \
                'select "维修领用下单" as status,b.id,a.id,a.FRUSelect_id,a.FRU,b.author,b.update_time,"维修领用入库" ' \
                'from stockout_manage_repair_use_stockout a,' \
                'stockout_manage_repair_use b ' \
                'where b.id = a.repairid_id and b.id in %s' % id
          generic.update(sql)

          messages.success(self.request, '提交维修领用下单成功！')
          # 返回 HttpResponse
          return redirect(self.request.get_full_path())

# 提交所选的 维修领用出库
class Act_Repair_use_stockout(BaseActionView): # 定义一个动作
    action_name = "repair_use_stockout"  # 相当于这个 Action 的唯一标示, 尽量用比较针对性的名字
    description = "提交所选的 维修领用出库"  # 要显示的名字
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
            SN = str(queryset.values_list('SN')[i]).strip('(,)')
            print('SN:' + SN)
            if (status == '6') and (SN != 'None'):
              a = a + queryset.values_list('id')[i]
              b = b + queryset.values_list('repairid_id')[i]
        print(a)
        id = str(a).strip().rstrip(',)')
        id = id + ')'
        print(id)
        repairid = str(b).strip().rstrip(',)')
        repairid = repairid + ')'
        print(repairid)
        # 状态待出库   才能提交
        if a:
          # SN码不等于空值，更新状态和出库单号
          billid = generic.getOrderMaxNO('WXLYCK')
          sql = 'update stockout_manage_repair_use_stockout set status = 7,billid = "%s",author = "%s"  where replace(sn," ","") <> "" and id in  %s' % (
              billid, author, id)
          print(sql)
          generic.update(sql)

          # 如果入库日期没选，默认系统日期
          sql = 'update stockout_manage_repair_use_stockout set pub_date = "%s",author = "%s"  where pub_date is null and replace(sn," ","") <> "" and id in  %s' % (
              d1, author, id)
          print(sql)
          generic.update(sql)

          # 生成出入库报表数据,单个SN码
          sql = 'insert into report_manage_stock_detail' \
              ' (customer_id,stock_type,bill_type,bill_id,sn, FRU, PN, machineModel, machineSN, price,quantity, useage,source, desc, replace, image,FRUSelect_id, author, remark, location_id,shopid_id,pub_date,update_time) ' \
              'select customer_id,1,6,billid,sn, FRU, PN, machineModel, machineSN, price, -1, useage,source, desc, replace, image, FRUSelect_id, author, remark, location_id,shopid_id,pub_date,date() ' \
              'from stockout_manage_repair_use_stockout where replace(sn," ","") <> "" and (instr(sn, ",") <= 0  or  sn is null) and id in %s' % id
          print(sql)
          generic.update(sql)
          # 拆分SN码批量入库
          sql = 'select billid,sn,quantity,id ' \
                'from stockout_manage_repair_use_stockout where instr(sn, ",") > 0 and id in %s' % id
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
                      rksl = rksl + 1  # 计算入库数量
              # 拆分剩余数量的回收入库单
              sysl = quantity - rksl
              print('剩余数量：')
              print(str(sysl))
              if sysl > 0:
                  # 拆分单据，插入剩余数量的入库单据
                  sql = 'insert into stockout_manage_repair_use_stockout ' \
                        '(customer_id,repairid_id, status, ifsure,  FRU, PN, machineModel,useage, price, quantity, source, desc, replace, customersSignid_id, image, remark, location_id, shopid_id,FRUSelect_id,update_time ) ' \
                        'select customer_id,repairid_id, 6, ifsure,  FRU, PN, machineModel,useage, price, %s, source, desc, replace, customersSignid_id, image, remark, location_id, shopid_id,FRUSelect_id,date() from stockout_manage_repair_use_stockout where id = %s ' \
                        % (-sysl, Fid)
                  print(sql)
                  generic.update(sql)
                  # 更新入库单据信息
                  sql = 'update stockout_manage_repair_use_stockout set quantity =%s,billid = "%s" where id = %s' % (
                      -rksl, billid, Fid)
                  print(sql)
                  generic.update(sql)
              # 生成出入库报表数据，批量SN码
              sql = 'insert into report_manage_stock_detail ' \
                    '(customer_id,stock_type,bill_type,bill_id,sn, FRU, PN, machineModel, machineSN, price,quantity, useage,source, desc, replace, image,FRUSelect_id, author, remark, location_id,shopid_id,pub_date,update_time) ' \
                    'select a.customer_id,1,6, a.billid, b.sn, a.FRU, a.PN, a.machineModel, a.machineSN, a.price, -1, a.useage, a.source, a.desc, a.replace, a.image, a.FRUSelect_id, a.author, a.remark, a.location_id, a.shopid_id, a.pub_date,date() ' \
                    'from stockout_manage_repair_use_stockout a, splitSN b where instr(a.sn, ",") > 0 and a.billid = b.bill and a.id in %s' % id
              print(sql)
              generic.update(sql)
          else:  # 输入一个SN，拆分单据，插入剩余数量单据
              sql = 'insert into stockout_manage_repair_use_stockout ' \
                    '(customer_id,repairid_id, status, ifsure, FRU, PN, machineModel,useage, price, quantity, source, desc, replace, customersSignid_id, image, remark, location_id, shopid_id,FRUSelect_id,update_time) ' \
                    'select customer_id,repairid_id,6,ifsure,FRU,PN,machineModel,useage,price,quantity+1,source, desc, replace, customersSignid_id, image, remark, location_id, shopid_id,FRUSelect_id,date() from stockout_manage_repair_use_stockout where -quantity > 1 and  replace(sn," ","") <> ""  and id in %s' % id
              print(sql)
              generic.update(sql)
              # 更新单据信息
              sql = 'update stockout_manage_repair_use_stockout set quantity = -1  where replace(sn," ","") <> "" and instr(sn, ",") <= 0  and -quantity >= 1 and id in  %s' % id
              print(sql)
              generic.update(sql)

          # 更新状态
          sql = 'update stockout_manage_repair_use set status = 7  where id in %s' % repairid
          print(sql)
          generic.update(sql)
          # 插入维修返回入库
          sql = 'insert into stockin_manage_repair_use_stockin ' \
                '(customer_id,ifsure,status,stockouid_id,FRUSelect_id,SN,customersSignid_id,desc,source,replace,useage,price,quantity,image,remark,location_id,update_time) ' \
                'select customer_id,0,4,id,FRUSelect_id, SN, customersSignid_id, desc,source, replace, useage,price,-quantity,image, remark,location_id,date() ' \
                'from stockout_manage_repair_use_stockout  where  replace(sn," ","") <> "" and id in %s' % id
          print(sql)
          generic.update(sql)

          # 更新单据流程
          sql = 'update report_manage_workflow_query ' \
                'set author2 = "%s",update_time2 = "%s",name2 = "%s",flowstatus3 = "维修返回入库" ' \
                'where pid in %s' % (author, d1, billid, id)
          generic.update(sql)

          messages.success(self.request, '提交维修领用出库成功！')
          # 返回 HttpResponse
          return redirect(self.request.get_full_path())

# 提交所选的 租用下单
class Act_Device_lend(BaseActionView): # 定义一个动作
    action_name = "device_lend"  # 相当于这个 Action 的唯一标示, 尽量用比较针对性的名字
    description = "提交所选的 租用下单"  # 要显示的名字
    icon = 'fa fa-tasks'  # 图标
    model_perm = "change"   # 该动作所需权限

    def do_action(self, queryset):  # 重载do_action()方法
        # queryset 是包含了已经选择的数据的 queryset
        # 生成采购下单明细
        # queryset.update(status = 6)
        d1 = timezone.now()
        # d1 = d1.strftime("%Y-%m-%d %H:%M")
        a = ()
        for i in range(0, queryset.count()):
            status = str(queryset.values_list('status')[i]).strip('(,)')
            parts = str(queryset.values_list('machineSelects')[i]).strip('(,)')
            print('parts: ' + parts)
            if (status == '0') and (parts != 'None') :
              # a = a + queryset.values_list('id')[i]
              lendid = queryset.values_list('id')[i]
              lendids = ''.join(lendid)
              lendids = lendids.strip('()')
              print(lendids)
              sql = 'select distinct SN,FRUSelect_id from report_manage_stock_detail where FRUSelect_id in ' \
                    '(select device_id  from baseinfo_manage_selectorderdetail where id in '\
                    '(select selectorderdetail_id from stockout_manage_device_lend_machineSelects where device_lend_id = "%s")) and stock_type = 0 '  %queryset.values_list('id')[i]
              print(sql)
              cds = generic.query(sql)
              sn = ''
              fruSelectid = '0'
              if cds:
                  a = a + queryset.values_list('id')[i]
                  tempid = cds[0][1]
                  for i in range(0, len(cds)):
                      # 遇见不同的备件新增
                      if cds[i][1] is not None:
                         fruSelectid = cds[i][1]
                         if tempid != fruSelectid:
                             sql = 'insert into splitSN (bill,SN,FRUselectid) ' \
                                   'VALUES ("%s","%s","%s") ' % (lendids, sn, cds[i-1][1])
                             print(sql)
                             generic.update(sql)
                             sn = ''
                             tempid = fruSelectid
                      if cds[i][0] is not None:
                          if sn != '':
                             sn = sn + ',' + cds[i][0]
                          else: sn = cds[i][0]

                  sql = 'insert into splitSN (bill,SN,FRUselectid) ' \
                          'VALUES ("%s","%s","%s") ' % (lendids,sn,fruSelectid)
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
          sql = 'update stockout_manage_device_lend set status = 6,update_time = "%s" where id in  %s' % (
              d1, id)
          print(sql)
          generic.update(sql)
          # 提交单据租用下单
          sql = 'insert into stockout_manage_device_lend_stockout' \
              '(customer_id,ifsure,SN,lendid_id,desc,shopid_id,useage,price,quantity,remark,FRUSelect_id,status,customersSignid_id,fru,pn,machinemodel,replace,image,location_id,update_time) ' \
              'select distinct b.customer_id,0,g.SN,b.id,c.desc,d.shop_id,0,d.price,-c.quantity,b.remark,c.device_id,6,b.customersSignid_id,e.name,d.pn,f.name,d.replaces,d.image,1,date() ' \
              'from stockout_manage_device_lend_machineSelects a,stockout_manage_device_lend b,baseinfo_manage_selectorderdetail c,baseinfo_manage_devicestores d,params_manage_device_fru e, params_manage_device_kind f,splitSN g ' \
              'where a.device_lend_id = b.id and c.id=a.selectorderdetail_id and  c.device_id = d.id and d.FRUS_id = e.id and f.id = d.machineModels_id and c.device_id = g.fruSelectid and g.bill = b.id and b.id in %s' % id
          print(sql)
          generic.update(sql)

          # 插入单据流程
          sql = 'insert into report_manage_workflow_query ' \
                '(flowstatus1,name1,pid,FRUSelect_id,FRU,author1,update_time1,flowstatus2) ' \
                'select "租用下单" as status,b.id,a.id,a.FRUSelect_id,a.FRU,b.author,b.update_time,"租用入库" ' \
                'from stockout_manage_device_lend_stockout a,' \
                'stockout_manage_device_lend b ' \
                'where b.id = a.lendid_id and b.id in %s' % id
          generic.update(sql)

          messages.success(self.request, '提交租用下单成功！')
          # 返回 HttpResponse
          return redirect(self.request.get_full_path())

# 提交所选的 租用单出库
class Act_Device_lend_stockout(BaseActionView): # 定义一个动作
    action_name = "device_lend_stockout"  # 相当于这个 Action 的唯一标示, 尽量用比较针对性的名字
    description = "提交所选的 租用单出库"  # 要显示的名字
    icon = 'fa fa-tasks'  # 图标
    model_perm = "change"   # 该动作所需权限

    def do_action(self, queryset):  # 重载do_action()方法
        # queryset 是包含了已经选择的数据的 queryset
        # 生成采购下单明细
        author = self.request.user
        d1 = timezone.now()
        d1 = d1.strftime("%Y-%m-%d %H:%M")
        # queryset.update(pub_date = d1.strftime("%Y-%m-%d"))
        a = ()
        b = ()
        for i in range(0, queryset.count()):
            status = str(queryset.values_list('status')[i]).strip('(,)')
            print(status)
            SN = str(queryset.values_list('SN')[i]).strip('(,)')
            print('SN:' + SN)
            if (status == '6') and (SN != 'None'):
              a = a + queryset.values_list('id')[i]
              b = b + queryset.values_list('lendid_id')[i]
        print(a)
        id = str(a).strip().rstrip(',)')
        id = id + ')'
        print(id)
        lendidid = str(b).strip().rstrip(',)')
        lendidid = lendidid + ')'
        # 状态待出库  才能提交
        if a:
          # SN码不等于空值，更新状态和出库单号
          billid = generic.getOrderMaxNO('ZYDCK')
          sql = 'update stockout_manage_device_lend_stockout set status = 7,billid = "%s",author = "%s"   where replace(sn," ","") <> "" and id in  %s' % (
               billid, author, id)
          print(sql)
          generic.update(sql)

          # 如果入库日期没选，默认系统日期
          sql = 'update stockout_manage_device_lend_stockout set pub_date = "%s",author = "%s"  where pub_date is null and replace(sn," ","") <> "" and id in  %s' % (
              d1, author, id)
          print(sql)
          generic.update(sql)

          # 生成出入库报表数据，单个SN码
          sql = 'insert into report_manage_stock_detail' \
              ' (customer_id,stock_type,bill_type,bill_id,sn, FRU, PN, machineModel, machineSN, price,quantity, useage,source, desc, replace, image,FRUSelect_id, author, remark, location_id,shopid_id,pub_date,update_time) ' \
              'select customer_id,1,4,billid,sn, FRU, PN, machineModel, machineSN, price, -1, useage,source, desc, replace, image, FRUSelect_id, author, remark, location_id,shopid_id,pub_date,date() ' \
              'from stockout_manage_device_lend_stockout where replace(sn," ","") <> "" and  (instr(sn, ",") <= 0  or  sn is null) and id in %s' % id
          print(sql)
          generic.update(sql)

          # 拆分SN码批量入库
          sql = 'select billid,sn,quantity,id ' \
                'from stockout_manage_device_lend_stockout where instr(sn, ",") > 0 and id in %s' % id
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
                          sql = 'insert into stockout_manage_device_lend_stockout' \
                                '(customer_id,ifsure,lendid_id,desc,shopid_id,useage,price,quantity,remark,FRUSelect_id,status,customersSignid_id,fru,pn,machinemodel,replace,image,location_id,update_time) ' \
                                'select customer_id,ifsure,lendid_id,desc,shopid_id,useage,price,%s,remark,FRUSelect_id,6,customersSignid_id,fru,pn,machinemodel,replace,image,location_id,date() from stockout_manage_device_lend_stockout where id = %s' % (
                                -sysl, Fid)
                          print(sql)
                          generic.update(sql)
                          # 更新入库单据信息
                          sql = 'update stockout_manage_device_lend_stockout set quantity =%s,billid = "%s" where id = %s' % (
                          -rksl, billid, Fid)
                          print(sql)
                          generic.update(sql)
              # 生成出入库报表数据，批量SN码
              sql = 'insert into report_manage_stock_detail' \
                    ' (customer_id,stock_type,bill_type,bill_id,sn, FRU, PN, machineModel, machineSN, price,quantity, useage,source, desc, replace, image,FRUSelect_id, author, remark, location_id,shopid_id,pub_date,update_time) ' \
                    'select customer_id,1,4,a.billid, b.sn, a.FRU, a.PN, a.machineModel, a.machineSN, a.price, -1, a.useage, a.source, a.desc, a.replace, a.image, a.FRUSelect_id, a.author, a.remark, a.location_id, a.shopid_id, a.pub_date,date() ' \
                    'from stockout_manage_device_lend_stockout a,splitSN b where instr(a.sn, ",") > 0 and a.billid = b.bill and a.id in %s' % id
              print(sql)
              generic.update(sql)
          else:  # 输入一个SN，拆分单据，插入剩余数量单据
              sql = 'insert into stockout_manage_device_lend_stockout' \
                    '(customer_id,ifsure,lendid_id,desc,shopid_id,useage,price,quantity,remark,FRUSelect_id,status,customersSignid_id,fru,pn,machinemodel,replace,image,location_id,update_time) ' \
                    'select customer_id,ifsure,lendid_id,desc,shopid_id,useage,price,quantity+1,remark,FRUSelect_id,6,customersSignid_id,fru,pn,machinemodel,replace,image,location_id,date() from stockout_manage_device_lend_stockout where -quantity > 1 and  replace(sn," ","") <> "" and id in %s' % id
              print(sql)
              generic.update(sql)
              # 更新单据信息
              sql = 'update stockout_manage_device_lend_stockout set quantity = -1  where replace(sn," ","") <> "" and instr(sn, ",") <= 0  and -quantity >= 1 and id in  %s' % id
              print(sql)
              generic.update(sql)

          # 更新状态
          # sql = 'update stockout_manage_device_lend set status = 7  where id in %s' % lendidid
          # print(sql)
          # generic.update(sql)

          sql = 'select * from stockout_manage_device_lend_stockout where status <> 7 and lendid_id in %s' % lendidid
          print(sql)
          datas = generic.query(sql)
          # 还有未入库的备件
          if datas:
              sql = 'update stockout_manage_device_lend set status = 9  where id in %s' % lendidid
          else:
              sql = 'update stockout_manage_device_lend set status = 7  where id in %s' % lendidid
          print(sql)
          generic.update(sql)

          # 更新单据流程
          sql = 'update report_manage_workflow_query ' \
                'set author2 = "%s",update_time2 = "%s",name2 = "%s" ' \
                'where pid in %s' % (author, d1, billid, id)
          generic.update(sql)

          messages.success(self.request, '提交维修领用出库成功！')
          # 返回 HttpResponse
          return redirect(self.request.get_full_path())

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
    # list_per_page设置每页显示多少条记录，默认是100条
    list_per_page = 5
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
    # list_per_page设置每页显示多少条记录，默认是100条
    list_per_page = 5
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
    # list_per_page设置每页显示多少条记录，默认是100条
    list_per_page = 5
    date_hierarchy = ['pub_date']
    # 列聚合，在list表格下面会增加一行统计的数据，可用的值："count","min","max","avg",  "sum"
    aggregate_fields = {'quantity': 'sum',
                        }

class ChapterInline:
    model = Device_lend_stockout
    extra = 0

# 租用下单
class ContactAdminDevice_lend(object):
    def save_models(self):
        obj = self.new_obj
        flag = self.org_obj is None and 'create' or 'change'
        request = self.request
        obj.author = str(request.user)
        if flag == 'create':  # 新增默认回填操作员
            OrderNO = generic.getOrderMaxNO('ZYD')
            obj.id = OrderNO
            obj.save()
        else:
            obj.save()

    list_display = ('id','status', 'machineSelects',  'date_begin' ,'date_end','customer',
                    'remark',  'author',  'update_time','pub_date')
    exclude = ('id','status', 'customersSignid','update_time')
    # 多选样式
    style_fields = {'machineSelects': 'm2m_transfer', }
    # style_fields = {'machineSelects': 'm2m_dropdown',}
    filter_horizontal = ['machineSelects']
    readonly_fields = ('author',)
    actions = [Act_Device_lend]
    ordering = ('status', '-id')
    # 设置过滤
    list_filter = ('status', 'date_begin','date_end','customer','pub_date')
    # search_fields = ('remark', )
    # list_per_page设置每页显示多少条记录，默认是100条
    list_per_page = 5
    refresh_times = (10, 60)  # 指定列表页的数据定时刷新
    list_display_links = ('id', 'machineSelects', )
    model_icon = 'fa fa-outdent'   # 图标样式
    # 如果想添加数据的同时方便添加关联model：inlines 机制 同一个页面 可以添加 所有的相关信息
    # inlines = [ChapterInline]
    # reversion_enable = True
    # 过滤，只能查看自己下的工单
    def queryset(self):
        # 取出当前Courses表单的所有对象
        qs = super().queryset()
        # 如果不是超级管理员,就对qs进行过滤
        if not self.request.user.is_superuser:
            qs = qs.filter(author=self.request.user)
        return qs

# 租用出库
class ContactAdminDevice_lend_stockout(object):
    def save_models(self):
        obj = self.new_obj
        flag = self.org_obj is None and 'create' or 'change'
        request = self.request
        # obj.author = str(request.user)
        if flag == 'create':  # 新增默认回填操作员
            if obj.quantity > 0 :
                obj.quantity = -obj.quantity
            obj.save()
        else:
            if obj.quantity > 0 :
                obj.quantity = -obj.quantity
            obj.save()
    list_display = ('billid', 'lendid', 'status', 'ifsure', 'customer', 'shopid', 'FRUSelect','quantity', 'SN', 'FRU','PN','desc', 'replace',
                    'location', 'image_data', 'remark', 'pub_date', 'author','update_time')
    list_display_links = ('billid', 'lendid','FRUSelect')
    exclude = ('customersSignid', 'billid','lendid','status', 'FRU','PN','machineModel','machineSN','update_time','price','useage')
    actions = [Act_Device_lend_stockout]
    readonly_fields = ('author',)
    # list_per_page设置每页显示多少条记录，默认是100条
    list_per_page = 5
    refresh_times = (10, 60)  # 指定列表页的数据定时刷新
    # 设置过滤
    list_filter = ('status', 'ifsure','customer', 'shopid','location','pub_date')
    search_fields = ('SN','FRU','PN','machineSN','replace' )
    aggregate_fields = {'quantity': 'sum', }
    ordering = ('status', '-billid','-ifsure','-lendid')
    list_editable = ['SN', 'location']
    model_icon = 'fa fa-outdent'   # 图标样式


# 维修领用下单
class ContactAdminRepair_use(object):
    def save_models(self):
        obj = self.new_obj
        flag = self.org_obj is None and 'create' or 'change'
        request = self.request
        obj.author = str(request.user)
        if flag == 'create':  # 新增默认回填操作员
            OrderNO = generic.getOrderMaxNO('WXLY')
            obj.id = OrderNO
            # id = str(obj.FRUSelect_id)
            # sql = 'select b.name,a.PN,a.machineSN,a.machineModel,a.price,a.image,a.descs,a.replaces,a.source,a.shop_id,a.remark from baseinfo_manage_devicestores a,params_manage_device_fru b  where a.FRUS_id = b.id and a.id = %s' % id
            # cds = generic.query(sql)
            # obj.FRU = cds[0][0]
            # obj.PN = cds[0][1]
            # obj.machineSN = cds[0][2]
            # obj.machineModel = cds[0][3]
            # obj.price = cds[0][4]
            # # obj.image = cds[0][5]
            # obj.desc = cds[0][6]
            # obj.replace = cds[0][7]
            # obj.source = cds[0][8]
            # obj.shopid_id = cds[0][9]
            # if obj.quantity > 0 :
            #     obj.quantity = -obj.quantity
            obj.save()
            # 保存维修领用下单后，自动生成维修领用下单入库信息
            # id = obj.id
            # sql = 'insert into stockout_manage_repair_use_stockout' \
            #       ' (repairid_id, sn, FRU, PN, machineModel,useage, price, quantity, source, image, author, remark, location_id, shopid_id,FRUSelect_id)' \
            #       'select id, sn, FRU, PN, machineModel,useage, price, quantity, source, image, author, remark, 1, shopid_id, FRUSelect_id ' \
            #       'from stockout_manage_repair_use where id="%s"' % id
            # generic.update(sql)
            # print(sql)
            # obj.remark = sql
            # obj.save()
        else:
            # if obj.quantity > 0 :
            #     obj.quantity = -obj.quantity
            obj.save()

    exclude = ('customersSignid','shopid', 'FRUSelect','status', 'quantity', 'desc','id','SN','FRU','PN','replace','price','useage','source','machineSN','machineModel','update_time' )

    list_display = ('id', 'status', 'machineSelects','desc','customer',
                    'image_data','remark', 'author', 'update_time','pub_date')

    actions = [Act_Repair_use]
    ordering = ('status','-id')
    # list_per_page设置每页显示多少条记录，默认是100条
    list_per_page = 5
    # 设置过滤
    list_filter = ('status', 'customer','update_time')
    # search_fields = ('SN', 'FRU', 'PN', 'machineSN', 'replace')
    refresh_times = (10, 60)  # 指定列表页的数据定时刷新
    aggregate_fields = {'quantity': 'sum', }
    # 多选样式
    style_fields = {'machineSelects': 'm2m_transfer', }
    # style_fields = {'machineSelect': 'm2m_dropdown',}
    filter_horizontal = ['machineSelects']
    readonly_fields = ('author',)
    list_display_links = ('id', 'machineSelects')
    model_icon = 'fa fa-outdent'   # 图标样式
    # 过滤，只能查看自己下的工单
    def queryset(self):
        # 取出当前Courses表单的所有对象
        qs = super().queryset()
        # 如果不是超级管理员,就对qs进行过滤
        if not self.request.user.is_superuser:
            qs = qs.filter(author=self.request.user)
        return qs


# 维修领用出库
class ContactAdminRepair_use_stockout(object):
    def save_models(self):
        obj = self.new_obj
        flag = self.org_obj is None and 'create' or 'change'
        request = self.request
        obj.author = str(request.user)
        if flag == 'create':
            if obj.quantity > 0 :
                obj.quantity = -obj.quantity
            obj.save()
        else:
            # OrderNO = generic.getOrderMaxNO('WXLYCK')
            # obj.billid = OrderNO
            if obj.quantity > 0 :
                obj.quantity = -obj.quantity
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

    list_display = ('billid','repairid', 'status','ifsure','customer','shopid','FRUSelect', 'quantity', 'SN', 'FRU','PN','desc', 'replace',
                    'location', 'image_data', 'remark', 'author', 'pub_date','update_time')
    # 添加和修改时那些界面不显示
    exclude = ('customersSignid','status','source','FRU','PN','price','shopid','useage','machineSN','machineModel')
    readonly_fields = ('billid','repairid','author')
    list_display_links = ('billid','repairid','FRUSelect' )
    list_editable = ['SN','location']
    actions = [Act_Repair_use_stockout]
    # list_per_page设置每页显示多少条记录，默认是100条
    list_per_page = 5
    refresh_times = (10, 60)  # 指定列表页的数据定时刷新
    # 设置过滤
    list_filter = ('status', 'ifsure','shopid','customer','location','pub_date')
    search_fields = ('SN', 'FRU', 'PN', 'machineSN', 'replace')
    aggregate_fields = {'quantity': 'sum', }
    ordering = ('status','-billid', '-repairid','-ifsure')
    model_icon = 'fa fa-outdent'  # 图标样式

# Register your models here.

# 设置登陆窗口的标题
xadmin.site.header = 'test'
# 设置页签标题
xadmin.site.title = 'test'

# 注册备件Model类
# xadmin.site.register(Devices, ContactAdminDevices)
# xadmin.site.register(DeviceStore, ContactAdminDeviceStore)
xadmin.site.register(Device_lend, ContactAdminDevice_lend)# 租用下单
xadmin.site.register(Device_lend_stockout, ContactAdminDevice_lend_stockout)# 租用出库
# xadmin.site.register(Device_stockinout_detail, ContactAdminDevice_stockinout_detail)# 备件出入库明细
xadmin.site.register(Repair_use, ContactAdminRepair_use)# 维修领用下单
xadmin.site.register(Repair_use_stockout, ContactAdminRepair_use_stockout)# 维修领用出库

# xadmin.site.register(Devices, ContactAdminInstock)


