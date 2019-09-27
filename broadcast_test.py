#coding=utf-8
import socket
import  time
import _struct

send_server=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
send_server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
send_server.setsockopt(socket.SOL_SOCKET,socket.SO_BROADCAST,1)



dest=('<broadcast>',54231)

while 1:
    send_server.sendto('i am here',dest)
    time.sleep(5)







