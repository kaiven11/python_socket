#coding=utf-8
from email.mime.text import MIMEText
import smtplib
import email.utils



message="hello,this is test"
msg=MIMEText(message)
msg['TO']='1064187559@qq.com'
msg['FROM']='fengchubojue@126.com'
msg['SUBJECT']='test'
msg['DATE']=email.utils.formatdate(localtime=1)
msg['Message-ID']=email.utils.make_msgid()

print msg.as_string()

