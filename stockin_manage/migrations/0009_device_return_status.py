# Generated by Django 2.0 on 2020-07-20 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stockin_manage', '0008_auto_20200720_1631'),
    ]

    operations = [
        migrations.AddField(
            model_name='device_return',
            name='status',
            field=models.IntegerField(choices=[(0, '待办'), (1, '已办'), (2, '已下单'), (3, '已入库')], default=0, verbose_name='回收状态'),
        ),
    ]
