# -*- coding: utf-8 -*-
import logging
from django.http import HttpResponse
import json
import sys
sys.path.append('...')
from ctb.models import user
from ctb.models import carInfo
from ctb.models import taskInfo
from ctb.models import getTask

from .. import Comm
from .. import Jurisdiction

# 获取当前用户参与的任务
def wxGetJoinTask(request):
    callBackDict = {}
    # 验证用户的openID
    userObj = Jurisdiction.jurisdictGETOpenId(request, callBackDict)
    if userObj == None:
        return callBackDict
    getTaskList = getTask.objects.filter(userId=userObj.userId,openId=userObj.openId)
    list = []
    for getTask in getTaskList:
        try:
            carInfoObj = carInfo.objects.get(id = getTask.carId)
        except BaseException as e:
            carInfoObj = None
        try:
            taskInfoObj = taskInfo.objects.get(id = getTask.taskId)
        except BaseException as e:
            taskInfoObj = None
        dict = {"id":getTask.id,"carId":getTask.carId,"taskId":getTask.taskId,"createTime":getTask.createTime,"status":getTask.status,"startdoTaskTime":getTask.startdoTaskTime}
        if carInfoObj:
            dict['carInfo'] = {"id":carInfoObj.id,"carNum":carInfoObj.carNum,"carModel":carInfoObj.carModel,"remark":carInfoObj.remark,"adImgs":json.loads(carInfoObj.adImgs)}
        if taskInfoObj:
            dict['taskInfo'] = makeDictaskInfo(taskInfoObj)
        list.append(dict)
    # 组装完数据的回调
    Comm.callBackSuccess(callBackDict, 1, list)
    return callBackDict



# 将任务的对象信息转换为字典
def makeDictaskInfo(carInfo):
    imgsJosn = json.loads(carInfo.adImgs)
    return  {"id": carInfo.id, "title": taskInfo.title, "createTime": taskInfo.createTime,
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
        for taskInfo in taskInfoList:
            list.append(makeDictaskInfo(taskInfo))
        Comm.callBackSuccess(callBackDict, 1, list)
    except BaseException as e:
        Comm.callBackFail(callBackDict,-1,"系统异常")
    return callBackDict

