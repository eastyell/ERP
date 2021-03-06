# 模块名称：采购管理模型
# 创建日期：2020-4
# 最后修改日期：2020-6
# 作者：Jason

from django.db import models
from params_manage.models import Purchase_type
from baseinfo_manage.models import Shop, Suppliers, \
    DeviceStores,CustomersSign,SelectOrderDetail,Customers
from django.utils.safestring import mark_safe
from crm.settings import MEDIA_URL
from params_manage.models import Location
from common import generic
import django.utils.timezone as timezone
from common import const



# 自定义采购下单
# class Purchase_order_self(models.Model):
#     class Meta:
#         verbose_name = u"自定义采购下单"
#         verbose_name_plural = verbose_name
#         db_table = 'change_into'
#
#     def __str__(self):
#         return self.Meta.verbose_name

# 采购申请
class Purchase_order(models.Model):
    id = models.CharField('采购单号', primary_key= True, max_length=18)
    status = models.IntegerField(verbose_name=("申请状态"), choices=const.virtual_status, default=0)
    purchase_type = models.ForeignKey(Purchase_type, on_delete=models.CASCADE, verbose_name='采购类型', default=1)
    purchasedesc = models.CharField(u'采购说明', max_length=100, null=True, blank=True)
    arrive_date = models.DateField(u'最晚到货日期', default=timezone.now)
    ifimportant = models.IntegerField(verbose_name=("是否加急"), choices=const.virtual_important, default=0)
    shopid = models.ForeignKey(Shop, to_field='id', on_delete=models.CASCADE, verbose_name='备件类别', default=1)
    desc = models.CharField('备件描述', max_length=50, null=True, blank=True)
    machineSelect = models.ManyToManyField(DeviceStores, verbose_name='整机型号 | 备件类别 | FRU码 | PN码',
                                           related_name='machineSelectOrder', blank=True, symmetrical=False)
    machineSelects = models.ManyToManyField(SelectOrderDetail, verbose_name='整机型号 | 备件类别 | FRU码 | PN码 | 库存量 | 数量 | 描述',
                                           related_name='SelectOrder', blank=True, symmetrical=False)
    quantity = models.IntegerField('采购数量', null=True, blank=True, default=0)
    price = models.FloatField('采购价格', null=True, blank=True)
    amount = models.DecimalField('采购总价', max_digits=12, decimal_places=2, blank=True, null=True,
                                 default=0.00)
    suppliersid = models.ForeignKey(Suppliers, to_field='id', on_delete=models.CASCADE, verbose_name='供应商名称', default=1)
    customer = models.ForeignKey(Customers, on_delete=models.CASCADE, verbose_name='所属项目', default='1')
    customersSignid = models.ForeignKey(CustomersSign, to_field='id', on_delete=models.CASCADE, verbose_name='签约项目', default=1)
    remark = models.TextField(u'备注', null=True, blank=True)
    pub_date = models.DateField(u'创建日期', auto_now_add=True, null=True)
    author = models.CharField(u'申请人', max_length=10, null=True, default=None)
    update_time = models.DateTimeField(u'申请时间', default=None, null=True)

    def short_content(self):
        if len(str(self.remark)) > 30:
            return '{}...'.format(str(self.remark)[0:30])
        else:
            return str(self.remark)
    short_content.allow_tags = True
    short_content.short_description = u'采购单流程追踪'

    # 下面为新增代码
    class Meta:
        verbose_name = '采购申请'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{} / {} / {} / {}'.format(self.id, self.purchase_type, self.shopid, self.desc)
        # return self.id

