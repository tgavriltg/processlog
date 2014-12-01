#!/usr/bin/env python
#coding:utf-8

import re

class parseLog:
    """
    解析日志：
        1.根据提供的正则获取与正则配置的groupdict。
        2.如果没有正则的是日志就是dict的list，一样的获取需要字段的dict。
    """
    logDate = {}
    logTag = "client_net_fatal_error"
    regexStr = ''
    parseErrorCount = 0

    def __init__(self,_logTag,_regexStr,_regexStr1,_logging):
        self.logTag = _logTag
        self.regexStr = _regexStr
        self.regexStr1 = _regexStr1
        self.logging = _logging
        if len(self.regexStr) > 0:
            self.regexObj = re.compile('''%s'''% (self.regexStr))
        else:
            self.regexObj = None
        if len(_regexStr1) > 0:
            self.regexObj1 = re.compile('''%s'''% (self.regexStr1))
        else:
            self.regexObj1 = None

    def parseData(self,_logStr):
        """解析一行一行过来的日志"""
        #self.logging.info('parse logTag %s start.' % self.logTag)
        if self.logTag == 'client_net_fatal_error':
            logData1 = {}
            self.logData = []
            try:
                for str in eval(_logStr):
                    if dict(str).has_key('type') and dict(str).has_key('network_type'):
                        logData1['type'] = str['type']
                        logData1['network_type'] = str['network_type']
                        self.logData.append(logData1)
                        logData1 = {}
                    else:
                        self.parseErrorCount += 1
                        self.logging.info('parse log error: str not has "network_type"')
            except:
                self.logData = {}
                self.logging.error('parse log string failed:logTag:%s,log:%s' % (self.logTag, _logStr))
        else:   #处理由正则匹配的日志。
            try:
                regexData = self.regexObj.match(_logStr)
                if regexData:
                    self.logData = regexData.groupdict()
                    if self.logData.has_key('responseTime'):
                        self.logData['responseTime'] = int(self.logData['responseTime'])
                else:   #处理第一个正在没有匹配如果有第二个正则的情况。
                    if self.regexObj1:

                        regexData = self.regexObj1.match(_logStr)
                        if regexData:
                            self.logData = regexData.groupdict()
                            if self.logData.has_key('responseTime'):
                                self.logData['responseTime'] = int(self.logData['responseTime'])
                        else:
                            self.logData = {}
                            self.logging.error('parse log string failed.logTag:%s,regexStr1:%s,logStr:%s' % (self.logTag, self.regexStr1, _logStr))
                            self.parseErrorCount += 1
                    else:
                        self.logData = {}
                        self.logging.error('parse log string failed.logTag:%s,regexStr:%s,logStr:%s' % (self.logTag, self.regexStr, _logStr))
                        self.parseErrorCount += 1
            except:
                self.logData = {}
                self.logging.error('parse log string failed:%s,%s,%s' % (self.logTag, self.regexStr, _logStr))

    def getLogData(self,_logStr=''):
        self.parseData(_logStr)
        self.logging.info('parse log result:%s' %self.logData)
        return self.logData