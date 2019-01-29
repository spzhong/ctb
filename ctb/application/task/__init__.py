# -*- coding: utf-8 -*-
import json
import TaskInfo

from django.http import HttpResponse


def index(request,route):
    if route == 'wxGetJoinTask':
        callBackDict = TaskInfo.wxGetJoinTask(request)
    elif route == 'wxGetALLTask':
        callBackDict = TaskInfo.wxGetALLTask(request)
    else:
         return HttpResponse("no found !!!")
    return HttpResponse(json.dumps(callBackDict))

