# -*- coding: utf-8 -*-
import json
import automaticHandshake


from django.http import HttpResponse

from django.db import connections

def close_old_connections():
    for conn in connections.all():
        conn.close_if_unusable_or_obsolete()

def index(request,route):
    close_old_connections()
    if route == 'appAutoHandshake':
        callBackDict = automaticHandshake.appAutoHandshake(request)
    elif route == 'createProjectInfo':
        callBackDict = automaticHandshake.createProjectInfo(request)
    elif route == 'openAndCloseProject':
        callBackDict = automaticHandshake.openAndCloseProject(request)
    elif route == 'submitAuditProject':
        callBackDict = automaticHandshake.submitAuditProject(request)
    elif route == 'manualreleaseProject':
        callBackDict = automaticHandshake.manualreleaseProject(request)
    elif route == 'exchangeRegionCoefficient':
        callBackDict = automaticHandshake.exchangeRegionCoefficient(request)
    elif route == 'delAll':
        callBackDict = automaticHandshake.delAll(request)
    elif route == 'allProjectInfoList':
        callBackDict = automaticHandshake.allProjectInfoList(request)
    elif route == 'allOtherRegionCoefficient':
        callBackDict = automaticHandshake.allOtherRegionCoefficient(request)
    elif route == 'allAutoHandshakeUser':
        callBackDict = automaticHandshake.allAutoHandshakeUser(request)
    else:
         return HttpResponse("no found !!!")
    if callBackDict == None :
        callBackDict = {"code":-1,'msg':'系统异常'}
    return HttpResponse(json.dumps(callBackDict))



