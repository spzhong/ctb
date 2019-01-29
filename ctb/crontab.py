# -*- coding: utf-8 -*-
import logging
import time

from models import taskInfo
from models import getTask
from models import doTask


# 执行的任务
def doTask():
    createTime = int(time.time() * 1000)
    getTaskList = getTask.objects.filter(state=1,createTime__gte=createTime)



doTask()