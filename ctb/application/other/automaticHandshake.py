# -*- coding: utf-8 -*-
import logging
from django.http import HttpResponse
import json
import time
import sys
import uuid
import urllib2
import httplib
sys.path.append('...')
from ctb.models import otherProjectInfo
from ctb.models import otherAutoHandshakeUser
from ctb.models import otherRegionCoefficient
from .. import Comm


def appAutoHandshake(request):
    callBackDict = {}
    #首先的判断当前项目的情况
    getbundleIdentifier = Comm.tryTranslate(request, "bundleIdentifier")
    getclientUUId = Comm.tryTranslate(request, "clientUUI")
    if Comm.tryTranslateNull("项目的签名为空", getbundleIdentifier, callBackDict) == False:
        return callBackDict
    if Comm.tryTranslateNull("客户端的标识为空", getclientUUId, callBackDict) == False:
        return callBackDict
    #查询具体的项目信息
    try:
        projectInfoObj = otherProjectInfo.objects.filter(bundleIdentifier=getbundleIdentifier)[0]
        logger = logging.getLogger("django")
        # 分析IP
        dictIP = analysisIP(request)
        logger.info(str(dictIP))
        getauroraTag = "default"
        if dictIP["province"]:
            getauroraTag = dictIP["province"]
        # 判断提交审核的时间--判断发布通过的时间(审核中的)
        getisBlacklistUser = 0
        if projectInfoObj.submitAuditTime > 0 and projectInfoObj.manualreleaseTime == 0:
            getisBlacklistUser = 1
        # 创建一条用户的记录数据
        logger.info("1")
        createAndSelecteUser(getbundleIdentifier, getclientUUId, getauroraTag,getisBlacklistUser,dictIP)
        logger.info("2")
        # 关闭的状态
        # 审核中的状态,# 注意此时标记为黑名单
        if getisBlacklistUser == 1:
            try:
                regionCoefficientObj = otherRegionCoefficient.objects.create(country=dictIP["country"],province=dictIP["province"],city=dictIP["city"],coefficient=100)
                regionCoefficientObj.save()
            except BaseException as e:
                logger = logging.getLogger("django")
                logger.info(str(e))
            return Comm.callBackSuccess(callBackDict, 1, {"auroraTag": "default",
                                                          "token": str(uuid.uuid1()) + str(uuid.uuid1())})
        # 如果是关闭的状态
        if projectInfoObj.isOpen == 0:
            return Comm.callBackSuccess(callBackDict, 1, {"auroraTag":"default","token":str(uuid.uuid1())+str(uuid.uuid1())})
        # 跳过审核状态的情况下--正常的逻辑情况下
        # 判断IP区域的状态
        lastCoefficient = 0
        lastProvince = 'default'
        regionCoefficientList = otherRegionCoefficient.objects.all()
        # 按照省份进行判断
        for regionCoefficientoneObj in regionCoefficientList:
            if dictIP["province"] and regionCoefficientoneObj.city == dictIP["province"]:
                lastCoefficient = regionCoefficientoneObj.coefficient
                lastProvince = dictIP["province"]
                break
        if lastCoefficient == 0:
            return Comm.callBackSuccess(callBackDict, 1, {"auroraTag": "default",
                                                          "token": str(uuid.uuid1()) + str(uuid.uuid1())})
        else:
            # 显示
            return Comm.callBackSuccess(callBackDict, 1, {"auroraTag": lastProvince,
                                                          "token": str(uuid.uuid1()) + str(uuid.uuid1())})
    except BaseException as e:
        logger = logging.getLogger("django")
        logger.info(str(e))
        Comm.callBackSuccess(callBackDict, 1, {"auroraTag": "default","token": str(uuid.uuid1()) + str(uuid.uuid1())})
    return callBackDict


def createAndSelecteUser(getbundleIdentifier,getclientUUId,getauroraTag,getisBlacklistUser,dictIP):
    getcreateTime = int(time.time() * 1000)
    autoHandshakeUserObj = None
    try:
        autoHandshakeUserObj = otherAutoHandshakeUser.objects.create(isBlacklistUser=getisBlacklistUser,bundleIdentifier=getbundleIdentifier, clientUUId=getclientUUId,auroraTag=getauroraTag,loginTime=getcreateTime)
        if dictIP['ip']:
            autoHandshakeUserObj.ip = dictIP['ip']
        if dictIP['country']:
            autoHandshakeUserObj.country = dictIP['country']
        if dictIP['province']:
            autoHandshakeUserObj.province = dictIP['province']
        if dictIP['city']:
            autoHandshakeUserObj.city = dictIP['city']
        autoHandshakeUserObj.save()
    except BaseException as e:
        logger = logging.getLogger("django")
        logger.info(str(e))
    return autoHandshakeUserObj



