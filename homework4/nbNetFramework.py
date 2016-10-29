#!/usr/bin/env python
# coding: utf-8

from daemon import Daemon
import socket
import select
import time
import pdb

__all__ = ["nbNet", "sendData_mh"]
#DEBUG = True

from nbNetUtils import *

class nbNetBase:
    '''non-blocking Net'''
    def setFd(self, sock):
        """sock is class object of socket"""
        #dbgPrint("\n -- setFd start!")
        tmp_state = STATE()  #初始化状态机  默认状态为 accept 
        tmp_state.sock_obj = sock   #sock_obj  is   obeject
        self.conn_state[sock.fileno()] = tmp_state
        #self.conn_state[sock.fileno()].printState()
        #dbgPrint("\n -- setFd end!")

    def accept(self, fd): 
        """fd is fileno() of socket"""
        #dbgPrint("\n -- accept start!")
        sock_state = self.conn_state[fd]
        sock = sock_state.sock_obj
        conn, addr = sock.accept()
        # set to non-blocking: 0
        conn.setblocking(0)   # 设置为非阻塞
        return conn
    
    def close(self, fd):
        """fd is fileno() of socket"""
        #pdb.set_trace()
        print "closing", fd, self.conn_state
        try:
            # cancel of listen to event
            sock = self.conn_state[fd].sock_obj  #获得要关闭的sock
            self.epoll_sock.unregister(fd)       #取消在epoll 的注册
            sock.close()                         #服务器端关闭socket  
            self.conn_state.pop(fd)              #从conn_state list中  清除
            tmp_pipe = self.popen_pipe           
            self.popen_pipe = 0
            tmp_pipe.close()
        except:
            #dbgPrint("Close fd: %s abnormal" % fd)
            pass
    #@profile
    def read(self, fd):
        """fd is fileno() of socket"""
        #pdb.set_trace()
        try:
            sock_state = self.conn_state[fd]
            conn = sock_state.sock_obj
            if sock_state.need_read <= 0:
                raise socket.error

            one_read = conn.recv(sock_state.need_read)
            #dbgPrint("\tread func fd: %d, one_read: %s, need_read: %d" % (fd, one_read, sock_state.need_read))
            if len(one_read) == 0:
                raise socket.error
            # process received data
            sock_state.buff_read += one_read
            sock_state.have_read += len(one_read)
            sock_state.need_read -= len(one_read)
            #sock_state.printState()

            # read protocol header
            if sock_state.have_read == 10:
                header_said_need_read = int(sock_state.buff_read)
                if header_said_need_read <= 0:
                    raise socket.error
                sock_state.need_read += header_said_need_read
                sock_state.buff_read = ''
                # call state machine, current state is read. 
                # after protocol header haven readed, read the real cmd content, 
                # call machine instead of call read() it self in common.
                #sock_state.printState()
                return "readcontent"
            elif sock_state.need_read == 0:
                # recv complete, change state to process it
                return "process"
            else:
                return "readmore"
        except (socket.error, ValueError), msg:
            try:
                if msg.errno == 11:
                    #dbgPrint("11 " + msg)
                    return "retry"
            except:
                pass
            return 'closing'
        

    #@profile
    def write(self, fd):
        sock_state = self.conn_state[fd]
        conn = sock_state.sock_obj
        #pdb.set_trace()
        
        if isinstance(sock_state.popen_pipe, file):    #判断是否为文件对象 (file object) 
            try:
                output = sock_state.popen_pipe.read()
                #print output
            except (IOError, ValueError), msg:
                pass
            #have_send = conn.send("%010d%s" % (len(output), output))
            #todo

        else:
            last_have_send = sock_state.have_write
            try:
                # to send some Bytes, but have_send is the return num of .send()
                have_send = conn.send(sock_state.buff_write[last_have_send:])  #发送
                sock_state.have_write += have_send     # 计算已经发送的  和将要发送的 很可能不能一次发完
                sock_state.need_write -= have_send
                if sock_state.need_write == 0 and sock_state.have_write != 0:  # 当没有要发送 并且 发送过数据
                    # send complete, re init status, and listen re-read
                    #sock_state.printState()
                    #dbgPrint('\n write data completed!')
                    return "writecomplete"
                else:
                    return "writemore"   # 为什么会出现 超写???
            except socket.error, msg:   
                return "closing"


    def run(self):
        while True:
            #dbgPrint("\nrun func loop:")
            # print conn_state
            #for i in self.conn_state.iterkeys():
                #dbgPrint("\n - state of fd: %d" % i)
                #self.conn_state[i].printState()

            epoll_list = self.epoll_sock.poll() # 为什么是 poll  不是  epoll   为可在类Unix平台跑???
            for fd, events in epoll_list:       # 开始查询epoll 中事件记录
                #dbgPrint('\n-- run epoll return fd: %d. event: %s' % (fd, events))
                print self.conn_state   
                print fd, events
                sock_state = self.conn_state[fd]  
                if select.EPOLLHUP & events:    # 挂断 访问文件描述符
                    #dbgPrint("EPOLLHUP")
                    sock_state.state = "closing"  
                elif select.EPOLLERR & events:   #发生错误，
                    #dbgPrint("EPOLLERR")
                    sock_state.state = "closing"
                self.state_machine(fd)

    def state_machine(self, fd):
        #time.sleep(0.1)
        #dbgPrint("\n - state machine: fd: %d, status: %s" % (fd, self.conn_state[fd].state))
        sock_state = self.conn_state[fd]
        self.sm[sock_state.state](fd)

