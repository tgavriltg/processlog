#!/bin/env python
#coding=utf8
import ConfigParser
import sys
import logging
import optparse
import time
#common function lib
from common import readConf
from common import parseLog_dict
from common import mergeLogClientNetFatalError
from common import mergeLogwwwlog
from common import mergeLogMClog
from common import queueLog
from common import queueLogwwwlog
from common import queueLogMClog
from common import zabbixSender
from common import getHostIp


defaultConfigFilePath='/usr/local/sinawap/processlog/conf/processlog.conf'
defaultLogTag='client_net_fatal_error'
debugFlag = True
readFileFlag = False

def getOptions():
    usage = "usage: %prog [options]"
    OptionParser = optparse.OptionParser
    parser = OptionParser(usage)
    parser.add_option("-f","--configFile",action="store",type="string",dest="configFile",default=defaultConfigFilePath,help="please input configure file path.")
    parser.add_option("-t","--logTag",action="store",type="string",dest="logTag",default=defaultLogTag,help="default log tag.")
    options,args = parser.parse_args()
    return options,args

def readLog(file):
    tmpLine=""
    print(file)
    with open(file,'r') as f:
        f.seek(0,2)
        while 1:
            line = f.readline()
            if not line:
                time.sleep(1)
                pass
            else:
                if not line.endswith("\n"):
                    tmpLine += line
                else:
                    line = tmpLine + line
                    tmpLine = ""
                    logData = parseLogObj.getLogData(line)
                    mergeLogObj.mergeData(logData)


if __name__ == "__main__":
    options,args = getOptions()

    conf = readConf.covertListToDict(options.configFile)  #把conf文件转换成字典。

    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)-3s : %(message)s %(filename)s | [%(module)s %(lineno)d]', datefmt='%Y-%m-%d %H:%M:%S' )
    if debugFlag == False:
        logging.disable(logging.INFO)

    zSend = zabbixSender.ZSend(logging,conf['zabbix']['zabbixserver'],int(conf['zabbix']['zabbixport']))
    ipAddress = getHostIp.getHostIp(logging)
    host = ipAddress.matchIpAddress()

    if options.logTag == "client_net_fatal_error":
        parseLogObj = parseLog_dict.parseLog(options.logTag,'','',logging)
        mergeLogObj = mergeLogClientNetFatalError.mergeLogClientNetFatalError(options.logTag,conf[options.logTag]['mergekeylist'],logging)
        queueLogObj = queueLog.queueLog(conf[options.logTag]['intervalsecond'],parseLogObj,mergeLogObj,logging,zSend,host)
    elif options.logTag == "wwwlog":
        parseLogObj = parseLog_dict.parseLog(options.logTag,conf[options.logTag]['regex'],'',logging)
        mergeLogObj = mergeLogwwwlog.mergeLogwwwlog(options.logTag,conf[options.logTag]['mergekeylist'],logging)
        queueLogObj = queueLogwwwlog.queueLogwwwlog(conf[options.logTag]['intervalsecond'],parseLogObj,mergeLogObj,logging,zSend,host)
    elif options.logTag == "mclog":
        parseLogObj = parseLog_dict.parseLog(options.logTag,conf[options.logTag]['regex'],'',logging)
        mergeLogObj = mergeLogMClog.mergeLogMClog(options.logTag,conf[options.logTag]['mergekeylist'],logging)
        queueLogObj = queueLogMClog.queueLogMClog(conf[options.logTag]['intervalsecond'],parseLogObj,mergeLogObj,logging,zSend,host)


    queueLogObj.setDaemon(True)
    queueLogObj.start()

    if debugFlag == True and readFileFlag == True:
        if options.logTag == 'client_net_fatal_error':
            file = open('/tmp/client_net_fatal_error.log')

    sum = 0

    if options.logTag == "wwwlog":
        readLog("/tmp/www.log")
    else:
        while 1:
            if debugFlag == True and readFileFlag == True:
                line = file.readline()
            else:
                line = sys.stdin.readline()

            if not line:
                logging.warning('processlog.py stop.total process %s msg.' % sum)
                break
            else:
                logData = parseLogObj.getLogData(line)
                if logData and options.logTag == "client_net_fatal_error":
                    mergeLogObj.mergeData(logData)
                elif logData and options.logTag == "wwwlog":
                    mergeLogObj.mergeData(logData)
                elif logData and options.logTag == "mclog":
                    mergeLogObj.mergeData(logData)
