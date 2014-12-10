#!/usr/bin/env python
#coding:utf-8

import threading,time

class queueLogV4wwwlog(threading.Thread):
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
        self.logging.error('parse error count is %d' % int(self.parseErrorCount))

    def run(self):
        """{'mapi-total-2000-999999': 0, 'mapi-page-card-1000-2000': 0, 'mapi-page-card-2000-999999': 0, 'mapi-total-400': 0, 'mapi-other-200': 0, 'total': 0, 'mapi-other-2000-999999': 0, 'mapi-other-responseTime': 0}"""
        threadname = threading.currentThread().getName()
        self.logging.info('queueLog (%s) thread started!'%(threadname))
        while 1:
            time.sleep(int(self.intervalSecond))
            self.sendData()

    def sendData(self):
        tmpRetData = self.mergeLogObj.getData()
        self.logging.info('tmpRetData is %s' % tmpRetData)
        self.getParseErrorCount()
        rt = 'responseTime'
        try:
            for key in tmpRetData:
                if rt in key:
                    preKey = key.rstrip(rt)
                    num = tmpRetData[preKey+'200'] + tmpRetData[preKey+'400'] + tmpRetData[preKey+'500']
                    if num != 0:
                        tmpRetData[preKey+rt] = tmpRetData[preKey+rt] / num
        except Exception as err:
            self.logging.error('handle avg responseTime error: %s' % err)
            pass

        self.logging.info('send tmpRetData is %s' % tmpRetData)
        try:
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