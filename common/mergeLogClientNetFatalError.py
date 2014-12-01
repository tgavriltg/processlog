#!/usr/bin/env python
#coding:utf-8

import json,copy
from common import mergeLog

class mergeLogClientNetFatalError(mergeLog.mergeLog):

    def __init__(self,_logTag,_mergeKeyList,_logging):
        mergeLog.mergeLog.__init__(self,_logTag,_mergeKeyList,_logging)

    def mergeData(self,_logData):
        """
        for data in _logData:
            '''[{'type': 'bussiness_error', 'network_type': '3g'}]'''
            key = data['network_type']+'-type-'+data['type']
            self.retData['total'] += 1
            if str(key) in self.retData.keys():
                self.retData[str(key)] += 1
            else:
                if self.retData.has_key('other'):
                    self.retData['other'] += 1
            self.logging.info('merge log result: %s' % self.retData)
        """
        for data in _logData:
            key = data['network_type']+'-type-'+data['type']
            try:
                self.retData['total'] += 1
                self.retData[key] += 1
            except:
                if self.retData.has_key('other'):
                    self.retData['other'] += 1
            self.logging.info('merge log result: %s' % self.retData)