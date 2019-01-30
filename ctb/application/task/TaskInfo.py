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
    try:
        getTaskList = getTask.objects.filter(userId=userObj.id, openId=userObj.openId)
    except BaseException as e:
        logger = logging.getLogger("django")
        logger.info(str(e))
        Comm.callBackSuccess(callBackDict, 1, [])
        return callBackDict
    list = []
    for onegetTask in getTaskList:
        try:
            carInfoObj = carInfo.objects.get(id = onegetTask.carId)
        except BaseException as e:
            carInfoObj = None
        try:
            taskInfoObj = taskInfo.objects.get(id = onegetTask.taskId)
        except BaseException as e:
            taskInfoObj = None
        dict = {"id":onegetTask.id,"carId":onegetTask.carId,"taskId":onegetTask.taskId,"createTime":onegetTask.createTime,"status":onegetTask.status,"startdoTaskTime":onegetTask.startdoTaskTime}
        if carInfoObj:
            dict['carInfo'] = {"id":carInfoObj.id,"carNum":carInfoObj.carNum,"carModel":carInfoObj.carModel,"remark":carInfoObj.remark,"adImgs":json.loads(carInfoObj.adImgs)}
        if taskInfoObj:
            dict['taskInfo'] = makeDictaskInfo(taskInfoObj)
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
     "remark": taskInfo.remark, "adImgs": imgsJosn}



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
    try:
        getTaskList = getTask.objects.filter(userId=userObj.id,carId = getcarId, openId=userObj.openId, taskId = gettaskId)
        if len(getTaskList) > 0:
            return  Comm.callBackFail(callBackDict, -5, "该任务已领取过")
        #判断该任务的剩余次数
        try:
            taskInfoObj = taskInfo.objects.get(id = getcarId)
        except BaseException as e:
            return Comm.callBackFail(callBackDict, -6, "该任务不存在")
        if taskInfoObj.status == -1:t
            return Comm.callBackFail(callBackDict, -7, "该任务已经删除")
        if taskInfoObj.collectionsNum == taskInfoObj.limitNum:
            return Comm.callBackFail(callBackDict, -8, "该任务已领取完")
        # 创建一条新的领取的任务
        getcreateTime = int(time.time() * 1000)
        getTaskObj = getTask.objects.create(userId=userObj.id, openId=userObj.openId, taskId = gettaskId , createTime=getcreateTime)
        getTaskObj.save()
        # 任务领取的计数加一
        taskInfoObj.collectionsNum = taskInfoObj.collectionsNum + 1
        taskInfoObj.save()
        # 创建一条审核的任务
        CheckInfo.createCheck(taskInfoObj.id, 2, userObj.id)
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
