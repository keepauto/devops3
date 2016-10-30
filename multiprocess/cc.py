#!/usr/bin/env python

import socket, sys, os
import threading
import time

HOST = '127.0.0.1'
PORT = 9079
CNT = int(sys.argv[2])


print time.time()
def s():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))

    cmd = sys.argv[1]
    data = "%010d%s"%(len(cmd), cmd)
    s.send(data * CNT)
#s.recv(len(data) * CNT)
    for i in xrange(CNT):
        buf = s.recv(len(data))
        #print buf
t=[]
for i in range(2):
    t.append(threading.Thread(target=s))

for i in t:
    i.start()

for i in t:
    i.join()

print time.time()
