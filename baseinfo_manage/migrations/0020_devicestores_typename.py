# Generated by Django 2.2.14 on 2020-12-02 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('baseinfo_manage', '0019_auto_20201202_1341'),
    ]

    operations = [
        migrations.AddField(
            model_name='devicestores',
            name='typename',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='设备类型'),
        ),
    ]