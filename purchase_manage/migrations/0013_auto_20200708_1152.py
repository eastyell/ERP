# Generated by Django 2.0 on 2020-07-08 03:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('purchase_manage', '0012_auto_20200708_1144'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchase_order',
            name='machineSelect',
            field=models.ManyToManyField(blank=True, null=True, related_name='machineSelectOrder', to='baseinfo_manage.DeviceStores', verbose_name='整机型号 / 商品名称 / FRU码 / PN码'),
        ),
    ]
