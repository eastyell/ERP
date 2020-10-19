# 模块名称：参数设置数据模型
# 创建日期：2020-6
# 最后修改日期：2020-6
# 作者：Jason

from django.db import models
# from supplier_manage.models import  Customers
# Create your models here.

# 库存位置
class Location(models.Model):
    """
    Django 要求模型必须继承 models.Model 类。
    Category 只需要一个简单的分类名 name 就可以了。
    CharField 指定了分类名 name 的数据类型，CharField 是字符型，
    CharField 的 max_length 参数指定其最大长度，超过这个长度的分类名就不能被存入数据库。
    然后给name设置了一个'分类'的名称
    """
    code = models.CharField('库位代码', max_length=20)
    name = models.CharField('库存位置', max_length=10)
    level1 = models.CharField('库位一级', max_length=20, null=True, blank=True)
    level2 = models.CharField('库位二级', max_length=10, null=True, blank=True)
    level3 = models.CharField('库位三级', max_length=10, null=True, blank=True)
    remark = models.TextField(u'备注', null=True, blank=True)
    pub_date = models.DateField(u'创建时间', auto_now_add=True, null=True)
    author = models.CharField(u'操作人', max_length=10, default=None)
    update_time = models.DateTimeField(u'更新时间', auto_now=True, null=True)

    # 下面为新增代码
    class Meta:
        verbose_name = '库位'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{} / {} / {} / {}'.format(self.level1, self.level2, self.level3, self.name)

# 客户类型
class Customer_type(models.Model):
    name = models.CharField('客户类型', max_length=10)
    pub_date = models.DateField(u'创建时间', auto_now_add=True, null=True)
    author = models.CharField(u'操作人', max_length=10, default=None)
    update_time = models.DateTimeField(u'更新时间', auto_now=True, null=True)

    # 下面为新增代码
    class Meta:
        verbose_name = '客户类型'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

# 客户地址信息
class Customer_address(models.Model):
    # customer = models.ForeignKey(Customers, on_delete=models.CASCADE, verbose_name='客户', default='1')
    customer_id = models.CharField('客户ID', max_length=10)
    address_type = models.CharField('地址类型', max_length=10, null=True, blank=True)
    name = models.CharField('客户名称', max_length=30, null=True, blank=True)
    address = models.CharField('地址', max_length=50)
    people = models.CharField('联系人', max_length=30, null=True, blank=True)
    tel = models.CharField('联系方式', max_length=30, null=True, blank=True)
    pub_date = models.DateField(u'创建时间', auto_now_add=True, null=True)
    author = models.CharField(u'操作人', max_length=10, default=None)
    update_time = models.DateTimeField(u'更新时间', auto_now=True, null=True)

    # 下面为新增代码
    class Meta:
        verbose_name = '客户地址信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.customer_id

# 采购类型
class Purchase_type(models.Model):
    type = models.CharField('采购类型', max_length=20)
    pub_date = models.DateField(u'创建时间', auto_now_add=True, null=True)
    author = models.CharField(u'操作人', max_length=10, default=None)
    update_time = models.DateTimeField(u'更新时间', auto_now=True, null=True)

    # 下面为新增代码
    class Meta:
        verbose_name = '采购类型'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.type

# 整机类型
class Device_kind(models.Model):
    name = models.CharField('类型名称', max_length=20)
    desc = models.CharField('描述信息', max_length=30, default='')
    pub_date = models.DateField(u'创建时间', auto_now_add=True)
    author = models.CharField(u'操作人', max_length=10, default=None)
    update_time = models.DateTimeField(u'更新时间', auto_now=True, null=True)

    # 下面为新增代码
    class Meta:
        verbose_name = '整机类型'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

# 备件类别
class Device_type(models.Model):
    name = models.CharField('备件类别', max_length=20)
    pub_date = models.DateField(u'创建时间', auto_now_add=True)
    author = models.CharField(u'操作人', max_length=10, default=None)
    update_time = models.DateTimeField(u'更新时间', auto_now=True, null=True)

    # 下面为新增代码
    class Meta:
        verbose_name = '备件类别'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

# FRU信息
class Device_FRU(models.Model):
    name = models.CharField(u'FRU', max_length=20)
    desc = models.CharField('描述信息', max_length=30, default='')
    pub_date = models.DateField(u'创建时间', auto_now_add=True)
    author = models.CharField(u'操作人', max_length=10, default=None)
    update_time = models.DateTimeField(u'更新时间', auto_now=True)

    # 下面为新增代码
    class Meta:
        verbose_name = 'FRU信息'
        verbose_name_plural = verbose_name
        ordering = ('name',)

    def __str__(self):
        return '{} / {}'.format(self.name,self.desc)

# 基础类别
class Base_type(models.Model):
    name = models.CharField('备件类别', max_length=20)
    pub_date = models.DateField(u'创建时间', auto_now_add=True)
    author = models.CharField(u'操作人', max_length=10, default=None)
    update_time = models.DateTimeField(u'更新时间', auto_now=True)

    # 下面为新增代码
    class Meta:
        verbose_name = '备件类别'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

# 备件品牌
class Base_brand(models.Model):
    name = models.CharField('备件品牌', max_length=20)
    pub_date = models.DateField(u'创建时间', auto_now_add=True)
    author = models.CharField(u'操作人', max_length=10, default=None)
    update_time = models.DateTimeField(u'更新时间', auto_now=True)

    # 下面为新增代码
    class Meta:
        verbose_name = '备件品牌'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

# 备件子品牌
class Base_brand_child(models.Model):
    name = models.CharField('备件子品牌', max_length=20)
    pub_date = models.DateField(u'创建时间', auto_now_add=True)
    author = models.CharField(u'操作人', max_length=10, default=None)
    update_time = models.DateTimeField(u'更新时间', auto_now=True)

    # 下面为新增代码
    class Meta:
        verbose_name = '备件子品牌'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

# 备件等级
class Base_level(models.Model):
    name = models.CharField('备件等级', max_length=20)
    pub_date = models.DateField(u'创建时间', auto_now_add=True)
    author = models.CharField(u'操作人', max_length=10, default=None)
    update_time = models.DateTimeField(u'更新时间', auto_now=True)

    # 下面为新增代码
    class Meta:
        verbose_name = '备件等级'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name