'''
***************
Name:Sunny
Time:2020/3/12
***************
'''
import os


base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# conf目录的地址
conf_dir = os.path.join(base_dir,"conf")
# logs目录的地址
logs_dir = os.path.join(base_dir,"logs")
# data目录的地址
data_dir = os.path.join(base_dir,"data")
# reports目录的地址
reports_dir = os.path.join(base_dir,"reports")
# testcases目录的地址
restcases_dir = os.path.join(base_dir,"testcases")