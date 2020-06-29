from django.db import models
from baseinfo_manage.models import Shop

# Create your models here.
# 回收下单
class Device_return(models.Model):
    id = models.CharField('回收单号', primary_key= True, max_length=12)
    shopid = models.ForeignKey(Shop, to_field='id', on_delete=models.CASCADE, verbose_name='商品名称', default='1')
    quantity = models.IntegerField('数量')
    price = models.FloatField('回收价格')
    remark = models.CharField('备注', max_length=100)
    pub_date = models.DateField(u'回收时间', auto_now_add=True, null=True)
    author = models.CharField(u'回收人', max_length=10, default=None)
    update_time = models.DateTimeField(u'更新时间', auto_now=True, null=True)

    # 下面为新增代码
    class Meta:
        verbose_name = '回收下单'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.id

# 回收入库
class Device_return_stockin(models.Model):
    id = models.CharField('回收入库单', primary_key= True, max_length=12)
    shopid = models.ForeignKey(Shop, to_field='id', on_delete=models.CASCADE, verbose_name='商品名称', default='1')
    quantity = models.IntegerField('数量')
    remark = models.CharField('备注', max_length=100)
    pub_date = models.DateField(u'回收入库时间', auto_now_add=True, null=True)
    author = models.CharField(u'入库人', max_length=10, default=None)
    update_time = models.DateTimeField(u'更新时间', auto_now=True, null=True)

    # 下面为新增代码
    class Meta:
        verbose_name = '回收入库'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.id