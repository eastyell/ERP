from django.apps import AppConfig

class StockoutManageConfig(AppConfig):
    name = 'stockout_manage'
    verbose_name = u'5 其他出库'
    orderIndex_ = 5
    model_icon = 'fa fa-user'  # 图标样式