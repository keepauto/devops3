#!/usr/bin/env python
import socket
import sys, os
import time
import signal
import Queue
import threading
"""
GET /index.html HTTP/1.1
Host: www.baidu.com
"""
resp = "HTTP/1.1 200 OK\r\nConetent-Length: 15\r\n\r\n<h1>luojiyin</h1>"

signal.signal(signal.SIGCHLD, signal.SIG_IGN)
q = Queue.Queue()


def worker(conn, addr):

        all_read = ""
        #conn = q.get()
        while "\r\n\r\n"   not in all_read:
            read_data = conn.recv(1)
            all_read += read_data
        all_read.split(" ")
        conn.send(resp)
        #print "ok"
        conn.close()
        #q.task_done()

#for i in xrange(10):
#    t = threading.Thread(target = worker)
#    t.deamon = True
#    t.start()

listen_fd = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
listen_fd.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
listen_fd.bind(("0.0.0.0", 1987))
listen_fd.listen(10)
thread_num = 0
while True:
    conn, addr = listen_fd.accept()
    #t = threading.Thread(target = worker)
    #t.deamon = True
    #t.start()
    thread_num = thread_num + 1
    #print thread_num
    t = threading.Thread(target=worker,name='server process thread'+str(thread_num),args=(conn, addr))
    t.start()
