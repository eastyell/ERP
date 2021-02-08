# Generated by Django 2.0 on 2020-07-08 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('params_manage', '0002_auto_20200708_1740'),
    ]

    operations = [
        migrations.CreateModel(
            name='Device_FRU',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='FRU')),
                ('pub_date', models.DateField(auto_now_add=True, verbose_name='创建时间')),
                ('author', models.CharField(default=None, max_length=10, verbose_name='操作人')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
            ],
            options={
                'verbose_name_plural': 'FRU信息',
                'verbose_name': 'FRU信息',
            },
        ),
    ]