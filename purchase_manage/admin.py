# 模块名称：采购管理业务处理模块
# 创建日期：2020-4
# 最后修改日期：2020-6
# 作者：Jason

# from django.contrib import admin
from purchase_manage.models import *
import xadmin
from common import generic
from xadmin.views.base import CommAdminView
from xadmin.plugins.actions import BaseActionView
import time
from xadmin.layout import Fieldset
from django.contrib import messages
from django.shortcuts import redirect
# from notifications.signals import notify
from django.http import HttpResponse
from django.contrib.auth.models import User

# 提交所选的 采购申请
class OrderPost(BaseActionView): # 定义一个动作
    action_name = "order_post"  # 相当于这个 Action 的唯一标示, 尽量用比较针对性的名字
    description = "提交所选的 采购申请"  # 要显示的名字
    icon = 'fa fa-tasks'  # 图标
    model_perm = "change"   # 该动作所需权限
    # 生成邮件内容
    def queryContent(self,id):
        sql = 'select b.id,f.name,g.name||" / "||h.name,e.name,d.pn,c.quantity,c.desc,b.author ' \
        'from purchase_manage_purchase_order_machineSelects a,purchase_manage_purchase_order b,baseinfo_manage_selectorderdetail c,' \
        'baseinfo_manage_devicestores d,params_manage_device_fru e,params_manage_device_kind f,baseinfo_manage_shop g,params_manage_base_brand h ' \
        'where a.purchase_order_id = b.id and c.id=a.selectorderdetail_id and  c.device_id = d.id and d.FRUS_id = e.id and h.id=g.shop_brand_id ' \
        'and d.machineModels_id = f.id and c.shopid_id =g.id and b.id= "' + id + '"'
        print(sql)
        cds = generic.query(sql)
        content = ''
        if cds:
          for i in range(0,len(cds)):
            content = content + '\n' + '采购单号：' + cds[i][0] + '，'
            if (cds[i][1] != '') and (cds[i][1] is not None):
               content = content + ', 整机型号：' +  cds[i][1] + '，'
            content = content + ', 备件类别：' + cds[i][2] + '，'
            if (cds[i][3] != '') and (cds[i][3] is not None):
               content = content + ', FRU：' +  cds[i][3] + '，'
            if (cds[i][4] != '') and (cds[i][4] is not None):
               content = content + ', PN：' + cds[i][4] + '，'
            content = content + ', 数量：' + str(cds[i][5]) + '，'
            if (cds[i][6] != '') and (cds[i][6] is not None):
               content = content + ', 描述：' + cds[i][6] + '，'
            if (cds[i][7] != '') and (cds[i][7] is not None):
                content = content + ', 申请人：' + cds[i][7]
            print(content)
        return content

    def do_action(self, queryset):  # 重载do_action()方法
        # queryset 是包含了已经选择的数据的 queryset
        # 生成采购下单明细
        a = ()
        contents = ''
        d1 = timezone.now()
        request = self.request
        author = str(request.user)
        for i in range(0, queryset.count()):
            status = str(queryset.values_list('status')[i]).strip('(,)')
            # 状态待提交 才能提交
            if status == '0':
              # 备件没选，不能下单
              parts = str(queryset.values_list('machineSelects')[i]).strip('(,)')
              print(parts)
              if parts != 'None':
                a =  a + queryset.values_list('id')[i]
                ids = queryset.values_list('id')[i]
                print(ids)
                id = ids[0]
                id =  str(id)
                print(id)
                contents = contents + self.queryContent(id)
              # contents = contents + queryset.values_list('id')[i] + queryset.values_list('machineSelects')[i]
        print(a)
        id = '("' + '","'.join(a) + '")'
        print(id)
        # 状态待提交 才能提交
        if a:
          # 更新申请状态
          sql = 'update  purchase_manage_purchase_order set status = 1,update_time = "%s",author = "%s"   where id in  %s' % (d1,author,id)
          print(sql)
          generic.update(sql)
          # 提交采购下单
          sql = 'insert into purchase_manage_purchase_order_detail' \
              '(customer_id,status,bill_id_id,desc,shopid_id,useage,price,quantity,remark,FRUSelect_id,ifmachine,status,suppliersid_id,fru,pn,machinemodel,replace,image,arrive_date,pub_date) ' \
              'select b.customer_id,2,b.id,c.desc,d.shop_id,0,d.price,c.quantity,b.remark,c.device_id,d.ifmachine,0,1,e.name,d.pn,f.name,d.replaces,d.image,date(),date() ' \
              'from purchase_manage_purchase_order_machineSelects a,purchase_manage_purchase_order b,baseinfo_manage_selectorderdetail c,baseinfo_manage_devicestores d,params_manage_device_fru e,params_manage_device_kind f ' \
              'where a.purchase_order_id = b.id and c.id=a.selectorderdetail_id and  c.device_id = d.id and d.FRUS_id = e.id and d.machineModels_id = f.id and b.id in %s' % id
          print(sql)
          generic.update(sql)
          # 插入单据流程
          sql = 'insert into report_manage_workflow_query ' \
                '(flowstatus1,name1,FRUSelect_id,FRU,author1,update_time1,flowstatus2,name2) ' \
                'select "采购申请" as status,a.id,c.device_id,e.name,a.author,a.update_time,"采购下单",a.id ' \
                'from purchase_manage_purchase_order a,' \
                'purchase_manage_purchase_order_machineSelects b,' \
                'baseinfo_manage_selectorderdetail c,baseinfo_manage_devicestores d,params_manage_device_fru e ' \
                'where b.selectorderdetail_id = c.id and c.device_id = d.id and d.FRUS_id = e.id ' \
                'and a.id = b.purchase_order_id and a.id in %s' % id
          generic.update(sql)
          # 邮件通知
          id = id.strip('()')
          id = id.replace('"','')
          title = '采购单号：' + id + ' 已经采购申请下单，请尽快处理！'
          receiver_list = []
          cds = generic.getmaillist('采购下单')
          if cds:
             for i in range (0,len(cds)):
               mail =  cds[i][1]
               receiver_list.append(mail)
          receiver_lists = tuple(receiver_list)
          print(receiver_lists)
          generic.send_mail(title,contents,receiver_lists)
          messages.success(self.request, '提交采购申请成功！')
          # 返回 HttpResponse
          return redirect(self.request.get_full_path())

