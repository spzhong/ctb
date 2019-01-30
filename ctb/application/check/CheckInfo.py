# -*- coding: utf-8 -*-
import logging
from django.http import HttpResponse
import json
import time
import sys
sys.path.append('...')
from ctb.models import user
from ctb.models import carInfo
from ctb.models import taskInfo
from ctb.models import getTask
from ctb.models import doTask
from ctb.models import checkRecord
from ctb.models import outStream
from ctb.models import incomeStream


from .. import Comm
from .. import Jurisdiction


# 获取待审核的任务
def getStayAdminCheck(request):
    callBackDict = {}
    # 验证用户的openID
    userObj = Jurisdiction.jurisAdminGETOpenId(request, callBackDict)
    if userObj == None:
        return callBackDict
    try:
        getcheckRecordList = checkRecord.objects.filter(isDone=0)
        list = []
        for oneRecord in getcheckRecordList:
            list.append({"id":oneRecord.id,"businessId":oneRecord.businessId,"type":oneRecord.type,"isDone":oneRecord.isDone,"createTime":oneRecord.createTime})
        return Comm.callBackSuccess(callBackDict,1,list)
    except BaseException as e:
        logger = logging.getLogger("django")
        logger.info(str(e))
        return Comm.callBackFail(callBackDict, -1, "系统异常")
    return callBackDict


# 获取所有的审核任务
def getALlAdminCheck(request):
    callBackDict = {}
    # 验证用户的openID
    userObj = Jurisdiction.jurisAdminGETOpenId(request, callBackDict)
    if userObj == None:
        return callBackDict
    try:
        getcheckRecordList = checkRecord.objects.all()
        list = []
        for oneRecord in getcheckRecordList:
            list.append({"id": oneRecord.id, "businessId": oneRecord.businessId, "type": oneRecord.type,
                         "isDone": oneRecord.isDone, "createTime": oneRecord.createTime})
        return Comm.callBackSuccess(callBackDict, 1, list)
    except BaseException as e:
        logger = logging.getLogger("django")
        logger.info(str(e))
        return Comm.callBackFail(callBackDict, -1, "系统异常")
    return callBackDict


# 提交任务
def submitCheck(request):
    callBackDict = {}
    # 验证用户的openID
    userObj = Jurisdiction.jurisdictGETOpenId(request, callBackDict)
    if userObj == None:
        return callBackDict
    getbusinessId = Comm.tryTranslate(request, "businessId")
    if Comm.tryTranslateNull("businessId", getbusinessId, callBackDict) == False:
        return callBackDict
    gettype = Comm.tryTranslate(request, "type")
    if Comm.tryTranslateNull("type", gettype, callBackDict) == False:
        return callBackDict
    try:
        getcreateTime = int(time.time() * 1000)
        checkRecordObj = checkRecord.objects.create(userId=userObj.id,createTime=getcreateTime,businessId=getbusinessId,type=gettype)
        checkRecordObj.save()
        return Comm.callBackSuccess(callBackDict,1,checkRecordObj.id)
    except BaseException as e:
        logger = logging.getLogger("django")
        logger.info(str(e))
        return Comm.callBackFail(callBackDict, -1, "系统异常")
    return callBackDict



# 内部程序创建任务
#0是审核创建的任务，1是审核车辆，2是审核领取任务，3是审核提交的任务，4是审核提现的任务
def createCheck(getbusinessId,gettype,userId):
    try:
        getcreateTime = int(time.time() * 1000)
        checkRecordObj = checkRecord.objects.create(userId=userId,createTime=getcreateTime,businessId=getbusinessId,type=gettype)
        checkRecordObj.save()
        return checkRecordObj
    except BaseException as e:
        logger = logging.getLogger("django")
        logger.info(str(e))
        return None



# 审核车辆的信息
def adminCheckCarInfo(request):
    callBackDict = {}
    # 验证用户的openID
    userObj = Jurisdiction.jurisAdminGETOpenId(request, callBackDict)
    if userObj == None:
        return callBackDict
    getcheckId = Comm.tryTranslate(request, "checkId")
    if Comm.tryTranslateNull("checkId", getcheckId, callBackDict) == False:
        return callBackDict
    getisDone = Comm.tryTranslate(request, "isDone")
    if Comm.tryTranslateNull("isDone", getisDone, callBackDict) == False:
        return callBackDict
    try:
        checkRecordObj = checkRecord.objects.get(id=getcheckId)
        checkRecordObj.isDone = getisDone;
        #处理自己的相关的业务员
        # 1是审核通过，1是审核失败
        if getisDone == 1 or getisDone == 2:
            carInfoObject = carInfo.objects.get(id=checkRecordObj.businessId)
            carInfoObject.status = getisDone
            carInfoObject.save()
        # 保存审核记录的状态
        checkRecordObj.save()
        return Comm.callBackSuccess(callBackDict,1,checkRecordObj.id)
    except BaseException as e:
        logger = logging.getLogger("django")
        logger.info(str(e))
        return Comm.callBackFail(callBackDict, -1, "系统异常")
    return callBackDict




