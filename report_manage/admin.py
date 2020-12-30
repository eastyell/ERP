# 模块名称：报表管理业务处理模块
# 创建日期：2020-6
# 最后修改日期：2020-6
# 作者：Jason

from django.contrib import admin
import xadmin,win32ui
from report_manage.models import *
from django.contrib import messages
from xadmin.plugins.actions import BaseActionView
from django.shortcuts import redirect
from xlrd import open_workbook
from xadmin import views
from report_manage.views import StockInView,StockOutView,Repairview
import pyecharts
from pyecharts.engine import create_default_environment

# 系统参数设置
class BaseSetting(object):
    enable_themes = True #开启主题选择
    use_bootswatch = True

class GlobalSettings(object):
    # 设置左上角title名字
    site_title = "备件库存管理系统 V1.0.6"
    # 设置底部关于版权信息
    site_footer = "腾孝(上海)网络科技"
    #设置菜单缩放
    menu_style = "accordion"     #左侧导航条修改可折叠
    global_models_icon = {
         # Devices: "glyphicon glyphicon-user", #UserDistrict: "fa fa-cloud"
      }  # 设置models的全局图标

    # 自定义菜单
    def get_site_menu(self):  # 名称不能改
        return [
            {
                'title': '   数据分析',
                'icon': 'fa fa-bar-chart-o',
                'menus': (
                    {
                        'title': '备件入库统计',  # 这里是你菜单的名称
                        'url': '/admin/report_manage/StockIn_view',  # 这里填写你将要跳转url
                        'icon': 'fa fa-spinner fa-spin fa-1x fa-fw'  # 这里是bootstrap的icon类名，要换icon只要登录bootstrap官网找到icon的对应类名换上即可
                    },
                    {
                        'title': '备件出库统计',
                        'url': '/admin/report_manage/StockOut_view',  # 这里填写你将要跳转url
                        'icon': 'fa fa-cog fa-spin fa-1x fa-fw'
                    }
                    ,
                    {
                        'title': '客户维修情况统计',
                        'url': '/admin/report_manage/Repair_view',  # 这里填写你将要跳转url
                        'icon': 'fa fa-refresh fa-spin fa-1x fa-fw'
                    }
                )
            }
        ]


#注册你上面填写的url
 #从你的app的view里引入你将要写的view，你也可以另外写一个py文件，把后台的view集中在一起方便管理
xadmin.site.register_view(r'StockIn_view/$', StockInView, name='Stock_In')
xadmin.site.register_view(r'StockOut_view/$', StockOutView, name='Stock_Out')
xadmin.site.register_view(r'Repair_view/$', Repairview, name='Repair')

# 出入库信息图形化显示
def showGui():
    furs = {}
    month = ['202001','202002','202003','202004','202005','202006','202007','202008','202009','202010','202011','202012']
    qunatity = ['0','0','0','0','0','0','0','0','0','0','0','0']
    line = pyecharts.Line("备件入库统计",width = 1100,height = 520,title_top=10,title_text_size=16)
    # sql = 'select fru,strftime("%Y%m",pub_date) as month,sum(quantity) '\
    #       'from report_manage_stock_detail where stock_type = 0 ' \
    #       'group by fru,month order by fru,month'
    sql = 'select c.name,strftime("%Y%m",a.pub_date) as month,sum(a.quantity) ' \
          'from report_manage_stock_detail a,baseinfo_manage_shop b,params_manage_base_type c ' \
          'where a.stock_type = 0 and a.shopid_id = b.id and b.shop_type_id = c.id ' \
          'group by c.name,month order by month,c.name'

    print(sql)
    datas = generic.query(sql)
    for value in datas:
       fru = value[0]
       ny = value[1]
       sl = value[2]
       if (fru != None) and (fru != ''):
             if fru not in furs:
                qunatity = ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']

             ws = ny[-2:-1]
             if int(ws) < 0:
                 p = ny[-1:]
                 qunatity[int(p)-1] = sl
             else:
               p = ny[-2:]
               qunatity[int(p)-1] = sl
             # furs[fru]=[month,qunatity]
             furs[(ny,fru)]=[month,qunatity]
             print('目标记录值：',end='')
             print(fru)
             print(qunatity)
             print('p:' + str(p) + '  sl:' + str(sl))

    # print('遍历')
    sorted(furs)
    for key in furs:
        print(key,furs[key])
        line.add(key[1], furs[key][0], furs[key][1],
        pos_top="20",
        pos_left="50",
        is_datazoom_show=True,
        line_width = 1,
        # line_color = 'cyan',
        line_type='solid',  # 线型，可以是solid,dashed,或者dotted
        is_toolbox_show=True,  # 是否开启工具箱
        is_more_utils=True     # 是否显示更多工具
        )
    # line.add("85Y6278", ["202003","202008","202009"], ["1","4","9"],
    #          is_toolbox_show=True,  # 是否开启工具箱
    #          is_more_utils=True  # 是否显示更多工具
    #          )
    # line.add("3555-L3A", ["202003","202008","202009"], ["0","11","0"],
    #          is_toolbox_show=True,  # 是否开启工具箱
    #          is_more_utils=True  # 是否显示更多工具
    #          )
    # line.add("74Y6495", ["202008"], ["3"],
    #          is_toolbox_show=True,  # 是否开启工具箱
    #          is_more_utils=True  # 是否显示更多工具
    #          )
    env = create_default_environment("html")
    env.render_chart_to_file(line, path="\report_manage\templates\入库统计信息11.html")

