# Generated by Django 2.2.14 on 2020-12-09 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assets_manage', '0015_auto_20201208_1723'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gifts',
            name='name',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='_____品名_____'),
        ),
    ]
