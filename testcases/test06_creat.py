'''
***************
Name:Sunny
Time:2020/3/20
***************
'''
import os
import unittest
import jsonpath
from common.readexcel import ReadExcel
from library.ddt import ddt, data
from common.handlepath import data_dir
from common.handlerequests import SendRequest
from common.handleconfig import conf
from common.handle_data import CaseData
from common.random_data import RandomData


@ddt
class TestCreatCases(unittest.TestCase):
    excel = ReadExcel(os.path.join(data_dir, "test_cases.xlsx"), "creatcases")
    cases = excel.read_data()
    request = SendRequest()

    @classmethod
    def setUpClass(cls):
        # 执行用例前先登录系统
        url = conf.get("env", "url") + "/user/login/"
        headers = eval(conf.get("env", "headers"))
        data = {
            "username": conf.get("testcase", "username"),
            "password": "123456"
        }
        reponse = cls.request.send(url=url, headers=headers, method="post", json=data)
        res = reponse.json()
        token = jsonpath.jsonpath(res, "$.token")[0]
        CaseData.token_value = "JWT" + " " + token

    @data(*cases)
    def test_creatcases(self, case):
        # 准备用例数据
        url = conf.get("env", "url") + case["url"]
        headers = eval(conf.get("env", "headers"))
        headers["Authorization"] = getattr(CaseData, "token_value")
        case["data"] = CaseData.replace_data(case["data"])
        case["data"] = case["data"].replace("@testcases@", RandomData.random_testcases())
        if case["title"] == "新增项目成功":
            case["data"] = case["data"].replace("@project@", RandomData.random_project())
            CaseData.pass_project = eval(case["data"])["name"]
        if case["title"] == "创建成功-创建接口成功":
            case["data"] = case["data"].replace("@interface@", RandomData.random_interface())
            CaseData.pass_interface = eval(case["data"])["name"]
        data = eval(case["data"])
        if case["title"] != "创建失败-用例名称为空":
            CaseData.pass_testcases = data["name"]
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
            CaseData.interface_id = str(jsonpath.jsonpath(res, "$.id")[0])
        if case["title"]=="创建成功-用例创建成功":
            CaseData.repeat_testcases=jsonpath.jsonpath(res,"$.name")[0]
        print("预期结果：", expected)
        print("实际结果：", res)
        # 断言
        try:
            if case["assert"] == "n":
                self.assertEqual(expected["name"], res["name"])
            elif case["assert"] == "ni":
                self.assertEqual(expected["name"], res["name"])
                self.assertEqual(expected["interface"], res["interface"])
            elif case["assert"] == "i":
                self.assertEqual(expected["interface"], res["interface"])
            elif case["assert"] == "a":
                self.assertEqual(expected["author"], res["author"])
            elif case["assert"] == "r":
                self.assertEqual(expected["request"], res["request"])
        except AssertionError as e:
            self.excel.write_data(row=row, column=9, value="不通过")
            raise e
        else:
            self.excel.write_data(row=row, column=9, value="通过")
