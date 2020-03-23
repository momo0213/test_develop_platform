'''
***************
Name:Sunny
Time:2020/3/13
***************
'''
'''
qq邮箱：smtp.qq.com  端口：465
163邮箱：smtp.163.com  端口：465

QQ邮箱账号:418040021@qq.com
smtp服务授权码:yqrsvrauiwaybhdi

'''

import smtplib
from email.mime.text import MIMEText

smtp = smtplib.SMTP_SSL(host="smtp.qq.com",port=465)
smtp.login(user="418040021@qq.com",password="yqrsvrauiwaybhdi")
