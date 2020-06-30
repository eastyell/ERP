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

# Create your models here.

class Stock_detail(models.Model):
    bill_type = models.IntegerField(verbose_name=("单据类型"), choices=const.bill_type, default=0)
    bill_id = models.CharField('入库单号', max_length=30, null=True, blank=True)
    # purchase_id = models.ForeignKey(Purchase_order_detail, to_field='id', on_delete=models.CASCADE, verbose_name='采购单号', default=1)
    FRUSelect = models.ForeignKey(DeviceStores, to_field='id', on_delete=models.CASCADE,
                                  verbose_name='FRU码 / PN码 / 整机型号', default=1)
    shop = models.CharField('商品名称', max_length=50, null=True, blank=True)
    FRU = models.CharField(u'FRU码', max_length=15, null=True, blank=True)
    SN = models.CharField(u'SN码', max_length=15, null=True, blank=True)
    PN = models.CharField(u'PN码', max_length=15, null=True, blank=True)
    machineModel = models.CharField(u'整机型号', max_length=30, null=True, blank=True)
    machineSN = models.CharField(u'整机SN', max_length=30, null=True, blank=True)
    desc = models.CharField(u'描述', max_length=50, null=True, blank=True)
    source = models.CharField(u'来源', max_length=30, null=True, blank=True)
    replace = models.CharField(u'替代号', max_length=15, null=True, blank=True)
    useage = models.IntegerField('使用年限')
    price = models.FloatField('单价')
    quantity = models.IntegerField('数量', default=1)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, verbose_name='库存位置')
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
    pub_date = models.DateField(u'入库时间', null=True)
    author = models.CharField(u'入库人', max_length=10, default=None)
    update_time = models.DateTimeField(u'更新时间', auto_now=True, null=True)


    # 下面为新增代码
    class Meta:
        verbose_name = '出入库明细'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.bill_id)
