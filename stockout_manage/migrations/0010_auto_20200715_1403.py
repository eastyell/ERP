# Generated by Django 2.0 on 2020-07-15 06:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stockout_manage', '0009_auto_20200715_1123'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device_lend',
            name='quantity',
            field=models.IntegerField(default=0, verbose_name='数量'),
        ),
    ]
