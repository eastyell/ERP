# Generated by Django 2.2.14 on 2020-12-02 17:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('baseinfo_manage', '0020_devicestores_typename'),
    ]

    operations = [
        migrations.AlterField(
            model_name='devicestores',
            name='typename',
            field=models.ForeignKey(default='0', on_delete=django.db.models.deletion.CASCADE, to='params_manage.Device_type', verbose_name='设备类型'),
        ),
    ]
