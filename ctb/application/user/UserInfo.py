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
    getopenId = Comm.tryTranslate(request, "openId")
    if Comm.tryTranslateNull('openId', getopenId, callBackDict) == False:
        return callBackDict
    try:
        # 查询判断用户是否已经存在的
        userList = user.objects.filter(openId=getopenId)
        if len(userList) > 0:
            Comm.callBackSuccess(callBackDict, 1, userList[0].id)
            return callBackDict
        createTime = int(time.time() * 1000)
        if getopenId == '10000':
            userObj = user.objects.create(openId=getopenId, role=0, createTime=createTime)
        else:
            userObj = user.objects.create(openId=getopenId, role=2, createTime=createTime)
        userObj.save()
        Comm.callBackSuccess(callBackDict, 1, userObj.id)
    except BaseException as e:
        logger = logging.getLogger("django")
        logger.info(str(e))
        Comm.callBackFail(callBackDict,-1,"系统异常")
    return callBackDict



# 查询所有的用户
def adminGetAllUsers(request):
    # 取得获取的值
    callBackDict = {}
    # 验证用户的openID
    userObj = Jurisdiction.jurisdictGETOpenId(request, callBackDict)
    if userObj == None:
        return callBackDict
    userList = user.objects.all()
    list = []
    for oneuser in userList:
        list.append({"id":oneuser.id,"openId":oneuser.openId,"name":oneuser.name,"phone":oneuser.phone,"role":oneuser.role})
    return Comm.callBackSuccess(callBackDict, 1, list)