# Generated by Django 2.2.14 on 2020-09-18 10:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('baseinfo_manage', '0015_auto_20200915_1337'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='devicestores',
            options={'ordering': ('shop', 'machineModels', 'FRUS'), 'verbose_name': '备件明细', 'verbose_name_plural': '备件明细'},
        ),
        migrations.CreateModel(
            name='SelectOrderDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('desc', models.CharField(blank=True, max_length=50, null=True, verbose_name='备件描述')),
                ('quantity', models.IntegerField(blank=True, default=1, null=True, verbose_name='申请数量')),
                ('device', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='baseinfo_manage.DeviceStores', verbose_name='整机型号 | 备件类别 | FRU码 | PN码 | 库存量')),
                ('shopid', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='baseinfo_manage.Shop', verbose_name='备件类别')),
            ],
            options={
                'verbose_name_plural': '备件选择明细',
                'verbose_name': '备件选择明细',
                'ordering': ['device'],
            },
        ),
    ]
