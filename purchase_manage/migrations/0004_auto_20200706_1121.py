# Generated by Django 2.0 on 2020-07-06 03:21

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('purchase_manage', '0003_auto_20200702_1357'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='purchase_order',
            options={'verbose_name': '采购申请', 'verbose_name_plural': '采购申请'},
        ),
        migrations.AddField(
            model_name='purchase_order',
            name='ifimportant',
            field=models.IntegerField(choices=[(0, '一般'), (1, '紧急')], default=0, verbose_name='是否加急'),
        ),
        migrations.AlterField(
            model_name='purchase_stockin_detail',
            name='pub_date',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='入库时间'),
        ),
    ]
