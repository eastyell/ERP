# Generated by Django 2.2.14 on 2020-09-01 13:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('baseinfo_manage', '0012_auto_20200813_1625'),
    ]

    operations = [
        migrations.AlterField(
            model_name='devicestores',
            name='FRUS',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to='params_manage.Device_FRU', verbose_name='FRU码 / 描述'),
        ),
    ]