class nbNet(nbNetBase):
    def __init__(self, addr, port, logic):
        #dbgPrint('\n__init__: start!')
        self.conn_state = {}   # 初始化状态
        self.listen_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) #AF_INET 为IPV4, SOCK_STREAM 为流套接字
        self.listen_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #防止端口不释放的情况
        self.listen_sock.bind((addr, port))   #绑定IP地址  端口
        self.listen_sock.listen(10)           #设定backlog 值 为非负整数，一般为5
        self.setFd(self.listen_sock)          #把socket的文件描述传人状态机进行处理
        self.epoll_sock = select.epoll()      #创建 epoll对象  Linux可用
        # LT for default, ET add ' | select.EPOLLET '
        self.epoll_sock.register(self.listen_sock.fileno(), select.EPOLLIN ) #对listen_sock_fileno 在epoll 注册为EPOLLIN（可读）
        self.logic = logic    #把状态值初始化
        self.sm = {
            "accept" : self.accept2read,
            "read"   : self.read2process,
            "write"  : self.write2read,
            "process": self.process,
            "closing": self.close,
        }                    #通过字典初始化各种处理函数
        #dbgPrint('\n__init__: end, register no: %s' % self.listen_sock.fileno() )

    #@profile
    def process(self, fd):
        sock_state = self.conn_state[fd]  #获取文件描述符状态
        response = self.logic(fd, sock_state.buff_read)  #获取sock接收缓冲区数据
        #pdb.set_trace()
        if response == None:   #如果为空
            conn = sock_state.sock_obj 
            self.setFd(conn)
            self.conn_state[fd].state = "read"
            self.epoll_sock.modify(fd, select.EPOLLIN)
        else:  
            sock_state.buff_write = "%010d%s" % (len(response), response)
            sock_state.need_write = len(sock_state.buff_write)
            #sock_state.printState()
            #self.state_machine(fd)
            sock_state.state = "write"
            self.epoll_sock.modify(fd, select.EPOLLOUT)

             

    #@profile
    def accept2read(self, fd):
        conn = self.accept(fd)
        self.epoll_sock.register(conn.fileno(), select.EPOLLIN)
        # new client connection fd be initilized 
        self.setFd(conn)
        self.conn_state[conn.fileno()].state = "read"
        # now end of accept, but the main process still on 'accept' status
        # waiting for new client to connect it.
        #dbgPrint("\n -- accept end!")

    #@profile
    def read2process(self, fd):
        """fd is fileno() of socket"""
        #pdb.set_trace()
        read_ret = ""
        try:
            read_ret = self.read(fd)
        except (Exception), msg:
            #dbgPrint(msg)
            read_ret = "closing"
        if read_ret == "process":
            # recv complete, change state to process it
            #sock_state.state = "process"
            self.process(fd)
        elif read_ret == "readcontent":
            pass
        elif read_ret == "readmore":
            pass
        elif read_ret == "retry":
            pass
        elif read_ret == "closing":
            self.conn_state[fd].state = 'closing'
            # closing directly when error.
            self.state_machine(fd)
        else:
            raise Exception("impossible state returned by self.read")

    #@profile
    def write2read(self, fd):
        try:
            write_ret = self.write(fd)
        except socket.error, msg:
            write_ret = "closing"

        if write_ret == "writemore":
            pass
        elif write_ret == "writecomplete":
            sock_state = self.conn_state[fd]
            conn = sock_state.sock_obj
            self.setFd(conn)
            self.conn_state[fd].state = "read"
            self.epoll_sock.modify(fd, select.EPOLLIN)
        elif write_ret == "closing":
            #dbgPrint(msg)
            self.conn_state[fd].state = 'closing'
            # closing directly when error.
            self.state_machine(fd)
    
counter = 0
if __name__ == '__main__':
    
    def logic(d_in):      #d_in  是干什么的
        global counter    #定义全局变量counter   
        counter += 1
        if counter % 100000 == 0:
            print counter, time.time()
        return("a")

    reverseD = nbNet('0.0.0.0', 9099, logic)
    reverseD.run()
