# Generated by Django 2.2.14 on 2020-10-10 17:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('baseinfo_manage', '0017_auto_20200918_1049'),
        ('sale_manage', '0015_auto_20200924_1537'),
    ]

    operations = [
        migrations.AddField(
            model_name='sales_out_stockout',
            name='customer',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to='baseinfo_manage.Customers', verbose_name='销售客户'),
        ),
        migrations.AlterField(
            model_name='sales_out_stockout',
            name='customersSignid',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='baseinfo_manage.CustomersSign', verbose_name='销售客户1'),
        ),
    ]
