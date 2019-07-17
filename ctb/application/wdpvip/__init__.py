# -*- coding: utf-8 -*-
import json

from django.http import HttpResponse

from django.db import connections

import UserVdp
import WdpOrder




def close_old_connections():
    for conn in connections.all():
        conn.close_if_unusable_or_obsolete()

def index(request,route):
    close_old_connections()
    if route == 'wxegisterSign':
        callBackDict = UserVdp.wxegisterSign(request)
    elif route == 'adminGetAllUsers':
        callBackDict = UserVdp.adminGetAllUsers(request)
    elif route == 'perfectUserInfo':
        callBackDict = UserVdp.perfectUserInfo(request)
    elif route == 'webSign':
        callBackDict = UserVdp.webSign(request)
    elif route == 'adminisEnabledUser':
        callBackDict = UserVdp.adminisEnabledUser(request)
    elif route == 'createPlanningRoutes':
        callBackDict = WdpOrder.createPlanningRoutes(request)
    elif route == 'getPlanningRoutes':
        callBackDict = WdpOrder.getPlanningRoutes(request)
    elif route == 'getPlanningRoutes':
        callBackDict = WdpOrder.adminGetVdpOrder(request)
    elif route == 'adminModifyVdpOrder':
        callBackDict = WdpOrder.adminModifyVdpOrder(request)
    elif route == 'adminModifyPlanningRouteOk':
        callBackDict = WdpOrder.adminModifyPlanningRouteOk(request)
    elif route == 'adminModifyPlanningRouteFail':
        callBackDict = WdpOrder.adminModifyPlanningRouteFail(request)
    else:
         return HttpResponse("no found !!!")
    if callBackDict == None :
        callBackDict = {"code":-1,'msg':'系统异常'}
    return HttpResponse(json.dumps(callBackDict))




