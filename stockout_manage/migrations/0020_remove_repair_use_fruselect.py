# Generated by Django 2.2.14 on 2020-08-20 11:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stockout_manage', '0019_repair_use_machineselects'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='repair_use',
            name='FRUSelect',
        ),
    ]
