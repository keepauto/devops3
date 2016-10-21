import socket
import sys, os
import time
import signal
import Queue
import threading

resp = "HTTP/1.1 200 OK\r\nContent-Length: 15\r\n\r\n<h1>auxten</h1>"

signal.signal(signal.SIGCHLD,signal.SIG_IGN)
q = Queue.Queue()

class Worker_thread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.conn = q.get()
        self.all_read = ""
        self.thread_stop = False
    def run(self):
        while "\r\n\r\n" not in self.all_read:
            read_data = conn.recv(1)
            self.all_read += read_data
        self.all_read.split(" ")
        self.conn.send(resp)
        conn.close()
        q.task_done()
    def stop(self):
        self.thread_stop = True

def main():
    worker = Worker_thread()
    worker.start()
    worker.stop()
    print "done"
    return
    
listen_fd = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
listen_fd.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listen_fd.bind(("0.0.0.0", 2133))
listen_fd.listen(10) # backlog

    
while True:
    conn, addr = listen_fd.accept()
    q.put(conn)
    main()
