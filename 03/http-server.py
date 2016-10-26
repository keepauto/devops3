#coding:utf-8
import socket
import threading

resp = "HTTP/1.1 200 OK\r\nConten-Length:22\r\n\r\n<h1>OmegaEinstein</h1>\r\n"

listen_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
listen_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listen_sock.bind(('0.0.0.0',2120))
listen_sock.listen(10)

def worker(conn,):
    all_read = ''
    if '\r\n\r\n' not in all_read:
	all_read += conn.recv(1)
    conn.send(resp)
    conn.close()
    

while True:
    conn, addr = listen_sock.accept()
    t = threading.Thread(target=worker,args=(conn,))
    t.start()
