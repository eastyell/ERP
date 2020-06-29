# 模块名称：自定义常量
# 创建日期：2020-6
# 最后修改日期：2020-6
# 作者：Jason

from django.db import connection

# 备件类别
device_type = (
    (0, '新购'),
    (1, '回收'),
)

# 潜在客户状态
customersLatent_status = (
    (0, '跟进中'),
    (1, '已签约'),
)

# 合同类型
Contract_type = (
    (0, '维护服务类'),
    (1, '产品销售类'),
)

# 合同项目状态
customersSign_status = (
    (0, '维护中'),
    (1, '结束'),
)

# 合同收款情况
contract_paystatus = (
    (0, '未收款'),
    (1, '已收款'),
)

# 项目需求是否解决
virtual_choice = (
    (0, '否'),
    (1, '是'),
)