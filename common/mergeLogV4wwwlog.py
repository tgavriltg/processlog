#!/usr/bin/env python
#coding:utf-8

import json,copy
from common import mergeLog

class mergeLogV4wwwlog(mergeLog.mergeLog):

    def __init__(self,_logTag,_mergeKeyList,_logging):
        mergeLog.mergeLog.__init__(self,_logTag,_mergeKeyList,_logging)

    def mergeData(self,_logData):
        """_logData={'httpUri': '/page/card', 'responseTime': 1100.0, 'httpCode': '786'}"""
        preKey = 'api'+_logData['httpUri']+'-'
        preKey = preKey.replace('/','-')

        responseTime = int(_logData['responseTime'])
        httpCode = _logData['httpCode'][0:1]+'00'
        self.logging.info('preKey:%s,responseTime:%d,httpCode:%s' % (preKey,responseTime,httpCode))
        """统计200,4xx,5xx个数"""
        try:
            self.retData['api-total-'+httpCode] += 1
            self.retData[preKey+httpCode] += 1
        except:
            self.retData['api-other-'+httpCode] += 1
        """统计各url总共的响应时间"""
        try:
            self.retData['api-total-responseTime'] = self.retData['api-total-responseTime'] + _logData['responseTime']
            self.retData[preKey+'responseTime'] = self.retData[preKey+'responseTime'] + _logData['responseTime']
        except:
            self.retData['api-other-responseTime'] = self.retData['api-other-responseTime'] + _logData['responseTime']
        """统计各url响应时间区间的个数"""
        try:
            if responseTime <= 200:
                self.retData['api-total-0-200'] += 1
                self.retData[preKey+'0-200'] += 1
            elif 200 < responseTime <= 500:
                self.retData['api-total-200-500'] += 1
                self.retData[preKey+'200-500'] += 1
            elif 500 < responseTime <= 1000:
                self.retData['api-total-500-1000'] += 1
                self.retData[preKey+'500-1000'] += 1
            elif 1000 < responseTime <= 2000:
                self.retData['api-total-1000-2000'] += 1
                self.retData[preKey+'1000-2000'] += 1
            else:
                self.retData['api-total-2000-999999'] += 1
                self.retData[preKey+'2000-999999'] += 1
        except:
            if responseTime <= 200:
                self.retData['api-other-0-200'] += 1
            elif 200 < responseTime <= 500:
                self.retData['api-other-200-500'] += 1
            elif 500 < responseTime <= 1000:
                self.retData['api-other-500-1000'] += 1
            elif 1000 < responseTime <= 2000:
                self.retData['api-other-1000-2000'] += 1
            else:
                self.retData['api-other-2000-999999'] += 1

        self.logging.info('result merge log:%s' % self.retData)