#从EXCEL中获取数据
def readExcel(xls_name):
  # 读取excel文件
  file = open_workbook(xls_name)
  # sheet = file.sheet_by_name(sheet_name)
  sheet = file.sheet_by_index(0)
  # 获取所有行数；
  nrows = sheet.nrows -1
  print(nrows)
  datasTemp = []
  for i in range(nrows):
    datasTemp.append(sheet.row_values(i + 1 ))
  # for i in range(len(datasTemp)):
  #     print(datasTemp[i])
  return datasTemp

class ImportReplaceIBM(BaseActionView): # 定义一个动作
    action_name = "import_replaceIBM"  # 相当于这个 Action 的唯一标示, 尽量用比较针对性的名字
    description = "Excel批量导入"  # 要显示的名字
    icon = 'fa fa-tasks'  # 图标
    model_perm = "change"   # 该动作所需权限
    date_hierarchy = 'update_time'
    list_filter = ('update_time',)
    date_hierarchy = 'update_time'

    def do_action(self, queryset):  # 重载do_action()方法
        # 过滤出文件结尾为 xlsx 与 xls
        bOpen = False
        filename_filter = "文件类型 (*.xls)|*.xls|文件类型 (*.xlsx)|*.xlsx||"
        dlg = win32ui.CreateFileDialog(1 if bOpen else 0, None, None, 1, filename_filter, None)  # 1表示打开文件对话框
        # dlg.SetOFNInitialDir('E:/Python')  # 设置打开文件对话框中的初始显示目录
        # 返回是否完成操作 1代表完成选取文件
        flag = dlg.DoModal()  # 成功选中文件地址 返回文件名,失败返回 None
        if 1 == flag:
            filename = dlg.GetPathName()  # 获取选择的文件名称
            print(filename)
            try:
                getValues = readExcel(filename)
                for i in range(len(getValues)):
                   # print(getValues[i])
                   queryset.create(machineSN = getValues[i][0],
                                   name = getValues[i][1],
                                   partNo = getValues[i][2],
                                   ccin = getValues[i][3],
                                   fc = getValues[i][4],
                                   replace = getValues[i][5],
                                   descs = getValues[i][6],
                                   author = self.request.user)
                messages.success(self.request, str(len(getValues)) + '条记录，导入成功！')
            except: messages.error(self.request, '文件格式不一致，导入失败！')

        # from tkinter import filedialog
        #
        # Fpath = filedialog.askopenfilename()
        # filename = Fpath
        # fobj = open(filename, 'r', encoding='UTF-8')
        # for eachline in fobj:
        #     print(eachline)
        # fobj.close()

    # 返回 HttpResponse
    # return redirect(self.request.get_full_path())


