# -*- coding: utf-8 -*-
import logging
from django.http import HttpResponse
import json
import sys
import time
sys.path.append('...')
from ctb.models import user
from ctb.models import carInfo
from ctb.models import taskInfo
from ctb.models import getTask
from ctb.models import doTask
from ctb.models import incomeStream
from ..check import CheckInfo

from .. import Comm
from .. import Jurisdiction


# 获取当前用户参与的任务
def wxGetJoinTask(request):
    callBackDict = {}
    # 验证用户的openID
    userObj = Jurisdiction.jurisdictGETOpenId(request, callBackDict)
    if userObj == None:
        return callBackDict
    # 领取审核通过的数据
    logger = logging.getLogger("django")
    logger.info("userId:"+str(userObj.id))
    logger.info("openId:" + str(userObj.openId))
    try:
        getTaskList = getTask.objects.all()
    except BaseException as e:
        logger = logging.getLogger("django")
        logger.info(str(e))
        return Comm.callBackFail(callBackDict,-1,"暂无数据")
    list = []
    logger.info("len:" + str(len(getTaskList)))
    for onegetTask in getTaskList:
        dict = {}
        # 查询未完成的订单
        dict["id"] = onegetTask.id
        dict["carId"] = onegetTask.carId
        dict["taskId"] = onegetTask.taskId
        incomeStreamList = incomeStream.objects.filter(userId=userObj.id, openId=userObj.openId,getTaskId=onegetTask.id, status=0).order_by("-createTime")
        # 没有产生任何的订单
        if len(incomeStreamList)==0:
            dict['billingCycle'] = 0
            continue
        dict['billingCycle'] = incomeStreamList[0].createTime
        list.append(dict)
    # 组装完数据的回调
    Comm.callBackSuccess(callBackDict, 1, list)
    return callBackDict





# 将任务的对象信息转换为字典
def makeDictaskInfo(taskInfo):
    try:
        imgsJosn = json.loads(taskInfo.adImgs)
    except BaseException as e:
        imgsJosn = []
    return  {"id": taskInfo.id, "title": taskInfo.title, "createTime": taskInfo.createTime,
     "activityRange": taskInfo.activityRange, "billingCycle": taskInfo.billingCycle,
     "collectionsNum": taskInfo.collectionsNum, "limitNum": taskInfo.limitNum, "priceMonth": taskInfo.priceMonth,
     "stickerArea": taskInfo.stickerArea, "deadline": taskInfo.deadline, "info": taskInfo.info,
     "remark": taskInfo.remark,"status":taskInfo.status, "adImgs": imgsJosn}



# 微信获取所有的任务
def wxGetALLTask(request):
    callBackDict = {}
    # 验证用户的openID
    userObj = Jurisdiction.jurisdictGETOpenId(request, callBackDict)
    if userObj == None:
        return callBackDict
    try:
        taskInfoList = taskInfo.objects.filter(status__range=[2, 3])
        list = []
        for onetaskInfo in taskInfoList:
            list.append(makeDictaskInfo(onetaskInfo))
        Comm.callBackSuccess(callBackDict, 1, list)
    except BaseException as e:
        Comm.callBackFail(callBackDict,-1,"系统异常")
        logger = logging.getLogger("django")
        logger.info(str(e))
    return callBackDict



# wxGetTaskInfo
def wxGetTaskInfo(request):
    callBackDict = {}
    gettaskId = Comm.tryTranslate(request, "taskId")
    if Comm.tryTranslateNull('taskId', gettaskId, callBackDict) == False:
        return callBackDict
    # 验证用户的openID
    userObj = Jurisdiction.jurisdictGETOpenId(request, callBackDict)
    if userObj == None:
        return callBackDict
    try:
        onetaskInfo = taskInfo.objects.get(id=gettaskId)
        # 查询当前用户是否已经领取了
        getTaskUserList = getTask.objects.filter(userId=userObj.id,openId=userObj.openId,taskId=gettaskId)
        dict = makeDictaskInfo(onetaskInfo)
        if len(getTaskUserList) > 0:
            dict["isGet"] = 1
        else:
            dict["isGet"] = 0
        Comm.callBackSuccess(callBackDict, 1, dict)
    except BaseException as e:
        Comm.callBackFail(callBackDict,-1,"系统异常")
        logger = logging.getLogger("django")
        logger.info(str(e))
    return callBackDict



