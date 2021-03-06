# -*- coding: utf-8 -*-
import logging
from django.http import HttpResponse
import json
import time
import sys
from django.db.models import Sum
from ctb.models import user
sys.path.append('...')
from ctb.models import incomeStream
from ctb.models import outStream
from .. import Comm
from .. import Jurisdiction



# 获取收入的流水
def getIncomeStreamList(request):
    callBackDict = {}
    # 验证用户的openID
    userObj = Jurisdiction.jurisdictGETOpenId(request, callBackDict)
    if userObj == None:
        return callBackDict
    getstatus = Comm.tryTranslate(request, "status")
    if Comm.tryTranslateNull("status", getstatus, callBackDict) == False:
        return callBackDict
    # 匹配当前的状态
    if getstatus == 'all':
        incomeStreamList = incomeStream.objects.filter(userId=userObj.id, openId=userObj.openId)
    else:
        incomeStreamList = incomeStream.objects.filter(userId=userObj.id, openId=userObj.openId, status=getstatus)
    list = []
    for oneincomeStream in incomeStreamList:
        list.append({"id":oneincomeStream.id,"checkRecordId":oneincomeStream.checkRecordId,"getTaskId":oneincomeStream.getTaskId,"money":oneincomeStream.money,"createTime":oneincomeStream.createTime,"endTime":oneincomeStream.endTime,"status":oneincomeStream.status})
    return  Comm.callBackSuccess(callBackDict, 1, list)



# 获取支出的流水
def getoutStreamList(request):
    callBackDict = {}
    # 验证用户的openID
    userObj = Jurisdiction.jurisdictGETOpenId(request, callBackDict)
    if userObj == None:
        return callBackDict
    outStreamList = outStream.objects.filter(userId=userObj.id, openId=userObj.openId)
    list = []
    for oneoutStream in outStreamList:
        list.append({"id":oneoutStream.id,"checkRecordId": oneoutStream.checkRecordId,
                     "money": oneoutStream.money, "createTime": oneoutStream.createTime})
    return Comm.callBackSuccess(callBackDict, 1, list)


# 收支概述
def reviewofPayments(request):
    callBackDict = {}
    # 验证用户的openID
    userObj = Jurisdiction.jurisdictGETOpenId(request, callBackDict)
    if userObj == None:
        return callBackDict
    try:
        futureMoney = incomeStream.objects.filter(userId=userObj.id, openId=userObj.openId, status=0).aggregate(
            Sum("money"))
    except BaseException as e:
        logger = logging.getLogger("django")
        logger.info(str(e))
        return Comm.callBackFail(callBackDict, -1, "系统异常")
    try:
        incomeStreammoney = incomeStream.objects.filter(userId=userObj.id, openId=userObj.openId, status=1).aggregate(
            Sum("money"))
    except BaseException as e:
        logger = logging.getLogger("django")
        logger.info(str(e))
        return Comm.callBackFail(callBackDict, -1, "系统异常")
    try:
        outcomeStreammoney = outStream.objects.filter(userId=userObj.id, openId=userObj.openId).aggregate(Sum("money"))
    except BaseException as e:
        logger = logging.getLogger("django")
        logger.info(str(e))
        return  Comm.callBackFail(callBackDict, -1, "系统异常")

    logger = logging.getLogger("django")
    logger.info(str(incomeStreammoney))

    # 综述的回调
    if incomeStreammoney["money__sum"] == None:
        incomeStreammoneyInt = 0
    else:
        incomeStreammoneyInt = int(incomeStreammoney["money__sum"])

    if outcomeStreammoney["money__sum"] == None:
        outcomeStreammoneyInt = 0
    else:
        outcomeStreammoneyInt = int(outcomeStreammoney["money__sum"])
    if futureMoney["money__sum"] == None:
        futureMoneyInt = 0
    else:
        futureMoneyInt = int(futureMoney["money__sum"])
    balance = incomeStreammoneyInt - outcomeStreammoneyInt
    return Comm.callBackSuccess(callBackDict, 1, {"futureMoney":futureMoneyInt,"alreadyMoney":incomeStreammoneyInt,"payMoney":outcomeStreammoneyInt,"balance":balance})

