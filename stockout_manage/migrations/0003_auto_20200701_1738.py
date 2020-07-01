# Generated by Django 2.0 on 2020-07-01 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stockout_manage', '0002_auto_20200701_1718'),
    ]

    operations = [
        migrations.AddField(
            model_name='repair_use',
            name='machineModel',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='整机型号'),
        ),
        migrations.AddField(
            model_name='repair_use',
            name='machineSN',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='整机SN'),
        ),
        migrations.AddField(
            model_name='repair_use_stockout',
            name='machineModel',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='整机型号'),
        ),
        migrations.AddField(
            model_name='repair_use_stockout',
            name='machineSN',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='整机SN'),
        ),
    ]