# 获取所有提交过的任务信息
def getUserAllDoTaskList(request):
    callBackDict = {}
    getopenId = Comm.tryTranslate(request, "openId")
    getuserId = Comm.tryTranslate(request, "userId")
    getgettaskId = Comm.tryTranslate(request, "getTaskId")
    if Comm.tryTranslateNull('openId', getopenId, callBackDict) == False:
        return callBackDict
    if Comm.tryTranslateNull('userId', getuserId, callBackDict) == False:
        return callBackDict
    if Comm.tryTranslateNull('getTaskId', getgettaskId, callBackDict) == False:
        return callBackDict
    # 查询当前永不所有提交的任务信息
    doTaskList = doTask.objects.filter(userId=getuserId,openId=getopenId,getTaskId=getgettaskId)
    list = []
    for doTaskObj in doTaskList:
        dataDict = {}
        dataDict["id"] = doTaskObj.id
        dataDict["userId"] = doTaskObj.userId
        dataDict["openId"] = doTaskObj.openId
        dataDict["createTime"] = doTaskObj.createTime
        dataDict["status"] = doTaskObj.status
        dataDict["getTaskId"] = doTaskObj.getTaskId
        dataDict["latitude"] = doTaskObj.latitude
        dataDict["longitude"] = doTaskObj.longitude
        dataDict["status"] = doTaskObj.status
        try:
            dataDict["adImgs"] = json.loads(doTaskObj.adImgs)
        except BaseException as e:
            dataDict["adImgs"] = []
        list.append(dataDict)
    return Comm.callBackSuccess(callBackDict, 1, list)



# 领取任务
def wxReceiveTask(request):
    callBackDict = {}
    # 验证用户的openID
    userObj = Jurisdiction.jurisdictGETOpenId(request, callBackDict)
    if userObj == None:
        return callBackDict
    gettaskId = Comm.tryTranslate(request,"taskId")
    getcarId = Comm.tryTranslate(request,"carId")
    if Comm.tryTranslateNull('taskId', gettaskId, callBackDict) == False:
        return callBackDict
    if Comm.tryTranslateNull('carId', getcarId, callBackDict) == False:
        return callBackDict
    #判断车辆和任务的审核状态
    taskMsg = judgeAuditStatusTaskId(gettaskId)
    if taskMsg != None:
        return Comm.callBackFail(callBackDict, -1, taskMsg)
    catMsg = judgeAuditStatusCarId(getcarId)
    if catMsg != None:
        return Comm.callBackFail(callBackDict, -1, catMsg)
    try:
        getTaskList = getTask.objects.filter(userId=userObj.id,carId = getcarId, openId=userObj.openId, taskId = gettaskId)
        if len(getTaskList) > 0:
            return Comm.callBackFail(callBackDict, -5, "该任务已领取过")
        #判断该任务的剩余次数
        try:
            taskInfoObj = taskInfo.objects.get(id = gettaskId)
        except BaseException as e:
            return Comm.callBackFail(callBackDict, -6, "该任务不存在")
        if taskInfoObj.status == -1:
            return Comm.callBackFail(callBackDict, -7, "该任务已经删除")
        if taskInfoObj.collectionsNum == taskInfoObj.limitNum:
            return Comm.callBackFail(callBackDict, -8, "该任务已领取完")
        # 创建一条新的领取的任务
        getcreateTime = int(time.time() * 1000)
        getTaskObj = getTask.objects.create(userId=userObj.id,carId=getcarId, openId=userObj.openId, taskId = gettaskId , createTime=getcreateTime)
        getTaskObj.save()
        # 任务领取的计数加一
        taskInfoObj.collectionsNum = taskInfoObj.collectionsNum + 1
        taskInfoObj.save()
        # 创建一条审核的任务
        CheckInfo.createCheck(getTaskObj.id, 2, userObj.id)
        Comm.callBackSuccess(callBackDict, 1, getTaskObj.id)
    except BaseException as e:
        logger = logging.getLogger("django")
        logger.info(str(e))
        Comm.callBackFail(callBackDict, -1, "系统异常")
    return callBackDict



# 管理员获取所有的任务
def adminGetALLTask(request):
    callBackDict = {}
    # 验证用户的openID
    userObj = Jurisdiction.jurisAdminGETOpenId(request, callBackDict)
    if userObj == None:
        return callBackDict
    getstatus = Comm.tryTranslate(request, "status")
    if Comm.tryTranslateNull('status', getstatus, callBackDict) == False:
        return callBackDict
    try:
        if getstatus == 'all':
            taskInfoList = taskInfo.objects.all()
        else:
            taskInfoList = taskInfo.objects.filter(status=getstatus)
        list = []
        for onetaskInfo in taskInfoList:
            list.append(makeDictaskInfo(onetaskInfo))
        Comm.callBackSuccess(callBackDict, 1, list)
    except BaseException as e:
        Comm.callBackFail(callBackDict, -1, "系统异常")
        logger = logging.getLogger("django")
        logger.info(str(e))
    return callBackDict




