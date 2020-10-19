# 模块名称：其他入库数据模型模块
# 创建日期：2020-6
# 最后修改日期：2020-6
# 作者：Jason

from django.db import models
from baseinfo_manage.models import Shop
from crm.settings import MEDIA_URL
from common import const
from baseinfo_manage.models import *
from stockout_manage.models import  Repair_use_stockout
from purchase_manage.models import SelectOrderDetail
import django.utils.timezone as timezone

# Create your models here.
# 回收下单
class Device_return(models.Model):
    id = models.CharField('回收单号', primary_key= True, max_length=12)
    desc = models.CharField(u'描述', max_length=50, null=True, blank=True)
    status = models.IntegerField(verbose_name=("回收状态"), choices=const.virtual_status, default=0)
    # shopid = models.ForeignKey(Shop, to_field='id', on_delete=models.CASCADE, verbose_name='备件名称', default='1')
    machineSelects = models.ManyToManyField(SelectOrderDetail, verbose_name='整机型号 | 备件类别 | FRU码 | PN码 | 库存量| 数量 | 描述',
                                            related_name='Selectreturn', blank=True, symmetrical=False)
    quantity = models.IntegerField('数量', default=1)
    price = models.FloatField('回收价格', default=0)
    customer = models.ForeignKey(Customers, on_delete=models.CASCADE, verbose_name='客户', default='1')
    remark = models.TextField(u'备注', null=True, blank=True)
    pub_date = models.DateField(u'创建日期', auto_now_add=True, null=True)
    author = models.CharField(u'下单人', max_length=10, null=True, default=None)
    update_time = models.DateTimeField(u'下单时间', default=None, null=True)

    # 下面为新增代码
    class Meta:
        verbose_name = '回收下单'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.id)

# 回收入库
class Device_return_stockin(models.Model):
    billid = models.CharField('回收入库单号', max_length=30, null=True, blank=True)
    status = models.IntegerField(verbose_name=("回收状态"), choices=const.virtual_status, default=0)
    ifsure = models.IntegerField(verbose_name=("是否已确认"), choices=const.virtual_choice, default=0)
    returnid = models.ForeignKey(Device_return, to_field='id', on_delete=models.CASCADE, verbose_name='回收单号',
                                    default=1)
    shopid = models.ForeignKey(Shop, to_field='id', on_delete=models.CASCADE, verbose_name='备件名称', default='1')
    FRUSelect = models.ForeignKey(DeviceStores, to_field='id', on_delete=models.CASCADE,
                                  verbose_name='整机型号 | 备件类别 | FRU码 | PN码 | 库存量', default=1)
    desc = models.CharField(u'备件描述', max_length=50, null=True, blank=True)
    SN = models.CharField(u'SN码', max_length=150, null=True, blank=True)
    machineModel = models.CharField(u'整机型号', max_length=30, null=True, blank=True)
    machineSN = models.CharField(u'整机SN', max_length=150, null=True, blank=True)
    FRU = models.CharField(u'FRU码', max_length=15, null=True, blank=True)
    PN = models.CharField(u'PN码', max_length=15, null=True, blank=True)
    quantity = models.IntegerField('数量', default=1)
    source = models.CharField(u'来源', max_length=30, null=True, blank=True)
    replace = models.CharField(u'替代号', max_length=15, null=True, blank=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, verbose_name='库存位置', default=1)
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

    customer = models.ForeignKey(Customers, on_delete=models.CASCADE, verbose_name='客户', default='1')
    remark = models.TextField(u'备注', null=True, blank=True)
    pub_date = models.DateTimeField(u'入库时间', null=True, default=None)
    author = models.CharField(u'入库人', max_length=10, null=True, default=None)
    update_time = models.DateField(u'创建日期', auto_now=True, null=True)

    # 下面为新增代码
    class Meta:
        verbose_name = '回收入库'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.FRUSelect)

# 维修返回入库
class Repair_use_stockin(models.Model):
    billid = models.CharField('维修返回入库单', max_length=30, null=True, blank=True)
    status = models.IntegerField(verbose_name=("入库状态"), choices=const.virtual_status, default=4)
    ifsure = models.IntegerField(verbose_name=("是否已确认"), choices=const.virtual_choice, default=0)
    stockouid = models.ForeignKey(Repair_use_stockout, to_field='id', on_delete=models.CASCADE, verbose_name='维修领用出库号')
    # shopid = models.ForeignKey(Shop, to_field='id', on_delete=models.CASCADE, verbose_name='备件类别')
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
    customersSignid = models.ForeignKey(CustomersSign, to_field='id', on_delete=models.CASCADE, verbose_name='所属签约项目',
                                        default=1)
    customer = models.ForeignKey(Customers, on_delete=models.CASCADE, verbose_name='所属项目', default='1')
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
    pub_date = models.DateTimeField(u'入库时间', null=True, default=None)
    author = models.CharField(u'入库人', max_length=10, null=True, default=None)
    update_time = models.DateField(u'创建日期', auto_now=True, null=True)

    # 下面为新增代码
    class Meta:
        verbose_name = '维修返回入库'
        verbose_name_plural = verbose_name

    def __str__(self):
        if self.billid:
          return str(self.billid)
        else:
          return ''