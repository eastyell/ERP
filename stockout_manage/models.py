# 模块名称：其他出库数据模型模块
# 创建日期：2020-6
# 最后修改日期：2020-6
# 作者：Jason

from django.db import models
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from crm.settings import MEDIA_URL
from params_manage.models import *
from baseinfo_manage.models import *
from common import const
import os
from purchase_manage.models import *

# Create your models here.

virtual_type = (
    (0, '新购'),
    (1, '回收'),
)

def user_directory_path(instance, filename):
    ext = filename.split('.').pop()
    filename = '{0}{1}.{2}'.format(instance.name, instance.identity_card, ext)
    return os.path.join(instance.major.name, filename) # 系统路径分隔符差异，增强代码重用性

# # 备件下单明细
# class Device_order_detail(models.Model):
#     bill_id = models.CharField('单据号', max_length=12)
#     shopid = models.ForeignKey(Shop, to_field='id', on_delete=models.CASCADE, verbose_name='备件名称', default='1')
#     SN = models.CharField(u'SN码', max_length=15, null=True, )
#     FRU = models.CharField(u'FRU码', max_length=15, null=True, )
#     PN = models.CharField(u'PN码', max_length=15, null=True, blank=True)
#     desc = models.CharField(u'描述', max_length=50, null=True, blank=True)
#     source = models.CharField(u'来源', max_length=30, null=True, blank=True)
#     replace = models.CharField(u'替代号', max_length=15, null=True, blank=True)
#     useage = models.IntegerField('使用年限', default=0)
#     price = models.FloatField('单价')
#     quantity = models.IntegerField('数量')
#     image = models.ImageField(u'图片', upload_to='images/%m%d', null=True, blank=True, )
#     def image_data(self):
#         if self.image != '':
#             return mark_safe(
#                 '<a href="%s%s" target="blank" title="备件图片预览"> <img src="%s%s" height="50" width="50"/> </a>' % (
#                 MEDIA_URL, self.image, MEDIA_URL, self.image,))
#         else:
#             return ''
#     image_data.short_description = u'图片'
#     image_data.allow_tags = True
#
#     remark = models.TextField(u'备注', null=True, blank=True)
#     pub_date = models.DateField(u'创建时间', auto_now_add=True, null=True)
#     author = models.CharField(u'操作人', max_length=10, default=None)
#     update_time = models.DateTimeField(u'更新时间', auto_now=True, null=True)
#
#     # 下面为新增代码
#     class Meta:
#         verbose_name = '下单明细'
#         verbose_name_plural = verbose_name
#
#     def __str__(self):
#         return self.bill_id

# 备件出入库明细
# class Device_stockinout_detail(models.Model):
#     virtual_TradeType = (
#         (0, '采购'),
#         (1, '销售'),
#         (2, '回收'),
#         (3, '领用'),
#     )
#     virtual_stockinout_type = (
#         (0, '出库'),
#         (1, '入库'),
#     )
#     bill_id = models.CharField('单据号', max_length=12)
#     shopid = models.ForeignKey(Shop, to_field='id', on_delete=models.CASCADE, verbose_name='备件名称', default='1')
#     trade_type = models.IntegerField(verbose_name=("交易类型"), choices=virtual_TradeType, default=0)
#     stockinout_type = models.IntegerField(verbose_name=("出入库类型"), choices=virtual_stockinout_type, default=0)
#     SN = models.CharField(u'SN码', max_length=15, null=True, )
#     FRU = models.CharField(u'FRU码', max_length=15, null=True, )
#     PN = models.CharField(u'PN码', max_length=15, null=True, blank=True)
#     type = models.IntegerField(verbose_name=("备件类别"), choices=virtual_type, default=0)
#     desc = models.CharField(u'描述', max_length=50, null=True, blank=True)
#     source = models.CharField(u'来源', max_length=30, null=True, blank=True)
#     replace = models.CharField(u'替代号', max_length=15, null=True, blank=True)
#     useage = models.IntegerField(u'使用年限', default=0)
#     price = models.FloatField(u'单价')
#     quantity = models.IntegerField(u'数量')
#     location = models.ForeignKey(Location, on_delete=models.CASCADE, verbose_name='库存位置', default='1')
#     image = models.ImageField(u'图片', upload_to='images/%m%d', null=True, blank=True, )
#     def image_data(self):
#         if self.image != '':
#             return mark_safe(
#                 '<a href="%s%s" target="blank" title="备件图片预览"> <img src="%s%s" height="50" width="50"/> </a>' % (
#                 MEDIA_URL, self.image, MEDIA_URL, self.image,))
#         else:
#             return ''
#     image_data.short_description = u'图片'
#     image_data.allow_tags = True
#
#     remark = models.TextField(u'备注', null=True, blank=True)
#     pub_date = models.DateField(u'出入库时间', auto_now_add=True, null=True)
#     author = models.CharField(u'操作人', max_length=10, default=None)
#     update_time = models.DateTimeField(u'更新时间', auto_now=True, null=True)
#
#     # 下面为新增代码
#     class Meta:
#         verbose_name = '出入库明细'
#         verbose_name_plural = verbose_name
#
#     def __str__(self):
#         return self.bill_id

