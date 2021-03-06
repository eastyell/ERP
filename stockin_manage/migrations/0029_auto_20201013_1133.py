# Generated by Django 2.2.14 on 2020-10-13 11:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('baseinfo_manage', '0017_auto_20200918_1049'),
        ('stockin_manage', '0028_auto_20200924_1537'),
    ]

    operations = [
        migrations.AddField(
            model_name='repair_use_stockin',
            name='customer',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to='baseinfo_manage.Customers', verbose_name='所属项目'),
        ),
        migrations.AlterField(
            model_name='repair_use_stockin',
            name='customersSignid',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='baseinfo_manage.CustomersSign', verbose_name='所属签约项目'),
        ),
    ]
