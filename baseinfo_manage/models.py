# 模块名称：基本信息模型
# 创建日期：2020-4
# 最后修改日期：2020-6
# 作者：Jason

from django.db import models
from django.utils.safestring import mark_safe
from crm.settings import MEDIA_URL
from params_manage.models import *
from common import const
from common import generic

# 备件信息
class Shop(models.Model):
     # name = models.CharField(u'设备类型', max_length=30, null=True, blank=True )
     name = models.ForeignKey(Device_type, on_delete=models.CASCADE, verbose_name='备件类型', default='0')
     shop_type = models.ForeignKey(Base_type, on_delete=models.CASCADE, verbose_name='备件类别', default='1')
     shop_level = models.ForeignKey(Base_level, on_delete=models.CASCADE, verbose_name='备件等级', default='1')
     shop_brand = models.ForeignKey(Base_brand, on_delete=models.CASCADE, verbose_name='备件品牌', default='1')
     # shop_brand_childs = models.ForeignKey(Base_brand_child, on_delete=models.CASCADE, verbose_name='备件子品牌', default='1')
     status = models.CharField(u'备件状态', max_length=30, null=True, blank=True)
     cost = models.FloatField(u'采购成本',default=0)
     useage = models.IntegerField(u'使用年限',default=0)
     quantity_good = models.IntegerField(u'最佳备货量',default=0)
     price = models.FloatField(u'标准售价',default=0)
     remark = models.TextField(u'备注', null=True, blank=True)
     author = models.CharField(u'操作人', max_length=10, default=None)
     pub_date = models.DateField(u'创建时间', auto_now_add=True)
     update_time = models.DateTimeField(u'更新时间', auto_now=True)

     # 列表中显示的内容
     def __str__(self):
        return '{} / {}'.format(self.shop_type, self.shop_brand)

     class Meta:
         verbose_name_plural = '备件类别'
         verbose_name = '备件类别'
         ordering = ('shop_type', )

# 供应商信息
class Suppliers(models.Model):
    name = models.CharField(u'名称', max_length=30,)
    adress = models.CharField(u'地址', max_length=30, null=True, blank=True)
    people = models.CharField(u'联系人', max_length=30, null=True, blank=True)
    tel = models.CharField(u'联系方式', max_length=20, null=True, blank=True)
    remark = models.TextField(u'备注', null=True, blank=True)
    author = models.CharField(u'操作人', max_length=10, default=None)
    pub_date = models.DateField(u'创建时间', auto_now_add=True)
    update_time = models.DateTimeField(u'更新时间', auto_now=True)

    # 列表中显示的内容
    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = '供应商信息'
        verbose_name = '供应商信息'

