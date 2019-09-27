#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-09-27 9:40
# @Author  : sate
# @File    : 信号量.py
# @license : Copyright(C)2017-2018, New Armor Technology（北京数盾信息科技有限公司）

import threading
from threading import BoundedSemaphore

import time
sem = BoundedSemaphore(2)

def fun(i):
     with sem:
         print("---------current num is %s-----------\n"%i)
         time.sleep(3)



thread_list = []
for i in xrange(10):
    t=threading.Thread(target=fun,args=(i,))
    t.start()
    thread_list.append(t)


for i in thread_list:
    i.join()






