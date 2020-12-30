# 模块名称：业务处理模块
# 创建日期：2020-6
# 最后修改日期：2020-6
# 作者：Jason

from django.db import connection,transaction
import time
from email.mime.text import MIMEText
from email.header import Header
import smtplib
from xlrd import open_workbook

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
                print(sql)
                cursor.execute(sql,params)
            else:
                print(sql)
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

# 查询是否存在重复的SN备件
def querySN(sn,machinesn,id):
    if (sn != '') and (sn is not None):
        if id != '':
           sql = 'select * from report_manage_stock_detail where SN = "%s" and id <> %s' % (sn,id)
        else:
           sql = 'select * from report_manage_stock_detail where SN = "%s"' % sn
    elif (machinesn != '') and (machinesn is not None):
        if id != '':
          sql = 'select * from report_manage_stock_detail where machinesn = "%s" and id <> %s ' % (machinesn,id)
        else:
          sql = 'select * from report_manage_stock_detail where machinesn = "%s"' % machinesn
    else: sql='select * from report_manage_stock_detail  where 1 = 2'
    print(sql)
    cds = query(sql)
    return cds

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
        filedid = 'id'
        id = orderType.upper() + time.strftime("%Y%m%d", time.localtime()) + '%'
        if (orderType.upper()=='CGD'):
           tableName = 'purchase_manage_purchase_order'
        elif (orderType.upper() == 'CGRKSQ'):
           tableName = 'purchase_manage_purchase_stockin'
        elif (orderType.upper() == 'CGRK'):
           tableName = 'purchase_manage_purchase_stockin_detail'
           filedid = 'bill_id'
        elif (orderType.upper() == 'WXLY'):
           tableName = 'stockout_manage_repair_use'
        elif (orderType.upper()=='WXLYCK'):
           tableName = 'stockout_manage_repair_use_stockout'
           filedid = 'billid'
        elif (orderType.upper()=='WXFHRK'):
           tableName = 'stockin_manage_repair_use_stockin'
           filedid = 'billid'
        elif (orderType.upper()=='ZYD'):
           tableName = 'stockout_manage_device_lend'
        elif (orderType.upper()=='ZYDCK'):
           tableName = 'stockout_manage_device_lend_stockout'
           filedid = 'billid'
        elif (orderType.upper() == 'HSD'):
            tableName = 'stockin_manage_device_return'
        elif (orderType.upper() == 'HSRK'):
            tableName = 'stockin_manage_device_return_stockin'
            filedid = 'billid'
        elif (orderType.upper() == 'XSD'):
            tableName = 'sale_manage_sales_out'
        elif (orderType.upper() == 'XSDCK'):
            tableName = 'sale_manage_sales_out_stockout'
            filedid = 'billid'
        sql = 'select max(%s) from %s where  %s  like "%s"' %(filedid,tableName,filedid,id)
        print(sql)
        cursor.execute(sql)
        maxid = cursor.fetchone()
        MaxOrderNO = maxid[0]
        print(MaxOrderNO)
        if not MaxOrderNO:
           MaxOrderNO = '001'
        else:
           # 查找倒数三个字符串为订单数字，自动加1
           MaxOrderNO = int(MaxOrderNO[-3:]) + 1
           print(MaxOrderNO)
           #不足三位补0
           if (len(str(MaxOrderNO)) == 1):
               MaxOrderNO = '00' + str(MaxOrderNO)
           elif (len(str(MaxOrderNO)) == 2):
                MaxOrderNO = '0' + str(MaxOrderNO)
           else:
                MaxOrderNO = str(MaxOrderNO)
        print(MaxOrderNO)
        return orderType.upper()  + time.strftime("%Y%m%d", time.localtime()) + MaxOrderNO

      except Exception as e:
         print (e)

# 发送邮件
def send_mail(title,contents,receivers):
    # 发件人邮箱的SMTP服务器（即sender的SMTP服务器）
  # smtpserver = 'smtp.qq.com'
  sender = 'eastyell@163.com'
  msg = contents
  receiver = receivers
  mail_title = title
  mail_body = str(msg)
# 创建一个实例
  message = MIMEText(mail_body, 'plain', 'utf-8')  # 邮件正文
# (plain表示mail_body的内容直接显示，也可以用text，则mail_body的内容在正文中以文本的形式显示，需要下载）


# 邮件的发件人
  message['From'] = sender
# 邮件的收件人
#   message['To'] = receiver
# 收件人为多个收件人,通过join将列表转换为以;为间隔的字符串
  message['To'] = ";".join(receiver)

# 邮件主题
  message['Subject'] = Header(mail_title, 'utf-8')

# 创建发送邮件连接
  try:
    smtp = smtplib.SMTP_SSL("smtp.163.com", 465)
    # smtp = smtplib.SMTP_SSL("smtp.exmail.qq.com", port=465)

# 连接发送邮件的服务器
    mail_host = "smtp.163.com"  # 设置服务器
    # mail_host = "smtp.exmail.qq.com"  # 设置服务器
    smtp.connect(mail_host)

# 登录到邮件服务器
    username = 'eastyell'
    # username = 'lvjianhong@tengxiaosh.com'
    password = 'lyc8531626'
    # password = 'Ljh8531626'
    smtp.login(username, password)

# 填入邮件的相关信息并发送
    smtp.sendmail(sender, receiver, message.as_string())

    print("邮件发送成功！")
  except smtplib.SMTPException:
    print("Error: 无法发送邮件")

  smtp.quit()

# 获取邮件列表
def getmaillist(title):
   sql = 'select username,email from auth_user where id in ' \
         '(select user_id from auth_user_groups  where group_id in ' \
         '(select auth_group_permissions.group_id from auth_group_permissions where permission_id in ' \
         '(select id from auth_permission where name like "%' +  title + '%" and codename  like "%change%")' + ')) ' \
         'and (is_staff and is_active) or (is_superuser)'
   print(sql)
   cds = query(sql)
   print(cds)
   return cds

#从EXCEL中获取数据
def readExcel(xls_name):
  # 读取excel文件
  print(xls_name)
  file = open_workbook(xls_name)
  # sheet = file.sheet_by_name(sheet_name)
  print('open_Excel')
  sheet = file.sheet_by_index(0)
  # 获取所有行数；
  nrows = sheet.nrows -1
  print(nrows)
  datasTemp = []
  for i in range(nrows):
    datasTemp.append(sheet.row_values(i + 1 ))
  # for i in range(len(datasTemp)):
  #     print(datasTemp[i])
  print('success_Excel')
  return datasTemp