# Generated by Django 2.2.14 on 2020-12-08 16:27

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('assets_manage', '0011_auto_20201208_1129'),
    ]

    operations = [
        migrations.AddField(
            model_name='gifts',
            name='pub_date',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='创建时间'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='gifts',
            name='quantity_inout',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='出入库数量'),
        ),
        migrations.AlterField(
            model_name='gifts',
            name='remark',
            field=models.TextField(blank=True, null=True, verbose_name='_____备注_____'),
        ),
    ]
