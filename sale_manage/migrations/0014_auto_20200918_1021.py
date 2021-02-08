# Generated by Django 2.2.14 on 2020-09-18 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sale_manage', '0013_auto_20200916_1539'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sales_out',
            name='machineSelects',
            field=models.ManyToManyField(blank=True, related_name='SelectDeviceSales', to='baseinfo_manage.SelectOrderDetail', verbose_name='整机型号 | 备件类别 | FRU码 | PN码 | 库存量 | 数量 | 描述'),
        ),
    ]