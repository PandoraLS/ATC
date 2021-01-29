# -*- coding: utf-8 -*-
# @Time : 2020/11/30 下午12:59

"""
程序片段, 同时输出到控制台和文件中
"""
import sys


class Logger:
    def __init__(self):
        self.terminal = sys.stdout
        self.log = open("run_log.txt", "a")

    def write(self, message):
        self.terminal.write(message)
        self.terminal.flush()
        self.log.write(message)
        self.log.flush()

    def flush(self):
        """
        this flush method is needed for python 3 compatibility.
        this handles the flush command by doing nothing.
        you might want to specify some extra behavior here.
        :return:
        """
        pass


sys.stdout = Logger()