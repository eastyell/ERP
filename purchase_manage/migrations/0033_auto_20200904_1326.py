# Generated by Django 2.2.14 on 2020-09-04 13:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('purchase_manage', '0032_auto_20200901_1358'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='purchase_stockin_detail',
            options={'ordering': ['status', '-bill_id', 'purchase_id', 'shopid'], 'verbose_name': '采购入库', 'verbose_name_plural': '采购入库'},
        ),
    ]