# Generated by Django 2.0 on 2020-07-17 03:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('params_manage', '0004_device_fru_desc'),
    ]

    operations = [
        migrations.AddField(
            model_name='device_kind',
            name='desc',
            field=models.CharField(default='', max_length=30, verbose_name='描述信息'),
        ),
        migrations.AlterField(
            model_name='device_fru',
            name='desc',
            field=models.CharField(default='', max_length=30, verbose_name='描述信息'),
        ),
    ]
