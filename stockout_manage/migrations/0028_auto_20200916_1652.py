# Generated by Django 2.2.14 on 2020-09-16 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stockout_manage', '0027_auto_20200916_1032'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device_lend',
            name='pub_date',
            field=models.DateField(auto_now_add=True, null=True, verbose_name='创建日期'),
        ),
        migrations.AlterField(
            model_name='device_lend',
            name='update_time',
            field=models.DateTimeField(default=None, null=True, verbose_name='下单时间'),
        ),
        migrations.AlterField(
            model_name='device_lend_stockout',
            name='update_time',
            field=models.DateField(auto_now=True, null=True, verbose_name='创建日期'),
        ),
    ]