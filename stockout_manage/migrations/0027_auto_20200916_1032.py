# Generated by Django 2.2.14 on 2020-09-16 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stockout_manage', '0026_auto_20200915_1607'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device_lend',
            name='pub_date',
            field=models.DateField(auto_now_add=True, null=True, verbose_name='创建时间'),
        ),
    ]
