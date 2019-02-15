# -*- coding: utf-8 -*-
import json
import Car
import UserInfo
import CheckGetInfo

from django.http import HttpResponse


def index(request,route):
    if route == 'wxegisterSign':
        callBackDict = UserInfo.wxegisterSign(request)
    elif route == 'wxgetCarList':
        callBackDict = Car.wxgetCarList(request)
    elif route == 'wxAddCar':
        callBackDict = Car.wxAddCar(request)
    elif route == 'wxEditCar':
        callBackDict = Car.wxEditCar(request)
    elif route == 'getCarInfo':
        callBackDict = CheckGetInfo.getCarInfo(request)
    elif route == 'getGetTaskInfo':
        callBackDict = CheckGetInfo.getGetTaskInfo(request)
    elif route == 'getDoTaskInfo':
        callBackDict = CheckGetInfo.getDoTaskInfo(request)
    elif route == 'adminGetAllUsers':
        callBackDict = UserInfo.adminGetAllUsers(request)
    elif route == 'perfectUserInfo':
        callBackDict = UserInfo.perfectUserInfo(request)
    else:
         return HttpResponse("no found !!!")
    return HttpResponse(json.dumps(callBackDict))

