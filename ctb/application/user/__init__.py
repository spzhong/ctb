# -*- coding: utf-8 -*-
import json
import Car
import UserInfo

from django.http import HttpResponse


def index(request,route):
    if route == 'wxegisterSign':
        callBackDict = UserInfo.wxegisterSign(request)
    elif route == 'wxgetCarList':
        callBackDict = Car.wxgetCarList(request)
    elif route == 'wxAddCar':
        callBackDict = Car.wxAddCar(request)
    else:
         return HttpResponse("no found !!!")
    return HttpResponse(json.dumps(callBackDict))

