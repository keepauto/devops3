#!/usr/bin/env python
# coding=utf-8

import sys, os 
import signal
import socket
import select
import time
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from nbNet.nbNetFramework import nbNet

pidList = []
s1pairList = []
fnoList = []
def _handle_sigint(signo, this):
    for i in pidList:
        os.kill(i, signal.SIGKILL)
    exit()
if __name__ == '__main__':
    def logic(ob, fd, d_in):
        if fd in fnoList:
            if ob.resigterFlag == 0:
                ob.epoll_sock.unregister(ob.listen_sock.fileno())
                ob.resigterFlag = 1
            else:
                ob.epoll_sock.register(ob.listen_sock.fileno(), select.EPOLLIN )
                ob.resigterFlag = 0
            #s2.recv(10)
        return(d_in[::-1])

    reverseD = nbNet('0.0.0.0', 9079, logic)
    for i in range(2):
        s1, s2 = socket.socketpair()
        s1pairList.append(s1)
        fnoList.append(s2.fileno())
        print s2.fileno()
        pid = os.fork()
        if pid == 0 :
            s1.close()
            s2.recv(10)
            reverseD.epoll_sock = select.epoll()
            reverseD.epoll_sock.register(reverseD.listen_sock.fileno(), select.EPOLLIN )
            reverseD.epoll_sock.register(s2.fileno(), select.EPOLLIN )
            reverseD.setFd(s2)
            reverseD.resigterFlag = 0
            reverseD.conn_state[s2.fileno()].state = "read"
            reverseD.run()
            exit()
        else:
            pidList.append(pid)
    
    reverseD.epoll_sock.unregister(reverseD.listen_sock.fileno())
    reverseD.epoll_sock.close()
    for i in s1pairList:
        i.send("go")
    signal.signal(signal.SIGINT, _handle_sigint)
    time.sleep(5)
    while True:
        for i in s1pairList:
            i.send("%010d%s" % (len("break"), "break"))
            time.sleep(1)
            #i.send("123")
            #i.recv(20)
    reverseD.run()


