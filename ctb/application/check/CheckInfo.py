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
    getpage = Comm.tryTranslate(request, "page")
    getpageSize = Comm.tryTranslate(request, "pageSize")
    if getpage == None:
        getpage = 0
    else:
        getpage = int(getpage)
    if getpageSize == None:
        getpageSize = 20
    else:
        getpageSize = int(getpageSize)
    try:
        getcheckRecordList = checkRecord.objects.filter(isDone=0).order_by("-createTime")[getpage*getpageSize:(getpage*getpageSize+getpageSize)]
        list = []
        for oneRecord in getcheckRecordList:
            list.append({"id":oneRecord.id,"businessId":oneRecord.businessId,"type":oneRecord.type,"isDone":oneRecord.isDone,"createTime":oneRecord.createTime})
        callBackDict['totalNum'] = checkRecord.objects.filter(isDone=0).count()
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
    getpage = Comm.tryTranslate(request, "page")
    getpageSize = Comm.tryTranslate(request, "pageSize")
    if getpage == None:
        getpage = 0
    else:
        getpage = int(getpage)
    if getpageSize == None:
        getpageSize = 20
    else:
        getpageSize = int(getpageSize)
    try:
        getcheckRecordList = checkRecord.objects.all().order_by("-createTime")[getpage*getpageSize:(getpage*getpageSize+getpageSize)]
        list = []
        for oneRecord in getcheckRecordList:
            list.append({"id": oneRecord.id, "businessId": oneRecord.businessId, "type": oneRecord.type,
                         "isDone": oneRecord.isDone, "createTime": oneRecord.createTime})
        callBackDict['totalNum'] = checkRecord.objects.all().count()
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
        logger = logging.getLogger("django")
        logger.info("创建一条审核的记录 getbusinessId：" + str(getbusinessId))
        checkRecordObj = checkRecord.objects.create(userId=userId,createTime=getcreateTime,businessId=getbusinessId,type=gettype)
        checkRecordObj.save()
        return checkRecordObj
    except BaseException as e:
        logger = logging.getLogger("django")
        logger.info("异常了")
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
        logger = logging.getLogger("django")
        logger.info(str(getisDone))
        if getisDone == "1" :
            carInfoObject = carInfo.objects.get(id=checkRecordObj.businessId)
            carInfoObject.status = getisDone
            carInfoObject.save()
        else:
            # 删除该条记录
            carInfo.objects.get(id=checkRecordObj.businessId).delete()
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
    intGetIsDone = int(getisDone)
    if Comm.tryTranslateNull("isDone", getisDone, callBackDict) == False:
        return callBackDict
    try:
        checkRecordObj = checkRecord.objects.get(id=getcheckId)
        checkRecordObj.isDone = getisDone;
        # 处理自己的相关的业务员
        # 1是审核通过，1是审核失败
        logger = logging.getLogger("django")
        logger.info('审核任务的状态：'+str(getisDone))
        if intGetIsDone == 1 or intGetIsDone == 2:
            getTaskObject = getTask.objects.get(id=checkRecordObj.businessId)
            # 判断车辆和任务的审核状态
            taskMsg = judgeAuditStatusTaskId(getTaskObject.taskId)
            if taskMsg != None:
                return Comm.callBackFail(callBackDict, -1, "[审核失败]"+taskMsg)
            catMsg = judgeAuditStatusCarId(getTaskObject.carId)
            if catMsg != None:
                return Comm.callBackFail(callBackDict, -1, "[审核失败]"+catMsg)
            getTaskObject.status = intGetIsDone
            getTaskObject.save()
        # 释放审核的资源
        if intGetIsDone != 1:
            taskInfoObj = taskInfo.objects.get(id=checkRecordObj.businessId)
            taskInfoObj.collectionsNum = taskInfoObj.collectionsNum - 1
            taskInfoObj.save()
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
        if getisDone == "1" or getisDone == "2":
            doTaskObject = doTask.objects.get(id=checkRecordObj.businessId)
            doTaskObject.createTime = int(time.time() * 1000)
            # 审核通过的逻辑，创建一条的流水
            if getisDone == "1":
                # 判断是否审核失败了
                errorMsg = createIncomeStream(checkRecordObj, doTaskObject)
                if len(errorMsg) > 0:
                    doTaskObject.status = 2
                    checkRecordObj.isDone = 2
                    checkRecordObj.save()
                    doTaskObject.save()
                    return Comm.callBackFail(callBackDict, -1, "[审核失败]:"+errorMsg)
            # 更新当前任务的状态
            doTaskObject.status = getisDone
            doTaskObject.save()
        # 保存审核记录的任务
        checkRecordObj.save()
        return Comm.callBackSuccess(callBackDict, 1, checkRecordObj.id)
    except BaseException as e:
        logger = logging.getLogger("django")
        logger.info(str(e))
        return Comm.callBackFail(callBackDict, -1, "系统异常")
    return callBackDict