# 提交所选的 采购下单
class OrderStockIn(BaseActionView): # 定义一个动作
    action_name = "order_stockin"  # 相当于这个 Action 的唯一标示, 尽量用比较针对性的名字
    description = "提交所选的 采购下单"  # 要显示的名字
    icon = 'fa fa-tasks'  # 图标
    model_perm = "change"   # 该动作所需权限

    def do_action(self, queryset):  # 重载do_action()方法
        # queryset 是包含了已经选择的数据的 queryset
        # 生成采购下单明细
        request = self.request
        author = str(request.user)
        d1 = timezone.now()
        print(d1)
        a = ()
        billids = ()
        fruselect = ()
        for i in range(0, queryset.count()):
            status = str(queryset.values_list('status')[i]).strip('(,)')
            if status == '2':
              a = a + queryset.values_list('id')[i]
              billids = billids + queryset.values_list('bill_id_id')[i]
              fruselect = fruselect + queryset.values_list('FRUSelect_id')[i]
              # 更新单据流程状态
              pid = queryset.values_list('id')[i]
              pid = str(pid).strip().rstrip(',)')
              pid = pid.strip('()')
              bid = queryset.values_list('bill_id_id')[i]
              bid = str(bid).strip().rstrip(',)')
              bid = bid + ')'
              fruid = queryset.values_list('FRUSelect_id')[i]
              fruid = str(fruid).strip().rstrip(',)')
              fruid = fruid + ')'
              sql = 'update report_manage_workflow_query ' \
                    'set author2 = "%s",update_time2 = "%s",pid = %s,flowstatus3 = "采购入库" ' \
                    'where name1 in %s and FRUSelect_id in %s' % (author, d1, pid, bid, fruid)
              generic.update(sql)
        print(a)
        id = str(a).strip().rstrip(',)')
        id = id + ')'
        print(id)
        billids = str(billids).strip().rstrip(',)')
        billids = billids + ')'
        print(billids)
        fruselect = str(fruselect).strip().rstrip(',)')
        fruselect = fruselect + ')'
        print(fruselect)
        # 状态待下单  才能提交
        if a:
          # 更新下单状态
          sql = 'update purchase_manage_purchase_order_detail set status = 3,update_time = "%s",author = "%s" where id in  %s' %(d1,author,id)
          print(sql)
          generic.update(sql)
          # 提交单据采购入库
          sql = 'insert into purchase_manage_purchase_stockin_detail ' \
              '(customer_id,ifsure,status,desc,source,price,quantity,useage,image,remark,shopid_id,FRUSelect_id,location_id,purchase_id_id,fru,pn,machinemodel,replace,update_time) ' \
              'select customer_id,0,4,desc,source,price,quantity,0,image,remark,shopid_id,FRUSelect_id,1,id,fru,pn,machinemodel,replace,date() ' \
              'from purchase_manage_purchase_order_detail where id in %s' % id
          print(sql)
          generic.update(sql)
          # 更新单据状态
          billid = ()
          machinemodel = ()
          fru = ()
          contents = ''
          # 记录下单信息和邮件发送内容
          for i in range(0, queryset.count()):
             billid = queryset.values_list('bill_id_id')[i]
             billid = str(billid).strip().rstrip(',)') + ')'
             machinemodel = queryset.values_list('machineModel')[i]
             machinemodel = str(machinemodel).strip().rstrip(',)') + ')'
             fru = queryset.values_list('FRU')[i]
             fru = str(fru).strip().rstrip(',)') + ')'
             fru = str(fru).replace("'","")
             arrivedate = queryset.values_list('arrive_date')[i]
             arrivedate = str(arrivedate).strip().rstrip(',)') + ')'
             arrivedate = arrivedate[14: ]
             arrivedate = str(arrivedate).replace(",","-")
             ids = str(billid)
             print(ids)
             print(str(machinemodel))
             print(str(fru))
             d1 = timezone.now()
             d1 = d1.strftime("%Y-%m-%d %H:%M")
             remark = '\n采购下单时间：' + d1 + '，   FRU: '+ str(fru) + '，  估计到货时间：' + arrivedate
             sql = 'update purchase_manage_purchase_order set status = 3,remark = remark || "%s"  where id in %s' % (remark,ids)
             print(sql)
             contents = contents + '\n' + '采购单号：' + str(ids).strip('()').replace('"','') + ', 采购下单时间：' + d1 + ', FRU: ' + str(
                 fru.strip('()')) + ', 估计到货时间：' + arrivedate.strip('()')
             generic.update(sql)

          # 邮件通知
          billids = billids.strip('()')
          billids = str(billids).replace('"','')
          title = '采购单号：' + billids + ' 已经采购下单！'
          receiver_list = []
          cds = generic.getmaillist('采购单')
          if cds:
              for i in range(0, len(cds)):
                  mail = cds[i][1]
                  receiver_list.append(mail)
          receiver_lists = tuple(receiver_list)
          print(receiver_lists)
          generic.send_mail(title, contents, receiver_lists)
          messages.success(self.request, '提交采购下单成功！')
          # 返回 HttpResponse
          return redirect(self.request.get_full_path())