# 管理员创建任务
def adminCreateTask(request):
    callBackDict = {}
    # 验证用户的openID
    userObj = Jurisdiction.jurisAdminGETOpenId(request, callBackDict)
    if userObj == None:
        return callBackDict
    gettitle = Comm.tryTranslate(request, "title")
    if Comm.tryTranslateNull('title', gettitle, callBackDict) == False:
        return callBackDict
    getinfo = Comm.tryTranslate(request, "info")
    if Comm.tryTranslateNull('info', getinfo, callBackDict) == False:
        return callBackDict
    getadImgs = Comm.tryTranslate(request, "adImgs")
    if Comm.tryTranslateNull('adImgs', getadImgs, callBackDict) == False:
        return callBackDict
    getdeadline = Comm.tryTranslate(request, "deadline")
    if Comm.tryTranslateNull('deadline', getdeadline, callBackDict) == False:
        return callBackDict
    getstickerArea = Comm.tryTranslate(request, "stickerArea")
    if Comm.tryTranslateNull('stickerArea', getstickerArea, callBackDict) == False:
        return callBackDict
    if int(getstickerArea)<0 or int(getstickerArea)>4:
        return Comm.callBackFail(callBackDict, -1, "贴纸的区域类型错误")
    getpriceMonth = Comm.tryTranslate(request, "priceMonth")
    if Comm.tryTranslateNull('priceMonth', getpriceMonth, callBackDict) == False:
        return callBackDict
    if int(getpriceMonth) < 0 or int(getpriceMonth) > 10000:
        return Comm.callBackFail(callBackDict, -1, "每月单价异常")
    getlimitNum = Comm.tryTranslate(request, "limitNum")
    if Comm.tryTranslateNull('limitNum', getlimitNum, callBackDict) == False:
        return callBackDict
    # 创建当前的任务
    getcreateTime = int(time.time() * 1000)
    try:
        taskInfoObj = taskInfo.objects.create(status=2,limitNum = getlimitNum ,priceMonth = getpriceMonth,stickerArea = getstickerArea,title =gettitle,info = getinfo,deadline =getdeadline,
                                      adImgs=getadImgs, createTime=getcreateTime)
        taskInfoObj.save()
        Comm.callBackSuccess(callBackDict, 1, taskInfoObj.id)
    except BaseException as e:
        Comm.callBackFail(callBackDict, -1, "系统异常")
        logger = logging.getLogger("django")
        logger.info(str(e))
    return callBackDict



# 删除任务
def adminDelTask(request):
    callBackDict = {}
    # 验证用户的openID
    userObj = Jurisdiction.jurisAdminGETOpenId(request, callBackDict)
    if userObj == None:
        return callBackDict
    gettaskId = Comm.tryTranslate(request, "taskId")
    if Comm.tryTranslateNull('taskId', gettaskId, callBackDict) == False:
        return callBackDict
    try:
        taskInfoObj = taskInfo.objects.get(id=gettaskId)
        taskInfoObj.status = -1
        taskInfoObj.save()
        Comm.callBackSuccess(callBackDict, 1, None)
    except BaseException as e:
        Comm.callBackFail(callBackDict, -1, "删除失败")
        logger = logging.getLogger("django")
        logger.info(str(e))
    return callBackDict



# 判断该任务是否已经审核通过了
def judgeAuditStatusTaskId(taskId):
    try:
        taskInfoObj = taskInfo.objects.get(id=taskId)
        if taskInfoObj.status == 0:
            return "任务还未审核通过"
        if taskInfoObj.status == 3:
            return "任务已经领取完"
        if taskInfoObj.status == 4:
            return "任务已经截止"
        if taskInfoObj.status == -1:
            return "任务已经删除"
        return None
    except BaseException as e:
        logger = logging.getLogger("django")
        logger.info(str(e))
        return "任务不存在"


# 判断该任务是否已领取过了
def judgeAuditStatusgetTaskObj(getTaskId):
    try:
        getTaskObj = getTask.objects.get(id=getTaskId)
        if getTaskObj.status == 0:
            return "领取的任务还未审核通过"
        if getTaskObj.status == 2:
            return "领取的任务审核不通过"
        if getTaskObj.status == -1:
            return "领取的任务已经删除"
        return None
    except BaseException as e:
        logger = logging.getLogger("django")
        logger.info(str(e))
    return "领取的任务ID不存在"


# 判断车辆信息是否审核通过了
def judgeAuditStatusCarId(carId):
    try:
        carIdObj = carInfo.objects.get(id=carId)
        if carIdObj.status == 0:
            return "车辆还未审核通过"
        if carIdObj.status == 2:
            return "车辆审核失败"
        if carIdObj.status == -1:
            return "车辆已经删除"
        return None
    except BaseException as e:
        logger = logging.getLogger("django")
        logger.info(str(e))
        return "车辆不存在"

