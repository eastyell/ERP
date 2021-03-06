# Generated by Django 2.0 on 2020-07-21 16:37

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('purchase_manage', '0026_auto_20200720_1016'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchase_order_detail',
            name='arrive_date',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='估计到货时间'),
        ),
        migrations.AlterField(
            model_name='purchase_order',
            name='status',
            field=models.IntegerField(choices=[(0, '待提交'), (1, '采购中'), (2, '待下单'), (3, '已下单'), (4, '待入库'), (5, '已入库')], default=0, verbose_name='申请状态'),
        ),
        migrations.AlterField(
            model_name='purchase_order_detail',
            name='status',
            field=models.IntegerField(choices=[(0, '待提交'), (1, '采购中'), (2, '待下单'), (3, '已下单'), (4, '待入库'), (5, '已入库')], default=0, verbose_name='下单状态'),
        ),
        migrations.AlterField(
            model_name='purchase_stockin_detail',
            name='status',
            field=models.IntegerField(choices=[(0, '待提交'), (1, '采购中'), (2, '待下单'), (3, '已下单'), (4, '待入库'), (5, '已入库')], default=0, verbose_name='入库状态'),
        ),
    ]