# 备件库存
# class DeviceStore(models.Model):
#     FRU = models.CharField(u'FRU码', max_length=15,null=True, blank=True )
#     PN = models.CharField(u'PN码', max_length=15, null=True, blank=True)
#     desc = models.CharField(u'描述', max_length=50, null=True, blank=True)
#     price = models.FloatField(u'单价', default=0)
#     quantity = models.IntegerField(u'数量', default=0)
#     type = models.IntegerField(verbose_name=("备件类别"), choices=virtual_type, default=0)
#     location = models.ForeignKey(Location, on_delete=models.CASCADE, verbose_name='库存位置', default='1')
#     source = models.CharField(u'来源', max_length=30, null=True, blank=True)
#     replace = models.CharField(u'替代号', max_length=15, null=True, blank=True)
#     remark = models.TextField(u'备注', null=True, blank=True)
#     author = models.CharField(u'操作人', max_length=10, default=None)
#     update_time = models.DateTimeField(u'更新时间', auto_now=True)
#     image = models.ImageField(u'图片', upload_to='images/%m%d', null=True, blank=True, )
#     def image_data(self):
#         if self.image != '':
#           return mark_safe('<a href="%s%s" target="blank" title="备件图片预览"> <img src="%s%s" height="50" width="50"/> </a>'% (MEDIA_URL, self.image,MEDIA_URL, self.image,))
#         else:
#           return  ''
#     image_data.short_description = u'图片'
#     image_data.allow_tags = True
#
#     # update_time.editable = True
#     # 列表中显示的内容
#     def __str__(self):
#         # return "标题:{},字数:{},概要:{}".format(self.title, len(self.content), self.content[:18])
#         #   return self.remark[:30] + '...'
#         return  '修改库存'
#
#     class Meta:
#         verbose_name_plural = '备件库存'
#         verbose_name = '备件库存'
#
# # 备件出入库
# class Devices(models.Model):
#     SN = models.CharField(u'SN码', max_length=15,null=True, )
#     FRU = models.CharField(u'FRU码', max_length=15,null=True, )
#     PN = models.CharField(u'PN码', max_length=15, null=True, blank=True)
#     desc = models.CharField(u'描述', max_length=50, null=True, blank=True)
#     quantityIn = models.IntegerField(u'入库数量', default=0)
#     quantityOut = models.IntegerField(u'出库数量', default=0)
#     quantity = models.IntegerField(u'库存数量', default=0)
#     # location = models.ForeignKey(Location, on_delete=models.CASCADE, verbose_name='库存位置', default='1')
#     source = models.CharField(u'来源', max_length=30, null=True, blank=True)
#     replace = models.CharField(u'替代号', max_length=15, null=True, blank=True)
#     remark = models.TextField(u'备注', null=True, blank=True)
#     pub_date = models.DateField(u'入库时间', auto_now_add=True)
#     author = models.CharField(u'入库人', max_length=10, default=None)
#     update_time = models.DateTimeField(u'更新时间', auto_now=True)
#     # upload_to 参数接收一个回调函数 user_directory_path，该函数返回具体的路径字符串，图片会自动上传到指定路径下，即 MEDIA_ROOT + upload_to
#     # user_directory_path 函数必须接收 instace 和 filename 两个参数。参数 instace 代表一个定义了 ImageField 的模型的实例，说白了就是当前数据记录；filename 是原本的文件名
#     # null 是针对数据库而言，如果 null = True, 表示数据库的该字段可以为空；blank 是针对表单的，如果 blank = True，表示你的表单填写该字段的时候可以不填，但是对数据库来说，没有任何影响
#     # image = models.ImageField(u'照片', upload_to='images', blank=True, null=True)
#     # image = models.ImageField(upload_to='booktest', verbose_name='图片', null=True)
#     image = models.ImageField(u'图片', upload_to='images/%m%d', null=True, blank=True, )
#
#     # image = models.CharField(verbose_name='图片', max_length=100)
#     # def image_data(self):
#     #     return format_html(
#     #         '<img src="{}" width="100px"/>',
#     #         self.image,
#     #     )
#     # image_data.short_description = u'图片'
#
#     # def get_account_state(self, obj):
#     #     if obj.balance < 0:
#     #         return u'<span style="color:red;font-weight:bold">%s</span>' % (u"已欠费",)
#     #     elif obj.balance <= 50:
#     #         return u'<span style="color:orange;font-weight:bold">%s</span>' % (u"余额不足",)
#     #     else:
#     #         return u'<span style="color:green;font-weight:bold">%s</span>' % (u"正常",)
#     #
#     # get_account_state.short_description = u'账户状态'
#     # get_account_state.allow_tags = True
#
#     def image_data(self):
#         if self.image != '':
#           return mark_safe('<a href="%s%s" target="blank" title="备件图片预览"> <img src="%s%s" height="50" width="50"/> </a>'% (MEDIA_URL, self.image,MEDIA_URL, self.image,))
#         else:
#           return  ''
#     image_data.short_description = u'图片'
#     image_data.allow_tags = True
#
#     def TotalQuantity(self):
#         return self.quantityIn - self.quantityOut
#     TotalQuantity.short_description = u'库存数量'
#
#     # update_time.editable = True
#     # 列表中显示的内容
#     def __str__(self):
#         # return "标题:{},字数:{},概要:{}".format(self.title, len(self.content), self.content[:18])
#         #   return self.remark[:30] + '...'
#         return  '修改备件'
#
#     class Meta:
#         verbose_name_plural = '备件出入库'
#         verbose_name = '备件出入库'


