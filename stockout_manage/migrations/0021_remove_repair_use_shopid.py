# Generated by Django 2.2.14 on 2020-08-20 11:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stockout_manage', '0020_remove_repair_use_fruselect'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='repair_use',
            name='shopid',
        ),
    ]
