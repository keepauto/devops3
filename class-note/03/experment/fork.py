#!/usr/bin/env python
import os
import time

def task(id):
    print "work %d" %id

print 'start now'
pid = os.fork()
print "pid is %d" %pid
if pid == 0:
    print "I am a child"
    task(1)
else:
    print "I am father child"

print "who am i"
time.sleep(10)