# 出入库明细
class ContactAdminStock_detail(object):
    def save_models(self):
        obj = self.new_obj
        flag = self.org_obj is None and 'create' or 'change'
        request = self.request
        obj.author = str(request.user)
        sn = obj.SN
        machinesn = obj.machineSN
        id = obj.id
        if flag == 'create':
          datas = generic.querySN(sn, machinesn,'')
          if not datas:
            sql = 'select a.descs,b.name,a.pn,a.machineModel from baseinfo_manage_devicestores a,params_manage_device_fru b where a.FRUS_id = b.id and a.id = %s' % obj.FRUSelect_id
            print(sql)
            datas = generic.query(sql)
            print(sql)
            if datas:
                desc = datas[0][0]
                fru =  datas[0][1]
                pn =  datas[0][2]
                machineModel =  datas[0][3]
                print(desc)
                print(fru)
                print(datas)
                obj.desc = desc
                obj.FRU = fru
                obj.PN = pn
                obj.machineModel = machineModel
                obj.save()
            if obj.stock_type == 1:
                if obj.quantity > 0:
                    obj.quantity = -obj.quantity
            obj.save()
          else:
            messages.set_level(request, messages.ERROR)
            if (sn != '') and (sn is not None):
               messages.error(request, 'SN码：%s 存在重复！' % sn)
            else:
               messages.error(request, '整机SN码：%s 存在重复！' % machinesn)
        else:
          datas = generic.querySN(sn, machinesn, id)
          if not datas:
            if obj.stock_type == 1:
              if obj.quantity > 0:
                   obj.quantity = -obj.quantity
            # FRU如果为空，更新FRU
            if (obj.FRU == '') or  (obj.FRU is None):
                sql = 'select a.descs,b.name,a.pn,a.machineModel from baseinfo_manage_devicestores a,params_manage_device_fru b where a.FRUS_id = b.id and a.id = %s' % obj.FRUSelect_id
                print(sql)
                datas = generic.query(sql)
                if datas:
                    fru = datas[0][1]
                    obj.FRU = fru
            obj.save()
          else:
            messages.set_level(request, messages.ERROR)
            if (sn != '') and (sn is not None):
              messages.error(request, 'SN码：%s 存在重复！' % sn)
            else:
              messages.error(request, '整机SN码：%s 存在重复！' % machinesn)

    model_icon = 'fa fa-file-text-o'  # 图标样式
    list_display = ('stock_type','shopid', 'FRUSelect','FRU', 'SN','PN','machineModel',
                    'machineSN','desc','customer','quantity','source','replace','location','image_data',
                    'remark', 'author', 'pub_date', 'update_time')
    # 添加和修改时那些界面不显示
    exclude = ('author', 'useage','PN','machineModel','FRU','shop')
    # 设置过滤
    list_filter = ('stock_type','bill_type','customer','shopid','pub_date','location','author')
    search_fields = ('SN','FRU', 'PN','machineModel','replace','bill_id')
    aggregate_fields = {'quantity': 'sum', }
    list_display_links = ('bill_id', 'FRUSelect')
     # list_per_page设置每页显示多少条记录，默认是100条
    list_per_page = 5
    refresh_times = (10, 60)  # 指定列表页的数据定时刷新
    # data_charts = {
    #     # "user_count": {'title': u"出货量统计",
    #     #                "x-field": "pub_date",
    #     #                "y-field": ("quantity",),
    #     #                'option': {
    #     #                    "series": {"bars": {"align": "center", "barWidth": 0.8, "show": True}},
    #     #                    "xaxis": {"aggregate": "sum", "mode": "categories"},
    #     #                },
    #     #                },
    #         "quantityOut_counts": {
    #             'title': '出入库统计',
    #             'x-field': "pub_date",
    #             'y-field': ("quantity",),
    #             'order': ('pub_date',)
    #             # 'option': {
    #             #     "series": {"bars": {"align": "center", "barWidth": 0.5, "show": True}},
    #             #     "xaxis": {"aggregate": "count", "mode": "categories"}
    #             # }
    #         },
    # }

# 流程信息查询
class ContactAdminWorkflow_Query(object):

    list_display = ('FRUSelect','FRU','flowstatus1','name1','author1','update_time1',
                   'flowstatus2','name2','author2','update_time2',
                   'flowstatus3','name3','author3','update_time3')
    search_fields = ('name1', 'name2', 'name3', 'FRU',)  # 如果只有一个值，结尾必须有一个逗号，证明是list或元组
    search_name = '合同编号'
    # 设置过滤
    list_filter = ('flowstatus1', 'author1','flowstatus2', 'author2','flowstatus3','author3',
                   'update_time1','update_time2','update_time3' )
    # list_per_page设置每页显示多少条记录，默认是100条
    list_per_page = 5
    # ordering设置默认排序字段，负号表示降序排序
    ordering = ('-update_time1',)
    # 指定列表显示的哪列可以点击跳转到详情更新页
    list_display_links = ('FRUSelect', 'FRU',)
    model_icon = 'fa fa-file-text-o'  # 图标样式


# IBM替代号查询
class ContactAdminReplaceIBM_Query(object):
    def save_models(self):
        obj = self.new_obj
        flag = self.org_obj is None and 'create' or 'change'
        request = self.request
        obj.author = str(request.user)
        if flag == 'create':  # 新增默认回填操作员
            obj.save()
        else:
            obj.save()

    # listdisplay设置要显示在列表中的字段（id字段是Django模型的默认主键）
    list_display = ('machineSN','name','partNo','ccin','fc','replace',
                    'descs','remark','author','update_time')  # list
    search_fields = ('machineSN','name','partNo','ccin','fc','replace','descs')  # 如果只有一个值，结尾必须有一个逗号，证明是list或元组
    search_name = '合同编号'
    # 设置过滤
    list_filter = ('name','partNo', 'ccin', 'fc', 'replace', 'descs',)
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
    list_display_links = ('machineSN', 'partNo','name')
    model_icon = 'fa fa-file-text-o'  # 图标样式
    style_fields = {'csdevice': 'm2m_transfer', 'csservice': 'ueditor', }  # 字段显示样式
    list_per_page = 5
    refresh_times = (10, 60)  # 指定列表页的数据定时刷新
    actions = [ImportReplaceIBM]


# 界面主题、基本信息设置
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)


# Register your models here.
xadmin.site.register(Stock_detail, ContactAdminStock_detail) # 出入库信息
xadmin.site.register(Workflow_Query, ContactAdminWorkflow_Query) # 流程信息查询
xadmin.site.register(ReplaceIBM_Query, ContactAdminReplaceIBM_Query) # IBM替代号查询
# 自定义插件后，注册插件
# xadmin.site.register_plugin(LogPlugin, DeleteAdminView)