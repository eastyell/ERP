# Generated by Django 2.0 on 2020-07-08 08:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('baseinfo_manage', '0005_auto_20200708_1019'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='devicestores',
            options={'verbose_name': '商品明细', 'verbose_name_plural': '商品明细'},
        ),
        migrations.AlterField(
            model_name='devicestores',
            name='descs',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='商品描述'),
        ),
        migrations.AlterField(
            model_name='devicestores',
            name='shop',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to='baseinfo_manage.Shop', verbose_name='商品类别'),
        ),
    ]