# 备件明细
class DeviceStores(models.Model):
    # typename = models.CharField(u'设备类型', max_length=30, null=True, blank=True)
    typename = models.ForeignKey(Device_type, on_delete=models.CASCADE, verbose_name='设备类型', default='1')
    ifmachine = models.IntegerField(verbose_name=("是否整机备件"), choices=const.virtual_choice, default=0)
    machineModel = models.CharField(u'型号', max_length=30, null=True, blank=True)
    machineModels = models.ForeignKey(Device_kind, on_delete=models.CASCADE, verbose_name='型号', default='1')
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, verbose_name='备件类别', default='1')
    FRUS = models.ForeignKey(Device_FRU, on_delete=models.CASCADE, verbose_name='FRU码 / 描述', default='1')
    FRU = models.CharField(u'FRU码', max_length=15,null=True, blank=True )
    PN = models.CharField(u'PN码', max_length=15, null=True, blank=True)
    replaces = models.CharField(u'替代号', max_length=15, null=True, blank=True)
    machineSN = models.CharField(u'整机SN', max_length=30, null=True, blank=True)
    descs = models.CharField(u'备件描述', max_length=50, null=True, blank=True)
    price = models.FloatField(u'单价', default=0)
    quantity = models.IntegerField(u'库存数量', default=0)
    quantityLock = models.IntegerField(u'锁定数量', default=0)
    quantityLover = models.IntegerField(u'最低库存', default=0)
    type = models.IntegerField(verbose_name=("备件类别"), choices=const.device_type, default=1)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, verbose_name='库存位置', default='1')
    source = models.CharField(u'来源', max_length=30, null=True, blank=True)
    suppliers = models.ForeignKey(Suppliers, on_delete=models.CASCADE, verbose_name='首选供应商', default='1')
    author = models.CharField(u'操作人', max_length=10, default=None)
    update_time = models.DateTimeField(u'更新时间', auto_now=True)
    qrcode = models.ImageField(u'备件二维码', upload_to='images/%m%d', null=True, blank=True, )
    def qrcode_data(self):
        if self.qrcode != '':
            return mark_safe(
                '<a href="%s%s" target="blank" title="备件二维码预览"> <img src="%s%s" height="50" width="50"/> </a>' % (
                MEDIA_URL, self.qrcode, MEDIA_URL, self.qrcode,))
        else:
            return ''
    qrcode_data.short_description = u'备件二维码'
    qrcode_data.allow_tags = True

    image = models.ImageField(u'图片', upload_to='images/%m%d', null=True, blank=True, )
    def image_data(self):
        if self.image != '':
          return mark_safe('<a href="%s%s" target="blank" title="备件图片预览"> <img src="%s%s" height="50" width="50"/> </a>'% (MEDIA_URL, self.image,MEDIA_URL, self.image,))
        else:
          return  ''
    image_data.short_description = u'图片'
    image_data.allow_tags = True

    remark = models.TextField(u'备注', null=True, blank=True)

    def quantitys(self):
        id = self.id
        # fru = self.id
        # pn = self.PN
        # print(self.machineModel)
        # if (not self.machineModel) and (self.machineModel != None):
        #   sql = 'select sum(quantity) from report_manage_stock_detail where fru = "%s" or PN = "%s"' %(fru,pn)
        # else:
        #   sql = 'select sum(quantity) from report_manage_stock_detail where fru = "%s" or PN = "%s"' %(fru,pn)
        # print(sql)

        sql = 'select sum(quantity) from report_manage_stock_detail where FRUSelect_id = "%s"' %id
        print(sql)
        cds = generic.query(sql)
        if cds:
           if cds[0][0] != None:
             return  cds[0][0]
           else: return '0'
        else: return '0'
    quantitys.short_description = u'库存量'
    quantitys.allow_tags = True

    # # 自定义类别
    # def qytypename(self):
    #     id = self.shop_id
    #     sql = 'select b.name from baseinfo_manage_shop a,params_manage_device_type b where a.name_id = b.id and a.id  = "%s"' % id
    #     print(sql)
    #     cds = generic.query(sql)
    #     if cds:
    #        if cds[0][0] != None:
    #          return  cds[0][0]
    #        else: return '无'
    #     else: return '无'

    # typename.short_description = u'设备类型'
    # typename.allow_tags = True
    # update_time.editable = True
    # 列表中显示的内容
    def __str__(self):
        # return "标题:{},字数:{},概要:{}".format(self.title, len(self.content), self.content[:18])
        #   return self.remark[:30] + '...'
        return '{} | {} | {} | {} | {}'.format(self.machineModels, self.shop, self.FRUS, str(self.PN), str(self.quantitys()))

    class Meta:
        verbose_name_plural = '备件明细'
        verbose_name = '备件明细'
        ordering = ('shop','machineModels','FRUS')

# 备件选择历史信息
class SelectOrderDetail(models.Model):
    shopid = models.ForeignKey(Shop, to_field='id', on_delete=models.CASCADE, verbose_name='备件类别', default=1)
    device = models.ForeignKey(DeviceStores, to_field='id', on_delete=models.CASCADE, verbose_name='整机型号 | 备件类别 | FRU码 | PN码 | 库存量', default= 1)
    desc = models.CharField('备件描述', max_length=50, null=True, blank=True)
    quantity = models.IntegerField('申请数量', null=True, blank=True, default=1)

    class Meta:
        verbose_name = '备件申请信息'
        verbose_name_plural = verbose_name
        ordering = ['device']

    def __str__(self):
        return '{} | {} | {}'.format(self.device, str(self.quantity),self.desc )

