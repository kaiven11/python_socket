#!/usr/bin/env python
# -*- coding:utf-8 -*-

import MySQLdb

# 把 commit 放到外面
class MySQLCon:
    def __init__(self, host="", user="", password="", database="", tables="", charset='', manual=0, use_dict=False, none_value="default"):
        """
        初始化链接，如果不制定，则默认使用global_para中的参数，且初始化是不会指定表名
        :param host: MySQL地址
        :param user: 访问用户
        :param password: 访问用户的密码
        :param database: 数据库
        :param tables: 表名
        :param manual: 是否进行手动提交，默认为0 （不进行），当一次要操作的数据库条数比较多(100+)时，手动提交可以
        明显提高数据库操作速度，此值设为1后，需要在执行sql命令后手动调用提交函数,只适用于insert 和 update
        :param use_dict: bool 默认 False 是否使用字典返回select的查询结果，默认为否
        :param none_value: string 默认 default，当插入或者更新一个值为 Python 的 None 时，将 None 转换为那种字段插入数据库，如： null、default
        """
        self.host = SQL_HOST if not host else host
        self.user = SQL_USER if not user else user
        self.password = SQL_PASSWD if not password else password
        self.database = SQL_DATEBASES if not database else database
        self.tables = "" if not tables else tables
        self.status = False
        self.manual = manual
        self.charset = SQL_CHARSET if not charset else charset
        self.logs = logs  # 把logs模块赋值给MySQLCon内部属性,以免退出MySQLCon作用域时调用__del__方法时出现异常
        self.cur = False  # 判断连接是否建立
        self.none_value = none_value
        try:
            self.conn = MySQLdb.connect(host=self.host, user=self.user, passwd=self.password, db=self.database,
                                        charset=self.charset)
            self.logs.debug("conn databases host:%s ,database:%s ,table(Probably None):%s" % (
            self.host, self.database, str(self.tables)))
            self.cur_class = MySQLdb.cursors.DictCursor if use_dict else None
            self.cur = self.conn.cursor(self.cur_class)
        except MySQLdb.Error as e:
            self.logs.error("conn databases host:%s ,database:%s ,table(Probably None):%s Mysql Error %d: %s" %
                            (self.host, self.database, str(self.tables), e.args[0], e.args[1]))
            raise MySQLdb.Error, e  # 连接错误是肯定无法在执行新的函数的

    def select_tables(self, tables_str):
        """
        选择要使用的表
        :param tables_str:string
        :return:
        """
        self.tables = tables_str
        self.logs.debug("use tables `%s`" % self.tables)
        return self

    def _exec_sql_cmd(self, sql_cmd_str, force_commit=0):
        """
        执行具体的命令
        :param sql_cmd_str: 要执行的sql语句
        :param force_commit:是否强制提交 1 代表强制提交
        :return:
        """
        if not self.cur:
            logs.error("Unconnected sql to %s ,The link is not established" % self.host)
            return
        self.logs.debug("exec mysql cmd %s" % sql_cmd_str)
        try:
            self.cur.execute(sql_cmd_str)
        except MySQLdb.Error as e:
            self.logs.error("Mysql Error:%s  info:%s\n" % (sql_cmd_str, e))
            self.status = False
        if not self.manual or force_commit:
            self.commit_manual()
        return self.status

    def commit_manual(self):
        try:
            self.conn.commit()
            self.status = True
        except MySQLdb.Error as e:
            self.conn.rollback()
            self.logs.error("Mysql Error:%s\n" % e)
        return self.status

    def insert(self, sql_dicts, addition_str=""):
        """
        向数据库中插入一条数据，使用前应指定表（使用select_tables，或在初始化时指定）
        :param sql_dicts: 要更新或插入的数据的字典，字典的key值是字段名，value该字段要插入或更新的值
        :param addition_str: 其他条件，如WHERE等，内容包括关键字 默认为空
        :return:成功返回True 失败返回False
        """
        if not self.tables:
            self.logs.error("not select tables")
            return
        sql_cmd = "INSERT INTO " + self.tables + " SET "
        for items in sql_dicts.items():
            if items[1] is None:
                sql_cmd += "`" + items[0] + "`" + "=" + "%s," % self.none_value
            else:
                sql_cmd += "`" + items[0] + "`" + "=" + ("'%s'," % items[1])
        sql_cmd = sql_cmd[:-1]  # 去掉最后一个逗号
        sql_cmd += addition_str
        return self._exec_sql_cmd(sql_cmd)

    def update(self, sql_dicts, where_condition_str="", addition_str="", addition_str_front=""):
        """
        向数据库中更新一条数据，使用前应指定表（使用select_tables，或在初始化时指定）,注意自字符串中插入数据应有''
        :param sql_dicts:要更新或插入的数据的字典，字典的key值是字段名，value该字段要插入或更新的值
        :param where_condition_str:插入的位置
        :param addition_str: 其他条件 默认为空，会添加到 WHERE条件之后
        :param addition_str_front: 其他条件 默认为空， 会添加到 WHERE条件之前
        :return:成功返回True 失败返回False
        """
        if not self.tables:
            self.logs.error("not select tables")
            return
        sql_cmd = "UPDATE " + self.tables + " SET "
        for items in sql_dicts.items():
            if items[1] is None:
                sql_cmd += "`" + items[0] + "`" + "=" + "%s," % self.none_value
            else:
                sql_cmd += "`" + items[0] + "`" + "=" + ("'%s'," % items[1])
        sql_cmd = sql_cmd[:-1]  # 去掉最后一个逗号
        if addition_str_front:
            sql_cmd += " " + addition_str_front
        if where_condition_str:
            sql_cmd += " WHERE " + where_condition_str
        if addition_str:
            sql_cmd += " " + addition_str
        return self._exec_sql_cmd(sql_cmd)

    def select(self, select_column_str, where_condition_str="", addition_str=""):
        """
        查询使用前应指定表（使用select_tables，或在初始化时指定）,注意自字符串中插入数据应有''
        :param select_column_str: 查询列的字段,可查询多条，字符串中以逗号分隔，注意没有空格eg："name,age,score"
        :param where_condition_str: 查询条件，注意在要写上''
        :param addition_str: 其他条件 默认为空
        :return:查询到的元组，失败查询返回False
        """
        if not self.tables:
            self.logs.error("not select tables")
            return
        sql_cmd = "SELECT %s FROM %s" % (select_column_str, self.tables)
        if where_condition_str:
            sql_cmd += " WHERE %s %s" % (where_condition_str, addition_str)
        if self._exec_sql_cmd(sql_cmd, force_commit=1):
            result = self.cur.fetchall()
            self.logs.debug("select result %s" % str(result))
        else:
            result = False
        return result

    def count(self, table="", col="*", where_condition_str="", addition_str=""):
        """
        查询表中数据行数
        :param table: string 如果为空， 则会使用当前设置的表
        :param col: string 查询的列名，默认为 "*" 及查询行数
        :param where_condition_str:  string 查询限制条件, 即 where 关键字之后的字符串（不包括 where）
        :param addition_str: string 其他查询限制条件的字符串
        :return: 成功 long 失败 bool
        """
        table = self.tables if not table else table
        where_condition_str = where_condition_str if not where_condition_str else "WHERE " + where_condition_str
        sql_cmd = "SELECT count(%s) FROM %s %s %s" % (col, table, where_condition_str, addition_str)
        if self._exec_sql_cmd(sql_cmd, force_commit=1):
            result = self.cur.fetchall()
            self.logs.debug("select resself.none_valueult %s" % str(result))
            result = result[0][0]
        else:
            result = False
        return result

    def insert_if_exist_value_update(self, sql_dicts, value_key, update_addition_str="",
                                     insert_addition_str="", select_addition_str=""):
        """
        向数据库中插入一条数据，如果存在某一条数据，则更新，如果不存在则插入
        本函数主要执行两部操作
        第一步：
        根据 value_key 和 select_addition_str 对表进行查询，再根据是查询结果来执行后续定做
        第二部：
        第一步查询到了对应的一条或多条信息，则：
        根据 sql_dicts 和 update_addition_str 来执行 update 操作
        第一步没有查询到对应的一条或多条信息，则：
        根据 sql_dicts 和 insert_addition_str 来执行 insert 操作
        :param sql_dicts: dict 要更新或插入的数据的字典，字典的key值是字段名，value 该字段要插入或更新的值，
        注意字典中要包括用来判断是更新还是插入的那一个字段的信息，即 value_key
        :param value_key:string，用来判断是更新还是插入的那一个字段的的key（存在于第一个参数的字典中的一个key值）
        :param update_addition_str: string 默认为空 update 时的其他条件
        :param insert_addition_str: string 默认为空 insert 时的其它条件
        :param select_addition_str: string 默认为空 select 时的其它条件
        :return:成功返回True 失败返回False
        """
        if not self.tables:
            self.logs.error("not select tables")
            return
        if not sql_dicts.has_key(value_key):
            raise KeyError("sql_dicts no necessary key %s" % value_key)
        if self.select("*", "`%s`='%s'" % (value_key, sql_dicts[value_key]), select_addition_str):
            # 从sql_dicts中删除用来进行匹配的关键字，否则update会冲突
            value = sql_dicts[value_key]
            sql_cmd = "UPDATE " + self.tables + " SET "
            empty_falg = True
            for items in sql_dicts.items():
                if items[0] == value_key:
                    continue
                empty_falg = False

                if items[1] is None:
                    sql_cmd += "`" + items[0] + "`" + "=" + "%s," % self.none_value
                else:
                    sql_cmd += "`" + items[0] + "`" + "=" + ("'%s'," % items[1])
            if empty_falg:
                # 没有要更新的内容，一般会在要更新的信息只有一条的时候 empty_falg == True，表示你要更新的这一条信息已经
                # 存在了，所以没什么可更新的了，因为你只有这一条信息要进行更新
                logs.warning("empty sql info cmd when update %s" % self.tables)
                return
            sql_cmd = sql_cmd[:-1]  # 去掉最后一个逗号
            sql_cmd += " WHERE " + "`%s`='%s'" % (value_key, value)
            sql_cmd += update_addition_str
            return self._exec_sql_cmd(sql_cmd)
        else:
            # *************** 没有查询到对应的一条或多条信息 *******************
            return self.insert(sql_dicts, insert_addition_str)


    def delete_other(self, clear_list, clear_key, addition_str=""):
        """
        删除表中 clear_key 字段 clear_list 之外的所有数据
        例如
            clear_list = ["zhangsan", "lisi", "wanger", "mazi"]
            clear_key = "name"
            那么对应的表中 除了 name 是 "zhangsan", "lisi", "wanger", "mazi" 的其余的数据都将被删除，删除完毕后表中
            只会剩余 name 是 "zhangsan", "lisi", "wanger", "mazi" 这几条数据
            所以如果传入的 clear_list 是空链表，那么 表中所有数据将会被清除
        :param clear_list: list[value]: 字段值
        :param clear_key: string: 字段名
        :param addition_str: string: 附加条件
        :return:
        """
        if not clear_list:
            logs.warning("clear_list is None")
            return
        sql_com = ""  # 3个 “ ” 是为了当 clear_list为空时， 下面的[:-3]可以得到一个空字符串，这样可以删除表中所有数据
        for i in xrange(len(clear_list)):
            sql_com += "'{}', ".format(clear_list[i])
            if i == len(clear_list) - 1:
                sql_com = sql_com[:-2]
        if sql_com:
            sql_com = "`{}` NOT IN ".format(clear_key) + "(" + sql_com + ") "
        if addition_str:
            sql_com += addition_str
        return self.delete(sql_com)  # -3 是为了清除 最后一个 AND

    def delete(self, where_condition_str=None):
        """
        删除一条数据库信息
        :param where_condition_str: where后的条件，如果为空或""则会删除该表所有信息，注意在要写上''(`key` `value`)
        :return:成功返回True 失败返回False
        """
        sql = "DELETE FROM %s" % self.tables
        if not self.tables:
            self.logs.error("not select tables")
            return
        if where_condition_str:
            sql.join("%s" % where_condition_str)
            sql = " %s WHERE %s" % (sql, where_condition_str)
        return self._exec_sql_cmd(sql, force_commit=1)

    def manual_close_conn(self):
        self.__del__()

    def __del__(self):
        if self.cur:
            self.conn.close()
        self.logs.debug("success closed databases host:%s,database:%s" % (self.host, self.database))


# test
if __name__ == "__main__":
    pass

   
