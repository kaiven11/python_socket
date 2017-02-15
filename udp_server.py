#coding=utf-8

import socket
import time

sk=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sk.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)#一旦端口释放，即可使用

ip_port=('192.168.1.101',54555)
sk.bind(ip_port)
#sk.listen(5)

while 1:

    data,addr=sk.recvfrom(1024)
    if not data:
        break
    print data
    sk.sendto("return msg",addr)
