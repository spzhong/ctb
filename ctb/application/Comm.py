# -*- coding: utf-8 -*-
import logging
from django.http import HttpResponse
import json


# 校验用户上传的参数
def tryTranslate(request,key):
    try:
        getkey = request.GET[key]
    except BaseException as e:
        getkey = None
    return getkey


# 判断数据是否为空
def tryTranslateNull(key,value,callBackDict):
    if value == None:
        callBackDict['code'] = 0
        callBackDict['msg'] = "缺少["+key+"]字段"
        return False
    if len(value) == 0:
        callBackDict['code'] = 0
        callBackDict['msg'] = "[" + key + "]字段为空"
        return False
    if len(value) > 1024:
        callBackDict['code'] = 0
        callBackDict['msg'] = "[" + key + "]字段太长了"
        return False
    return True


# 成功的回调
def callBackSuccess(callBackDict,code,data):
    callBackDict['code'] = code
    callBackDict['data'] = data
    return callBackDict


# 失败的回调
def callBackFail(callBackDict,code,msg):
    callBackDict['code'] = code
    callBackDict['msg'] = msg
    return callBackDict