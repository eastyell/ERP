# Generated by Django 2.0 on 2020-07-21 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stockin_manage', '0012_auto_20200720_1727'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device_return',
            name='status',
            field=models.IntegerField(choices=[(0, '待提交'), (1, '采购中'), (2, '待下单'), (3, '已下单'), (4, '待入库'), (5, '已入库'), (6, '待出库'), (7, '已出库')], default=0, verbose_name='回收状态'),
        ),
        migrations.AlterField(
            model_name='device_return_stockin',
            name='status',
            field=models.IntegerField(choices=[(0, '待提交'), (1, '采购中'), (2, '待下单'), (3, '已下单'), (4, '待入库'), (5, '已入库'), (6, '待出库'), (7, '已出库')], default=0, verbose_name='回收状态'),
        ),
        migrations.AlterField(
            model_name='repair_use_stockin',
            name='status',
            field=models.IntegerField(choices=[(0, '待提交'), (1, '采购中'), (2, '待下单'), (3, '已下单'), (4, '待入库'), (5, '已入库'), (6, '待出库'), (7, '已出库')], default=4, verbose_name='入库状态'),
        ),
    ]