# # 备件入库
# class Instock(models.Model):
#     SN = models.CharField(u'SN码', max_length=15, primary_key=True)
#     FRU = models.CharField(u'FRU码', max_length=15)
#     PN = models.CharField(u'PN码', max_length=15, null=True, blank=True)
#     desc = models.CharField(u'描述', max_length=50, null=True, blank=True)
#     quantity = models.IntegerField(u'数量', default=0)
#     location = models.CharField(u'库存位置', max_length=10, null=True, blank=True)
#     source = models.CharField(u'来源', max_length=30, null=True, blank=True)
#     replace = models.CharField(u'替代号', max_length=15, null=True, blank=True)
#     remark = models.TextField(u'备注', null=True, blank=True)
#     pub_date = models.DateField(u'入库时间', auto_now_add=True)
#     author = models.CharField(u'入库人', max_length=10, default=None)
#     update_time = models.DateTimeField(u'更新时间', auto_now=True)
#     # upload_to 参数接收一个回调函数 user_directory_path，该函数返回具体的路径字符串，图片会自动上传到指定路径下，即 MEDIA_ROOT + upload_to
#     # user_directory_path 函数必须接收 instace 和 filename 两个参数。参数 instace 代表一个定义了 ImageField 的模型的实例，说白了就是当前数据记录；filename 是原本的文件名
#     # null 是针对数据库而言，如果 null = True, 表示数据库的该字段可以为空；blank 是针对表单的，如果 blank = True，表示你的表单填写该字段的时候可以不填，但是对数据库来说，没有任何影响
#     # image = models.ImageField(u'照片', upload_to='images', blank=True, null=True)
#     # image = models.ImageField(upload_to='booktest', verbose_name='图片', null=True)
#     image = models.ImageField(u'图片', upload_to='images/%m%d', null=True, blank=True, )
#
#     # image = models.CharField(verbose_name='图片', max_length=100)
#     # def image_data(self):
#     #     return format_html(
#     #         '<img src="{}" width="100px"/>',
#     #         self.image,
#     #     )
#     # image_data.short_description = u'图片'
#
#     def image_data(self):
#         if self.image != '':
#             return mark_safe(
#                 '<a href="%s%s" target="blank" title="备件图片预览"> <img src="%s%s" height="50" width="50"/> </a>' % (
#                 MEDIA_URL, self.image, MEDIA_URL, self.image,))
#         else:
#             return ''
#
#     image_data.short_description = u'图片'
#     image_data.allow_tags = True
#
#     # update_time.editable = True
#     # 列表中显示的内容
#     def __str__(self):
#         # return "标题:{},字数:{},概要:{}".format(self.title, len(self.content), self.content[:18])
#         #   return self.remark[:30] + '...'
#         return '修改入库'
#
#     class Meta:
#         verbose_name_plural = '备件入库'
#         verbose_name = '入库'


