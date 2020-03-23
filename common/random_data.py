'''
***************
Name:Sunny
Time:2020/3/16
***************
'''
import random

class RandomData(object):

    @staticmethod
    def random_user():
        username = "".join(random.sample("1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM", 6))
        return username

    @staticmethod
    def random_email():
        email = ("".join(random.sample("1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM", 4))
        +random.choice(("@163.com", "@126.com", "@qq.com")))
        return email

    @staticmethod
    def random_project():
        li = []
        for i in range(1,10001):
            s = "sunny的新增项目"
            s+=str(i)
            li.append(s)
        res = random.choice(li)
        return res

    @staticmethod
    def random_interface():
        li = []
        for i in range(1,10001):
            s = "sunny创建接口"
            s+=str(i)
            li.append(s)
        res = random.choice(li)
        return res

    @staticmethod
    def random_testcases():
        li = []
        for i in range(1, 10001):
            s = "sunny创建用例"
            s += str(i)
            li.append(s)
        res = random.choice(li)
        return res

if __name__=="__main__":
    res = RandomData.random_interface()
    print(res)


