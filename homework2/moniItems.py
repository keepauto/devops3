#!/usr/bin/env python
#coding=utf-8
import json
import urllib
import inspect
import os,time,socket

userDefine_check_time = 0
userDefine_json = []

class mon:
    def __init__(self):
        self.data = {}

    def getLoadAvg(self):
        with open('/proc/loadavg') as load_open:
            a = load_open.read().split()[:3]
            #return "%s %s %s %(a[0],a[1],a[2])"
            return float(a[0])

    def getMemTotal(self):
        with open('/proc/meminfo') as mem_open:
            a = int(mem_open.readline().split()[1])
            return a/1024

    def getMemUsage(self, noBufferCache=True):
        if noBufferCache:
            with open('/proc/meminfo') as mem_open:
                T = int(mem_open.readline().split()[1])
                F = int(mem_open.readline().split()[1])
                B = int(mem_open.readline().split()[1])
                C = int(mem_open.readline().split()[1])
                return (T-F-B-C)/1024
        else:
            with open('/proc/meminfo') as mem_open:
                a = int(mem_open.readline().split()[1])
                return a/1024

    def getHost(self):
        return  ['host1', 'host2', 'host3', 'host4','host5'][int(time.time() * 1000.0)%5]

    def getTime(self):
        return int(time.time())

    def userDefineMon(self):
        time.sleep(1)
        return{"ud":1}

    def runAllGet(self):
        for fun in inspect.getmembers(self, predicate=inspect.ismethod):
            if fun[0] == "userDefineMon":
                self.data.update(fun[1]())
            elif fun[0][:3] == 'get':
                self.data[fun[0][3:]] = fun[1]()
        return self.data

if __name__ == '__main__':
    print mon().runAllGet()

