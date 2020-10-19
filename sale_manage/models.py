# 模块名称：采销售管理数据模型
# 创建日期：2020-4
# 最后修改日期：2020-6
# 作者：Jason

# Create your models here.
from django.db import models
from baseinfo_manage.models import Shop
from common import const
from baseinfo_manage.models import *
from purchase_manage.models import *

# 销售下单
class Sales_out(models.Model):
    id = models.CharField('销售单', primary_key= True, max_length=12)
    status = models.IntegerField(verbose_name=("申请状态"), choices=const.virtual_status, default=0)
    customer = models.ForeignKey(Customers, on_delete=models.CASCADE, verbose_name='销售客户', default='1')
    customersSignid = models.ForeignKey(CustomersSign, to_field='id', on_delete=models.CASCADE, verbose_name='签约客户',
                                        default=1)
    machineSelects = models.ManyToManyField(SelectOrderDetail, verbose_name='整机型号 | 备件类别 | FRU码 | PN码 | 库存量 | 数量 | 描述',
                                             related_name='SelectDeviceSales', blank=True, symmetrical=False)
    remark = models.TextField(u'备注', null=True, blank=True)
    pub_date = models.DateField(u'创建日期', auto_now_add=True, null=True)
    author = models.CharField(u'下单人', max_length=10, null=True, default=None)
    update_time = models.DateTimeField(u'下单时间', default=None, null=True)

    # 下面为新增代码
    class Meta:
        verbose_name = '销售下单'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.id


# 销售下单出库
class Sales_out_stockout(models.Model):
    billid = models.CharField('销售出库单', max_length=30, null=True, blank=True)
    saleid = models.ForeignKey(Sales_out, to_field='id', on_delete=models.CASCADE, verbose_name='销售单', default=1)
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
    customersSignid = models.ForeignKey(CustomersSign, to_field='id', on_delete=models.CASCADE, verbose_name='签约销售客户',
                                        default=1)
    customer = models.ForeignKey(Customers, on_delete=models.CASCADE, verbose_name='销售客户', default='1')
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
        verbose_name = '销售出库'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.billid)

# 销售退单
class Sales_return(models.Model):
    id = models.CharField('销售退单号', primary_key= True, max_length=12)
    shopid = models.ForeignKey(Shop, to_field='id', on_delete=models.CASCADE, verbose_name='商品名称', default='1')
    quantity = models.IntegerField('数量')
    price = models.FloatField('价格')
    reason = models.CharField('退货原因', max_length=100)
    remark = models.CharField('备注', max_length=100)
    pub_date = models.DateField(u'退单时间', auto_now_add=True, null=True)
    author = models.CharField(u'退单人', max_length=10, default=None)
    update_time = models.DateTimeField(u'更新时间', auto_now=True, null=True)

    # 下面为新增代码
    class Meta:
        verbose_name = '销售退单'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.id

# 销售退单入库
class Sales_return_stockin(models.Model):
    id = models.CharField('销售入库单', primary_key= True, max_length=12)
    shopid = models.ForeignKey(Shop, to_field='id', on_delete=models.CASCADE, verbose_name='商品名称', default='1')
    quantity = models.IntegerField('数量')
    price = models.FloatField('价格')
    remark = models.CharField('备注', max_length=100)
    pub_date = models.DateField(u'入库时间', auto_now_add=True, null=True)
    author = models.CharField(u'入库人', max_length=10, default=None)
    update_time = models.DateTimeField(u'更新时间', auto_now=True, null=True)

    # 下面为新增代码
    class Meta:
        verbose_name = '销售退单入库'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.id