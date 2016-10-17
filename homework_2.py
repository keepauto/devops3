#!/usr/bin/python
# -*- coding: UTF-8 -*-

import threading
import time

count = 0

class myThread_1(threading.Thread):   #继承父类threading.Thread
    def __init__(self, lock, name):
        threading.Thread.__init__(self)
        self.lock = lock
        self.name = name
    def run(self):                   #把要执行的代码写到run函数里面 线程在创建后会直接运行run函数 
        global count
        self.lock.acquire()
        for i in xrange(1000):
            count = count + 10
        self.lock.release()


class myThread_2(threading.Thread):   #继承父类threading.Thread
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name
    def run(self):      #把要执行的代码写到run函数里面 线程在创建后会直接运行run函数 
        global count
        for i in xrange(1000):
            count = count + 10


def lockThreading():
    #有锁的写变量，结果为100000
    lock = threading.Lock()
    for i in range(10): 
       myThread_1(lock, "thread-" + str(i)).start()


def unlockThreading():
    #没有锁的写变量, 结果不一定
    for i in range(10): 
       myThread_2("thread-" + str(i)).start()

if __name__ == "__main__":
    #lockThreading()
    unlockThreading()
    #确保线程都执行完毕
    time.sleep(2)  
    print count
