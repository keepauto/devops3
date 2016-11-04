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
        #调用nbNetUtils的初始化状态机，实例化
        tmp_state = STATE()
        #设置socket对象
        tmp_state.sock_obj = sock
        #定义fd对应socket状态类的字典
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
        conn.setblocking(0)
        return conn
    
    def close(self, fd):
        """fd is fileno() of socket"""
        #pdb.set_trace()
        print "closing", fd, self.conn_state
        try:
            # cancel of listen to event
            sock = self.conn_state[fd].sock_obj
            self.epoll_sock.unregister(fd)
            sock.close()
            self.conn_state.pop(fd)
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
            #获取socket状态
            sock_state = self.conn_state[fd]
            #获取socket对象
            conn = sock_state.sock_obj
            if sock_state.need_read <= 0:
                raise socket.error

            #获取读取10个字节的内容
            one_read = conn.recv(sock_state.need_read)
            #dbgPrint("\tread func fd: %d, one_read: %s, need_read: %d" % (fd, one_read, sock_state.need_read))
            if len(one_read) == 0:
                raise socket.error
            # process received data
            #将数据放到读缓存
            sock_state.buff_read += one_read
            sock_state.have_read += len(one_read)
            sock_state.need_read -= len(one_read)
            #sock_state.printState()

            # read protocol header
            #读取协议的前十个字节
            if sock_state.have_read == 10:
                #response的长度，比如0000000030，则表示长度为30
                header_said_need_read = int(sock_state.buff_read)
                if header_said_need_read <= 0:
                    raise socket.error
                #需要读取的为10字节+response的长度
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
        #获取socket状态
        sock_state = self.conn_state[fd]
        #通过socket状态获取socket对象
        conn = sock_state.sock_obj
        #pdb.set_trace()

        #判断sock_state是否为file
        if isinstance(sock_state.popen_pipe, file):
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
                have_send = conn.send(sock_state.buff_write[last_have_send:])
                sock_state.have_write += have_send
                sock_state.need_write -= have_send
                if sock_state.need_write == 0 and sock_state.have_write != 0:
                    # send complete, re init status, and listen re-read
                    #sock_state.printState()
                    #dbgPrint('\n write data completed!')
                    return "writecomplete"
                else:
                    return "writemore"
            except socket.error, msg:
                return "closing"


    def run(self):
        while True:
            #dbgPrint("\nrun func loop:")
            # print conn_state
            #for i in self.conn_state.iterkeys():
                #dbgPrint("\n - state of fd: %d" % i)
                #self.conn_state[i].printState()

            #阻塞等待事件发生
            epoll_list = self.epoll_sock.poll()
            for fd, events in epoll_list:
                #dbgPrint('\n-- run epoll return fd: %d. event: %s' % (fd, events))
                print self.conn_state
                print fd, events
                sock_state = self.conn_state[fd]
                if select.EPOLLHUP & events:
                    #dbgPrint("EPOLLHUP")
                    sock_state.state = "closing"
                elif select.EPOLLERR & events:
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
        #定义一个连接状态的空字典
        self.conn_state = {}
        #建立一个服务器间网络通信和流式socket对象
        self.listen_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        #当关闭服务时，释放端口，避免被TIME_WAIT占用
        self.listen_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        #将socket绑定地址和端口
        self.listen_sock.bind((addr, port))
        #开始监听
        self.listen_sock.listen(10)
        #调用父类的setFd方法，传入listen_sock参数，得到socket的初始状态
        self.setFd(self.listen_sock)
        #创建epoll句柄
        self.epoll_sock = select.epoll()
        # LT for default, ET add ' | select.EPOLLET '
        self.epoll_sock.register(self.listen_sock.fileno(), select.EPOLLIN )
        self.logic = logic
        #state machine定义状态和对应处理函数的字典
        self.sm = {
            "accept" : self.accept2read,
            "read"   : self.read2process,
            "write"  : self.write2read,
            "process": self.process,
            "closing": self.close,
        }
        #dbgPrint('\n__init__: end, register no: %s' % self.listen_sock.fileno() )

    #@profile
    def process(self, fd):
        #获取fd初始状态
        sock_state = self.conn_state[fd]
        #执行具体执行方法，得到符合传输协议的返回结果
        response = self.logic(fd, sock_state.buff_read)
        #pdb.set_trace()
        if response == None:
            #没有response，则读缓冲区没数据
            conn = sock_state.sock_obj
            self.setFd(conn)
            self.conn_state[fd].state = "read"
            #epoll监听可读事件
            self.epoll_sock.modify(fd, select.EPOLLIN)
        else:
            #有response，则将response写到写缓冲区
            sock_state.buff_write = "%010d%s" % (len(response), response)
            sock_state.need_write = len(sock_state.buff_write)
            #sock_state.printState()
            #self.state_machine(fd)
            sock_state.state = "write"
            #epoll监听可写事件
            self.epoll_sock.modify(fd, select.EPOLLOUT)

             

    #@profile
    def accept2read(self, fd):
        #生成一个新的socket对象
        conn = self.accept(fd)
        #注册新的socket可读事件
        self.epoll_sock.register(conn.fileno(), select.EPOLLIN)
        #初始化新的socket
        # new client connection fd be initilized 
        self.setFd(conn)
        #将状态从accept转到read
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
            #read结果返回，readcontent/process/readmore/closing
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
    #定义计数器逻辑函数
    def logic(d_in):
        global counter
        counter += 1
        if counter % 100000 == 0:
            print counter, time.time()
        return("a")

    #实例化一个nbNet对象
    reverseD = nbNet('0.0.0.0', 9099, logic)
    #启动实例
    reverseD.run()
