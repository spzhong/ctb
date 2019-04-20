# -*- coding: utf-8 -*-
import json
import CheckInfo

from django.http import HttpResponse



def index(request,route):
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
    return HttpResponse(json.dumps(callBackDict))

