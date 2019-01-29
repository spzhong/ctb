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
    else:
         return HttpResponse("no found !!!")
    return HttpResponse(json.dumps(callBackDict))

