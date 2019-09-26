#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-08-28 15:02
# @File    : orm.py

import logging
from sql import MySQLCon


logs =logging.getLogger(__file__)
logs.setLevel(logging.DEBUG)
logs.addHandler(logging.StreamHandler)




class ModelMetaclass(type):

    def __new__(cls, name, bases, attrs):
        # skip base Model class:
        if name == 'Model':
            return type.__new__(cls, name, bases, attrs)
        if not '__database__' in attrs:
            attrs['__database__'] = 'default'
        if not '__table__' in attrs:
            attrs['__table__'] = name.lower()
        attrs['db'] = MySQLCon(use_dict=True)
        return type.__new__(cls, name, bases, attrs)



#定义model
class Model(dict):
    __metaclass__ = ModelMetaclass

    def __init__(self, **kw):
        super(Model, self).__init__(**kw)
        #Model.db.select_tables(self.__table__)
        #self.db.select_tables(self.__table__)
        
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError("'%s' instance has no attribute '%s'" % (self.__class__.__name__, key))

    def __setattr__(self, key, value):
        self[key]=value

    @classmethod
    def get(cls, id):
        '''
        Fetch from database by primary key id
        '''
        select_column_str = '*'
        where_condition_str='id=%s'%id
        d=cls.db.select(select_column_str,where_condition_str)
        return cls(**d[0]) if d else None

    @classmethod
    def filter(cls, where='', *args):
        '''
        Fetch a list of object according to the condition
        '''
        
        cls.db.select_tables(cls.__table__)
        select_column_str = '*'
        where_condition_str=where if where else ''

        L = cls.db.select(select_column_str,where)
        return [cls(**d) for d in L]
    @classmethod
    def filter_one(cls, where='', *args):
        '''
        Fetch the first object according to the condition
        '''
        
        L = cls.filter(where, *args)
        if len(L) > 0:
            return L[0]
        return None

    def save(self):
        '''
        Persisted to the database
        '''
        
        #self.db.select_tables(self.__table__)
        params = {}
        
        for k in self.__fields__:
            if hasattr(self, k):
                params[k] = getattr(self, k)
        # update or insert
        sql_dicts=dict(zip(params.keys(),params.values()))
        if hasattr(self,'id'):
            result = self.db.update(sql_dicts,'id=%s'%self.id)
        else:
            result =self.db.insert(sql_dicts)
        return result

    def remove(self):
        sql = 'DELETE FROM {} WHERE id=%s'.format(self.__table__)
        result = self.db.delete('id=%s'%self.id)
        self = None
        return result






class mytest(Model):
    __table__ ='testinfo'
    
    __fileds__ = ('id','size')

     


if __name__ == '__main__':
    test=mytest()
    a=test.filter_one("id='1'")
    a.size=1
    a.save()
    




    
    



    
    
    

   