# 提交所选的 批量入库
class BatchStockIn(BaseActionView): # 定义一个动作
    action_name = "batch_stockin"  # 相当于这个 Action 的唯一标示, 尽量用比较针对性的名字
    description = "提交所选的 采购入库"  # 要显示的名字
    icon = 'fa fa-tasks'  # 图标
    model_perm = "change"   # 该动作所需权限

    def do_action(self, queryset):  # 重载do_action()方法
        # queryset 是包含了已经选择的数据的 queryset
        # 生成采购下单明细
        d1 = timezone.now()
        request = self.request
        author = str(request.user)
        a = ()
        pid = ()
        for i in range(0, queryset.count()):
            status = str(queryset.values_list('status')[i]).strip('(,)')
            SN = str(queryset.values_list('SN')[i]).strip('(,)')
            print('SN:' + SN)
            if (status == '4') and (SN != 'None'):
              a = a + queryset.values_list('id')[i]
              pid = pid + queryset.values_list('purchase_id_id')[i]
        print(a)
        id = str(a).strip().rstrip(',)')
        id = id + ')'
        print(id)

        pid = str(pid).strip().rstrip(',)')
        pid = pid + ')'
        print(pid)

        # 入库状态待入库  才能提交
        if a:
          # 更新状态
          billid = generic.getOrderMaxNO('CGRK')
          rkdh = billid
          sql = 'update purchase_manage_purchase_stockin_detail set status = 5,bill_id = "%s",author = "%s"  where replace(sn," ","") <> "" and id in  %s' % (billid, author,id)
          print(sql)
          generic.update(sql)
          # 生成出入库报表数据
          sql = 'insert into report_manage_stock_detail' \
              ' (customer_id,stock_type,bill_type,bill_id,sn, FRU, PN, price,quantity, useage,source, image,FRUSelect_id, author, remark, location_id,pub_date,fru,pn,machinemodel,replace,shopid_id,update_time) ' \
              'select customer_id,0,0,bill_id,sn, FRU, PN, price, 1, useage,source, image, FRUSelect_id, author, remark, location_id,pub_date,fru,pn,machinemodel,replace,shopid_id,date() ' \
              'from purchase_manage_purchase_stockin_detail where (instr(sn, ",") <= 0 or sn is null) and id in %s' % id
          print(sql)
          generic.update(sql)
          # 拆分SN码批量入库
          sql = 'select bill_id,sn,quantity,id  ' \
                'from purchase_manage_purchase_stockin_detail where instr(sn, ",") > 0 and id in %s' % id
          print(sql)
          cds = generic.query(sql)
          rksl = 0  # 拆分剩余数量的回收入库单
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
                    sql = 'insert into purchase_manage_purchase_stockin_detail ' \
                          '(customer_id,ifsure,status,desc,source,price,quantity,useage,image,remark,shopid_id,FRUSelect_id,location_id,purchase_id_id,fru,pn,machinemodel,replace,update_time) ' \
                          'select customer_id,ifsure,4,desc,source,price,%s,useage,image,remark,shopid_id,FRUSelect_id,location_id,purchase_id_id,fru,pn,machinemodel,replace,date() ' \
                          'from purchase_manage_purchase_stockin_detail where id = %s' % (sysl, Fid)
                    print(sql)
                    generic.update(sql)
                    print(billid)
                    sql = 'update purchase_manage_purchase_stockin_detail set quantity =%s,billid = "%s" where id = %s' % (rksl, billid, Fid)
                    print(sql)
                    generic.update(sql)

             sql = 'insert into report_manage_stock_detail ' \
                   '(customer_id,stock_type,bill_type,bill_id,sn, FRU, PN, price,quantity, useage,source, image,FRUSelect_id, author, remark, location_id,pub_date,fru,pn,machinemodel,replace,shopid_id,update_time) ' \
                   'select a.customer_id,0,0,a.bill_id,b.sn, a.FRU, a.PN, a.price, 1, a.useage,a.source, a.image, a.FRUSelect_id, a.author, a.remark, a.location_id,a.pub_date,a.fru,a.pn,a.machinemodel,a.replace,a.shopid_id,date() ' \
                   'from purchase_manage_purchase_stockin_detail a,splitSN b where instr(a.sn, ",") > 0  and a.bill_id = b.bill and a.id in %s' % id
             print(sql)
             generic.update(sql)
          else:  # 输入一个SN
              sql = 'insert into purchase_manage_purchase_stockin_detail' \
                    '(customer_id,ifsure,status,desc,source,price,quantity,useage,image,remark,shopid_id,FRUSelect_id,location_id,purchase_id_id,fru,pn,machinemodel,replace,update_time) ' \
                    'select customer_id,ifsure,4,desc,source,price,quantity-1,useage,image,remark,shopid_id,FRUSelect_id,location_id,purchase_id_id,fru,pn,machinemodel,replace,date() ' \
                    'from purchase_manage_purchase_stockin_detail where quantity > 1 and id in %s' % id
              print(sql)
              generic.update(sql)
              # 更新单据信息
              sql = 'update purchase_manage_purchase_stockin_detail set quantity = 1  where replace(sn," ","") <> "" and instr(sn, ",") <= 0  and quantity >= 1 and id in  %s' % id
              print(sql)
              generic.update(sql)

          # 更新单据流程
          sql = 'update report_manage_workflow_query ' \
                'set author3 = "%s",update_time3 = "%s",name3 = "%s" ' \
                'where pid in %s' % (author, d1, rkdh, pid)
          generic.update(sql)

          # 更新单据状态和记录入库信息
          billid = ()
          machinemodel = ()
          fru = ()
          quantity = ()
          contents = ''
          for i in range(0, queryset.count()):
            billid = queryset.values_list('purchase_id_id')[i]
            billid = str(billid).strip().rstrip(',)') + ')'
            machinemodel = queryset.values_list('machineModel')[i]
            machinemodel = str(machinemodel).strip().rstrip(',)') + ')'
            fru = queryset.values_list('FRU')[i]
            fru = str(fru).strip().rstrip(',)') + ')'
            quantity = str(queryset.values_list('quantity')[i]).strip('()').rstrip(',')
            id = str(billid)
            print(id)
            print(str(machinemodel))
            print(str(fru))
            d1 = timezone.now()
            d1 = d1.strftime("%Y-%m-%d %H:%M")
            remark = '\n采购入库时间：' + d1 + '，   FRU: '+ str(fru)

            sql = 'update purchase_manage_purchase_order_detail set status = 5 where id in %s' % billid
            print(sql)
            generic.update(sql)

            sql = 'select bill_id_id from purchase_manage_purchase_order_detail where id in %s' % id
            datas = generic.query(sql)
            print(sql)
            purchases = []
            if datas:
              bid = datas[0][0]
              print(bid)
              purchases.append(bid)
              sql = 'select * from purchase_manage_purchase_order_detail where status <> 5 and bill_id_id = "%s"' % bid
              print(sql)
              datas = generic.query(sql)
              # 还有未入库的备件
              if datas:
                  sql = 'update purchase_manage_purchase_order set status = 8,remark = remark || "%s"  where id = "%s"' % (remark, bid)
              else: # 全部入库
                  sql = 'update purchase_manage_purchase_order set status = 5,remark = remark || "%s"  where id = "%s"' % (remark, bid)

              print(sql)
              generic.update(sql)

              contents = contents + '\n' + '采购单号：' + id.strip('()') + ', 采购入库时间：' + d1 + ', FRU: '+ str(fru).strip('()').replace('"','')\
                         + '， 入库数量：' + quantity

          # 邮件通知
          purchases = list(set(purchases))
          title = '采购单号：' + str(tuple(purchases)).strip('()').strip(',') + ' 已经采购入库！'
          receiver_list = []
          cds = generic.getmaillist('采购单')
          if cds:
            for i in range(0, len(cds)):
               mail = cds[i][1]
               receiver_list.append(mail)
          receiver_lists = tuple(receiver_list)
          print(receiver_lists)
          generic.send_mail(title, contents, receiver_lists)
          messages.success(self.request, '提交采购入库成功！')
          # 返回 HttpResponse
          return redirect(self.request.get_full_path())

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

