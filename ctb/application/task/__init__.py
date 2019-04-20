# -*- coding: utf-8 -*-
import json
import TaskInfo
import DoTask

from django.http import HttpResponse


def index(request,route):
    if route == 'wxGetJoinTask':
        callBackDict = TaskInfo.wxGetJoinTask(request)
    elif route == 'wxGetALLTask':
        callBackDict = TaskInfo.wxGetALLTask(request)
    elif route == 'wxReceiveTask':
        callBackDict = TaskInfo.wxReceiveTask(request)
    elif route == 'wxdoTask':
        callBackDict = DoTask.wxdoTask(request)
    elif route == 'adminGetALLTask':
        callBackDict = TaskInfo.adminGetALLTask(request)
    elif route == 'adminCreateTask':
        callBackDict = TaskInfo.adminCreateTask(request)
    elif route == 'adminDelTask':
        callBackDict = TaskInfo.adminDelTask(request)
    elif route == 'getUserAllDoTaskList':
        callBackDict = TaskInfo.getUserAllDoTaskList(request)
    elif route == 'wxGetTaskInfo':
        callBackDict = TaskInfo.wxGetTaskInfo(request)
    else:
         return HttpResponse("no found !!!")
    if callBackDict == None :
        callBackDict = {"code":-1,'msg':'系统异常'}
    return HttpResponse(json.dumps(callBackDict))

