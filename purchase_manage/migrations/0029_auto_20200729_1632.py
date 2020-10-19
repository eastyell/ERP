# Generated by Django 2.0 on 2020-07-29 16:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('purchase_manage', '0028_auto_20200721_1826'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchase_stockin_detail',
            name='ifsure',
            field=models.IntegerField(choices=[(0, '否'), (1, '是')], default=0, verbose_name='是否已确认'),
        ),
        migrations.AlterField(
            model_name='purchase_order',
            name='machineSelects',
            field=models.ManyToManyField(blank=True, null=True, related_name='SelectOrder', to='purchase_manage.SelectOrderDetail', verbose_name='整机型号 | 商品类别 | FRU码 | PN码 | 库存量 | 数量 | 描述'),
        ),
        migrations.AlterField(
            model_name='purchase_order',
            name='status',
            field=models.IntegerField(choices=[(0, '待提交'), (1, '采购中'), (2, '待下单'), (3, '已下单'), (4, '待入库'), (5, '已入库'), (6, '待出库'), (7, '已出库'), (8, '部分入库'), (9, '部分出库')], default=0, verbose_name='申请状态'),
        ),
        migrations.AlterField(
            model_name='purchase_order_detail',
            name='FRUSelect',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='baseinfo_manage.DeviceStores', verbose_name='整机型号 | 商品类别 | FRU码 | PN码 | 库存量'),
        ),
        migrations.AlterField(
            model_name='purchase_order_detail',
            name='machineSelects',
            field=models.ManyToManyField(blank=True, null=True, related_name='SelectOrderDetail', to='purchase_manage.SelectOrderDetail', verbose_name='整机型号 | 商品类别 | FRU码 | PN码 | 库存量 | 数量 | 描述'),
        ),
        migrations.AlterField(
            model_name='purchase_order_detail',
            name='status',
            field=models.IntegerField(choices=[(0, '待提交'), (1, '采购中'), (2, '待下单'), (3, '已下单'), (4, '待入库'), (5, '已入库'), (6, '待出库'), (7, '已出库'), (8, '部分入库'), (9, '部分出库')], default=0, verbose_name='下单状态'),
        ),
        migrations.AlterField(
            model_name='purchase_stockin_detail',
            name='FRUSelect',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='baseinfo_manage.DeviceStores', verbose_name='整机型号 | 商品类别 | FRU码 | PN码 | 库存量'),
        ),
        migrations.AlterField(
            model_name='purchase_stockin_detail',
            name='status',
            field=models.IntegerField(choices=[(0, '待提交'), (1, '采购中'), (2, '待下单'), (3, '已下单'), (4, '待入库'), (5, '已入库'), (6, '待出库'), (7, '已出库'), (8, '部分入库'), (9, '部分出库')], default=0, verbose_name='入库状态'),
        ),
        migrations.AlterField(
            model_name='selectorderdetail',
            name='device',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='baseinfo_manage.DeviceStores', verbose_name='整机型号 | 商品类别 | FRU码 | PN码 | 库存量'),
        ),
    ]
