#!/usr/bin/env python
#coding:utf-8

from common import mergeLog

class mergeLogMClog(mergeLog.mergeLog):

    def __init__(self,_logTag,_mergeKeyList,_logging):
        mergeLog.mergeLog.__init__(self,_logTag,_mergeKeyList,_logging)

    def mergeData(self,_logData):

        key = _logData['status']+'-mcCode-'+_logData['mcCode']
        try:
            self.retData[key] += 1
        except Exception as err:
            self.logging.error('mergeKeyList is not have %s:%s' %(key,err))

        self.logging.debug('merge log result: %s' % self.retData)