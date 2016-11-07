#!/usr/bin/env python

import socket
import sys, os
import time
import signal

"""
GET /index.html HTTP/1.1
Host: www.baidu.com
"""
resp = "HTTP/1.1 200 OK\r\nContent-Length: 15\r\n\r\n<h1>auxten</h1>"

signal.signal(signal.SIGCHLD,signal.SIG_IGN)

listen_fd = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
listen_fd.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listen_fd.bind(("0.0.0.0", 2120))
listen_fd.listen(10) # backlog
while True:
    all_read = ""
    conn, addr = listen_fd.accept()
    pid = os.fork()
    if pid != 0:
        print pid
        pass
    else:
        print conn, addr
        while "\r\n\r\n" not in all_read:
            read_data = conn.recv(1)
            all_read += read_data
        all_read.split(" ")
        conn.send(resp)
        conn.close()
        sys.exit(0)