# 审核是否可以领取该任务
def adminCheckGetTask(request):
    callBackDict = {}
    # 验证用户的openID
    userObj = Jurisdiction.jurisAdminGETOpenId(request, callBackDict)
    if userObj == None:
        return callBackDict
    getcheckId = Comm.tryTranslate(request, "checkId")
    if Comm.tryTranslateNull("checkId", getcheckId, callBackDict) == False:
        return callBackDict
    getisDone = Comm.tryTranslate(request, "isDone")
    if Comm.tryTranslateNull("isDone", getisDone, callBackDict) == False:
        return callBackDict
    try:
        checkRecordObj = checkRecord.objects.get(id=getcheckId)
        checkRecordObj.isDone = getisDone;
        # 处理自己的相关的业务员
        # 1是审核通过，1是审核失败
        if getisDone == 1 or getisDone == 2:
            getTaskObject = getTask.objects.get(id=checkRecordObj.businessId)
            getTaskObject.status = getisDone
            getTaskObject.save()
        checkRecordObj.save()
        return Comm.callBackSuccess(callBackDict, 1, checkRecordObj.id)
    except BaseException as e:
        logger = logging.getLogger("django")
        logger.info(str(e))
        return Comm.callBackFail(callBackDict, -1, "系统异常")
    return callBackDict



# 审核做的任务
def adminCheckDoTask(request):
    callBackDict = {}
    # 验证用户的openID
    userObj = Jurisdiction.jurisAdminGETOpenId(request, callBackDict)
    if userObj == None:
        return callBackDict
    getcheckId = Comm.tryTranslate(request, "checkId")
    if Comm.tryTranslateNull("checkId", getcheckId, callBackDict) == False:
        return callBackDict
    getisDone = Comm.tryTranslate(request, "isDone")
    if Comm.tryTranslateNull("isDone", getisDone, callBackDict) == False:
        return callBackDict
    try:
        checkRecordObj = checkRecord.objects.get(id=getcheckId)
        checkRecordObj.isDone = getisDone;
        # 处理自己的相关的业务员
        # 1是审核通过，1是审核失败
        if getisDone == 1 or getisDone == 2:
            doTaskObject = doTask.objects.get(id=checkRecordObj.businessId)
            doTaskObject.status = getisDone
            doTaskObject.save()
            createIncomeStream(checkRecordObj,doTaskObject,getisDone)
        checkRecordObj.save()
        return Comm.callBackSuccess(callBackDict, 1, checkRecordObj.id)
    except BaseException as e:
        logger = logging.getLogger("django")
        logger.info(str(e))
        return Comm.callBackFail(callBackDict, -1, "系统异常")
    return callBackDict




# 审核做的任务--如果是第二次的话，创建收入的记录
def createIncomeStream(checkRecordObj,doTaskObject,getisDone):
    # 审核失败
    if getisDone == 2:
        return
    # 审核通过的 - doTaskObject- 查询出来，审核通过2的数据，之间的差
    doTaskList = doTask.objects.filter(userId=doTaskObject.userId,openId=doTaskObject.openId,getTaskId=doTaskObject.getTaskId,status=1)
    if len(doTaskList) == 0:
        return
    # 取得第一条的数据，判断其时间
    theFisrtDoTask = doTaskList[0]
    if theFisrtDoTask == None:
        return
    try:
        # 更新结算日
        getTaskObj = getTask.objects.get(id=doTaskObject.getTaskId)
        getTaskObj.startdoTaskTime = theFisrtDoTask.createTime
        getTaskObj.save()
        # 获取具体的任务详情
        taskInfoObj = taskInfo.objects.get(id=getTaskObj.taskId)
        if taskInfoObj.status == -1:
            # 已经删除了，就不在产生订单了
            return
        # 取得交易的结算日--异常的数据
        if theFisrtDoTask.createTime > taskInfoObj.deadline:
            # 任务已经超过截止的时间了，就不在产生订单了
            return
        # --查询最后一条的订单，按照时间倒叙排序
        incomeStreamList = incomeStream.objects.filter(userId=getTaskObj.userId,openId=getTaskObj.openId,getTaskId=getTaskObj.id).order_by("-createTime")[:1]
        theLastTime = doTaskObject.createTime
        if len(incomeStreamList) == 0:
            return
        # 最后的时间
        theLastTime = incomeStreamList[0].createTime
    except BaseException as e:
        logger = logging.getLogger("django")
        logger.info(str(e))



# 审核提现的任务
def adminCheckOutStream(request):
    callBackDict = {}
    # 验证用户的openID
    userObj = Jurisdiction.jurisAdminGETOpenId(request, callBackDict)
    if userObj == None:
        return callBackDict
    getcheckId = Comm.tryTranslate(request, "checkId")
    if Comm.tryTranslateNull("checkId", getcheckId, callBackDict) == False:
        return callBackDict
    getisDone = Comm.tryTranslate(request, "isDone")
    if Comm.tryTranslateNull("isDone", getisDone, callBackDict) == False:
        return callBackDict
    try:
        checkRecordObj = checkRecord.objects.get(id=getcheckId)
        checkRecordObj.isDone = getisDone;
        # 处理自己的相关的业务员
        # 1是审核通过，1是审核失败
        if getisDone == 1 or getisDone == 2:
            outStreamObject = outStream.objects.get(id=checkRecordObj.businessId)
            outStreamObject.status = getisDone
            outStreamObject.save()
        checkRecordObj.save()
        return Comm.callBackSuccess(callBackDict, 1, checkRecordObj.id)
    except BaseException as e:
        logger = logging.getLogger("django")
        logger.info(str(e))
        return Comm.callBackFail(callBackDict, -1, "系统异常")
    return callBackDict
