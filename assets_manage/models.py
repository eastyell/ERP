from django.db import models
from django.utils import timezone
from django.utils.safestring import mark_safe
from crm.settings import MEDIA_URL
from common import const

# Create your models here.

# 礼品信息
class Gifts(models.Model):
     status = models.IntegerField(verbose_name=("出入库状态"), choices=const.gifts_status, default=10)
     name = models.CharField(u'_____品名_____', max_length=100, null=True, blank=True)
     quantity = models.IntegerField(u'库存数量', null=True, blank=True, default=0)
     quantity_inout = models.IntegerField(u'出入库数量', null=True, blank=True, default=0)
     product_date = models.DateField(u'生产日期', null=True, blank=True )
     exp = models.IntegerField(u'保质期(年)', null=True, blank=True, default=0)
     degree = models.FloatField(u'度数(%vol)', null=True, blank=True, default=0)
     volume = models.IntegerField(u'容量(ml)', null=True, blank=True, default=0)
     image = models.ImageField(u'正面图片', upload_to='images/%m%d', null=True, blank=True, )
     image2 = models.ImageField(u'反面图片', upload_to='images/%m%d', null=True, blank=True, )

     def image_data(self):
         if self.image != '':
             return mark_safe(
                 '<a href="%s%s" target="blank" title="图片预览"> <img src="%s%s" height="50" width="50"/> </a>' % (
                 MEDIA_URL, self.image, MEDIA_URL, self.image,))
         else:
             return ''
     image_data.short_description = u'正面图片'
     image_data.allow_tags = True
     def image_data2(self):
         if self.image2 != '':
             return mark_safe(
                 '<a href="%s%s" target="blank" title="图片预览"> <img src="%s%s" height="50" width="50"/> </a>' % (
                 MEDIA_URL, self.image2, MEDIA_URL, self.image2,))
         else:
             return ''
     image_data2.short_description = u'反面图片'
     image_data2.allow_tags = True
     author_checkin = models.CharField(u'入库人', max_length=10, null=True, blank=True,default=None)
     checkin_date = models.DateTimeField(u'入库时间', null=True, blank=True,default = None)
     author_checkout = models.CharField(u'出库人', max_length=10, null=True, blank=True, default=None)
     checkout_date = models.DateTimeField(u'出库时间', null=True, blank=True,default = None)
     author_user = models.CharField(u'使用人', max_length=10, null=True, blank=True, default=None)
     remark = models.TextField(u'_____备注_____', null=True, blank=True)
     pub_date = models.DateTimeField(u'创建时间',  null=True, blank=True,default = None)

     # 列表中显示的内容
     def __str__(self):
        return self.name

     class Meta:
         verbose_name_plural = '礼品信息'
         verbose_name = '礼品信息'
         # ordering = ('name','-status','-checkin_date','-checkout_date' )
         ordering = ('name','-pub_date' )