# 采购下单明细
class Purchase_order_detail(models.Model):
    bill_id = models.ForeignKey(Purchase_order, to_field='id', on_delete=models.CASCADE, verbose_name='采购单号')
    status = models.IntegerField(verbose_name=("下单状态"), choices=const.virtual_status, default=0)
    ifmachine = models.IntegerField(verbose_name=("是否整机备件"), choices=const.virtual_choice, default=0)
    machineModel = models.CharField(u'整机型号', max_length=30, null=True, blank=True)
    shopid = models.ForeignKey(Shop, to_field='id', on_delete=models.CASCADE, verbose_name='备件名称', default=1)
    SN = models.CharField(u'SN码', max_length=15, null=True, blank=True )
    FRU = models.CharField(u'FRU码', max_length=15, null=True, blank=True)
    machineSelects = models.ManyToManyField(SelectOrderDetail, verbose_name='整机型号 | 备件类别 | FRU码 | PN码 | 库存量 | 数量 | 描述',
                                            related_name='SelectOrderDetail', blank=True, symmetrical=False)
    machineSelect = models.ManyToManyField(DeviceStores, verbose_name='整机型号 | 备件类别 | FRU码 | PN码',
                                           related_name='machineSelect', blank=True, symmetrical=False)
    FRUSelect = models.ForeignKey(DeviceStores, to_field='id', on_delete=models.CASCADE, verbose_name='整机型号 | 备件类别 | FRU码 | PN码 | 库存量', default= 1)
    PN = models.CharField(u'PN码', max_length=15, null=True, blank=True)
    machineSN = models.CharField(u'整机SN', max_length=30, null=True, blank=True)
    desc = models.CharField(u'备件描述', max_length=50, null=True, blank=True)
    quantity = models.IntegerField('数量', default=1)
    source = models.CharField(u'来源', max_length=30, null=True, blank=True)
    replace = models.CharField(u'替代号', max_length=15, null=True, blank=True)
    useage = models.IntegerField('使用年限', default=0)
    price = models.FloatField('单价', default=1)

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

    arrive_date = models.DateField(u'估计到货时间', default=timezone.now)
    customer = models.ForeignKey(Customers, on_delete=models.CASCADE, verbose_name='所属项目', default='1')
    suppliersid = models.ForeignKey(Suppliers, to_field='id', on_delete=models.CASCADE, verbose_name='供应商名称', default=1)
    remark = models.TextField(u'采购单流程追踪', null=True, blank=True)
    pub_date = models.DateField(u'创建日期', auto_now_add=True, null=True)
    author = models.CharField(u'下单人', max_length=10, null=True, default=None)
    update_time = models.DateTimeField(u'下单时间', default=None, null=True)
    # 通过下单明细，更新单子的总数和金额
    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        money = 0
        if self.price and self.quantity:
            money = self.price * self.quantity
            # self.amount = money
        super(Purchase_order_detail, self).save(force_insert, force_update, using, update_fields)
        if money > 0:
            sql = 'UPDATE purchase_manage_purchase_order SET amount = ' \
                   '(SELECT sum(price*quantity) as amount FROM purchase_manage_purchase_order_detail WHERE bill_id_id=%s) where id=%s'
            params = [self.bill_id.id,self.bill_id.id]
            generic.update(sql,params)
        if self.quantity > 0:
            sql = 'UPDATE purchase_manage_purchase_order SET quantity = ' \
                  '(SELECT sum(quantity) as quantity FROM purchase_manage_purchase_order_detail WHERE bill_id_id=%s) where id=%s'
            params = [self.bill_id.id, self.bill_id.id]
            generic.update(sql, params)


        # self.material.purchase_price = self.price
        # self.material.save()
        # sql = 'UPDATE purchase_purchaseorder SET amount = (SELECT SUM(a.price*a.cnt) AS amount FROM ' \
        #       'purchase_poitem a WHERE a.po_id = %s) WHERE id = %s'
        # params = [self.po.id, self.po.id]
        # generic.update(sql, params)
    # 下面为新增代码
    class Meta:
        verbose_name = '采购下单'
        verbose_name_plural = verbose_name
        ordering = ['-bill_id']

    def __str__(self):
        return str(self.bill_id)

# 采购入库
class Purchase_stockin(models.Model):
    id = models.CharField('采购入库申请单号', primary_key= True, max_length=30)
    purchase_id = models.ForeignKey(Purchase_order, to_field='id', on_delete=models.CASCADE, verbose_name='采购单号')
    shopid = models.ForeignKey(Shop, to_field='id', on_delete=models.CASCADE, verbose_name='备件名称', default=1)
    quantity = models.IntegerField('采购数量', default=1)
    price = models.FloatField('采购金额')
    suppliersid = models.ForeignKey(Suppliers, to_field='id', on_delete=models.CASCADE, verbose_name='供应商名称', default=1)
    remark = models.TextField(u'备注', null=True, blank=True)
    pub_date = models.DateField(u'创建时间', auto_now_add=True, null=True)
    author = models.CharField(u'入库人', max_length=10, default=None)
    update_time = models.DateTimeField(u'更新时间', auto_now=True, null=True)

    # remark = 'test'
    # 下面为新增代码
    class Meta:
        verbose_name = '采购入库单'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.id

