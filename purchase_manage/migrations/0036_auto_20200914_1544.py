# Generated by Django 2.2.14 on 2020-09-14 15:44

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('purchase_manage', '0035_auto_20200909_1605'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchase_stockin_detail',
            name='pub_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='入库时间'),
        ),
    ]
