# Generated by Django 2.2.14 on 2020-09-14 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('purchase_manage', '0036_auto_20200914_1544'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchase_stockin_detail',
            name='pub_date',
            field=models.DateTimeField(default=None, null=True, verbose_name='入库时间'),
        ),
    ]
