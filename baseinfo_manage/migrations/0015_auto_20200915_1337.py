# Generated by Django 2.2.14 on 2020-09-15 13:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('baseinfo_manage', '0014_auto_20200909_1122'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='devicestores',
            options={'ordering': ('machineModels', 'shop', 'FRUS'), 'verbose_name': '备件明细', 'verbose_name_plural': '备件明细'},
        ),
        migrations.AlterModelOptions(
            name='shop',
            options={'ordering': ('shop_type',), 'verbose_name': '备件信息', 'verbose_name_plural': '备件信息'},
        ),
    ]