# 租用下单
class Device_lend(models.Model):
    # id = models.CharField('租用单号', primary_key= True, max_length=12)
    id = models.CharField('租用单号', primary_key=True, max_length=12)
    status = models.IntegerField(verbose_name=("申请状态"), choices=const.virtual_status, default=0)
    customersSignid = models.ForeignKey(CustomersSign, to_field='id', on_delete=models.CASCADE, verbose_name='所租签约客户',
                                        default=1)
    customer = models.ForeignKey(Customers, on_delete=models.CASCADE, verbose_name='所租客户', default='1')
    # shopid = models.ForeignKey(Shop, to_field='id', on_delete=models.CASCADE, verbose_name='备件名称', default='1')
    machineSelects = models.ManyToManyField(SelectOrderDetail, verbose_name='整机型号 | 备件类别 | FRU码 | PN码 | 库存量 | 数量 | 描述',
                                            related_name='SelectDeviceLend', blank=True, symmetrical=False)

    # quantity = models.IntegerField(u'数量', default=0)
    # price = models.FloatField('价格')
    date_begin = models.DateField(u'起租日期', default=timezone.now)
    date_end = models.DateField(u'讫租日期', default=timezone.now)
    remark = models.TextField(u'备注', null=True, blank=True)
    pub_date = models.DateField(u'创建日期', auto_now_add=True, null=True)
    author = models.CharField(u'下单人', max_length=10, null=True, default=None)
    update_time = models.DateTimeField(u'下单时间', default=None, null=True)

    # 下面为新增代码
    class Meta:
        verbose_name = '租用下单'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.id

