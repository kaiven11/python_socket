# coding=utf-8
import socket
import time

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
address = ('192.168.1.101', 54555)
client.connect(address)
while 1:
    # data=client.recvfrom(1024)
    # client.connect(address)

    client.sendto('haha', address)
    data, addr = client.recvfrom(1024)
    if not data:
        break
    print data
