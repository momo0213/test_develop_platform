'''
***************
Name:Sunny
Time:2020/3/16
***************
'''
import jsonpath
import random
from common.handleconfig import conf
from common.readexcel import ReadExcel
from common.handle_data import CaseData
from common.handlerequests import SendRequest

def random_user():
    username = "".join(random.sample("1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM", 6))
    return username


def random_email():
    email = ("".join(random.sample("1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM", 4))
             + random.choice(("@163.com", "@126.com", "@qq.com")))
    return email

def random_testcases():
    li = []
    for i in range(1, 1001):
        s = "新增项目"
        s += str(i)
        li.append(s)
    res = random.choice(li)
    return res

excel = ReadExcel(r"C:\sunny\test_develop_platform\data\test_cases.xlsx","creatcases")
case = excel.read_data()
request = SendRequest()

# user = random_user()
# em = random_email()
url = conf.get("env", "url") + case["url"]

# case[0]["data"] = case[0]["data"].replace("@username@",user)
# case[0]["data"] = case[0]["data"].replace("@email@",em)
case["data"] = CaseData.replace_data(case["data"])
case["data"] = case["data"].replace("@testcases@",random_testcases())
data = eval(case["data"])
CaseData.pass_testcases = data["name"]

expected = eval(case["expected"])
headers = eval(conf.get("env", "headers"))
headers["Authorization"] = "JWT"+" "+"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxNDcsInVzZXJuYW1lIjoic3VubnkwMSIsImV4cCI6MTU4NDkzNTQ3NCwiZW1haWwiOiIxMTE3MkAxNjMuY29tIn0.pVMYwMnzUeuspM0MrqF_ssd5f4qbaOzwmBMvpTFcg7Y"
method = case["method"]
row = case["case_id"] + 1
# 发送请求
response = request.send(url=url, json=data, headers=headers, method=method)
res = response.json()
if case["assert"] == "ni":
    expected = eval(CaseData.replace_data(case["expected"]))

print(res)
# CaseData.pass_username = jsonpath.jsonpath(res, "$.username")[0]
# print(CaseData.pass_username)
# CaseData.pass_email = em
# print(getattr(CaseData,"pass_email"))





