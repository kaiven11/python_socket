#coding=utf-8

from email.mime.multipart import  MIMEMultipart
from email.mime.text import MIMEText
from email import utils
import mimetypes
import sys
from email.mime.base import MIMEBase
from email.mime.application import MIMEApplication

import smtplib

#

email_object=MIMEMultipart()
email_object['From']='fengchubojue@126.com'
email_object['To']='1064187559@qq.com'
#email_object['FROM']='13731250529@163.com'
email_object['Subject']='new111 test'
#email_object['Date']=utils.formatdate(localtime=1)
#email_object['Message-Id']=utils.make_msgid()
#print type(email_object)           print email_object.as_string()


email_body_text=MIMEText("不是你的也不是我的")
email_object.attach(email_body_text)

from email import Encoders
#这里添加附件
'''
a=MIMEApplication(open('1.txt','rb').read(),_subtype='octet-stream')
a.add_header('Content-Disposition', 'attachment', filename="2.PNG")
email_object.attach(a)

a=open('123.PNG','rb')
part=MIMEBase('application','octet-stream')
part.set_payload(a.read())
Encoders.encode_base64(part)
part.add_header('Content-Disposition', 'attachment', filename="2.txt")
email_object.attach(part)

'''

def gettype(filename):
    data=open(filename,'rb')
    mimetype,mimecoding=mimetypes.guess_type(filename)
    if mimetype is None:
        mimetype="application/octet-stream"
    a=attament(data.read(),mimetype)
    a.add_header('Content-Disposition', 'attachment', filename=filename)
    data.close()
    return a


def attament(data,filetype):
    a,b=filetype.split('/')
    email_base=MIMEBase(a,b)
    email_base.set_payload(data)
    Encoders.encode_base64(email_base)

    return email_base



server='smtp.126.com'

passwd='123456q'
fromaddr='fengchubojue@126.com'
toaddr='1064187559@qq.com'

if __name__=='__main__':

    filename=sys.argv[1]
    email_object.attach(gettype(filename))

    try:
        s=smtplib.SMTP()
        s.connect(server)
        s.login(fromaddr,passwd)
        s.set_debuglevel(1)
        s.sendmail(fromaddr,toaddr,email_object.as_string())
        s.quit()
    except smtplib.SMTPAuthenticationError:
        print 'Auth error'
    except smtplib.SMTPRecipientsRefused:
        print 'recipient refused'
    except smtplib.SMTPSenderRefused:
        print 'sender refused'
    except smtplib.SMTPException,e:
        print e.message
