# Generated by Django 2.0 on 2020-07-06 08:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('baseinfo_manage', '0004_auto_20200706_1043'),
        ('purchase_manage', '0005_purchase_order_detail_ifmachine'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='purchase_order_detail',
            options={'ordering': ['-bill_id'], 'verbose_name': '采购下单', 'verbose_name_plural': '采购下单'},
        ),
        migrations.AddField(
            model_name='purchase_order',
            name='machineSelect',
            field=models.ManyToManyField(blank=True, to='baseinfo_manage.DeviceStores', verbose_name='整机型号 / 商品名称 / FRU码 / PN码'),
        ),
        migrations.AlterField(
            model_name='purchase_order_detail',
            name='FRUSelect',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='baseinfo_manage.DeviceStores', verbose_name='整机型号 / 商品名称 / FRU码 / PN码'),
        ),
        migrations.AlterField(
            model_name='purchase_stockin_detail',
            name='FRUSelect',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='baseinfo_manage.DeviceStores', verbose_name='整机型号 / 商品名称 / FRU码 / PN码'),
        ),
    ]
