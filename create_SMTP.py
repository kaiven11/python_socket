#coding=utf-8
import socket
import  time
from email.mime.text import MIMEText
client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#socket.setdefaulttimeout(2)
def getreply(sk):
    flag = True
    while flag:
        data = sk.recv(8192)
        if data[3:4] != '-':
            break
        print data


ip_port=('smtp.126.com',25)
#第一阶段 发送 ehlo 或者 helo
client.connect(ip_port)
client.send('ehlo li\r\n')
getreply(client)

# client.sendall('')
# 第二个阶段 auth plain



client.sendall('AUTH PLAIN AGZlbmdjaHVib2p1ZUAxMjYuY29tADEyMzQ1NnE=\r\n')
# client.sendall('')

# data1=client.recv(1024)

getreply(client)
client.send('mail FROM:<fengchubojue@126.com>\r\n')

getreply(client)
client.send('rcpt TO:<1064187559@qq.com>\r\n')
getreply(client)

client.send('data\r\n')
getreply(client)



email_object=MIMEText('test1561456')
email_object['From']='fengchubojue@126.com'
email_object['To']='1064187559@qq.com'
#email_object['FROM']='13731250529@163.com'
email_object['Subject']='new111 test'



data='Content-Type: text/plain; charset="us-ascii"\r\nMIME-Version: 1.0\r\nContent-Transfer-Encoding: 7bit\r\nTo: 1064187559@qq.com\r\nFrom: fengchubojue@126.com\r\nMessage-Id: <148795327352.5504.8127330757937958674@MS-20160703XEYM>\r\nSubject: nimei\r\nDate: Sat, 25 Feb 2017 00:21:13 +0800\r\n\r\n\r\nnhello, this is a little test\r\n.\r\n'
client.send(data)

getreply(client)












#input()

