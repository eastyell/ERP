# Generated by Django 2.0 on 2020-07-15 06:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stockout_manage', '0010_auto_20200715_1403'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='device_lend',
            name='quantity',
        ),
    ]