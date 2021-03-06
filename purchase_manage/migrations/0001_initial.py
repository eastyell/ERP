# Generated by Django 2.0 on 2020-07-01 05:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('params_manage', '0001_initial'),
        ('baseinfo_manage', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Purchase_order',
            fields=[
                ('id', models.CharField(max_length=18, primary_key=True, serialize=False, verbose_name='采购单号')),
                ('desc', models.CharField(blank=True, max_length=50, null=True, verbose_name='描述')),
                ('quantity', models.IntegerField(blank=True, default=1, null=True, verbose_name='采购数量')),
                ('price', models.FloatField(blank=True, null=True, verbose_name='采购价格')),
                ('amount', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=12, null=True, verbose_name='采购总价')),
                ('remark', models.CharField(blank=True, max_length=100, null=True, verbose_name='备注')),
                ('pub_date', models.DateField(auto_now_add=True, null=True, verbose_name='创建时间')),
                ('author', models.CharField(default=None, max_length=10, verbose_name='下单人')),
                ('update_time', models.DateTimeField(auto_now=True, null=True, verbose_name='修改时间')),
                ('purchase_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='params_manage.Purchase_type', verbose_name='采购类型')),
                ('shopid', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='baseinfo_manage.Shop', verbose_name='商品名称')),
                ('suppliersid', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='baseinfo_manage.Suppliers', verbose_name='供应商名称')),
            ],
            options={
                'verbose_name_plural': '采购单',
                'verbose_name': '采购单',
            },
        ),
        migrations.CreateModel(
            name='Purchase_order_detail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
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
                ('pub_date', models.DateField(auto_now_add=True, null=True, verbose_name='创建时间')),
                ('author', models.CharField(default=None, max_length=10, verbose_name='下单人')),
                ('update_time', models.DateTimeField(auto_now=True, null=True, verbose_name='修改时间')),
                ('FRUSelect', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='baseinfo_manage.DeviceStores', verbose_name='FRU码 / PN码 / 整机型号')),
                ('bill_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='purchase_manage.Purchase_order', verbose_name='采购单号')),
                ('shopid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='baseinfo_manage.Shop', verbose_name='商品名称')),
            ],
            options={
                'verbose_name_plural': '采购下单',
                'verbose_name': '采购下单',
            },
        ),
        migrations.CreateModel(
            name='Purchase_return',
            fields=[
                ('id', models.CharField(max_length=12, primary_key=True, serialize=False, verbose_name='采购退货单号')),
                ('quantity', models.IntegerField(verbose_name='退货数量')),
                ('price', models.FloatField(verbose_name='价格')),
                ('reason', models.CharField(max_length=300, verbose_name='退货原因')),
                ('remark', models.CharField(max_length=100, verbose_name='备注')),
                ('pub_date', models.DateField(auto_now_add=True, null=True, verbose_name='退单时间')),
                ('author', models.CharField(default=None, max_length=10, verbose_name='退单人')),
                ('update_time', models.DateTimeField(auto_now=True, null=True, verbose_name='更新时间')),
                ('purchase_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='purchase_manage.Purchase_order', verbose_name='进货单号')),
                ('shopid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='baseinfo_manage.Shop', verbose_name='商品名称')),
            ],
            options={
                'verbose_name_plural': '采购退货下单',
                'verbose_name': '采购退货下单',
            },
        ),
        migrations.CreateModel(
            name='Purchase_returnout',
            fields=[
                ('id', models.CharField(max_length=12, primary_key=True, serialize=False, verbose_name='采购入库单号')),
                ('quantity', models.IntegerField(verbose_name='退货数量')),
                ('price', models.FloatField(verbose_name='退货价格')),
                ('remark', models.CharField(max_length=100, verbose_name='备注')),
                ('pub_date', models.DateField(auto_now_add=True, null=True, verbose_name='出库时间')),
                ('author', models.CharField(default=None, max_length=10, verbose_name='出库人')),
                ('update_time', models.DateTimeField(auto_now=True, null=True, verbose_name='更新时间')),
                ('purchase_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='purchase_manage.Purchase_order', verbose_name='采购单号')),
                ('shopid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='baseinfo_manage.Shop', verbose_name='商品名称')),
            ],
            options={
                'verbose_name_plural': '采购退货出库',
                'verbose_name': '采购退货出库',
            },
        ),
        migrations.CreateModel(
            name='Purchase_stockin',
            fields=[
                ('id', models.CharField(max_length=30, primary_key=True, serialize=False, verbose_name='采购入库单号')),
                ('quantity', models.IntegerField(default=1, verbose_name='采购数量')),
                ('price', models.FloatField(verbose_name='采购金额')),
                ('remark', models.TextField(blank=True, null=True, verbose_name='备注')),
                ('pub_date', models.DateField(auto_now_add=True, null=True, verbose_name='创建时间')),
                ('author', models.CharField(default=None, max_length=10, verbose_name='入库人')),
                ('update_time', models.DateTimeField(auto_now=True, null=True, verbose_name='更新时间')),
                ('purchase_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='purchase_manage.Purchase_order', verbose_name='采购单号')),
                ('shopid', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='baseinfo_manage.Shop', verbose_name='商品名称')),
                ('suppliersid', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='baseinfo_manage.Suppliers', verbose_name='供应商名称')),
            ],
            options={
                'verbose_name_plural': '采购入库单',
                'verbose_name': '采购入库单',
            },
        ),
        migrations.CreateModel(
            name='Purchase_stockin_detail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bill_id', models.CharField(blank=True, max_length=30, null=True, verbose_name='采购入库单号')),
                ('SN', models.CharField(max_length=15, null=True, verbose_name='SN码')),
                ('FRU', models.CharField(max_length=15, null=True, verbose_name='FRU码')),
                ('PN', models.CharField(blank=True, max_length=15, null=True, verbose_name='PN码')),
                ('desc', models.CharField(blank=True, max_length=50, null=True, verbose_name='描述')),
                ('source', models.CharField(blank=True, max_length=30, null=True, verbose_name='来源')),
                ('replace', models.CharField(blank=True, max_length=15, null=True, verbose_name='替代号')),
                ('useage', models.IntegerField(verbose_name='使用年限')),
                ('price', models.FloatField(verbose_name='单价')),
                ('quantity', models.IntegerField(default=1, verbose_name='数量')),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/%m%d', verbose_name='图片')),
                ('remark', models.TextField(blank=True, null=True, verbose_name='备注')),
                ('pub_date', models.DateField(null=True, verbose_name='入库时间')),
                ('author', models.CharField(default=None, max_length=10, verbose_name='入库人')),
                ('update_time', models.DateTimeField(auto_now=True, null=True, verbose_name='更新时间')),
                ('FRUSelect', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='baseinfo_manage.DeviceStores', verbose_name='FRU码 / PN码 / 整机型号')),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='params_manage.Location', verbose_name='库存位置')),
                ('purchase_id', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='purchase_manage.Purchase_order_detail', verbose_name='采购单号')),
                ('shopid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='baseinfo_manage.Shop', verbose_name='商品名称')),
            ],
            options={
                'verbose_name_plural': '采购入库',
                'verbose_name': '采购入库',
            },
        ),
    ]
