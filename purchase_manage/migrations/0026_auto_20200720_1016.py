# Generated by Django 2.0 on 2020-07-20 02:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('purchase_manage', '0025_auto_20200715_1123'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='selectorderdetail',
            options={'ordering': ['-device'], 'verbose_name': '备件选择明细', 'verbose_name_plural': '备件选择明细'},
        ),
        migrations.AlterField(
            model_name='purchase_order',
            name='status',
            field=models.IntegerField(choices=[(0, '待办'), (1, '已办'), (2, '已下单'), (3, '已入库')], default=0, verbose_name='申请状态'),
        ),
        migrations.AlterField(
            model_name='purchase_order',
            name='update_time',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='申请时间'),
        ),
        migrations.AlterField(
            model_name='purchase_order_detail',
            name='status',
            field=models.IntegerField(choices=[(0, '待办'), (1, '已办'), (2, '已下单'), (3, '已入库')], default=0, verbose_name='下单状态'),
        ),
        migrations.AlterField(
            model_name='purchase_order_detail',
            name='update_time',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='下单时间'),
        ),
        migrations.AlterField(
            model_name='purchase_stockin_detail',
            name='status',
            field=models.IntegerField(choices=[(0, '待办'), (1, '已办'), (2, '已下单'), (3, '已入库')], default=0, verbose_name='入库状态'),
        ),
    ]
