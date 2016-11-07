#!/usr/bin/env python

import socket
import time

"""
GET /index.html HTTP/1.1
Host: www.baidu.com
"""
resp = "HTTP/1.1 200 OK\r\nContent-Length:15\r\n\r\n<h1>auxten</h1>"

listen_fd  = socket.socket(socket.AF_INET,socket.SOCK_STREAM,0)
listen_fd.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listen_fd.bind(("0.0.0.0", 2180))
listen_fd.listen(10) #backlog
#time.sleep(100)
while True:
    all_read = ""
    conn, addr = listen_fd.accept()
    print conn,addr
#    read_data = conn.recv(100)
    while "\r\n\r\n" not in all_read:
        read_data = conn.recv(1)
        all_read += read_data
    print all_read
    requestURI = all_read.split()[1][1:]
    if requestURI != '/':
        with open(requestURI) as f:
            resp = f.read()
            conn.send(resp)
