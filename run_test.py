'''
***************
Name:Sunny
Time:2020/3/12
***************
'''
import os
import datetime
import unittest
from library.HTMLTestRunnerNew import HTMLTestRunner
from common.handlepath import reports_dir
from testcases import test01_register,test06_creat,test07_main_stream,test03_login


# 创建一个测试套件
suite = unittest.TestSuite()
# 将测试用例加载到套件中
loader = unittest.TestLoader()
suite.addTest(loader.discover("testcases"))
# suite.addTest(loader.loadTestsFromModule(test03_login))

# 执行测试用例
current_data = datetime.datetime.now().strftime("%y-%m-%d")
runner = HTMLTestRunner(stream=open(os.path.join(reports_dir,current_data+"report.html"),"wb"),
                        title="测开平台测试报告",
                        description="用户模块，创建项目、接口、用例的测试",
                        tester="Sunny")
runner.run(suite)