# 解析IP的信息
def analysisIP(request):
    # 判断请求的域名
    ip = get_client_ip(request)
    logger = logging.getLogger("django")
    logger.info(ip)
    country = None;
    region = None;
    city = None;
    if len(ip) > 0:
        url = "http://ip.taobao.com/service/getIpInfo.php?ip=" + ip
        # 同步发送网络请求
        res = urllib2.urlopen(url,timeout=2)
        page_source = res.read().decode('utf-8')
        try:
            decode_json = json.loads(page_source)
            country = decode_json['data']['country']
            region = decode_json['data']['region']
            city = decode_json['data']['city']
        except:
            country = None
            region = None
            city = None
            # 解析出来的域名
    return {"country":country,"province":region,"city":city,"ip":ip}


# 获取客户端的IP
def get_client_ip(request):
    try:
        real_ip = request.META['HTTP_X_FORWARDED_FOR']
        regip = real_ip.split(",")[0]
    except:
        try:
            regip = request.META['REMOTE_ADDR']
        except:
            regip = None
    return regip





def createProjectInfo(request):
    callBackDict = {}
    getbundleIdentifier = Comm.tryTranslate(request, "bundleIdentifier")
    getskipUrl = Comm.tryTranslate(request, "skipUrl")
    if Comm.tryTranslateNull("项目的签名为空", getbundleIdentifier, callBackDict) == False:
        return callBackDict
    if Comm.tryTranslateNull("跳转的URL为空", getskipUrl, callBackDict) == False:
        return callBackDict
    try:
        getcreateTime = int(time.time() * 1000)
        projectInfoObj = otherProjectInfo.objects.create(bundleIdentifier=getbundleIdentifier, skipUrl=getskipUrl,createTime=getcreateTime)
        projectInfoObj.save()
        Comm.callBackSuccess(callBackDict, 1, "创建成功")
    except BaseException as e:
        logger = logging.getLogger("django")
        logger.info(str(e))
        Comm.callBackFail(callBackDict, 0, "项目签名已存在")
    return callBackDict





def openAndCloseProject(request):
    callBackDict = {}
    getbundleIdentifier = Comm.tryTranslate(request, "bundleIdentifier")
    if Comm.tryTranslateNull("项目的签名为空", getbundleIdentifier, callBackDict) == False:
        return callBackDict
    getisOpen = Comm.tryTranslate(request, "isOpen")
    if int(getisOpen) < 0 or int(getisOpen) > 1 :
        Comm.callBackFail(callBackDict, 0, "项目的开关只能是0或1")
        return callBackDict
    try:
        projectInfoObjLsit = otherProjectInfo.objects.filter(bundleIdentifier=getbundleIdentifier)
        if len(projectInfoObjLsit) == 0:
            Comm.callBackFail(callBackDict, 0, "项目不存在")
        if int(getisOpen) == 1:
            if projectInfoObjLsit[0].manualreleaseTime == 0 or projectInfoObjLsit[0].submitAuditTime == 0:
                return Comm.callBackFail(callBackDict, 0, "该项目还尚未审核通过")
        try:
            projectInfoObjLsit[0].isOpen = int(getisOpen)
            projectInfoObjLsit[0].save()
            logger = logging.getLogger("django")
            Comm.callBackSuccess(callBackDict, 1, "更改状态已成功")
        except BaseException as e:
            Comm.callBackSuccess(callBackDict, 0, "更改状态失败")
    except BaseException as e:
        logger = logging.getLogger("django")
        logger.info(str(e))
        Comm.callBackFail(callBackDict, 0, "系统异常")
    return callBackDict



