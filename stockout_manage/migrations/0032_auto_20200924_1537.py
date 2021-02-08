# Generated by Django 2.2.14 on 2020-09-24 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stockout_manage', '0031_auto_20200918_1021'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device_lend',
            name='status',
            field=models.IntegerField(choices=[(0, '待提交'), (1, '采购中'), (2, '待下单'), (3, '已下单'), (4, '待入库'), (5, '已入库'), (6, '待出库'), (7, '已出库'), (8, '部分入库'), (9, '部分出库'), (10, '待出入库')], default=0, verbose_name='申请状态'),
        ),
        migrations.AlterField(
            model_name='device_lend_stockout',
            name='status',
            field=models.IntegerField(choices=[(0, '待提交'), (1, '采购中'), (2, '待下单'), (3, '已下单'), (4, '待入库'), (5, '已入库'), (6, '待出库'), (7, '已出库'), (8, '部分入库'), (9, '部分出库'), (10, '待出入库')], default=6, verbose_name='出库状态'),
        ),
        migrations.AlterField(
            model_name='repair_use',
            name='status',
            field=models.IntegerField(choices=[(0, '待提交'), (1, '采购中'), (2, '待下单'), (3, '已下单'), (4, '待入库'), (5, '已入库'), (6, '待出库'), (7, '已出库'), (8, '部分入库'), (9, '部分出库'), (10, '待出入库')], default=0, verbose_name='申请状态'),
        ),
        migrations.AlterField(
            model_name='repair_use_stockout',
            name='status',
            field=models.IntegerField(choices=[(0, '待提交'), (1, '采购中'), (2, '待下单'), (3, '已下单'), (4, '待入库'), (5, '已入库'), (6, '待出库'), (7, '已出库'), (8, '部分入库'), (9, '部分出库'), (10, '待出入库')], default=0, verbose_name='出库状态'),
        ),
    ]