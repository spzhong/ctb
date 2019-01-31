# -*- coding: utf-8 -*-
import json
import StreamInfo


from django.http import HttpResponse


def index(request,route):
    if route == 'getIncomeStreamList':
        callBackDict = StreamInfo.getIncomeStreamList(request)
    elif route == 'getoutStreamList':
        callBackDict = StreamInfo.getoutStreamList(request)
    elif route == 'reviewofPayments':
        callBackDict = StreamInfo.reviewofPayments(request)
    else:
         return HttpResponse("no found !!!")
    return HttpResponse(json.dumps(callBackDict))

