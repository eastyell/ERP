# 模块名称：业务处理模块
# 创建日期：2020-6
# 最后修改日期：2020-6
# 作者：Jason

from django.db import connection,transaction
import time

# 数据更新
def update(sql, params=None):
    """
    :param sql:
    :param params:
    :return:
    """
    cursor = connection.cursor()
    with transaction.atomic():
        try:
            if params:
                cursor.execute(sql,params)
            else:
                cursor.execute(sql)
        except Exception as e:
            print (e)

# 数据查询
def query(sql,params=None):
    cursor = connection.cursor()
    with transaction.atomic():
       try:
            if params:
                cursor.execute(sql,params)
            else:
                cursor.execute(sql)
            cds = cursor.fetchall()
            return cds
       except Exception as e:
            print (e)

# 定义自动获取订单编号，参数param传入订单类型
def getOrderNO(sql,params=None):
    cursor = connection.cursor()
    with transaction.atomic():
       try:
            if params:
                cursor.execute(sql,params)
            else:
                cursor.execute(sql)
            maxid = cursor.fetchone()
            return maxid[0]
       except Exception as e:
            print (e)

# 自动获取单据编号，参数param传入单据类型
def getOrderMaxNO(orderType):
    cursor = connection.cursor()
    with transaction.atomic():
      try:
        id = orderType.upper() + time.strftime("%Y%m%d", time.localtime()) + '%'
        if (orderType.upper()=='CGD'):
           tableName = 'purchase_manage_purchase_order'
        if (orderType.upper()=='WXLY'):
           tableName = 'stockout_manage_repair_use'
        sql = 'select max(id) from %s where id like "%s"' %(tableName,id)
        cursor.execute(sql)
        maxid = cursor.fetchone()
        MaxOrderNO = maxid[0]
        if not MaxOrderNO:
           MaxOrderNO = '001'
        else:
           # 查找倒数三个字符串为订单数字，自动加1
           MaxOrderNO = int(MaxOrderNO[-3:]) + 1
           #不足三位补0
           if (len(str(MaxOrderNO)) == 1):
               MaxOrderNO = '00' + str(MaxOrderNO)
           elif (len(MaxOrderNO) == 2):
                MaxOrderNO = '0' + str(MaxOrderNO)
           else:
                MaxOrderNO = str(MaxOrderNO)
        return orderType.upper()  + time.strftime("%Y%m%d", time.localtime()) + MaxOrderNO

      except Exception as e:
         print (e)