# 租用出库
class Device_lend_stockout(models.Model):
    billid = models.CharField('租用出库单', max_length=30, null=True, blank=True)
    lendid = models.ForeignKey(Device_lend, to_field='id', on_delete=models.CASCADE, verbose_name='租用单号' , default=1)
    status = models.IntegerField(verbose_name=("出库状态"), choices=const.virtual_status, default=6)
    ifsure = models.IntegerField(verbose_name=("是否已确认"), choices=const.virtual_choice, default=0)
    shopid = models.ForeignKey(Shop, to_field='id', on_delete=models.CASCADE, verbose_name='备件类别')
    FRUSelect = models.ForeignKey(DeviceStores, to_field='id', on_delete=models.CASCADE,
                                  verbose_name='整机型号 | 备件类别 | FRU码 | PN码 | 库存量', default=1)
    desc = models.CharField(u'备件描述', max_length=50, null=True, blank=True)
    SN = models.CharField(u'SN码', max_length=150, null=True, blank=True)
    FRU = models.CharField(u'FRU码', max_length=15, null=True, blank=True)
    PN = models.CharField(u'PN码', max_length=15, null=True, blank=True)
    machineModel = models.CharField(u'整机型号', max_length=30, null=True, blank=True)
    machineSN = models.CharField(u'整机SN', max_length=150, null=True, blank=True)
    source = models.CharField(u'来源', max_length=30, null=True, blank=True)
    replace = models.CharField(u'替代号', max_length=15, null=True, blank=True)
    useage = models.IntegerField('使用年限', default=0)
    price = models.FloatField('单价', default=1)
    quantity = models.IntegerField('数量', default=1)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, verbose_name='库存位置', default=1)
    customersSignid = models.ForeignKey(CustomersSign, to_field='id', on_delete=models.CASCADE, verbose_name='所租潜在客户',
                                        default=1)
    customer = models.ForeignKey(Customers, on_delete=models.CASCADE, verbose_name='所租客户', default='1')
    image = models.ImageField(u'图片', upload_to='images/%m%d', null=True, blank=True, )

    def image_data(self):
        if self.image != '':
            return mark_safe(
                '<a href="%s%s" target="blank" title="备件图片预览"> <img src="%s%s" height="50" width="50"/> </a>' % (
                    MEDIA_URL, self.image, MEDIA_URL, self.image,))
        else:
            return ''

    image_data.short_description = u'图片'
    image_data.allow_tags = True

    remark = models.TextField(u'备注', null=True, blank=True)
    author = models.CharField(u'出库人', max_length=10, null=True, default=None)
    pub_date = models.DateTimeField(u'出库时间', null=True, default=None)
    update_time = models.DateField(u'创建日期', auto_now=True, null=True)

    # 下面为新增代码
    class Meta:
        verbose_name = '租用出库'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.billid)

# 维修领用下单
class Repair_use(models.Model):
    id = models.CharField('维修领用单号', primary_key= True, max_length=30)
    status = models.IntegerField(verbose_name=("申请状态"), choices=const.virtual_status, default=0)
    customersSignid = models.ForeignKey(CustomersSign, to_field='id', on_delete=models.CASCADE, verbose_name='所属签约客户',
                                        default=1)
    customer = models.ForeignKey(Customers, on_delete=models.CASCADE, verbose_name='所属客户', default='1')
    # shopid = models.ForeignKey(Shop, to_field='id', on_delete=models.CASCADE, verbose_name='备件类别')
    # FRUSelect = models.ForeignKey(DeviceStores, to_field='id', on_delete=models.CASCADE,
    #                               verbose_name='整机型号 | 备件类别 | FRU码 | PN码 | 库存量')
    machineSelects = models.ManyToManyField(SelectOrderDetail, verbose_name='整机型号 | 备件类别 | FRU码 | PN码 | 库存量 | 数量 | 描述',
                                            related_name='SelectDeviceRepair', blank=True, symmetrical=False)
    SN = models.CharField(u'SN码', max_length=15, null=True, blank=True)
    FRU = models.CharField(u'FRU码', max_length=15, null=True, blank=True)
    PN = models.CharField(u'PN码', max_length=15, null=True, blank=True)
    machineModel = models.CharField(u'整机型号', max_length=30, null=True, blank=True)
    machineSN = models.CharField(u'整机SN', max_length=30, null=True, blank=True)
    desc = models.CharField(u'备件描述', max_length=50, null=True, blank=True)
    source = models.CharField(u'来源', max_length=30, null=True, blank=True)
    replace = models.CharField(u'替代号', max_length=15, null=True, blank=True)
    useage = models.IntegerField('使用年限', default=0)
    price = models.FloatField('单价', default=1)
    quantity = models.IntegerField('数量', default=1)

    image = models.ImageField(u'图片', upload_to='images/%m%d', null=True, blank=True, )
    def image_data(self):
        if self.image != '':
            return mark_safe(
                '<a href="%s%s" target="blank" title="备件图片预览"> <img src="%s%s" height="50" width="50"/> </a>' % (
                    MEDIA_URL, self.image, MEDIA_URL, self.image,))
        else:
            return ''

    image_data.short_description = u'图片'
    image_data.allow_tags = True
    remark = models.TextField(u'备注', null=True, blank=True)
    pub_date = models.DateField(u'创建日期', auto_now_add=True, null=True)
    author = models.CharField(u'下单人', max_length=10, null=True, default=None)
    update_time = models.DateTimeField(u'下单时间', default=None, null=True)

    # 下面为新增代码
    class Meta:
        verbose_name = '维修领用下单'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.id

