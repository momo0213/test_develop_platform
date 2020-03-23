'''
***************
Name:Sunny
Time:2020/3/12
***************
'''
import os
from configparser import ConfigParser
from common.handlepath import conf_dir

class HanlderConfig(ConfigParser):

    def __init__(self,conf_file):
        super().__init__()
        self.conf_file = conf_file
        self.read(conf_file)

    def write_conf(self,section,option,value):
        self.set(section=section,option=option,value=value)
        self.write(self.conf_file)

conf = HanlderConfig(os.path.join(conf_dir,"config.ini"))
