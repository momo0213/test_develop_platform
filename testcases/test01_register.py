'''
***************
Name:Sunny
Time:2020/3/12
***************
'''
import os
import random
import unittest
import jsonpath
from library.ddt import ddt,data
from common.readexcel import ReadExcel
from common.handlepath import data_dir
from common.handleconfig import conf
from common.handlerequests import SendRequest
from common.handle_data import CaseData


@ddt
class TestRegister(unittest.TestCase):
    excel = ReadExcel(os.path.join(data_dir,"test_cases.xlsx"),"register")
    cases = excel.read_data()
    request = SendRequest()

    @data(*cases)
    def test_register(self,case):
        # 准备用例数据
        user = self.random_user()
        email = self.random_email()
        url = conf.get("env","url") +case["url"]
        case["data"] = case["data"].replace("@username@",user)
        case["data"] = case["data"].replace("@email@",email)
        if case["title"] == "注册失败-用户名已注册" or case["title"] == "注册失败-邮箱已注册":
            case["data"] = CaseData.replace_data(case["data"])
        data = eval(case["data"])
        print(data)
        headers = eval(conf.get("env","headers"))
        method = case["method"]
        if case["title"]!="注册成功":
            expected = eval(case["expected"])
        row = case["case_id"]+1
        # 发送请求
        response = self.request.send(url=url,json=data,headers=headers,method=method)
        res = response.json()
        if case["title"] == "注册成功":
            CaseData.pass_username = jsonpath.jsonpath(res,"$.username")[0]
            CaseData.passemail = email
            expected = eval(CaseData.replace_data(case["expected"]))
        print("预期结果",expected)
        print("实际结果",res)
        # 断言
        try:
            if case["assert"]=="u":
                self.assertEqual(res["username"],expected["username"])
            elif case["assert"]=="e":
                self.assertEqual(res["email"],expected["email"])
            elif case["assert"]=="p":
                self.assertEqual(res["password"],expected["password"])
            elif case["assert"] == "pc":
                self.assertEqual(res["password_confirm"], expected["password_confirm"])
            elif case["assert"]=="nfe":
                self.assertEqual(res["non_field_errors"],expected["non_field_errors"])

        except AssertionError as e:
            self.excel.write_data(row=row,column=8,value="不通过")
            raise e
        else:
            self.excel.write_data(row=row,column=8,value="通过")

    def random_user(self):
        username = "".join(random.sample("1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM", 6))
        return username


    def random_email(self):
        email = ("".join(random.sample("1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM", 4))
                 + random.choice(("@163.com", "@126.com", "@qq.com")))
        return email


