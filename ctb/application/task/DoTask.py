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
from ctb.models import activityRange
from ..check import CheckInfo

from .. import Comm
from .. import Jurisdiction
import TaskInfo



# 做任务
def wxdoTask(request):
    callBackDict = {}
    # 验证用户的openID
    userObj = Jurisdiction.jurisdictGETOpenId(request, callBackDict)
    if userObj == None:
        return callBackDict
    getgetTaskId = Comm.tryTranslate(request, "getTaskId")
    getadImgs = Comm.tryTranslate(request, "adImgs")
    getlatitude = Comm.tryTranslate(request, "latitude")
    getlongitude = Comm.tryTranslate(request, "longitude")
    if Comm.tryTranslateNull("getTaskId", getgetTaskId, callBackDict) == False:
        return callBackDict
    if Comm.tryTranslateNull("adImgs", getadImgs, callBackDict) == False:
        return callBackDict
    try:
        try:
            getTaskObj = getTask.objects.get(id=getgetTaskId)
            # 判断车辆和任务的审核状态
            taskMsg = TaskInfo.judgeAuditStatusTaskId(getTaskObj.taskId)
            if taskMsg != None:
                return Comm.callBackFail(callBackDict, -1, taskMsg)
            catMsg = TaskInfo.judgeAuditStatusCarId(getTaskObj.carId)
            if catMsg != None:
                return Comm.callBackFail(callBackDict, -1, catMsg)
            getgetTaskMsg = TaskInfo.judgeAuditStatusgetTaskObj(getgetTaskId)
            if getgetTaskMsg != None:
                return Comm.callBackFail(callBackDict, -1, getgetTaskMsg)
        except BaseException as e:
            return Comm.callBackFail(callBackDict, -1, "领取任务的ID不存在")
        getcreateTime  = int(time.time() * 1000)
        doTaskObj = doTask.objects.create(userId = userObj.id,openId = userObj.openId,getTaskId=getgetTaskId,adImgs=getadImgs,createTime=getcreateTime)
        if getlatitude and getlongitude:
            doTaskObj.latitude = getlatitude
            doTaskObj.longitude = getlongitude
            # 同时添加为经常活动的范围
            try:
                activityRangeObj = activityRange.objects.create(latitude=getlatitude, longitude=getlongitude,
                                                                userId=userObj.id, openId=userObj.openId,
                                                                carInfoId=getTaskObj.carId, createTime=getcreateTime)
                activityRangeObj.save()
            except BaseException as e:
                return Comm.callBackFail(callBackDict, -1, "添加为经常活动的范围异常")
        # 保存领取的任务
        doTaskObj.save()
        # 创建一条审核的任务
        logger = logging.getLogger("django")
        logger.info("创建一条审核的记录："+str(doTaskObj.id))
        CheckInfo.createCheck(doTaskObj.id, 3, userObj.id)
        Comm.callBackSuccess(callBackDict, 1, doTaskObj.id)
    except BaseException as e:
        Comm.callBackFail(callBackDict,-1,"系统异常")
        logger = logging.getLogger("django")
        logger.info(str(e))
    return callBackDict