# 审核做的任务--如果是第二次的话，创建收入的记录
def createIncomeStream(checkRecordObj,doTaskObject):
    # 查询任务的详情
    try:
        getTaskObj = getTask.objects.get(id=doTaskObject.getTaskId)
        taskInfoObj = taskInfo.objects.get(id=getTaskObj.taskId)
    except BaseException as e:
        logger = logging.getLogger("django")
        logger.info("查询任务的详情失败" + str(e))
        return "任务不存在"
    # 首先查询当前用户的流水情况（是否有未完成的流水）
    incomeStreamList = incomeStream.objects.filter(userId=doTaskObject.userId, openId=doTaskObject.openId,
                                                   getTaskId=doTaskObject.getTaskId,status=0).order_by("-createTime")
    if len(incomeStreamList) == 0:
        try:
            # 创建一条新的流水
            incomeStreamObj = incomeStream.objects.create(userId=doTaskObject.userId, openId=doTaskObject.openId,
                                                          getTaskId=doTaskObject.getTaskId,
                                                          checkRecordId=checkRecordObj.id, status=0)
            incomeStreamObj.createTime = int(time.time() * 1000)
            incomeStreamObj.money = taskInfoObj.priceMonth
            incomeStreamObj.save()
        except BaseException as e:
            logger = logging.getLogger("django")
            logger.info("创建一条新的流水失败" + str(e))
            return "首次创建流水失败"
    else:
        # 获取当前的信息的流水
        unfinishedincomeStream = incomeStreamList[0]
        # 如果超过了28天就算有效的数据
        if doTaskObject.createTime - unfinishedincomeStream.createTime >= (3600 * 1000):
        #if doTaskObject.createTime - unfinishedincomeStream.createTime >= (taskInfoObj.billingCycle * 30 * 24*3600*1000):
            try:
                unfinishedincomeStream.endTime = doTaskObject.createTime
                unfinishedincomeStream.status = 1  # 审核通过的流水
                unfinishedincomeStream.save()
                # 同时判断一下是否要继续下一个的周期
                # 判断当前任务的状态
                if taskInfoObj.status == 4 or taskInfoObj.status == -1:
                    logger = logging.getLogger("django")
                    logger.info("当前任务已经删除，或是已截止")
                    return "当前任务已经删除，或是已截止"
                # 判断是否，有下一个周期
                #if (taskInfoObj.deadline-doTaskObject.createTime) < (taskInfoObj.billingCycle * 30 * 24 * 3600 * 1000):
                if (taskInfoObj.deadline - doTaskObject.createTime) < (3600*1000):
                    logger = logging.getLogger("django")
                    logger.info("小于一个周期的时候，就不创建未来的订单")
                    return "小于一个周期的时候，不创建未来的订单"
                # 判断是否，有下一个周期
                # --------暂时不处理---------
                # 同时判断一下是否要继续下一个的周期
                newIncomeStreamObj = incomeStream.objects.create(userId=doTaskObject.userId, openId=doTaskObject.openId,
                                                              getTaskId=doTaskObject.getTaskId,
                                                              checkRecordId=checkRecordObj.id, status=0)
                newIncomeStreamObj.createTime = doTaskObject.createTime
                newIncomeStreamObj.money = taskInfoObj.priceMonth
                newIncomeStreamObj.save()
            except BaseException as e:
                logger = logging.getLogger("django")
                logger.info("更新流水失败" + str(e))
                return "更新流水失败"
        else:
            logger = logging.getLogger("django")
            logger.info("更新流水失败，审核是失败的，没有到一个更新的周期")
            return "新流水失败，审核是失败的，没有到一个更新的周期"
    return ""



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
        if getisDone == "1" or getisDone == "2":
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


