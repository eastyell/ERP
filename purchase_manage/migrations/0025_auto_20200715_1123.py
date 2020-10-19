# Generated by Django 2.0 on 2020-07-15 03:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('purchase_manage', '0024_purchase_stockin_detail_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchase_order_detail',
            name='machineSelect',
            field=models.ManyToManyField(blank=True, null=True, related_name='machineSelect', to='baseinfo_manage.DeviceStores', verbose_name='整机型号 | 商品类别 | FRU码 | PN码'),
        ),
        migrations.AlterField(
            model_name='purchase_stockin_detail',
            name='FRUSelect',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='baseinfo_manage.DeviceStores', verbose_name='整机型号 | 商品类别 | FRU码 | PN码'),
        ),
    ]
