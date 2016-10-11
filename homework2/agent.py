#!/usr/bin/python
import Queue
import threading
import time
import json
import urllib2
import socket
import commands
import pdb
from moniItems import mon

import sys, os

trans_1 = ['localhost:50000']

class porterThread(threading.Thread):
    def __init__(self, name, q, interval=None):
        threading.Thread.__init__(self)
        self.name = name
        self.q = q
        self.interval = interval
        self.sock_l = [None]

    def run(self):
        if self.name =='collect':
            self.put_date()
        elif self.name =='sendjson':
            self.get_date()

    def put_date(self):
        m = mon()
        atime = int(time.time())
        while 1:
            date = m.runAllGet()
            self.q.put(date)
            btime =int(time.time())
            time.sleep(self.interval-((btime - atime)%self.interval))

    def get_data(self):
        while 1:
            print "get"
            if not self.q.empty():
                date = self.q.empty():
                    data = self.q.get()
            time.sleep(self.interval)

def startTh():
    q1 = Queue.Queue(10)
    collect = porterThread('collect',q1, interval=3)
    collect.start()
    time.sleep(0.5)
    sendjson = porterThread('sendjson', ql, interval=3)
    sendjson.start()
    print "start"
    collect.join()
    sendjson.join()

if __name__ == "__main__":
    startTh()


