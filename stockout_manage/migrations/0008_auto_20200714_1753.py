# Generated by Django 2.0 on 2020-07-14 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stockout_manage', '0007_repair_use_stockout_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='repair_use_stockout',
            name='author',
            field=models.CharField(default=None, max_length=10, verbose_name='出库人'),
        ),
        migrations.AlterField(
            model_name='repair_use_stockout',
            name='pub_date',
            field=models.DateField(null=True, verbose_name='出库时间'),
        ),
    ]
