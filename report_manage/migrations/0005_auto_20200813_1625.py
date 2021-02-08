# Generated by Django 2.2.14 on 2020-08-13 16:25

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('report_manage', '0004_auto_20200729_1632'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock_detail',
            name='FRUSelect',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='baseinfo_manage.DeviceStores', verbose_name='整机型号 | 备件类别 | FRU码 | PN码 | 库存量'),
        ),
        migrations.AlterField(
            model_name='stock_detail',
            name='bill_type',
            field=models.IntegerField(choices=[(0, '采购入库'), (1, '采购退货出库'), (2, '销售入库'), (3, '销售退货入库'), (4, '租用出库'), (5, '回收入库'), (6, '维修领用出库'), (7, '维修返回入库'), (8, '调拨出库'), (9, '调拨入库'), (10, '历史库存入库')], default=0, verbose_name='单据类型'),
        ),
        migrations.AlterField(
            model_name='stock_detail',
            name='desc',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='备件描述'),
        ),
        migrations.AlterField(
            model_name='stock_detail',
            name='location',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='params_manage.Location', verbose_name='库存位置'),
        ),
        migrations.AlterField(
            model_name='stock_detail',
            name='price',
            field=models.FloatField(default=0, verbose_name='单价'),
        ),
        migrations.AlterField(
            model_name='stock_detail',
            name='pub_date',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='出入库时间'),
        ),
        migrations.AlterField(
            model_name='stock_detail',
            name='shop',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='备件名称'),
        ),
        migrations.AlterField(
            model_name='stock_detail',
            name='shopid',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='baseinfo_manage.Shop', verbose_name='备件名称'),
        ),
        migrations.AlterField(
            model_name='stock_detail',
            name='useage',
            field=models.IntegerField(default=0, verbose_name='使用年限'),
        ),
    ]