# Generated by Django 2.2.14 on 2020-09-15 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stockin_manage', '0021_auto_20200915_1337'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device_return',
            name='pub_date',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建时间'),
        ),
        migrations.AlterField(
            model_name='device_return',
            name='update_time',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='下单时间'),
        ),
    ]
