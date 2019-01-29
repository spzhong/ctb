# -*- coding: utf-8 -*-
import logging
from django.http import HttpResponse
import json
import sys
import time
sys.path.append('...')
from ctb.models import user
from .. import Comm
from .. import Jurisdiction



# 微信登录注册认证
def wxegisterSign(request):
    # 取得获取的值
    callBackDict = {}
    getopneId = Comm.tryTranslate(request, "opneId")
    if Comm.tryTranslateNull('opneId', getopneId, callBackDict) == False:
        return callBackDict
    try:
        # 查询判断用户是否已经存在的
        userList = user.objects.filter(openId = getopneId)
        if len(userList) > 0:
            Comm.callBackSuccess(callBackDict, 1, userList[0].id)
            return
        createTime = int(time.time() * 1000)
        userObj = user.objects.create(openId=getopneId, role=2, createTime=createTime)
        userObj.save()
        Comm.callBackSuccess(callBackDict, 1, userObj.id)
    except BaseException as e:
        Comm.callBackFail(callBackDict,-1,"系统异常")
    return callBackDict



