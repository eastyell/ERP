# Generated by Django 2.2.14 on 2020-12-08 16:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assets_manage', '0012_auto_20201208_1627'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gifts',
            name='pub_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='创建时间'),
        ),
    ]