# Generated by Django 2.0 on 2020-07-07 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('purchase_manage', '0009_auto_20200707_2030'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchase_order',
            name='purchasedesc',
            field=models.TextField(blank=True, null=True, verbose_name='采购说明'),
        ),
    ]
