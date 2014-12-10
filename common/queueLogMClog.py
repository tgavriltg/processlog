#!/usr/bin/env python
#coding:utf-8

import threading,time

class queueLogMClog(threading.Thread):
    parseErrorCount = 0

    def __init__(self,_intervalSecond,_parseLogObj,_mergeLogObj,_logging,_zSend,_host):
        threading.Thread.__init__(self)
        self.intervalSecond = _intervalSecond
        self.parseLogObj = _parseLogObj
        self.mergeLogObj = _mergeLogObj
        self.logging = _logging
        self.zSend = _zSend
        self.host = _host

    def getParseErrorCount(self):
        self.parseErrorCount = self.parseErrorCount + self.parseLogObj.parseErrorCount
        self.logging.warning('parse error count is %d' % int(self.parseErrorCount))

    def run(self):
        """{'wifi-type-bussiness_error': 3, '3g-type-bussiness_error': 2, 'total': 8, 'other': 0, '3g-type-not_reachable': 3, 'wifi-type-not_reachable': 0}"""
        threadname = threading.currentThread().getName()
        self.logging.info('queueLog (%s) thread started!'%(threadname))
        while 1:
            time.sleep(int(self.intervalSecond))
            self.sendData()

    def sendData(self):
        tmpRetData = self.mergeLogObj.getData()

        self.getParseErrorCount()
        #去除请求数为0的key
        for key in tmpRetData.keys():
            if tmpRetData[key] == 0:
                tmpRetData.pop(key)
        self.logging.info('tmpRetData is %s' % tmpRetData)
        try:
            if tmpRetData:
                for key in tmpRetData:
                    self.zSend.add_data(self.host,key,tmpRetData[key])
                self.zSend.print_vals()
                (code,ret) = self.zSend.send(self.zSend.build_all())
                if code == 1:
                    self.logging.error('Problem during send!\n%s' % str(ret))
                elif code == 0:
                    self.logging.info('zabbix send result: %s' % str(ret))
                self.zSend.list = []
        except Exception as err:
            self.logging.critical('problem during handle sendData to zabbix!\n%s' % err)