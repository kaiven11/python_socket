#coding=utf-8

import socket
import  time
import _struct

recv_client=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
recv_client.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)#level,optionname,value
host=''
port=54231

recv_client.bind((host,port))


while 1:
    data=recv_client.recvfrom(1024)
    time.sleep(3)
    print data


