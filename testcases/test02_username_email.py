'''
***************
Name:Sunny
Time:2020/3/18
***************
'''
import os
import unittest
from library.ddt import ddt, data
from common.readexcel import ReadExcel
from common.handlerequests import SendRequest
from common.handlepath import data_dir
from common.handleconfig import conf
from common.handle_data import CaseData


@ddt
class TestUser(unittest.TestCase):
    excel = ReadExcel(os.path.join(data_dir, "test_cases.xlsx"), "username_email")
    cases = excel.read_data()
    request = SendRequest()

    @data(*cases)
    def test_user(self, case):
        # 准备用例数据
        url = conf.get("env", "url") + CaseData.replace_data(case["url"])
        data = eval(case["data"])
        headers = eval(conf.get("env", "headers"))
        method = case["method"]
        expected = eval(case["expected"])
        row = case["case_id"] + 1
        # 发送请求，获取相应结果
        reponse = self.request.send(url=url, method=method, headers=headers, params=data)
        res = reponse.json()
        print("预期结果",expected)
        print("实际结果",res)
        # 断言
        try:
            self.assertEqual(res["count"], expected["count"])
        except AssertionError as e:
            self.excel.write_data(row=row, column=8, value="不通过")
            raise e
        else:
            self.excel.write_data(row=row, column=8, value="通过")
