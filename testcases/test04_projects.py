'''
***************
Name:Sunny
Time:2020/3/18
***************
'''
import os
import unittest
import random
import jsonpath
from library.ddt import ddt,data
from common.readexcel import ReadExcel
from common.handlepath import data_dir
from common.handlerequests import SendRequest
from common.handleconfig import conf
from common.handle_data import CaseData


@ddt
class TestProjects(unittest.TestCase):
    excel = ReadExcel(os.path.join(data_dir,"test_cases.xlsx"),"projects")
    cases = excel.read_data()
    request = SendRequest()

    @classmethod
    def setUpClass(cls):
        url = conf.get("env","url")+"/user/login/"
        headers = eval(conf.get("env","headers"))
        data = {
            "username":conf.get("testcase","username"),
            "password":"123456"
        }
        response = cls.request.send(url=url,method="post",headers=headers,json=data)
        res = response.json()
        token = jsonpath.jsonpath(res,"$.token")[0]
        CaseData.token_value = "JWT"+" "+token


    @data(*cases)
    def test_projects(self,case):
        # 准备用例数据
        url = conf.get("env","url")+case["url"]
        headers = eval(conf.get("env","headers"))
        headers["Authorization"] = getattr(CaseData,"token_value")
        case["data"] = case["data"].replace("@project@",self.random_project())
        data = eval(case["data"])
        if case["title"] != "新增失败—项目名称为空":
            CaseData.pass_project = data["name"]
        case["expected"] = CaseData.replace_data(case["expected"])
        expected = eval(case["expected"])
        method = case["method"]
        row = case["case_id"]+1
        # 发送请求并获取响应结果
        response = self.request.send(url=url,method=method,json=data,headers=headers)
        res = response.json()
        print("预期结果",expected)
        print("实际结果",res)
        # 断言
        try:
            if case["assert"] == "n":
                self.assertEqual(expected["name"],res["name"])
            elif case["assert"] == "l":
                self.assertEqual(expected["leader"], res["leader"])
            elif case["assert"] == "t":
                self.assertEqual(expected["tester"], res["tester"])
            elif case["assert"] == "p":
                self.assertEqual(expected["programmer"], res["programmer"])
            elif case["assert"] == "pa":
                self.assertEqual(expected["publish_app"], res["publish_app"])
            elif case["assert"] == "d":
                self.assertEqual(expected["desc"], res["desc"])
            else:
                self.assertEqual(expected["name"],res["name"])
        except AssertionError as e:
            self.excel.write_data(row=row,column=8,value="不通过")
            raise e
        else:
            self.excel.write_data(row=row,column=8,value="通过")

    def random_project(self):
        li = []
        for i in range(1, 10001):
            s = "新增项目"
            s += str(i)
            li.append(s)
        res = random.choice(li)
        return res
