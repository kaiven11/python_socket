#coding=utf-8

from email.mime.text import MIMEText
import  email.utils
import  time
import smtplib

#create a email


message="hello, this is a little test"
msg=MIMEText(message)
msg['To']='1064187559@qq.com'
msg['From']='fengchubojue@126.com'
msg['Message-Id']=email.utils.make_msgid()
msg['Subject']='hahaaa'
msg['Date']=email.utils.formatdate(localtime=1)#

print msg.as_string()


s=smtplib.SMTP('smtp.126.com')
s.login('fengchubojue@126.com','123456q')
s.sendmail('fengchubojue@126.com','1064187559@qq.com',msg.as_string())
print 'send yes'


#resovl email text
'''
fd=open('1.txt')
msg=email.message_from_file(fd)
#print msg
if 'DATE' in msg:
    for key,value in msg.items():
        print msg['DATE']
        a=email.utils.mktime_tz(email.utils.parsedate_tz(msg['DATE']))
        print a

        break



#resovle date code
'''