# 将任务的对象信息转换为字典
def makeDictaskInfo(taskInfo):
    try:
        imgsJosn = json.loads(taskInfo.adImgs)
    except BaseException as e:
        imgsJosn = []
    return {"id": taskInfo.id, "title": taskInfo.title, "createTime": taskInfo.createTime,
            "activityRange": taskInfo.activityRange, "billingCycle": taskInfo.billingCycle,
            "collectionsNum": taskInfo.collectionsNum, "limitNum": taskInfo.limitNum,
            "priceMonth": taskInfo.priceMonth,
            "stickerArea": taskInfo.stickerArea, "deadline": taskInfo.deadline, "info": taskInfo.info,
            "remark": taskInfo.remark, "status": taskInfo.status, "adImgs": imgsJosn}



# 查看任务详情
def adminBusinessInfo(request):
    callBackDict = {}
    # 验证用户的openID
    userObj = Jurisdiction.jurisAdminGETOpenId(request, callBackDict)
    if userObj == None:
        return callBackDict
    getbusinessId = Comm.tryTranslate(request, "businessId")
    if Comm.tryTranslateNull("businessId", getbusinessId, callBackDict) == False:
        return callBackDict
    gettype = Comm.tryTranslate(request, "type")
    if Comm.tryTranslateNull("type", gettype, callBackDict) == False:
        return callBackDict
    #0是审核创建的任务，1是审核车辆，2是审核领取任务，3是审核提交的任务，4是审核提现的任务
    if gettype == "0":#0是审核创建的任务
        try:
            taskInfoObj = taskInfo.objects.get(id=getbusinessId)
            return Comm.callBackSuccess(callBackDict, 1, makeDictaskInfo(taskInfoObj))
        except BaseException as e:
            logger = logging.getLogger("django")
            logger.info(str(e))
            return Comm.callBackFail(callBackDict, -1, "系统异常")
    elif gettype == "1":#1是审核车辆
        try:
            onecarInfo = carInfo.objects.get(id=getbusinessId)
            imgsJosn = json.loads(onecarInfo.adImgs)
            return Comm.callBackSuccess(callBackDict, 1, {"status": onecarInfo.status, "id": onecarInfo.id, "carNum": onecarInfo.carNum,
                         "carModel": onecarInfo.carModel, "remark": onecarInfo.remark, "adImgs": imgsJosn})
        except BaseException as e:
            logger = logging.getLogger("django")
            logger.info(str(e))
            return Comm.callBackFail(callBackDict, -1, "系统异常")
    elif gettype == "2":#2是审核领取任务
        try:
            # 领取的任务
            getTaskObj = getTask.objects.get(id=getbusinessId)
            dict = {}
            dict['id'] = getTaskObj.id
            dict['userId'] = getTaskObj.userId
            dict['openId'] = getTaskObj.openId
            dict['createTime'] = getTaskObj.createTime
            dict['status'] = getTaskObj.status
            dict['carId'] = getTaskObj.carId
            try:
                oneuser = user.objects.get(id=getTaskObj.userId)
                dict['userInfo'] = {"id": oneuser.id, "isEnabled": oneuser.isEnabled,
                    "createTime": oneuser.createTime, "openId": oneuser.openId, "trueName": oneuser.trueName,
                    "name": oneuser.name, "address": oneuser.address, "phone": oneuser.phone,
                    "role": oneuser.role}
            except BaseException as e:
                logger = logging.getLogger("django")
                logger.info(str(e))
            try:
                onecarInfo = carInfo.objects.get(id=getTaskObj.carId)
                imgsJosn = json.loads(onecarInfo.adImgs)
                dict['carInfo'] = {"status": onecarInfo.status, "id": onecarInfo.id, "carNum": onecarInfo.carNum,
                             "carModel": onecarInfo.carModel, "remark": onecarInfo.remark, "adImgs": imgsJosn}
            except BaseException as e:
                logger = logging.getLogger("django")
                logger.info(str(e))
            # 获取任务详情的信息
            dict['taskInfo'] = makeDictaskInfo(taskInfo.objects.get(id=getTaskObj.taskId))
            return Comm.callBackSuccess(callBackDict, 1,dict)
        except BaseException as e:
            logger = logging.getLogger("django")
            logger.info(str(e))
            return Comm.callBackFail(callBackDict, -1, "系统异常")
    elif gettype == "3":#3是审核提交的任务
        try:
            doTaskObj = doTask.objects.get(id=getbusinessId)
            dict = {}
            dict['id'] = doTaskObj.id
            dict['userId'] = doTaskObj.userId
            dict['openId'] = doTaskObj.openId
            dict['createTime'] = doTaskObj.createTime
            dict['status'] = doTaskObj.status
            dict['getTaskId'] = doTaskObj.getTaskId
            try:
                getTaskObj = getTask.objects.get(id=doTaskObj.getTaskId)
                oneuser = user.objects.get(id=getTaskObj.userId)
                dict['userInfo'] = {"id": oneuser.id, "isEnabled": oneuser.isEnabled,
                                    "createTime": oneuser.createTime, "openId": oneuser.openId,
                                    "trueName": oneuser.trueName,
                                    "name": oneuser.name, "address": oneuser.address, "phone": oneuser.phone,
                                    "role": oneuser.role}
                onecarInfo = carInfo.objects.get(id=getTaskObj.carId)
                imgsJosn = json.loads(onecarInfo.adImgs)
                dict['carInfo'] = {"status": onecarInfo.status, "id": onecarInfo.id, "carNum": onecarInfo.carNum,
                                   "carModel": onecarInfo.carModel, "remark": onecarInfo.remark, "adImgs": imgsJosn}
                dict['taskInfo'] = makeDictaskInfo(taskInfo.objects.get(id=getTaskObj.taskId))
            except BaseException as e:
                logger = logging.getLogger("django")
                logger.info(str(e))
            try:
                imgsJosn = json.loads(doTaskObj.adImgs)
            except BaseException as e:
                imgsJosn = []
            dict['adImgs'] = imgsJosn
            return Comm.callBackSuccess(callBackDict, 1, dict)
        except BaseException as e:
            logger = logging.getLogger("django")
            logger.info(str(e))
            return Comm.callBackFail(callBackDict, -1, "系统异常")
    elif gettype == "4":#4是审核提现的任务
        try:
            outStreamObj = outStream.objects.get(id=getbusinessId)
            dict = {}
            dict['id'] = outStreamObj.id
            dict['userId'] = outStreamObj.userId
            dict['openId'] = outStreamObj.openId
            dict['createTime'] = outStreamObj.createTime
            dict['money'] = outStreamObj.status
            return Comm.callBackSuccess(callBackDict, 1, dict)
        except BaseException as e:
            logger = logging.getLogger("django")
            logger.info(str(e))
            return Comm.callBackFail(callBackDict, -1, "系统异常")
    return callBackDict



# 审核发放物料
def sendMateriel(request):
    callBackDict = {}
    # 验证用户的openID
    userObj = Jurisdiction.jurisAdminGETOpenId(request, callBackDict)
    if userObj == None:
        return callBackDict
    getTaskId = Comm.tryTranslate(request, "getTaskId")
    if Comm.tryTranslateNull("领取的任务ID为空", getTaskId, callBackDict) == False:
        return callBackDict
    try:
        getTaskObj = getTask.objects.get(id=getTaskId)
        getTaskObj.isSendMateriel = 1
        getTaskObj.save()
        return Comm.callBackSuccess(callBackDict, 1, getTaskId)
    except BaseException as e:
        logger = logging.getLogger("django")
        logger.info(str(e))
        return Comm.callBackFail(callBackDict, -1, "系统异常")
    return callBackDict