# 客户信息
class Customers(models.Model):
     name = models.CharField(u'名称', max_length=30, )
     customer_type = models.ForeignKey(Customer_type, on_delete=models.CASCADE, verbose_name='客户类型', default='1')
     base_info = models.CharField(u'常规资料', max_length=30, null=True, blank=True)
     contract_info = models.CharField(u'合约资料', max_length=30, null=True, blank=True)
     clue = models.CharField(u'线索', max_length=20, null=True, blank=True)
     service = models.CharField(u'维保服务', max_length=20, null=True, blank=True)
     people = models.CharField('联系人', max_length=30, null=True, blank=True)
     tel = models.CharField('联系方式', max_length=30, null=True, blank=True)
     address = models.CharField('联系地址', max_length=50, null=True, blank=True)
     remark = models.TextField(u'备注', null=True, blank=True)
     author = models.CharField(u'操作人', max_length=10, default=None)
     pub_date = models.DateField(u'创建时间', auto_now_add=True)
     update_time = models.DateTimeField(u'更新时间', auto_now=True)

     # 列表中显示的内容
     def __str__(self):
        return self.name

     class Meta:
         verbose_name_plural = '客户信息'
         verbose_name = '客户信息'

# 潜在客户
class CustomersLatent(models.Model):
     pub_date = models.DateField(u'项目开始日期', auto_now_add=False)
     saler = models.CharField(u'销售负责人', max_length=30, )
     customer = models.ForeignKey(Customers, on_delete=models.CASCADE, verbose_name='客户名称')
     item = models.CharField(u'追踪项目', max_length=100, null=True, blank=True)
     rate = models.TextField(u'追踪进展', null=True, blank=True)
     status = models.IntegerField(verbose_name=("状态"), choices=const.customersLatent_status, default=0)
     remark = models.TextField(u'备注', null=True, blank=True)
     author = models.CharField(u'操作人', max_length=10, default=None)
     update_time = models.DateTimeField(u'更新时间', auto_now=True)

     # 列表中显示的内容
     def __str__(self):
        return self.item

     class Meta:
         verbose_name_plural = '潜在客户'
         verbose_name = '潜在客户'

# 签约客户
class CustomersSign(models.Model):
     contractid = models.CharField(u'合同编号', max_length=30, )
     pub_date = models.DateField(u'签约时间')
     customer = models.ForeignKey(Customers, on_delete=models.CASCADE, verbose_name='客户名称')
     type = models.IntegerField(verbose_name=("合同类型"), choices=const.Contract_type, default=1)
     item = models.CharField(u'项目名称', max_length=100, null=True, blank=True)
     saler = models.CharField(u'销售负责人', max_length=30, )
     engineer = models.CharField(u'负责工程师', max_length=30, )
     # contents = models.ForeignKey(ContractContent, on_delete=models.CASCADE, verbose_name='服务内容')
     contents = models.TextField(u'服务内容', null=True, blank=True)
     status = models.IntegerField(verbose_name=("项目状态"), choices=const.customersSign_status, default=0)
     # rptservice = models.TextField(u'客户服务报告', null=True, blank=True)
     rptservice = models.FileField(u'客户服务报告', upload_to='files/%m%d', null=True, blank=True)
     def file_data(self):
         if self.rptservice != '':
             return mark_safe(
                 '<a href="%s%s" target="blank" title= %s> %s </a>' % (
                     MEDIA_URL, self.rptservice, self.rptservice, self.rptservice))
         else:
             return ''
     file_data.short_description = u'客户服务报告'
     file_data.allow_tags = True
     remark = models.TextField(u'备注', null=True, blank=True)
     author = models.CharField(u'操作人', max_length=10, default=None)
     update_time = models.DateTimeField(u'更新时间', auto_now=True)
     # 列表中显示的内容
     def __str__(self):
        return str(self.customer)

     class Meta:
         verbose_name_plural = '签约客户'
         verbose_name = '签约客户'

# 合同服务内容
class ContractContent(models.Model):
     contractid = models.ForeignKey(CustomersSign, on_delete=models.CASCADE, verbose_name='合同编号')
     type = models.IntegerField(verbose_name=("合同类型"), choices=const.Contract_type, default=1)
     model = models.CharField(u'型号', max_length=30, null=True, blank=True)
     SN = models.CharField(u'序列号', max_length=30, null=True, blank=True)
     level = models.CharField(u'服务级别', max_length=30, null=True, blank=True)
     begindate = models.DateField(u'服务开始日期',default='1900-01-01')
     enddate = models.DateField(u'服务结束日期', default='1900-01-01')
     address = models.CharField(u'服务地址', max_length=50, null=True, blank=True)
     deliverydate = models.DateField(u'交货日期', default='1900-01-01')
     setupdate = models.DateField(u'安装日期', default='1900-01-01')
     remark = models.TextField(u'备注', null=True, blank=True)
     author = models.CharField(u'操作人', max_length=10, default=None)
     update_time = models.DateTimeField(u'更新时间', auto_now=True)

     # 列表中显示的内容
     def __str__(self):
        return str(self.contractid)

     class Meta:
         verbose_name_plural = '合同服务内容'
         verbose_name = '合同服务内容'



