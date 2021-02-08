# Generated by Django 2.2.14 on 2020-12-08 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assets_manage', '0010_auto_20201010_1736'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gifts',
            name='status',
            field=models.IntegerField(choices=[(5, '已入库'), (7, '已出库'), (10, '当前库存')], default=10, verbose_name='出入库状态'),
        ),
    ]