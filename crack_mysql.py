#coding=utf-8

import MySQLdb

def getdbh(host=None,user='root',passwd=None):
    dbh_dict=dict()
    dbh_dict.update(host=host,user='root',passwd=passwd)
    return dbh_dict
file_handel=file('1.txt','rb')
file1_handel=file('passwd.txt','rb')

for i in file_handel.readlines():
    i=i.strip('\n')

    for passwd in file1_handel.readlines():
        passwd=passwd.strip('\n')

        dhb=getdbh(host=i,user='root',passwd=passwd)

        try:
            MySQLdb.connect(**dhb)
        except Exception,e:

            continue
        print "host %s password is %s" %(i,passwd)


