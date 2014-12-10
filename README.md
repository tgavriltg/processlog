processlog
==========
本程序主要是用来分析日志取出有用的信息然后对信息进行处理定时发送给zabbix，用于数据展示和报警。

#### 程序主要分为三部分：
        1.parseLog(分析日志)
          主要是通过正则匹配到日志中有用的信息放到字典中。
        2.mergeLog(处理日志)
          主要是把分析得到的字典进行处理，得到你在配置文件中配置的key的数据。
        3.queueLog(定时发送程序)
          主要是定时处理得到的结果发送到zabbix，然后对处理的数据进行重置。

#### 获取日志的方式两种方式：
        1.直接读取日志文件。
        2.读取从管道收集到的日志(其他程序通过管道发送给本程)。

#### 使用方式：
        python processlog.py -h
        Usage: processlog.py [options]

        Options:
          -h, --help            show this help message and exit
          -f CONFIGFILE, --configFile=CONFIGFILE
                                please input configure file path.
          -t LOGTAG, --logTag=LOGTAG
                                default log tag.

