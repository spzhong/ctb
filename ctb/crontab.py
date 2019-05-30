# -*- coding: utf-8 -*-
import logging
import time

import json
import urllib


# 执行的任务
def doTask():
    print '执行了'
    f = urllib.urlopen('http://appid.985-985.com:8088/getAppConfig.php?appid=chenspeed2')
    print f.read().decode('utf-8')







