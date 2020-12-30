from django.shortcuts import render
from xadmin.views import CommAdminView
import pyecharts
from common import generic
from pyecharts.engine import create_default_environment

# Create your views here.

# 入库统计图形化显示
def StockInGui(sl):
    if sl == 0:
        # title = '备件入库统计'
        title = ''
        filename = 'stockin.html'
        sql = 'select c.name,strftime("%Y%m",a.pub_date) as month,sum(a.quantity) ' \
              'from report_manage_stock_detail a,baseinfo_manage_shop b,params_manage_base_type c ' \
              'where a.stock_type = 0 and a.shopid_id = b.id and b.shop_type_id = c.id ' \
              'group by c.name,month order by c.name,month'
              # 'group by c.name,month ' \
              # 'Union select c.name,strftime("%Y%m",a.pub_date) as month,sum(a.quantity) ' \
              # 'from report_manage_stock_detail a,baseinfo_manage_shop b,params_manage_base_type c '  \
              # 'where a.stock_type = 1 and a.shopid_id = b.id and b.shop_type_id = c.id ' \
              # 'group by c.name,month order by month,c.name'
    elif sl == 1:
        # title = '备件出库统计'
        title = ''
        filename = 'stockout.html'
        sql = 'select c.name,strftime("%Y%m",a.pub_date) as month,-sum(a.quantity) ' \
              'from report_manage_stock_detail a,baseinfo_manage_shop b,params_manage_base_type c ' \
              'where a.stock_type = 1 and a.shopid_id = b.id and b.shop_type_id = c.id ' \
              'group by c.name,month order by c.name,month'
    else:
        # title = '客户维修情况统计'
        title = ''
        filename = 'repair.html'
        sql = 'select b.name||" "||d.name,strftime("%Y%m",a.pub_date) as month,-sum(a.quantity) ' \
              'from report_manage_stock_detail a,baseinfo_manage_customers b,baseinfo_manage_shop c,params_manage_base_type d ' \
              'where a.stock_type = 1 and a.customer_id = b.id and a.shopid_id = c.id and c.shop_type_id = d.id ' \
              'group by b.name,d.name,month order by b.name,d.name,month'
    furs = {}
    month = ['202001','202002','202003','202004','202005','202006','202007','202008','202009','202010','202011','202012']
    qunatity = ['0','0','0','0','0','0','0','0','0','0','0','0']
    line = pyecharts.Line(title,width = 1100,height = 520,title_top=10,title_text_size=16)
    # sql = 'select fru,strftime("%Y%m",pub_date) as month,sum(quantity) '\
    #       'from report_manage_stock_detail where stock_type = 0 ' \
    #       'group by fru,month order by fru,month'

    # sql = 'select c.name,strftime("%Y%m",a.pub_date) as month,sum(a.quantity) ' \
    #       'from report_manage_stock_detail a,baseinfo_manage_shop b,params_manage_base_type c ' \
    #       'where a.stock_type = 0 and a.shopid_id = b.id and b.shop_type_id = c.id ' \
    #       'group by c.name,month order by month,c.name'

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
             print('qunatity')
             print(qunatity)
             furs[fru]=[month,qunatity]
             # furs[(ny,fru)]=[month,qunatity]
             print('目标记录值：',end='')
             print(fru)
             print(qunatity)
             print('p:' + str(p) + '  sl:' + str(sl))

    # print('遍历')
    sorted(furs)
    for key in furs:
        print(key,furs[key])
        # line.add(key[1], furs[key][0], furs[key][1],
        line.add(key, furs[key][0], furs[key][1],
        pos_top="20",
        pos_left="50",
        is_yaxislabel_align=True,
        is_label_show = True,
        is_datazoom_show=True,
        datazoom_type="both",
        line_width = 1,
        # mark_line=["min", "max", "average"],  # 标记线，三个可选项
        # is_animation = True,
        yaxis_name= "备 件 数 量",
        yaxis_type="value",  # y轴类型，可选["value","category","log"]
        xaxis_name= "年 月",  # 配置x轴名字
        xaxis_name_size= 12 ,  # x轴名字字体大小。默认=14
        # xaxis_name_gap= 0,
        xaxis_type = "category",  # x轴类型，可选["value","category","log"]
        xaxis_rotate= 0,  # int类型  文字标签旋转的角度 0=不旋转 区间=-90-90
        # line_color = 'cyan',
        line_curve=0.5,  # 线条弯曲程度，0-1， 0=完全不弯曲，1=最弯曲 TODO 未测试出效果
        line_type='solid',  # 线型，可以是solid,dashed,或者dotted
        is_toolbox_show=True,  # 是否开启工具箱
        is_more_utils=True     # 是否显示更多工具
        )
    env = create_default_environment("html")
    filename = "./report_manage/templates/"+ filename
    env.render_chart_to_file(line, path = filename)

class StockInView(CommAdminView):
    def get(self, request):
        context = super().get_context()  # 这一步是关键，必须super一下继承CommAdminView里面的context，不然侧栏没有对应数据，我在这里卡了好久
        title = "备件入库统计分析"  # 定义面包屑变量
        context["breadcrumbs"].append({'url': '/admin/', 'title': title})  # 把面包屑变量添加到context里面
        context["title"] = title  # 把面包屑变量添加到context里面
        # 下面你可以接着写你自己的东西了，写完记得添加到context里面就可以了
        StockInGui(0)
        return render(request, 'stockin_report.html',context) # 最后指定自定义的template模板，并返回context


class StockOutView(CommAdminView):
    def get(self, request):
        context = super().get_context()  # 这一步是关键，必须super一下继承CommAdminView里面的context，不然侧栏没有对应数据，我在这里卡了好久
        title = "备件出库统计分析"  # 定义面包屑变量
        context["breadcrumbs"].append({'url': '/admin/', 'title': title})  # 把面包屑变量添加到context里面
        context["title"] = title  # 把面包屑变量添加到context里面
        # 下面你可以接着写你自己的东西了，写完记得添加到context里面就可以了
        StockInGui(1)
        return render(request, 'stockout_report.html',context) # 最后指定自定义的template模板，并返回context

class Repairview(CommAdminView):
    def get(self, request):
        context = super().get_context()  # 这一步是关键，必须super一下继承CommAdminView里面的context，不然侧栏没有对应数据，我在这里卡了好久
        title = "客户维修情况统计分析"  # 定义面包屑变量
        context["breadcrumbs"].append({'url': '/admin/', 'title': title})  # 把面包屑变量添加到context里面
        context["title"] = title  # 把面包屑变量添加到context里面
        # 下面你可以接着写你自己的东西了，写完记得添加到context里面就可以了
        StockInGui(2)
        return render(request, 'repair_report.html',context) # 最后指定自定义的template模板，并返回context