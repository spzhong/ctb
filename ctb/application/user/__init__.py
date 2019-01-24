# -*- coding: utf-8 -*-

from django.http import HttpResponse
import json


def index(request,route):
    callBackDict = {'URL':'测试'}
    return HttpResponse(json.dumps(callBackDict))
