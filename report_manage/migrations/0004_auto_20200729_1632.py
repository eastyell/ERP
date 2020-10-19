# Generated by Django 2.0 on 2020-07-29 16:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('report_manage', '0003_auto_20200717_1549'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock_detail',
            name='FRUSelect',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='baseinfo_manage.DeviceStores', verbose_name='整机型号 | 商品类别 | FRU码 | PN码 | 库存量'),
        ),
    ]
