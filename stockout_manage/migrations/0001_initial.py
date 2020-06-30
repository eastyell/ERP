# Generated by Django 2.0 on 2020-06-30 09:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('baseinfo_manage', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Device_lend',
            fields=[
                ('id', models.CharField(max_length=12, primary_key=True, serialize=False, verbose_name='租用单号')),
                ('quantity', models.IntegerField(verbose_name='数量')),
                ('price', models.FloatField(verbose_name='价格')),
                ('date_begin', models.DateField(null=True, verbose_name='起租日期')),
                ('date_end', models.DateField(null=True, verbose_name='讫租日期')),
                ('remark', models.CharField(max_length=100, verbose_name='备注')),
                ('pub_date', models.DateField(auto_now_add=True, null=True, verbose_name='下单时间')),
                ('author', models.CharField(default=None, max_length=10, verbose_name='入库人')),
                ('update_time', models.DateTimeField(auto_now=True, null=True, verbose_name='更新时间')),
                ('shopid', models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to='baseinfo_manage.Shop', verbose_name='商品名称')),
            ],
            options={
                'verbose_name': '租用下单',
                'verbose_name_plural': '租用下单',
            },
        ),
        migrations.CreateModel(
            name='Device_lend_stockout',
            fields=[
                ('id', models.CharField(max_length=12, primary_key=True, serialize=False, verbose_name='租用单号')),
                ('quantity', models.IntegerField(verbose_name='数量')),
                ('price', models.FloatField(verbose_name='价格')),
                ('date_begin', models.DateField(null=True, verbose_name='起租日期')),
                ('date_end', models.DateField(null=True, verbose_name='讫租日期')),
                ('remark', models.CharField(max_length=100, verbose_name='备注')),
                ('pub_date', models.DateField(auto_now_add=True, null=True, verbose_name='出库时间')),
                ('author', models.CharField(default=None, max_length=10, verbose_name='出库人')),
                ('update_time', models.DateTimeField(auto_now=True, null=True, verbose_name='更新时间')),
                ('shopid', models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to='baseinfo_manage.Shop', verbose_name='商品名称')),
            ],
            options={
                'verbose_name': '租用出库',
                'verbose_name_plural': '租用出库',
            },
        ),
        migrations.CreateModel(
            name='Repair_use',
            fields=[
                ('id', models.CharField(max_length=30, primary_key=True, serialize=False, verbose_name='维修领用单号')),
                ('SN', models.CharField(blank=True, max_length=15, null=True, verbose_name='SN码')),
                ('FRU', models.CharField(blank=True, max_length=15, null=True, verbose_name='FRU码')),
                ('PN', models.CharField(blank=True, max_length=15, null=True, verbose_name='PN码')),
                ('desc', models.CharField(blank=True, max_length=50, null=True, verbose_name='描述')),
                ('source', models.CharField(blank=True, max_length=30, null=True, verbose_name='来源')),
                ('replace', models.CharField(blank=True, max_length=15, null=True, verbose_name='替代号')),
                ('useage', models.IntegerField(default=0, verbose_name='使用年限')),
                ('price', models.FloatField(default=1, verbose_name='单价')),
                ('quantity', models.IntegerField(default=1, verbose_name='数量')),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/%m%d', verbose_name='图片')),
                ('remark', models.TextField(blank=True, null=True, verbose_name='备注')),
                ('pub_date', models.DateTimeField(auto_now_add=True, null=True, verbose_name='下单时间')),
                ('author', models.CharField(default=None, max_length=10, verbose_name='下单人')),
                ('update_time', models.DateTimeField(auto_now=True, null=True, verbose_name='修改时间')),
                ('FRUSelect', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='baseinfo_manage.DeviceStores', verbose_name='FRU码 / PN码 / 整机型号')),
                ('shopid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='baseinfo_manage.Shop', verbose_name='商品名称')),
            ],
            options={
                'verbose_name': '维修领用下单',
                'verbose_name_plural': '维修领用下单',
            },
        ),
        migrations.CreateModel(
            name='Repair_use_stockout',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('billid', models.CharField(blank=True, max_length=30, null=True, verbose_name='维修领用出库单')),
                ('SN', models.CharField(blank=True, max_length=15, null=True, verbose_name='SN码')),
                ('FRU', models.CharField(blank=True, max_length=15, null=True, verbose_name='FRU码')),
                ('PN', models.CharField(blank=True, max_length=15, null=True, verbose_name='PN码')),
                ('desc', models.CharField(blank=True, max_length=50, null=True, verbose_name='描述')),
                ('source', models.CharField(blank=True, max_length=30, null=True, verbose_name='来源')),
                ('replace', models.CharField(blank=True, max_length=15, null=True, verbose_name='替代号')),
                ('useage', models.IntegerField(default=0, verbose_name='使用年限')),
                ('price', models.FloatField(default=1, verbose_name='单价')),
                ('quantity', models.IntegerField(default=1, verbose_name='数量')),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/%m%d', verbose_name='图片')),
                ('remark', models.TextField(blank=True, null=True, verbose_name='备注')),
                ('pub_date', models.DateTimeField(auto_now_add=True, null=True, verbose_name='下单时间')),
                ('author', models.CharField(default=None, max_length=10, verbose_name='下单人')),
                ('update_time', models.DateTimeField(auto_now=True, null=True, verbose_name='修改时间')),
                ('FRUSelect', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='baseinfo_manage.DeviceStores', verbose_name='FRU码 / PN码 / 整机型号')),
                ('repairid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stockout_manage.Repair_use', verbose_name='维修领用单号')),
                ('shopid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='baseinfo_manage.Shop', verbose_name='商品名称')),
            ],
            options={
                'verbose_name': '维修领用出库',
                'verbose_name_plural': '维修领用出库',
            },
        ),
    ]