# 维修领用出库
class Repair_use_stockout(models.Model):
    billid = models.CharField('维修领用出库单', max_length=30, null=True, blank=True)
    status = models.IntegerField(verbose_name=("出库状态"), choices=const.virtual_status, default=0)
    ifsure = models.IntegerField(verbose_name=("是否已确认"), choices=const.virtual_choice, default=0)
    repairid = models.ForeignKey(Repair_use, to_field='id', on_delete=models.CASCADE, verbose_name='维修领用单号')
    shopid = models.ForeignKey(Shop, to_field='id', on_delete=models.CASCADE, verbose_name='备件类别')
    FRUSelect = models.ForeignKey(DeviceStores, to_field='id', on_delete=models.CASCADE,
                                  verbose_name='整机型号 | 备件类别 | FRU码 | PN码 | 库存量')
    desc = models.CharField(u'备件描述', max_length=50, null=True, blank=True)
    SN = models.CharField(u'SN码', max_length=150, null=True, blank=True)
    FRU = models.CharField(u'FRU码', max_length=15, null=True, blank=True)
    PN = models.CharField(u'PN码', max_length=15, null=True, blank=True)
    machineModel = models.CharField(u'整机型号', max_length=30, null=True, blank=True)
    machineSN = models.CharField(u'整机SN', max_length=150, null=True, blank=True)
    source = models.CharField(u'来源', max_length=30, null=True, blank=True)
    replace = models.CharField(u'替代号', max_length=15, null=True, blank=True)
    useage = models.IntegerField('使用年限', default=0)
    price = models.FloatField('单价', default=1)
    quantity = models.IntegerField('数量', default=1)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, verbose_name='库存位置', default= 1)
    customer = models.ForeignKey(Customers, on_delete=models.CASCADE, verbose_name='所属项目', default='1')
    customersSignid = models.ForeignKey(CustomersSign, to_field='id', on_delete=models.CASCADE, verbose_name='所属签约客户',
                                        default=1)
    customer = models.ForeignKey(Customers, on_delete=models.CASCADE, verbose_name='所属客户', default='1')
    image = models.ImageField(u'图片', upload_to='images/%m%d', null=True, blank=True, )
    def image_data(self):
        if self.image != '':
            return mark_safe(
                '<a href="%s%s" target="blank" title="备件图片预览"> <img src="%s%s" height="50" width="50"/> </a>' % (
                    MEDIA_URL, self.image, MEDIA_URL, self.image,))
        else:
            return ''

    image_data.short_description = u'图片'
    image_data.allow_tags = True

    remark = models.TextField(u'备注', null=True, blank=True)
    pub_date = models.DateTimeField(u'出库时间', null=True, default=None)
    author = models.CharField(u'出库人', max_length=10, null=True, default=None)
    update_time = models.DateField(u'创建日期', auto_now=True, null=True)

    # 下面为新增代码
    class Meta:
        verbose_name = '维修领用出库'
        verbose_name_plural = verbose_name

    def __str__(self):
        if self.repairid:
          return '{} / {} / {}'.format(self.billid, self.FRUSelect, self.customersSignid)
          # return str(self.repairid)
        else:
          return ''