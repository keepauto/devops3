#!/usr/bin/env python

import socket
import os
import time
import signal
import Queue
import threading

"""
GET /index.html HTTP/1.1
Host: www.baidu.com
"""
resp = "HTTP/1.1 200 OK\r\nContent-Length:15\r\n\r\n<h1>auxten</h1>"

signal.signal(signal.SIGCHLD,signal.SIG_IGN)
q = Queue.Queue()

def worker():
    while True:
        all_read = ""
        conn = q.get()
        while "\r\n\r\n" not in all_read:
            read_data = conn.recv(1)
            all_read += read_data
        #print all_read
        all_read.split(" ")
        conn.send(resp)
        conn.close()
        q.task_done()

for i in xrange(10):
    t = threading.Thread(target = worker)
    t.daemon = True
    t.start()

listen_fd  = socket.socket(socket.AF_INET,socket.SOCK_STREAM,0)
listen_fd.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listen_fd.bind(("0.0.0.0", 2180))
listen_fd.listen(10) #backlog
#time.sleep(100)
while True:
    conn, addr = listen_fd.accept()
    q.put(conn)
