'''
***************
Name:Sunny
Time:2020/3/12
***************
'''
import logging
import os
from common.handlepath import logs_dir
from common.handleconfig import conf


class HandleLogs(object):

    @staticmethod
    def creat_log():
        # 创建一个日志收集器
        mylog = logging.getLogger("SUNNY")
        # 设置日志收集器的收集等级
        mylog.setLevel("DEBUG")
        # 设置日志输出渠道
        # 控制台输出
        sh = logging.StreamHandler()
        # 设置输出渠道的输出等级
        sh.setLevel("INFO")
        # 将输出渠道添加到日志收集器中
        mylog.addHandler(sh)
        # 日志文件输出
        fh = logging.FileHandler(os.path.join(logs_dir,"log.log"),encoding="utf8")
        # 设置日志文件输出等级
        fh.setLevel("INFO")
        # 将输出渠道添加到日志收集器中
        mylog.addHandler(fh)
        # 创建日志输出格式对象
        form = "%(asctime)s - [%(filename)s-->line:%(lineno)d] - %(levelname)s: %(message)s"
        fm =logging.Formatter(form)
        # 设置控制台输出的格式
        sh.setFormatter(fm)
        # 设置日志文件输出的格式
        fh.setFormatter(fm)
        return mylog

log = HandleLogs.creat_log()
