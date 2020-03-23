'''
***************
Name:Sunny
Time:2020/3/12
***************
'''
'''
数据库地址：120.78.128.25
port：3306
用户：future
密码：123456
'''
import pymysql
from common.handleconfig import conf

class HandleMysql(object):
    def __init__(self):
        # 连接数据库
        self.connect = pymysql.connect(host=conf.get("bd","host"),
                                  port=conf.getint("bd","port"),
                                  user=conf.get("bd","user"),
                                  password=conf.get("bd","password"),
                                  charset="utf8",
                                  cursorclass=pymysql.cursors.DictCursor)
        # 创建一个游标对象
        self.cur = self.connect.cursor()
    def find_one(self,sql):
        self.connect.commit()
        self.cur.execute(sql)
        res = self.cur.fetchone()
        return res

    def find_all(self,sql):
        self.connect.commit()
        self.cur.execute(sql)
        res = self.cur.fetchall()
        return res

    def close(self):
        self.cur.close()
        self.connect.connect()



