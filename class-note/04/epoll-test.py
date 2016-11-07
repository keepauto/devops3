#!/usr/bin/env python
# coding=utf-8

import select
import socket

#建立一个的socket
listen_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
#使得socket可重复监听
listen_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#把socket绑定到指定地址和端口
listen_sock.bind(("0.0.0.0", 2120))
#使得socket处于监听状态
listen_sock.listen(10)
#设置socket参数为0表示非阻塞的
listen_sock.setblocking(0)
#设置一个水平/边缘触发对象
epoll_sock = select.epoll()
epoll_sock.register(listen_sock.fileno(), select.EPOLLIN )
fdsock = {
    listen_sock.fileno(): listen_sock,
}

# read 12345\r\n
# write 54321\r\n
sent = 0
buf = ""

while True:
    epoll_list = epoll_sock.poll()
    for fd, events in epoll_list:
        if select.EPOLLIN & events:
            if fd == listen_sock.fileno():
                conn,addr = listen_sock.accept()
                conn.setblocking(0)
                print conn, addr, conn.fileno()
                epoll_sock.register(conn.fileno(), select.EPOLLIN)
                fdsock[conn.fileno()] = conn
            else:
                buf += fdsock[fd].recv(100)
                if len(buf) > 2 and buf[-2] == '\r' and buf[-1] == '\n':
                    buf = buf[:-2][::-1]+ "\r\n"
                    epoll_sock.unregister(conn)
                    epoll_sock.register(conn.fileno(), select.EPOLLOUT)

        elif select.EPOLLOUT & events:
            print sent, buf
            s = fdsock[fd].send(buf[sent:])
            print 's', s
            if s > 0:
                sent += s
            if sent == len(buf):
                epoll_sock.unregister(conn)
                epoll_sock.register(conn.fileno(), select.EPOLLIN)
                buf = ""
                sent = 0

