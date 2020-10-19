# Generated by Django 2.0 on 2020-07-09 05:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('params_manage', '0003_device_fru'),
        ('baseinfo_manage', '0008_auto_20200708_1740'),
    ]

    operations = [
        migrations.AddField(
            model_name='devicestores',
            name='FRUS',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to='params_manage.Device_FRU', verbose_name='FRU码'),
        ),
    ]
