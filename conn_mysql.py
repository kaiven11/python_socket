#coding=utf-8
import MySQLdb

dbh=MySQLdb.connect(user='root',passwd='rootadmin',db='test',host='127.0.0.1')
print 'connection successful'

cursor = dbh.cursor()
# 使用execute方法执行SQL语句
cursor.execute("select version()")
# 使用 fetchone() 方法获取一条数据库。
data = cursor.fetchone()
print "Database version : %s " % data
# 关闭数据库连接
dbh.close()

#lianjie shujuku de fangfa
def getdhb(db=None,user=None,passwd=None,host=None):
    qq=dict()
    if user==None:
        import os,pwd
        user=pwd.getpwuid(os.getuid())[0]
        qq.update(user=user)
    if passwd!=None:
        qq.update(passwd=passwd)
    if host!=None:
        qq.update(host=host)
    return qq

dbh_name=getdhb('test','root','rootadmin')


mysql_handel=MySQLdb.connect(**dbh_name)
print 'connect the server success!'

mysql=mysql_handel.cursor()
mysql.execute('show databases')
ll=mysql.fetchone()

#insert into data into the tables
# mysql.execute('use test')
# mysql.execute('insert into student values("haha",45)')
# mysql_handel.commit()


#create database:
# sql="""create database newbase"""
# mysql.execute(sql)
# mysql_handel.commit()

#int the database of newbase create a table named empoly

mysql.execute('use newbase')
# sql='create table empoly (name char(20) not null,age int,salary int)'
# mysql.execute(sql)

# insert one data

# sql='insert into empoly (name,age,salary) values("kaiven",25,5200)'
# mysql.execute(sql)
# mysql_handel.commit()

#delete a data

# sql="""delete from empoly where name='kaiven'"""
# mysql.execute(sql)


#update the data

# sql="""update empoly set name='lisarong' where name='kaiven'"""
# mysql.execute(sql)

#query the data

# sql='select * from test11'
# mysql.execute(sql)
# for column in mysql.description:#get the column name ,sometimes it is very usefull
#     print column
# #dataone=mysql.fetchone()
# print mysql.rowcount
# datasource=mysql.fetchall()
# for item in datasource:
#     print 'name :%s '%item[0]




#insertinto huge data ,so we use 'executemany' method

# data_put=(['lilfdi',121],
#          ['hahasha',451])
# mysql.executemany("""insert into test11 (name,age) values(%s,%s)""",data_put)
#
#






mysql_handel.commit()