# 合同信息
class ContractInfo(models.Model):
     contractid = models.ForeignKey(CustomersSign, on_delete=models.CASCADE, verbose_name='合同编号')
     amount = models.FloatField(u'合同金额(¥)', )
     paydesc = models.CharField(u'付款条件', max_length=50, null=True, blank=True)
     rate = models.DecimalField(u'税率(%)', max_digits=5,decimal_places=2)
     paydays = models.IntegerField(u'账期(天)', )
     billdate = models.DateField(u'开票日期', auto_now_add=False)
     paystatus = models.IntegerField(verbose_name=("收款情况"), choices=const.contract_paystatus)
     file = models.FileField(u'合同文件', upload_to ='files/%m%d', null=True, blank=True)
     def file_data(self):
         if self.file != '':
             return mark_safe(
                 '<a href="%s%s" target="blank" title= %s> %s </a>' % (
                 MEDIA_URL, self.file,self.file,self.file))
         else:
             return ''

     file_data.short_description = u'合同盖章文件'
     file_data.allow_tags = True

     remark = models.TextField(u'备注', null=True, blank=True)
     author = models.CharField(u'操作人', max_length=10, default=None)
     update_time = models.DateTimeField(u'更新时间', auto_now=True)

     # 列表中显示的内容
     def __str__(self):
        return str(self.contractid)

     class Meta:
         verbose_name_plural = '合同信息'
         verbose_name = '合同信息'


# 项目需求管理
class Requirement(models.Model):

    type = models.CharField(u'类别', max_length=10, null=True, blank=True)
    important = models.CharField(u'重要性', max_length=10, null=True, blank=True)
    solve = models.IntegerField(verbose_name=("是否解决"), choices=const.virtual_choice, default=1)
    desc = models.TextField(u'场景描述')
    answer = models.TextField(u'解决方案', null=True, blank=True)
    pub_date = models.DateField(u'提交日期',)
    author = models.CharField(u'提交人', max_length=10, default=None)
    update_time = models.DateTimeField(u'更新时间', auto_now=True)
    # upload_to 参数接收一个回调函数 user_directory_path，该函数返回具体的路径字符串，图片会自动上传到指定路径下，即 MEDIA_ROOT + upload_to
    # user_directory_path 函数必须接收 instace 和 filename 两个参数。参数 instace 代表一个定义了 ImageField 的模型的实例，说白了就是当前数据记录；filename 是原本的文件名
    # null 是针对数据库而言，如果 null = True, 表示数据库的该字段可以为空；blank 是针对表单的，如果 blank = True，表示你的表单填写该字段的时候可以不填，但是对数据库来说，没有任何影响
    # image = models.ImageField(u'照片', upload_to='images', blank=True, null=True)
    # image = models.ImageField(upload_to='booktest', verbose_name='图片', null=True)
    image = models.ImageField(u'图片', upload_to='images/%m%d', null=True, blank=True, )
    def image_data(self):
        if self.image != '':
          return mark_safe('<a href="%s%s" target="blank" title="备件图片预览"> <img src="%s%s" height="50" width="50"/> </a>'% (MEDIA_URL, self.image,MEDIA_URL, self.image,))
        else:
          return  ''
    image_data.short_description = u'图片'
    image_data.allow_tags = True

    # update_time.editable = True
    # 列表中显示的内容
    def __str__(self):
        # return "标题:{},字数:{},概要:{}".format(self.title, len(self.content), self.content[:18])
        #   return self.remark[:30] + '...'
        return  '需求'

    class Meta:
        verbose_name_plural = '项目需求管理'
        verbose_name = '项目需求'

# 自定义菜单
# class change_into(models.Model):
#
#     class Meta:
#         verbose_name = u"转入分析"
#         verbose_name_plural = verbose_name
#         db_table = 'change_into'
#
#     def __str__(self):
#         return self.Meta.verbose_name






