#!/usr/bin/env python
#coding:utf-8

import sys
import fcntl
import struct
import socket
import re

class getHostIp:

    def __init__(self,_logging):
        self.logging = _logging

    def getIpAddress(self,ifname):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(
            s.fileno(),
            0x8915,
            struct.pack('256s', ifname[:15])
        )[20:24])

    def matchIpAddress(self):
        reg = re.compile(r"10\..*|172\.16\..*")
        try:
            if reg.match(self.getIpAddress('bond0')):
                return self.getIpAddress('bond0')
        except:
            pass
        try:
            if reg.match(self.getIpAddress('eth0')):
                return self.getIpAddress('eth0')
        except:
            pass
        try:
            if reg.match(self.getIpAddress('wlan0')):
                return self.getIpAddress('wlan0')
        except:
            self.logging('cat not get intra ip address,please check.')
            sys.exit(2)