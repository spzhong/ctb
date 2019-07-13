# -*- coding: utf-8 -*-
import json

from django.http import HttpResponse

from django.db import connections

def close_old_connections():
    for conn in connections.all():
        conn.close_if_unusable_or_obsolete()

def index(request,route):
    close_old_connections()
    callBackDict = {}
    if route == 'appAutoHandshake':
        pass
    else:
         return HttpResponse("no found !!!")
    if callBackDict == None :
        callBackDict = {"code":-1,'msg':'系统异常'}
    return HttpResponse(json.dumps(callBackDict))