#采购申请
class ContactAdminPurchase_order(object):
    def save_models(self):
        obj = self.new_obj
        flag = self.org_obj is None and 'create' or 'change'
        request = self.request
        obj.author = str(request.user)
        if flag == 'create':  # 新增默认回填操作员
            OrderNO = generic.getOrderMaxNO('CGD')
            obj.id =  OrderNO
            obj.save()
            # 插入单据流程
            # sql = 'insert into report_manage_workflow_query ' \
            #       '(flowstatus1,name1,FRU,author1,update_time1) ' \
            #       'select "采购申请" as status,a.id,d.FRU,a.author,a.update_time ' \
            #       'from purchase_manage_purchase_order a,' \
            #       'purchase_manage_purchase_order_machineSelects b,' \
            #       'baseinfo_manage_selectorderdetail c,baseinfo_manage_devicestores d ' \
            #       'where b.selectorderdetail_id = c.id and c.device_id = d.id ' \
            #       'and a.id = b.purchase_order_id and a.id = "%s"' %obj.id
            # sql = 'insert into report_manage_workflow_query ' \
            #       '(flowstatus1,name1,author1) ' \
            #       'select "采购申请" as flowstatus1,a.id,a.author ' \
            #       'from purchase_manage_purchase_order a,purchase_manage_purchase_order_machineSelects b  ' \
            #       'where a.id = b.purchase_order_id and a.id = "%s"' %obj.id
            # generic.update(sql)

        else:
            # 更新采购总数
            obj.save()
            # id = obj.id
            # sql = 'select sum(quantity) from baseinfo_manage_selectorderdetail where id in (select selectorderdetail_id from purchase_manage_purchase_order_machineSelects ' \
            #       'where purchase_order_id = "%s")' % id
            # cds = generic.query(sql)
            # print(sql)
            # print(str(cds[0][0]))
            # print(cds)
            # if (cds and cds != None) :
            #     obj.quantity = cds[0][0]
            # else:
            #     obj.quantity = 0
            # obj.save()

    # 后台自定义不是下拉选择框，而是搜索框
    # 下拉式可选，在外键对应的字段的adminx.py
    relfield_style = 'fk-ajax'
    list_display = ('id','status','arrive_date','purchasedesc','machineSelects','customer','short_content','author','update_time','pub_date')
    model_icon = 'fa fa-exchange'  # 图标样式
    # 添加和修改时那些界面不显示
    exclude = ('id','status','shopid','desc','ifimportant','purchase_type','customersSignid',
               'machineSelect','price','amount','quantity','suppliersid','update_time')
    readonly_fields = ('author',)
    # ordering设置默认排序字段，负号表示降序排序
    ordering = ['status','-id', ]
    # search_fields = ('purchasedesc')
    add_form_template = 'PurchaseOrder_form.html'
    change_form_template = 'PurchaseOrder_form.html'
    # 设置过滤
    list_filter = ('status','shopid','customer','arrive_date','update_time')
    # 多选样式
    style_fields = {'machineSelects': 'm2m_transfer',}
    # style_fields = {'machineSelect': 'm2m_dropdown',}
    filter_horizontal = ['machineSelects']
    actions = [OrderPost]
    # list_editable 设置默认可编辑字段,第一个字段不允许编辑
    list_editable = ('purchasedesc', 'arrive_date', 'customer')
    # list_per_page设置每页显示多少条记录，默认是100条
    list_per_page = 5
    refresh_times = (10, 60)  # 指定列表页的数据定时刷新
    show_detail_fileds = ('short_content')
    list_display_links = ('id', 'machineSelects', 'short_content')
    # 过滤，只能查看自己下的工单
    def queryset(self):
        # 取出当前Courses表单的所有对象
        qs = super().queryset()
        # 如果不是超级管理员,就对qs进行过滤
        if not self.request.user.is_superuser:
            qs = qs.filter(author=self.request.user)
        return qs

