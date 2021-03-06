# Generated by Django 2.2.14 on 2020-09-22 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('report_manage', '0016_auto_20200921_1534'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workflow_query',
            name='author1',
            field=models.CharField(default=None, max_length=10, null=True, verbose_name='操作人1'),
        ),
        migrations.AlterField(
            model_name='workflow_query',
            name='author2',
            field=models.CharField(default=None, max_length=10, null=True, verbose_name='操作人2'),
        ),
        migrations.AlterField(
            model_name='workflow_query',
            name='author3',
            field=models.CharField(default=None, max_length=10, null=True, verbose_name='操作人3'),
        ),
        migrations.AlterField(
            model_name='workflow_query',
            name='name1',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='单据号1'),
        ),
        migrations.AlterField(
            model_name='workflow_query',
            name='name2',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='单据号2'),
        ),
        migrations.AlterField(
            model_name='workflow_query',
            name='name3',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='单据号3'),
        ),
        migrations.AlterField(
            model_name='workflow_query',
            name='update_time1',
            field=models.DateTimeField(default=None, null=True, verbose_name='提交时间1'),
        ),
        migrations.AlterField(
            model_name='workflow_query',
            name='update_time2',
            field=models.DateTimeField(default=None, null=True, verbose_name='提交时间2'),
        ),
        migrations.AlterField(
            model_name='workflow_query',
            name='update_time3',
            field=models.DateTimeField(default=None, null=True, verbose_name='提交时间4'),
        ),
    ]
