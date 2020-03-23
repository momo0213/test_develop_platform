'''
***************
Name:Sunny
Time:2020/3/18
***************
'''
import os
import unittest
import jsonpath
from library.ddt import ddt, data
from common.readexcel import ReadExcel
from common.handlepath import data_dir
from common.handleconfig import conf
from common.handlerequests import SendRequest
from common.handle_data import CaseData


@ddt
class TestLogin(unittest.TestCase):
    excel = ReadExcel(os.path.join(data_dir, "test_cases.xlsx"), "login")
    cases = excel.read_data()
    request = SendRequest()

    @data(*cases)
    def test_login(self, case):
        # 准备用例数据
        url = conf.get("env", "url") + case["url"]
        headers = eval(conf.get("env", "headers"))
        case["data"] = CaseData.replace_data(case["data"])
        data = eval(case["data"])
        method = case["method"]
        if case["title"] != "登录成功":
            expected = eval(case["expected"])
        row = case["case_id"] + 1
        # 发送请求并获取响应结果
        response = self.request.send(url=url, method=method, headers=headers, json=data)
        res = response.json()
        if case["title"] == "登录成功":
            CaseData.pass_username = jsonpath.jsonpath(res, "$.username")[0]
            expected = eval(CaseData.replace_data(case["expected"]))
        print("预期结果：", expected)
        print("实际结果：", res)
        # 断言
        try:
            if case["assert"] == "u":
                self.assertEqual(expected["username"], res["username"])
            elif case["assert"] == "p":
                self.assertEqual(expected["password"], res["password"])
            elif case["assert"] == "n":
                self.assertEqual(expected["non_field_errors"], res["non_field_errors"])
        except AssertionError as e:
            self.excel.write_data(row=row, column=9, value="不通过")
            raise e
        else:
            self.excel.write_data(row=row, column=9, value="通过")
