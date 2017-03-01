# coding=utf-8

import socket


def getretv(sk):
    while 1:

        data=sk.recv(8192)
        print data[-2:]
        print data[0:3]
        if data[-2:]=='\r\n':
            print data
            break


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('192.168.1.100', 2121))
getretv(s)

#login

s.send('USER admin\r\n')
getretv(s)

s.send('PASS admin\r\n')
getretv(s)
s.send('PASV\r\n')
getretv(s)


s.send('LIST\r\n')
getretv(s)





