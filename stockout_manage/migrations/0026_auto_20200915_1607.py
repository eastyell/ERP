# Generated by Django 2.2.14 on 2020-09-15 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stockout_manage', '0025_auto_20200915_1524'),
    ]

    operations = [
        migrations.AlterField(
            model_name='repair_use',
            name='pub_date',
            field=models.DateField(auto_now_add=True, null=True, verbose_name='创建时间'),
        ),
        migrations.AlterField(
            model_name='repair_use',
            name='update_time',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='下单时间'),
        ),
    ]
