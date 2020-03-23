'''
***************
Name:Sunny
Time:2020/3/19
***************
'''
import os
import unittest
import jsonpath
from common.readexcel import ReadExcel
from library.ddt import ddt, data
from common.handlerequests import SendRequest
from common.handlepath import data_dir
from common.handleconfig import conf
from common.handle_data import CaseData
from common.random_data import RandomData


@ddt
class TestInterfaces(unittest.TestCase):
    excel = ReadExcel(os.path.join(data_dir, "test_cases.xlsx"), "interfaces")
    cases = excel.read_data()
    request = SendRequest()

    @classmethod
    def setUpClass(cls):
        url = conf.get("env", "url") + "/user/login/"
        data = {
            "username": conf.get("testcase", "username"),
            "password": "123456"
        }
        headers = eval(conf.get("env", "headers"))
        response = cls.request.send(url=url, method="post", headers=headers, json=data)
        res = response.json()
        token = jsonpath.jsonpath(res, "$.token")[0]
        CaseData.token_value = "JWT" + " " + token

    @data(*cases)
    def test_interfaces(self, case):
        # 准备用例数据
        url = conf.get("env", "url") + case["url"]
        headers = eval(conf.get("env", "headers"))
        headers["Authorization"] = getattr(CaseData, "token_value")
        if case["title"] == "新增项目成功":
            case["data"] = case["data"].replace("@project@", RandomData.random_project())
        if case["title"] != "新增项目成功":
            case["data"] = case["data"].replace("@interface@", RandomData.random_interface())
            case["data"] = CaseData.replace_data(case["data"])
        case["data"]=CaseData.replace_data(case["data"])
        data = eval(case["data"])
        if case["title"]!="创建失败-接口名称字段为空":
            CaseData.pass_project = data["name"]
            CaseData.pass_interface = data["name"]
        case["expected"] = CaseData.replace_data(case["expected"])
        expected = eval(case["expected"])
        method = case["method"]
        row = case["case_id"] + 1
        # 发送请求并获取响应结果
        response = self.request.send(url=url, headers=headers, method=method, json=data)
        res = response.json()
        if case["title"] == "新增项目成功":
            CaseData.project_id = str(jsonpath.jsonpath(res, "$.id")[0])
        if case["title"] == "创建成功-创建接口成功":
            CaseData.repeat_interface = jsonpath.jsonpath(res,"$.name")[0]
        print("预期结果", expected)
        print("实际结果", res)
        # 断言
        try:
            if case["assert"] == "n":
                self.assertEqual(expected["name"], res["name"])
            elif case["assert"] == "t":
                self.assertEqual(expected["tester"], res["tester"])
            elif case["assert"] == "p":
                self.assertEqual(expected["project_id"], res["project_id"])
            elif case["assert"] == "d":
                self.assertEqual(expected["desc"], res["desc"])
            elif case["assert"] == "j":
                self.assertLessEqual(expected["project_id"], res["project_id"])
            else:
                self.assertEqual(expected["name"], res["name"])
        except AssertionError as e:
            self.excel.write_data(row=row, column=9, value="不通过")
            raise e
        else:
            self.excel.write_data(row=row, column=9, value="通过")
