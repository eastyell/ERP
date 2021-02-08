# Generated by Django 2.2.14 on 2020-10-13 11:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sale_manage', '0017_auto_20201010_1746'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sales_out',
            name='customersSignid',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='baseinfo_manage.CustomersSign', verbose_name='签约客户'),
        ),
        migrations.AlterField(
            model_name='sales_out_stockout',
            name='customersSignid',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='baseinfo_manage.CustomersSign', verbose_name='签约销售客户'),
        ),
    ]