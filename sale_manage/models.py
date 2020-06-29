# 模块名称：采销售管理数据模型
# 创建日期：2020-4
# 最后修改日期：2020-6
# 作者：Jason

# Create your models here.
from django.db import models
from baseinfo_manage.models import Shop


# 销售下单
class Sales_out(models.Model):
    id = models.CharField('销售单', primary_key= True, max_length=12)
    shopid = models.ForeignKey(Shop, to_field='id', on_delete=models.CASCADE, verbose_name='商品名称', default='1')
    quantity = models.IntegerField('数量')
    price = models.FloatField('价格')
    remark = models.CharField('备注', max_length=100)
    pub_date = models.DateField(u'下单时间', auto_now_add=True, null=True)
    author = models.CharField(u'下单人', max_length=10, default=None)
    update_time = models.DateTimeField(u'更新时间', auto_now=True, null=True)

    # 下面为新增代码
    class Meta:
        verbose_name = '销售下单'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.id


# 销售下单出库
class Sales_out_stockout(models.Model):
    id = models.CharField('销售出库单', primary_key= True, max_length=12)
    shopid = models.ForeignKey(Shop, to_field='id', on_delete=models.CASCADE, verbose_name='商品名称', default='1')
    quantity = models.IntegerField('数量')
    price = models.FloatField('价格')
    remark = models.CharField('备注', max_length=100)
    pub_date = models.DateField(u'出库时间', auto_now_add=True, null=True)
    author = models.CharField(u'出库人', max_length=10, default=None)
    update_time = models.DateTimeField(u'更新时间', auto_now=True, null=True)

    # 下面为新增代码
    class Meta:
        verbose_name = '销售下单出库'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.id


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