# 采购入库明细
class Purchase_stockin_detail(models.Model):
    # bill_id = models.ForeignKey(Purchase_stockin, to_field='id', on_delete=models.CASCADE, verbose_name='采购入库单号')
    bill_id = models.CharField('采购入库单号', max_length=30, null=True, blank=True)
    status = models.IntegerField(verbose_name=("入库状态"), choices=const.virtual_status, default=0)
    ifsure = models.IntegerField(verbose_name=("是否已确认"), choices=const.virtual_choice, default=0)
    purchase_id = models.ForeignKey(Purchase_order_detail, to_field='id', on_delete=models.CASCADE, verbose_name='采购单号', default=1)
    shopid = models.ForeignKey(Shop, to_field='id', on_delete=models.CASCADE, verbose_name='备件类别')
    FRU = models.CharField(u'FRU码', max_length=15, null=True, )
    FRUSelect = models.ForeignKey(DeviceStores, to_field='id', on_delete=models.CASCADE,
                                  verbose_name='整机型号 | 备件类别 | FRU码 | PN码 | 库存量')
    PN = models.CharField(u'PN码', max_length=15, null=True, blank=True)
    desc = models.CharField(u'备件描述', max_length=50, null=True, blank=True)
    machineModel = models.CharField(u'整机型号', max_length=30, null=True, blank=True)
    SN = models.CharField(u'SN码', max_length=150, null=True, blank=True)
    machineSN = models.CharField(u'整机SN', max_length=150, null=True, blank=True)
    source = models.CharField(u'来源', max_length=30, null=True, blank=True)
    replace = models.CharField(u'替代号', max_length=15, null=True, blank=True)
    useage = models.IntegerField('使用年限',default=0)
    quantity = models.IntegerField('数量', default=0)
    price = models.FloatField('单价')
    location = models.ForeignKey(Location, on_delete=models.CASCADE, verbose_name='库存位置',default=1)
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

    remark = models.TextField(u'采购单流程追踪', null=True, blank=True)
    pub_date = models.DateTimeField(u'入库时间', null=True, default=None)#default = timezone.now)
    author = models.CharField(u'入库人', max_length=10, null=True, default=None)
    update_time = models.DateField(u'创建日期', auto_now_add=True, null=True)

    # # 根据FRU 更新库存
    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        # if self.price and self.quantity:
        #     money = self.price * self.quantity
        #     # self.amount = money
        super(Purchase_stockin_detail, self).save(force_insert, force_update, using, update_fields)
        # 由于自动拆分采购入库单，导致重复计算一次数量
        # if (self.quantity > 0) and (self.bill_id):
        #     sql = "UPDATE baseinfo_manage_devicestores SET quantity = quantity + %s where (FRU=%s or PN=%s) or (machineSN=%s)"
        #     params = [self.quantity, self.FRU, self.PN, 'test']
        #     generic.update(sql, params)


    # 下面为新增代码
    class Meta:
        verbose_name = '采购入库'
        verbose_name_plural = verbose_name
        ordering = ['status','-bill_id','purchase_id','shopid']

    def __str__(self):
        return str(self.bill_id)

# 采购退货下单
class Purchase_return(models.Model):
    id = models.CharField('采购退货单号', primary_key= True, max_length=12)
    purchase_id = models.ForeignKey(Purchase_order, to_field='id', on_delete=models.CASCADE, verbose_name='进货单号')
    shopid = models.ForeignKey(Shop, to_field='id', on_delete=models.CASCADE, verbose_name='备件名称')
    quantity = models.IntegerField('退货数量')
    price = models.FloatField('价格')
    reason = models.CharField('退货原因', max_length=300)
    remark = models.CharField('备注', max_length=100)
    pub_date = models.DateField(u'退单时间', auto_now_add=True, null=True)
    author = models.CharField(u'退单人', max_length=10, default=None)
    update_time = models.DateTimeField(u'更新时间', auto_now=True, null=True)

    # 下面为新增代码
    class Meta:
        verbose_name = '采购退货下单'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.id

# 采购退货出库
class Purchase_returnout(models.Model):
    id = models.CharField('采购入库单号', primary_key= True, max_length=12)
    purchase_id = models.ForeignKey(Purchase_order, to_field='id', on_delete=models.CASCADE, verbose_name='采购单号')
    shopid = models.ForeignKey(Shop, to_field='id', on_delete=models.CASCADE, verbose_name='备件名称')
    quantity = models.IntegerField('退货数量')
    price = models.FloatField('退货价格')
    remark = models.CharField('备注', max_length=100)
    pub_date = models.DateField(u'出库时间', auto_now_add=True, null=True)
    author = models.CharField(u'出库人', max_length=10, default=None)
    update_time = models.DateTimeField(u'更新时间', auto_now=True, null=True)

    # 下面为新增代码
    class Meta:
        verbose_name = '采购退货出库'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.id