def submitAuditProject(request):
    callBackDict = {}
    getbundleIdentifier = Comm.tryTranslate(request, "bundleIdentifier")
    if Comm.tryTranslateNull("项目的签名为空", getbundleIdentifier, callBackDict) == False:
        return callBackDict
    projectInfoObjLsit = otherProjectInfo.objects.filter(bundleIdentifier=getbundleIdentifier)
    if len(projectInfoObjLsit) == 0:
        Comm.callBackFail(callBackDict, 0, "项目不存在")
    try:
        projectInfoObjLsit[0].submitAuditTime = int(time.time() * 1000)
        projectInfoObjLsit[0].save()
        Comm.callBackSuccess(callBackDict, 1, "已提交审核")
    except BaseException as e:
        logger = logging.getLogger("django")
        logger.info(str(e))
        Comm.callBackFail(callBackDict, 0, "系统异常")
    return callBackDict

def manualreleaseProject(request):
    callBackDict = {}
    getbundleIdentifier = Comm.tryTranslate(request, "bundleIdentifier")
    if Comm.tryTranslateNull("项目的签名为空", getbundleIdentifier, callBackDict) == False:
        return callBackDict
    projectInfoObjLsit = otherProjectInfo.objects.filter(bundleIdentifier=getbundleIdentifier)
    if len(projectInfoObjLsit) == 0:
        Comm.callBackFail(callBackDict, 0, "项目不存在")
    try:
        projectInfoObjLsit[0].manualreleaseTime = int(time.time() * 1000)
        projectInfoObjLsit[0].save()
        Comm.callBackSuccess(callBackDict, 1, "appstore已确认审核通过了")
    except BaseException as e:
        logger = logging.getLogger("django")
        logger.info(str(e))
        Comm.callBackFail(callBackDict, 0, "系统异常")
    return callBackDict


def exchangeRegionCoefficient(request):
    callBackDict = {}
    getbundleIdentifier = Comm.tryTranslate(request, "bundleIdentifier")
    if Comm.tryTranslateNull("项目的签名为空", getbundleIdentifier, callBackDict) == False:
        return callBackDict
    return Comm.callBackFail(callBackDict, 0, "尚未开发")


def delAll(request):
    callBackDict = {}
    try:
        otherProjectInfo.objects.all().delete()
        otherAutoHandshakeUser.objects.all().delete()
        otherRegionCoefficient.objects.all().delete()
        Comm.callBackSuccess(callBackDict, 1, "projectInfo/autoHandshakeUser/regionCoefficient 全部已经清空")
    except BaseException as e:
        logger = logging.getLogger("django")
        logger.info(str(e))
        Comm.callBackFail(callBackDict, 0, "系统异常")
    return callBackDict



def allProjectInfoList(request):
    callBackDict = {}
    pageData = []
    projectInfoList = otherProjectInfo.objects.all()
    for oneprojectInfo in projectInfoList:
        pageData.append({"bundleIdentifier":oneprojectInfo.bundleIdentifier,"skipUrl":oneprojectInfo.skipUrl,"isOpen":oneprojectInfo.isOpen,"submitAuditTime":oneprojectInfo.submitAuditTime,"manualreleaseTime":oneprojectInfo.manualreleaseTime})
    return Comm.callBackSuccess(callBackDict, 1, pageData)


def allOtherRegionCoefficient(request):
    callBackDict = {}
    pageData = []
    otherRegionCoefficientList = otherRegionCoefficient.objects.all()
    for otherRegionInfo in otherRegionCoefficientList:
        pageData.append({"country":otherRegionInfo.country,"province":otherRegionInfo.province,"city":otherRegionInfo.city,"coefficient":otherRegionInfo.coefficient})
    return Comm.callBackSuccess(callBackDict, 1, pageData)



def allAutoHandshakeUser(request):
    callBackDict = {}
    pageData = []
    autoHandshakeUserList = otherAutoHandshakeUser.objects.all()
    for oneautoHandshake in autoHandshakeUserList:
        pageData.append({"bundleIdentifier":oneautoHandshake.bundleIdentifier,"clientUUId":oneautoHandshake.clientUUId,"ip":oneautoHandshake.ip,"country":oneautoHandshake.country,"province":oneautoHandshake.province,"city":oneautoHandshake.city,"auroraTag":oneautoHandshake.auroraTag,"isBlacklistUser":oneautoHandshake.isBlacklistUser})
    return Comm.callBackSuccess(callBackDict, 1, pageData)



