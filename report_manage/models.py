# 模块名称：报表管理数据模型
# 创建日期：2020-6
# 最后修改日期：2020-6
# 作者：Jason

from django.db import models
from common import const
from params_manage.models import Location
from crm.settings import MEDIA_URL
from django.utils.safestring import mark_safe
from purchase_manage.models import *
from baseinfo_manage.models import Customers

# Create your models here.

# 出入库信息
class Stock_detail(models.Model):
    stock_type = models.IntegerField(verbose_name=("出入库类型"), choices=const.stock_type, default=0)
    bill_type = models.IntegerField(verbose_name=("单据类型"), choices=const.bill_type, default=0)
    bill_id = models.CharField('入库单号', max_length=30, null=True, blank=True)
    # purchase_id = models.ForeignKey(Purchase_order_detail, to_field='id', on_delete=models.CASCADE, verbose_name='采购单号', default=1)
    shopid = models.ForeignKey(Shop, to_field='id', on_delete=models.CASCADE, verbose_name='备件名称', default=1)
    FRUSelect = models.ForeignKey(DeviceStores, to_field='id', on_delete=models.CASCADE,
                                  verbose_name='整机型号 | 备件类别 | FRU码 | PN码 | 库存量', default=1)
    desc = models.CharField(u'备件描述', max_length=50, null=True, blank=True)
    shop = models.CharField('备件名称', max_length=50, null=True, blank=True)
    FRU = models.CharField(u'FRU码', max_length=15, null=True, blank=True)
    SN = models.CharField(u'SN码', max_length=15, null=True, blank=True)
    PN = models.CharField(u'PN码', max_length=15, null=True, blank=True)
    machineModel = models.CharField(u'整机型号', max_length=30, null=True, blank=True)
    machineSN = models.CharField(u'整机SN', max_length=30, null=True, blank=True)
    source = models.CharField(u'来源', max_length=30, null=True, blank=True)
    replace = models.CharField(u'替代号', max_length=15, null=True, blank=True)
    useage = models.IntegerField('使用年限', default=0)
    price = models.FloatField('单价', default=0)
    quantity = models.IntegerField('数量', default=1)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, verbose_name='库存位置',default=1)
    customer = models.ForeignKey(Customers, on_delete=models.CASCADE, verbose_name='项目客户', default='1')
    # qrcode = models.ImageField(u'备件二维码', upload_to='images/%m%d', null=True, blank=True, )
    #
    # def qrcode_data(self):
    #     if self.qrcode != '':
    #         return mark_safe(
    #             '<a href="%s%s" target="blank" title="备件二维码预览"> <img src="%s%s" height="50" width="50"/> </a>' % (
    #                 MEDIA_URL, self.qrcode, MEDIA_URL, self.qrcode,))
    #     else:
    #         return ''
    #
    # qrcode_data.short_description = u'备件二维码'
    # qrcode_data.allow_tags = True

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
    pub_date = models.DateTimeField(u'出入库时间', default = timezone.now)
    author = models.CharField(u'出入库人', max_length=10, default=None)
    update_time = models.DateField(u'创建日期', auto_now=True, null=True)


    # 下面为新增代码
    class Meta:
        verbose_name = '出入库信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.bill_id)

# IBM替代号查询
class ReplaceIBM_Query(models.Model):
    machineSN = models.CharField(u'机型-型号', max_length=30, null=True, blank=True)
    name = models.CharField(u'备件名称', max_length=30, null=True, blank=True)
    partNo = models.CharField(u'备件号', max_length=30, null=True, blank=True)
    ccin = models.CharField(u'CCIN号', max_length=30, null=True, blank=True)
    fc = models.CharField(u'FC号', max_length=30, null=True, blank=True)
    replace = models.CharField(u'替代号(多个以逗号分隔)', max_length=300, null=True, blank=True)
    descs = models.CharField(u'备件描述', max_length=30, null=True, blank=True)
    remark = models.TextField(u'备注', null=True, blank=True)
    pub_date = models.DateField(u'创建时间', auto_now_add=True, null=True)
    author = models.CharField(u'操作人', max_length=10, default=None)
    update_time = models.DateTimeField(u'更新时间', auto_now=True, null=True)

    # remark = 'test'
    # 下面为新增代码
    class Meta:
        verbose_name = 'IBM替代号查询'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.partNo)

# 流程信息查询
class Workflow_Query(models.Model):
    flowstatus1 = models.CharField(u'流程状态1', max_length=20, null=True, blank=True)
    name1 = models.CharField(u'单据号1', max_length=30, null=True, blank=True)
    pid = models.IntegerField(u'申请单号ID', null=True, blank=True, default='0')
    FRUSelect = models.ForeignKey(DeviceStores, to_field='id', on_delete=models.CASCADE,
                                  verbose_name='整机型号 | 备件类别 | FRU码 | PN码 | 库存量', default=1)
    FRU = models.CharField(u'FRU码', max_length=15, null=True, blank=True)
    author1 = models.CharField(u'操作人1', max_length=10, default=None, null=True)
    update_time1 = models.DateTimeField(u'提交时间1', default=None, null=True)
    flowstatus2 = models.CharField(u'流程状态2', max_length=20, null=True, blank=True)
    name2 = models.CharField(u'单据号2', max_length=30, null=True, blank=True)
    author2 = models.CharField(u'操作人2', max_length=10, default=None, null=True)
    update_time2 = models.DateTimeField(u'提交时间2', default=None, null=True)
    flowstatus3 = models.CharField(u'流程状态3', max_length=20, null=True, blank=True)
    name3 = models.CharField(u'单据号3', max_length=30, null=True, blank=True)
    author3 = models.CharField(u'操作人3', max_length=10, default=None, null=True)
    update_time3 = models.DateTimeField(u'提交时间4', default=None, null=True)

    # remark = 'test'
    # 下面为新增代码
    class Meta:
        verbose_name = '单据流程信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.name1)
