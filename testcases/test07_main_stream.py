'''
***************
Name:Sunny
Time:2020/3/23
***************
'''
import os
import unittest
import jsonpath
from library.ddt import ddt, data
from common.readexcel import ReadExcel
from common.random_data import RandomData
from common.handlepath import data_dir
from common.handle_data import CaseData
from common.handleconfig import conf
from common.handlerequests import SendRequest
from common.hadlelogs import log
from common.random_data import RandomData


@ddt
class TestMainStream(unittest.TestCase):
    excel = ReadExcel(os.path.join(data_dir, "test_cases.xlsx"), "main_stream")
    cases = excel.read_data()
    request = SendRequest()

    @data(*cases)
    def test_main_stream(self, case):
        # 准备用例数据
        url = conf.get("env", "url") + CaseData.replace_data(case["url"])
        headers = eval(conf.get("env", "headers"))
        if case["interface"]=="projects" or case["interface"]=="interfaces" or case["interface"]=="testcases":
            headers["Authorization"] = getattr(CaseData,"token_value")
        case["data"] = CaseData.replace_data(case["data"])
        if case["interface"]=="register":
            case["data"]=case["data"].replace("@username@",RandomData.random_user())
            CaseData.pass_username = eval(case["data"])["username"]
            case["data"]=case["data"].replace("@email@",RandomData.random_email())
            CaseData.pass_email = eval(case["data"])["email"]
        if case["interface"]=="projects":
            case["data"]=case["data"].replace("@project@",RandomData.random_project())
            CaseData.pass_project = eval(case["data"])["name"]
        if case["interface"] == "interfaces":
            case["data"] = case["data"].replace("@interface@", RandomData.random_interface())
            CaseData.pass_interface = eval(case["data"])["name"]
        if case["interface"] == "testcases":
            case["data"] = case["data"].replace("@testcases@", RandomData.random_testcases())
            CaseData.pass_testcases = eval(case["data"])["name"]
        # case["data"] = CaseData.replace_data(case["data"])
        data = eval(case["data"])
        case["expected"] = CaseData.replace_data(case["expected"])
        expected = eval(case["expected"])
        method = case["method"]
        row = case["case_id"] + 1
        # 发送请求并获取响应结果
        response = self.request.send(url=url, method=method, headers=headers, json=data)
        res = response.json()
        print(res)
        if case["interface"]=="login":
            token = jsonpath.jsonpath(res,"$.token")[0]
            CaseData.token_value = "JWT"+" "+token
        if case["interface"]=="projects":
            CaseData.project_id = str(jsonpath.jsonpath(res,"$.id")[0])
        if case["interface"] == "interfaces":
            CaseData.interface_id = str(jsonpath.jsonpath(res,"$.id")[0])
        print("预期结果：",expected)
        print("实际结果：",res)
        # 断言
        try:
            if case["assert"] == "c":
                self.assertEqual(expected["count"],res["count"])
            elif case["assert"] == "u":
                self.assertEqual(expected["username"],res["username"])
            else:
                self.assertEqual(expected["name"],res["name"])
        except AssertionError as e:
            self.excel.write_data(row=row,column=9,value="不通过")
            log.error("用例：{}执行结果不通过".format(case["title"]))
            log.exception(e)
            raise e
        else:
            self.excel.write_data(row=row,column=9,value="通过")
            log.info("用例：{}执行通过".format(case["title"]))
