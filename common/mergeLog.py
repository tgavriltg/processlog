#!/usr/bin/env python
#coding:utf-8

import json,copy

class mergeLog:
    """
    父类（完成以下功能）：
        1.初始化数据。
        2.重置数据，到intervalSecond时间后，重置数据到初始化。
        3.获取数据到一个临时变量中。
    """
    def __init__(self,_logTag,_mergeKeyList,_logging):
        self.logTag = _logTag
        self.mergeKeyList = _mergeKeyList
        self.logging = _logging
        self.initData()
        self.resetData()

    def initData(self):
        """初始化数据，把一个list初始化为一个数据为0的dict。"""
        self.initRetData = {}
        if not self.initRetData.has_key('total'):
            self.initRetData['total'] = 0
        for i in eval(self.mergeKeyList):
            self.initRetData[i] = 0

    def resetData(self):
        """重置数据，到intervalSecond时间后，重置数据到初始化。"""
        self.retData = copy.deepcopy(self.initRetData)
        self.logging.info('initialize key dict: %s' %self.retData)

    def getData(self):
        """获取数据到一个临时变量中。"""
        tmpRetData = copy.deepcopy(self.retData)
        self.resetData()
        return tmpRetData