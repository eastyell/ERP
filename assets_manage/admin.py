from django.contrib import admin
import xadmin
from assets_manage.models import *
from xadmin.plugins.actions import BaseActionView
from common import generic
from xadmin.layout import Fieldset

# 提交所选的礼品 出入库
class giftPost(BaseActionView): # 定义一个动作
    action_name = "gift_post"  # 相当于这个 Action 的唯一标示, 尽量用比较针对性的名字
    description = "提交所选的 礼品出入库"  # 要显示的名字
    icon = 'fa fa-tasks'  # 图标
    model_perm = "change"   # 该动作所需权限
    def do_action(self, queryset):  # 重载do_action()方法
        # queryset 是包含了已经选择的数据的 queryset
        ids = ()
        for i in range(0, queryset.count()):
            status = str(queryset.values_list('status')[i]).strip('(,)')
            # 状态待提交 才能提交
            if status == '10':
                ids =  ids + queryset.values_list('id')[i]
        if ids:
          ids = str(ids)
          print(ids)
          ids = str(ids).strip().rstrip(',)')
          ids = ids + ')'
        print(ids)
        d1 = timezone.now()
        request = self.request
        author = str(request.user)
        # 状态待提交 才能提交
        if ids:
            # sql = 'update assets_manage_gifts set status = 1,checkin_date = "%s",author_checkin = "%s"   where id in  %s' % (
            #   d1, author, ids)
            sql = 'update assets_manage_gifts set status = 5,quantity = quantity + quantity_inout  where quantity_inout > 0 and id in  %s' % (
              ids)
            print(sql)
            generic.update(sql)
            sql = 'update assets_manage_gifts set status = 7,quantity = quantity + quantity_inout  where quantity_inout < 0 and id in  %s' % (
                ids)
            print(sql)
            generic.update(sql)
            # 生成新的出入库记录
            sql = 'insert into assets_manage_gifts' \
                  '(status,name,product_date,exp,degree,volume,remark,quantity,image,image2,pub_date) ' \
                  'select 10,name,product_date,exp,degree,volume,remark,quantity,image,image2,datetime(CURRENT_TIMESTAMP,"localtime") ' \
                  'from  assets_manage_gifts where id in  %s and (checkin_date <> "" or checkout_date <> "")' %ids
            print(sql)
            generic.update(sql)


class ContactAdminGifts(object):
    def save_models(self):
        obj = self.new_obj
        flag = self.org_obj is None and 'create' or 'change'
        request = self.request
        if flag == 'create':  # 新增默认回填操作员
            obj.save()
        else:
            obj.save()

    def get_form_layout(self):
        if self.org_obj:
            self.form_layout = (
                    Fieldset('礼品信息',
                             'name','quantity','quantity_inout','product_date','exp','degree','volume',
                             'image','image2','author_user',
                             ),
                    Fieldset('出库信息',
                             'author_checkout', 'checkout_date'
                             ),
                    Fieldset('入库信息',
                             'author_checkin', 'checkin_date'
                             ),
                    Fieldset('其它说明',
                             'remark'
                             ),
            )
        return super(ContactAdminGifts, self).get_form_layout()


    # listdisplay设置要显示在列表中的字段（id字段是Django模型的默认主键）
    list_display = ('status','name','quantity_inout','quantity','product_date','exp','degree',
                    'volume','image_data','image_data2','author_checkin','checkin_date','author_checkout',
                    'checkout_date','author_user','remark')  # list

    # list_per_page设置每页显示多少条记录，默认是100条
    readonly_fields = ('quantity',)
    list_per_page = 5
    search_fields = ('name', )
    # ordering设置默认排序字段，负号表示降序排序
    # ordering = ('shop_type',)
    # list_editable 设置默认可编辑字段,第一个字段不允许编辑
    # list_editable = ['location', ]
    # 设置过滤
    list_filter = ('status','checkin_date','checkout_date','product_date','degree','author_user',)
    # fk_fields 设置显示外键字段
    # fk_fields = ('machine_room_id',)
    # 详细时间分层筛选
    date_hierarchy = 'product_date'
    # 添加和修改时那些界面不显示
    # exclude = ('author_checkin','author_checkout')
    # 指定列表显示的哪列可以点击跳转到详情更新页
    list_display_links = ('name',)
    model_icon = 'fa fa-money'  # 图标样式
    exclude = ('status',)
    # list_editable = ('pub_date')
    actions = [giftPost]

# Register your models here.
xadmin.site.register(Gifts, ContactAdminGifts) # 商品信息