# -*- coding: utf-8 -*-
import json
import CheckInfo
from django.http import HttpResponse

from django.db import connections

def close_old_connections():
    for conn in connections.all():
        conn.close_if_unusable_or_obsolete()

def index(request,route):
    close_old_connections()
    if route == 'getStayAdminCheck':
        callBackDict = CheckInfo.getStayAdminCheck(request)
    elif route == 'submitCheck':
        callBackDict = CheckInfo.submitCheck(request)
    elif route == 'adminCheckCarInfo':
        callBackDict = CheckInfo.adminCheckCarInfo(request)
    elif route == 'adminCheckGetTask':
        callBackDict = CheckInfo.adminCheckGetTask(request)
    elif route == 'adminCheckDoTask':
         callBackDict = CheckInfo.adminCheckDoTask(request)
    elif route == 'adminCheckOutStream':
         callBackDict = CheckInfo.adminCheckOutStream(request)
    elif route == 'getALlAdminCheck':
         callBackDict = CheckInfo.getALlAdminCheck(request)
    elif route == 'adminBusinessInfo':
        callBackDict = CheckInfo.adminBusinessInfo(request)
    elif route == 'sendMateriel':
        callBackDict = CheckInfo.sendMateriel(request)
    else:
         return HttpResponse("no found !!!")
    if callBackDict == None :
        callBackDict = {"code":-1,'msg':'系统异常'}
    return HttpResponse(json.dumps(callBackDict))

