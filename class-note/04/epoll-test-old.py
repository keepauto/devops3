#coding:utf-8

import select
import socket

listen_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
listen_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listen_sock.bind(("0.0.0.0", 2120))
listen_sock.listen(10) # backlog
epoll_sock = select.epoll()
epoll_sock.register(listen_sock.fileno(), select.EPOLLIN) 
fdsock = {
    listen_sock.fileno(): listen_sock,
}


#read 12345\r\n
#write 54321\r\n
while True:
    epoll_list = epoll_sock.poll()
    for fd, events in epoll_list:
        print fd, events
        if fd == listen_sock.fileno():
            conn,addr = listen_sock.accept()
            print conn, addr, conn.fileno()
            epoll_sock.register(conn.fileno(), select.EPOLLIN)
            fdsock[conn.fileno()] = conn
        else:
            print fdsock[fd].recv(1)
            