#采购下单
class ContactAdminPurchase_order_detail(object):
    def save_models(self):
        obj = self.new_obj
        flag = self.org_obj is None and 'create' or 'change'
        request = self.request
        # obj.author = str(request.user)
        # 新增默认回填备件库数据
        if flag == 'create':
            # id = str(obj.FRUSelect_id)
            # sql = 'select FRU,PN,machineSN,machineModel,price,image,descs,replaces,source,remark from baseinfo_manage_devicestores where id = %s' % id
            # cds = generic.query(sql)
            # obj.FRU = cds[0][0]
            # obj.PN = cds[0][1]
            # obj.machineSN = cds[0][2]
            # obj.machineModel = cds[0][3]
            # # obj.price = cds[0][4]
            # obj.image = cds[0][5]
            # obj.desc = cds[0][6]
            # obj.replace = cds[0][7]
            # obj.source = cds[0][8]
            # obj.remark = cds[0][9]
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
    list_display = ('bill_id','status','FRUSelect','desc','quantity','price','source','customer',
                    'image_data','arrive_date','suppliersid','remark','author','update_time','pub_date')
    model_icon = 'fa fa-exchange'  # 图标样式
    # 添加和修改时那些界面不显示
    exclude = ('machineSelect','machineSelects','useage','shopid','replace','ifmachine',
               'status','FRU','SN','PN','machineSN','machineModel','update_time')
    # 多选样式
    # style_fields = {'machineSelect': 'm2m_transfer', 'machineSelects': 'm2m_transfer'}
    readonly_fields = ('author', )
    # ordering = ['-id', ]
    actions = [OrderStockIn]
    ordering = ['status','-bill_id' ]
    # 设置过滤
    list_filter = ('status', 'customer','suppliersid','arrive_date','update_time')
    # search_fields = ('desc')
    # list_per_page设置每页显示多少条记录，默认是100条
    list_per_page = 5
    refresh_times  = (10, 60)  # 指定列表页的数据定时刷新
    aggregate_fields = {'quantity': 'sum', }
    list_display_links = ('bill_id', 'FRUSelect',)
    list_editable = ('desc', 'quantity', 'price', 'source','arrive_date','suppliersid')
    # def formfield_for_dbfield(self, db_field, **kwargs):
    #     if not self.request.user.is_superuser:
    #         if db_field.name == "site":
    #             kwargs["queryset"] = Site.objects.filter(area_company=Group.objects.get(user=self.request.user))
    #     return super(DeviceAdmin, self).formfield_for_dbfield(db_field, **kwargs)


    # def formfield_for_dbfield(self, db_field, **kwargs):
    #     print('外键下拉框添加过滤')
    #     if not self.request.user.is_superuser:
    #         print('外键下拉框添加过滤')
    #         if db_field.name == "shopid_id":
    #             kwargs["queryset"] = DeviceStores.objects.filter(shop='1')
    #     return super(ContactAdminPurchase_order_detail, self).formfield_for_dbfield(db_field, **kwargs)

    def get_queryset(self, request):
        return DeviceStores.objects.filter(shop_id=Purchase_order_detail.shopid)

    # def get_readonly_fields(self, request, obj=None):
    #     fields = []
    #     if request.user.is_superuser:
    #         return fields
    #     else:
    #         fields = ['boss_verified', 'deliver_during']
    #         return fields
    #
    # def get_readonly_fields(self, request, obj=None):
    #     # objs = object
    #     print(obj)
    #     if obj :
    #         request.readonly_fields = ['bill_id']
    #     else:
    #         request.readonly_fields = []
    #     return request.readonly_fields

    # def get_readonly_fields(self, obj=None):
    #     if self.user.is_superuser:
    #         self.readonly_fields = []
    #     else:
    #         self.readonly_fields = ['bill_id']
    #     return self.readonly_fields

    # form_layout = (
    #     Fieldset(None,
    #              'pc_name', 'pc_icorn', 'pc_link', 'sort'
    #              ),
    #     Fieldset(None,
    #              'pc_id', 'pc_parent', **{"style": "display:None"}  # 隐藏前面两个字段
    #              ),
    # )

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
            OrderNO = generic.getOrderMaxNO('CGRKSQ')
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
            # sql = 'insert into purchase_manage_purchase_stockin_detail' \
            #       ' (purchase_id_id, sn, FRU, PN, machineModel,machineSN,useage, price, quantity, source, image, author, remark, location_id, shopid_id,FRUSelect_id)' \
            #       'select id, sn, FRU, PN, machineModel,machineSN,useage, price, quantity, source, image, author, remark, 1, shopid_id, FRUSelect_id ' \
            #       'from purchase_manage_purchase_order_detail where bill_id_id="%s"' % id
            sql = 'insert into purchase_manage_purchase_stockin_detail' \
                  ' (purchase_id_id, FRU, PN, machineModel,machineSN,useage, price, quantity, source, image, author, remark, location_id, shopid_id,FRUSelect_id,pub_date) ' \
                  'select a.id, c.FRU, c.PN, c.machineModel,c.machineSN,a.useage, a.price, 1, a.source, a.image, a.author, a.remark, 1, c.shop_id, c.id, "1919-01-01" ' \
                  'from purchase_manage_purchase_order_detail a,purchase_manage_purchase_order_detail_machineSelect b, baseinfo_manage_devicestores c ' \
                  'where  a.id = b.purchase_order_detail_id and b.devicestores_id = c.id and a.bill_id_id="%s"' % id
            generic.update(sql)
            print(sql)
            # obj.remark = sql
            # obj.save()
        else:
            obj.save()
    list_display = ('id','purchase_id','shopid','quantity','price','arrive_date','suppliersid','remark','author','update_time')
    model_icon = 'fa fa-exchange'  # 图标样式
    readonly_fields = ('id', 'price','quantity','author',)
    # 添加和修改时那些界面不显示
    # exclude = ('author',)
    # list_editable 设置默认可编辑字段,第一个字段不允许编辑
    list_editable = ['location', 'SN','machineSN']
    ordering = ['status', '-purchase_id']
    # list_per_page设置每页显示多少条记录，默认是100条
    list_per_page = 5
    refresh_times = (10, 60)  # 指定列表页的数据定时刷新
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
        # obj.author = str(request.user)
        if flag == 'create':  # 新增默认回填操作员
            obj.save()
        else:
          # if (obj.bill_id is None) or (obj.bill_id == ''):
          #   OrderNO = generic.getOrderMaxNO('CGRK')
          #   print(OrderNO)
          #   obj.bill_id = OrderNO
          #   obj.status = 5
          #   # obj.remark = 'test'
          #   obj.save()
          #   # 更新库存数量
          #   if (obj.quantity > 0) and (obj.bill_id):
          #       print(obj.machineModel)
          #       if (obj.machineModel and obj.machineModel.strip() != ''):
          #         sql = "UPDATE baseinfo_manage_devicestores SET quantity = quantity + %s where machineModel = %s and (FRU = %s or PN = %s) "
          #         params = [obj.quantity, obj.machineModel, obj.FRU, obj.PN]
          #       else:
          #         sql = "UPDATE baseinfo_manage_devicestores SET quantity = quantity + %s where FRU = %s or PN = %s"
          #         params = [obj.quantity, obj.FRU, obj.PN]
          #       print(params)
          #       print(sql)
          #       generic.update(sql, params)
            # 拆分采购入库单
            # 获取采购单号中采购数量
            # id = obj.purchase_id_id
            # sql1 = 'select quantity from purchase_manage_purchase_order_detail where id= "%s"' % id
            # cds1 = generic.query(sql1)
            # FRUSelectID = obj.FRUSelect_id
            # Fpurchase_id = obj.purchase_id_id
            # sql2 = 'select sum(quantity) from purchase_manage_purchase_stockin_detail where (FRUSelect_id = "%s" and purchase_id_id =  "%s")' % (FRUSelectID,Fpurchase_id)
            # print(sql1)
            # print(sql2)
            # # obj.remark = sql1 + '  ，  ' + sql2
            # # obj.save()
            # cds2 = generic.query(sql2)
            # quantity = 0
            # status = 5
            # if cds1 and cds2:
            #    quantity1 = cds1[0][0]
            #    quantity2 = cds2[0][0]
            #    quantity = quantity1 - quantity2 # 剩余数量
            # if  quantity > 0:
            #    status = 8
            #    purchase_stockin = Purchase_stockin_detail()
            #    purchase_stockin.purchase_id_id = obj.purchase_id_id
            #    purchase_stockin.status = 4
            #    purchase_stockin.FRU = obj.FRU
            #    purchase_stockin.PN = obj.PN
            #    purchase_stockin.price = obj.price
            #    purchase_stockin.quantity = quantity
            #    purchase_stockin.useage = 1
            #    purchase_stockin.source = obj.source
            #    purchase_stockin.image = obj.image
            #    purchase_stockin.author = obj.author
            #    purchase_stockin.location_id = 1
            #    purchase_stockin.shopid_id = obj.shopid_id
            #    purchase_stockin.FRUSelect_id = obj.FRUSelect_id
            #    purchase_stockin.save()
            # 插入出入库报表数据
            # id = obj.id
            # sql = 'insert into report_manage_stock_detail' \
            #          ' (stock_type,bill_type,bill_id,sn,FRU,PN,price,quantity,useage,source,desc,image,FRUSelect_id,author,remark,location_id,pub_date,fru,pn,machinemodel,replace,shopid_id) ' \
            #          'select 0,0,bill_id,sn,FRU,PN,price,1,useage,source,desc,image,FRUSelect_id,author,remark,location_id,pub_date,fru,pn,machinemodel,replace,shopid_id ' \
            #          'from purchase_manage_purchase_stockin_detail where (instr(sn, ",") <= 0 or sn is null) and id = "%s"' % id
            # print(sql)
            # generic.update(sql)
            # # 拆分SN码批量入库
            # sql = 'select bill_id,sn ' \
            #       'from purchase_manage_purchase_stockin_detail where instr(sn, ",") > 0 and id = %s' % id
            # print(sql)
            # cds = generic.query(sql)
            # if cds:
            #     for i in range(0, len(cds)):
            #         billids = cds[i][0]
            #         sn = cds[i][1]
            #         strlist = sn.split(',')  # 用逗号分割sn字符串，并保存到列表
            #         for value in strlist:  # 循环输出列表值
            #             sql = 'insert into splitSN (bill,SN) ' \
            #                   'VALUES ("%s","%s") ' % (billids, value)
            #             print(sql)
            #             generic.update(sql)
            #     sql = 'insert into report_manage_stock_detail ' \
            #           '(stock_type,bill_type,bill_id,sn, FRU, PN, price,quantity, useage,source, image,FRUSelect_id, author, remark, location_id,pub_date,fru,pn,machinemodel,replace,shopid_id) ' \
            #           'select 0,0,a.bill_id,b.sn, a.FRU, a.PN, a.price, 1, a.useage,a.source, a.image, a.FRUSelect_id, a.author, a.remark, a.location_id,a.pub_date,a.fru,a.pn,a.machinemodel,a.replace,a.shopid_id ' \
            #           'from purchase_manage_purchase_stockin_detail a,splitSN b where instr(a.sn, ",") > 0  and a.bill_id = b.bill and a.id = %s' % id
            #     print(sql)
            #     generic.update(sql)
            # 更新单据追踪信息
            # sql = 'update purchase_manage_purchase_order_detail set status = %s where id = "%s"' % (
            # status, obj.purchase_id_id)
            # print(sql)
            # generic.update(sql)
            # d1 = timezone.now()
            # d1 = d1.strftime("%Y-%m-%d %H:%M")
            # remark = '\n采购入库时间：' + d1 + '   FRU: ' + str(obj.FRU)  + ' 入库数量：' + str(obj.quantity)
            # sql = 'select bill_id_id from purchase_manage_purchase_order_detail where id = %s' % obj.purchase_id_id
            # datas = generic.query(sql)
            # print(sql)
            # if datas:
            #     id = datas[0][0]
            #     print(id)
            #     # sql = 'update purchase_manage_purchase_order set status = %s,remark = remark || "%s"  where id = "%s"' % (status,remark, id)
            #     # print(sql)
            #     # generic.update(sql)
            #     sql = 'select * from purchase_manage_purchase_order_detail where status <> 5 and bill_id_id = "%s"' % id
            #     print(sql)
            #     datas = generic.query(sql)
            #     # 还有未入库的备件
            #     if datas:
            #         sql = 'update purchase_manage_purchase_order set status = 8,remark = remark || "%s"  where id = "%s"' % (
            #         remark, id)
            #     else:
            #         sql = 'update purchase_manage_purchase_order set status = 5,remark = remark || "%s"  where id = "%s"' % (
            #         remark, id)
            #     print(sql)
            #     generic.update(sql)
            # # 邮件通知
            # title = '采购单号：' + str(id) + ' 已经采购入库！'
            # # contents =  '采购单号：' + id + ' 已经采购申请下单，请尽快处理！'
            # receiver_list = []
            # contents = '采购单号：' + str(id) + '，采购入库时间：' + d1 + '，FRU: ' + str(obj.FRU)  + '，入库数量：' + str(obj.quantity)
            # cds = generic.getmaillist('采购单')
            # if cds:
            #     for i in range(0, len(cds)):
            #         mail = cds[i][1]
            #         receiver_list.append(mail)
            # receiver_lists = tuple(receiver_list)
            # print(receiver_list)
            # generic.send_mail(title, contents, receiver_list)

          obj.save()

    list_display = ('bill_id','purchase_id','status','ifsure','customer','shopid','FRUSelect','SN','quantity','desc','source', 'price',
                   'location','image_data','remark','author','pub_date','update_time')
    model_icon = 'fa fa-exchange'  # 图标样式
    # 添加和修改时那些界面不显示
    exclude = ('FRU','PN','status','machineModel','machineSN','useage','replace')
    search_fields = ('FRU', 'SN','PN','replace')
    free_query_filter = ['FRU', 'SN', 'PN']
    # list_editable = ['location', ]
    list_filter = ('status','ifsure','customer','shopid','location','pub_date')
    # show_detail_fields = ['bill_id', 'purchase_id']  # 在指定的字段后添加一个显示数据详情的一个按钮
    list_display_links = ('bill_id', 'purchase_id', 'FRUSelect')
    date_hierarchy = ['pub_date']
    readonly_fields = ('bill_id', 'author',)
    actions = [BatchStockIn]
    # ordering = ['-status', '-bill_id']
    # list_editable 设置默认可编辑字段,第一个字段不允许编辑
    list_editable = ['location', 'machineSN']
    # list_per_page设置每页显示多少条记录，默认是100条
    list_per_page = 5
    refresh_times = (10, 60)  # 指定列表页的数据定时刷新
    aggregate_fields = {'quantity': 'sum', }

    # 表单根据用户显示不同的字段内容
    def get_model_form(self, **kwargs):
        obj = self.org_obj
        flag = self.org_obj is None and 'create' or 'change'
        # if flag == 'create':
        #     self.fields = ['FRUSelect', 'desc', 'quantity']
        return super().get_model_form(**kwargs)

    # def get_form(self, request, obj=None, **kwargs):
    #     self.exclude = []
    #     if not request.user.is_superuser:
    #         self.exclude.append('id')
    #     if not obj.machineModel:
    #         self.exclude.append('machineSN')
    #     print('test')
    #     print(obj.machineModel)
    #     return super(ContactAdminPurchase_stockin_detail, self).get_form(request, obj, **kwargs)

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
    # list_per_page设置每页显示多少条记录，默认是100条
    list_per_page = 5

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
    # list_per_page设置每页显示多少条记录，默认是100条
    list_per_page = 5

xadmin.site.register(Purchase_order, ContactAdminPurchase_order) # 采购申请
xadmin.site.register(Purchase_order_detail, ContactAdminPurchase_order_detail) # 采购下单明细
xadmin.site.register(Purchase_stockin_detail, ContactAdminPurchase_stockin_detail) # 采购入库明细
xadmin.site.register(Purchase_return, ContactAdminPurchase_return) # 采购退货下单
xadmin.site.register(Purchase_returnout, ContactAdminPurchase_returnout) # 采购退货出库