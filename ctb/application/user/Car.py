# -*- coding: utf-8 -*-
import logging
from django.http import HttpResponse
import json
import sys
sys.path.append('...')
from ctb.models import user
from ctb.models import carInfo
from .. import Comm
from .. import Jurisdiction
from ..check import CheckInfo


# 获取用户的车辆信息
def wxgetCarList(request):
    callBackDict = {}
    # 验证用户的openID
    userObj = Jurisdiction.jurisdictGETOpenId(request,callBackDict)
    if userObj == None:
        return callBackDict
    try:
        carInfoList = carInfo.objects.filter(userId = userObj.id)
        list = []
        for onecarInfo in carInfoList:
            imgsJosn = json.loads(onecarInfo.adImgs)
            list.append({"id":onecarInfo.id,"carNum":onecarInfo.carNum,"carModel":onecarInfo.carModel,"remark":onecarInfo.remark,"adImgs":imgsJosn})
        Comm.callBackSuccess(callBackDict, 1, list)
    except BaseException as e:
        logger = logging.getLogger("django")
        logger.info(str(e))
        Comm.callBackFail(callBackDict,-1,"系统异常")
    return callBackDict



# 添加车辆信息
def wxAddCar(request):
    callBackDict = {}
    # 验证用户的openID
    userObj = Jurisdiction.jurisdictGETOpenId(request,callBackDict)
    if userObj == None:
        return callBackDict
    getcarNum = Comm.tryTranslate(request, "carNum")
    getadImgs = Comm.tryTranslate(request, "adImgs")
    if Comm.tryTranslateNull("carNum",getcarNum,callBackDict) == False:
        return callBackDict
    if Comm.tryTranslateNull("adImgs", getadImgs, callBackDict) == False:
        return callBackDict
    try:
        json.loads(getadImgs)
    except BaseException as e:
        getadImgs='[]'
    # 其他额外信息
    getcarModel = Comm.tryTranslate(request, "carModel")
    getremark = Comm.tryTranslate(request, "remark")
    try:
        carInfoObj = carInfo.objects.create(userId = userObj.id,carNum=getcarNum, adImgs=getadImgs)
        if getcarModel:
            carInfoObj.carModel = getcarModel
        if getremark:
            carInfoObj.remark = getremark
        carInfoObj.save()
        # 创建一条审核的任务
        CheckInfo.createCheck(carInfoObj.id,1,userObj.id)
        Comm.callBackSuccess(callBackDict, 1, carInfoObj.id)
    except BaseException as e:
        logger = logging.getLogger("django")
        logger.info(str(e))
        Comm.callBackFail(callBackDict,-1,"车牌号已添加")
    return callBackDict


# 编辑车辆
def wxEditCar(request):
    callBackDict = {}
    # 验证用户的openID
    userObj = Jurisdiction.jurisdictGETOpenId(request, callBackDict)
    if userObj == None:
        return callBackDict
    getcarNum = Comm.tryTranslate(request, "carNum")
    getadImgs = Comm.tryTranslate(request, "adImgs")
    getcarId = Comm.tryTranslate(request, "carId")
    if Comm.tryTranslateNull("carId", getcarId, callBackDict) == False:
        return callBackDict
    if Comm.tryTranslateNull("carNum", getcarNum, callBackDict) == False:
        return callBackDict
    if Comm.tryTranslateNull("adImgs", getadImgs, callBackDict) == False:
        return callBackDict
    try:
        json.loads(getadImgs)
    except BaseException as e:
        getadImgs = '[]'
    # 其他额外信息
    getcarModel = Comm.tryTranslate(request, "carModel")
    getremark = Comm.tryTranslate(request, "remark")
    try:
        carInfoObj = carInfo.objects.get(id = getcarId)
        carInfoObj.carNum = getcarNum
        carInfoObj.adImgs = getadImgs
        if getcarModel:
            carInfoObj.carModel = getcarModel
        if getremark:
            carInfoObj.remark = getremark
        carInfoObj.save()
        Comm.callBackSuccess(callBackDict, 1, carInfoObj.id)
    except BaseException as e:
        logger = logging.getLogger("django")
        logger.info(str(e))
        Comm.callBackFail(callBackDict,-1,"车辆信息不存在")
    return callBackDict