# Generated by Django 2.0 on 2020-07-02 05:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('purchase_manage', '0002_auto_20200701_1738'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchase_stockin_detail',
            name='SN',
            field=models.CharField(blank=True, max_length=15, null=True, verbose_name='SN码'),
        ),
    ]