# Generated by Django 2.2.14 on 2020-09-11 17:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sale_manage', '0002_auto_20200911_1702'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sales_out',
            name='price',
        ),
        migrations.RemoveField(
            model_name='sales_out',
            name='quantity',
        ),
        migrations.RemoveField(
            model_name='sales_out',
            name='shopid',
        ),
    ]