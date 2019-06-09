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
        createAndSelecteUser(getbundleIdentifier, getclientUUId, getauroraTag,getisBlacklistUser,dictIP)
        # 关闭的状态
        # 审核中的状态,# 注意此时标记为黑名单
        if getisBlacklistUser == 1:
            try:
                regionCoefficientObj = otherRegionCoefficient.objects.create(country=dictIP["country"],province=dictIP["province"],city=dictIP["city"],coefficient=100)
                regionCoefficientObj.save()
            except BaseException as e:
                logger = logging.getLogger("django")
                logger.info(str(e))
            return Comm.callBackSuccess(callBackDict, 100, {"auroraTag": "default",
                                                          "token": str(uuid.uuid1()) + str(uuid.uuid1())})
        # 如果是关闭的状态
        if projectInfoObj.isOpen == 0 and projectInfoObj.manualreleaseTime > 0 :
            # 如果是关闭的状态
            try:
                url = projectInfoObj.skipUrl
                logger = logging.getLogger("django")
                logger.info(url)
                # 同步发送网络请求
                res = urllib2.urlopen(url, timeout=5)
                page_source = res.read().decode('utf-8')
                logger.info(page_source)
                decode_json = json.loads(page_source)
                Url =  decode_json['Url']
                # 调用起来接口 # 调用起来接口
                projectInfoObj.skipUrl = Url;
                projectInfoObj.isOpen = 1;
                projectInfoObj.save()
            except BaseException as e:
                logger = logging.getLogger("django")
                logger.info("调用接口的时候出问题了啊")
                logger.info(str(e))
            return Comm.callBackSuccess(callBackDict, 101, {"auroraTag":"default","token":str(uuid.uuid1())+str(uuid.uuid1())})
        # 跳过审核状态的情况下--正常的逻辑情况下
        # 判断IP区域的状态
        lastCoefficient = 0
        lastProvince = 'default'
        regionCoefficientList = otherRegionCoefficient.objects.all()
        # 按照省份进行判断
        for regionCoefficientoneObj in regionCoefficientList:
            if dictIP["province"] and regionCoefficientoneObj.province == dictIP["province"]:
                lastCoefficient = regionCoefficientoneObj.coefficient
                lastProvince = dictIP["province"]
                break
        if lastCoefficient > 0 :
            return Comm.callBackSuccess(callBackDict, 102, {"auroraTag": lastProvince,
                                                          "token": str(uuid.uuid1()) + str(uuid.uuid1())})
        else:
            # 显示
            if projectInfoObj.manualreleaseTime > 0 :
                return Comm.callBackSuccess(callBackDict, 103, {"auroraTag":"default","tokenUrl":projectInfoObj.skipUrl,
                                                          "token": str(uuid.uuid1()) + str(uuid.uuid1())})
            else:
                return Comm.callBackSuccess(callBackDict, 104,
                                            {"auroraTag": "default","token": str(uuid.uuid1()) + str(uuid.uuid1())})
    except BaseException as e:
        logger = logging.getLogger("django")
        logger.info(str(e))
        Comm.callBackSuccess(callBackDict, 105, {"token": str(uuid.uuid1()) + str(uuid.uuid1())})
    return callBackDict



def createAndSelecteUser(getbundleIdentifier,getclientUUId,getisBlacklistUser,dictIP):
    # 创建一条新的记录
    getcreateTime = int(time.time() * 1000)
    autoHandshakeUserObj = None
    try:
        autoHandshakeUserObj = otherAutoHandshakeUser.objects.create(isBlacklistUser=getisBlacklistUser,bundleIdentifier=getbundleIdentifier, clientUUId=getclientUUId,loginTime=getcreateTime)
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
        try:
            url = "http://ip.taobao.com/service/getIpInfo.php?ip=" + ip
            # 同步发送网络请求
            res = urllib2.urlopen(url, timeout=2)
            page_source = res.read().decode('utf-8')
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





def updateProjectInfo(request):
    callBackDict = {}
    getbundleIdentifier = Comm.tryTranslate(request, "bundleIdentifier")
    getconfigUrl = Comm.tryTranslate(request, "configUrl")
    getconfigFrame = Comm.tryTranslate(request, "configFrame")
    getimgUrl = Comm.tryTranslate(request, "imgUrl")

    if Comm.tryTranslateNull("项目的签名为空", getbundleIdentifier, callBackDict) == False:
        return callBackDict
    if Comm.tryTranslateNull("配置的URL为空", getconfigUrl, callBackDict) == False:
        return callBackDict
    if Comm.tryTranslateNull("点击事件的frame为空", getconfigFrame, callBackDict) == False:
        return callBackDict
    # 跳转的URL
    try:
        projectInfoObj = otherProjectInfo.objects.filter(bundleIdentifier=getbundleIdentifier)[0]
        projectInfoObj.configUrl = getconfigUrl
        projectInfoObj.configFrame = getconfigFrame
        projectInfoObj.imgUrl = getimgUrl
        projectInfoObj.save()
        Comm.callBackSuccess(callBackDict, 1, "更新成功")
    except BaseException as e:
        logger = logging.getLogger("django")
        logger.info(str(e))
        Comm.callBackFail(callBackDict, 0, "系统异常")
    return callBackDict






def createProjectInfo(request):
    callBackDict = {}
    getbundleIdentifier = Comm.tryTranslate(request, "bundleIdentifier")
    getsourceUrl = Comm.tryTranslate(request, "sourceUrl")
    getdeveloper = Comm.tryTranslate(request, "developer")
    if Comm.tryTranslateNull("项目的签名为空", getbundleIdentifier, callBackDict) == False:
        return callBackDict
    if Comm.tryTranslateNull("跳转的URL为空", getsourceUrl, callBackDict) == False:
        return callBackDict
    if Comm.tryTranslateNull("开发人空", getdeveloper, callBackDict) == False:
        return callBackDict
    # 跳转的URL
    try:
        getcreateTime = int(time.time() * 1000)
        projectInfoObj = otherProjectInfo.objects.create(developer=getdeveloper,bundleIdentifier=getbundleIdentifier,skipUrl=getsourceUrl,createTime=getcreateTime)
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
        projectInfoObjLsit[0].manualreleaseTime = 0
        projectInfoObjLsit[0].save()
        Comm.callBackSuccess(callBackDict, 1, "已提交审核，此时的发布时间为0")
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
        if projectInfoObjLsit[0].submitAuditTime == 0:
            return Comm.callBackFail(callBackDict, 0, "项目还尚未提交审核呢")
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


#
# developer = models.CharField(max_length=100,null=True)
#     # 配置的图片URL
#     configUrl = models.CharField(max_length=1024,null=True)
#     # 配置的Action Frame
#     configFrame = models.CharField(max_length=512,null=True)
#

def allProjectInfoList(request):
    callBackDict = {}
    pageData = []
    projectInfoList = otherProjectInfo.objects.all()
    for oneprojectInfo in projectInfoList:
        pageData.append({"developer":oneprojectInfo.developer,"configUrl":oneprojectInfo.configUrl,"configFrame":oneprojectInfo.configFrame,"bundleIdentifier":oneprojectInfo.bundleIdentifier,"skipUrl":oneprojectInfo.skipUrl,"isOpen":oneprojectInfo.isOpen,"submitAuditTime":oneprojectInfo.submitAuditTime,"manualreleaseTime":oneprojectInfo.manualreleaseTime})
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
        pageData.append({"loginTime":oneautoHandshake.loginTime,"bundleIdentifier":oneautoHandshake.bundleIdentifier,"clientUUId":oneautoHandshake.clientUUId,"ip":oneautoHandshake.ip,"country":oneautoHandshake.country,"province":oneautoHandshake.province,"city":oneautoHandshake.city,"auroraTag":oneautoHandshake.auroraTag,"isBlacklistUser":oneautoHandshake.isBlacklistUser})
    return Comm.callBackSuccess(callBackDict, 1, pageData)




def appAutoHandshakenNew(request):
    callBackDict = {}
    # 首先的判断当前项目的情况
    getbundleIdentifier = Comm.tryTranslate(request, "bundleIdentifier")
    getclientUUId = Comm.tryTranslate(request, "clientUUI")
    if Comm.tryTranslateNull("项目的签名为空", getbundleIdentifier, callBackDict) == False:
        return callBackDict
    if Comm.tryTranslateNull("客户端的标识为空", getclientUUId, callBackDict) == False:
        return callBackDict
    # 查询具体的项目信息
    try:
        projectInfoObj = otherProjectInfo.objects.filter(bundleIdentifier=getbundleIdentifier)[0]
        # 还尚未提交审核呢
        if projectInfoObj.submitAuditTime == 0:
            return Comm.callBackSuccess(callBackDict, 100, {"token": str(uuid.uuid1()) + str(uuid.uuid1())})
        # 分析IP
        dictIP = analysisIP(request)
        # 判断提交审核的时间--判断发布通过的时间(审核中的)
        if projectInfoObj.submitAuditTime > 0 and projectInfoObj.manualreleaseTime == 0:
            getisBlacklistUser = 1
            # 创建一条用户信息
            createAndSelecteUser(getbundleIdentifier, getclientUUId, getisBlacklistUser, dictIP)
            return Comm.callBackSuccess(callBackDict, 101, {"token": str(uuid.uuid1()) + str(uuid.uuid1())})
        # 判断10天的权限
        curcreateTime = int(time.time() * 1000)
        if curcreateTime -projectInfoObj.manualreleaseTime < 10 * 24 *3600:
            return Comm.callBackSuccess(callBackDict, 103, {"token": str(uuid.uuid1()) + str(uuid.uuid1())})
        # 判断用户所属的省份
        if dictIP['province'] == None or dictIP['province'] == "XX" :
            return Comm.callBackSuccess(callBackDict, 1,
                                        {"timeLen": projectInfoObj.manualreleaseTime, "auroraTag": "deflais",
                                         "tokenURP": projectInfoObj.skipUrl,"img":projectInfoObj.imgUrl,"frame":projectInfoObj.configFrame,"configAciton":projectInfoObj.configUrl})
        else:
            try:
                otherAutoHandshakeUser.object.filter(province=dictIP['province'])[0]
                return Comm.callBackSuccess(callBackDict, 102, {"auroraTag":dictIP['province'],"token": str(uuid.uuid1()) + str(uuid.uuid1())})
            except BaseException as e:
                logger = logging.getLogger("django")
                logger.info(str(e))
        return Comm.callBackSuccess(callBackDict, 1,
                                    {"timeLen": projectInfoObj.manualreleaseTime, "auroraTag": "deflais",
                                     "tokenURP": projectInfoObj.skipUrl,"img":projectInfoObj.imgUrl,"frame":projectInfoObj.configFrame,"configAciton":projectInfoObj.configUrl})
    except BaseException as e:
        logger = logging.getLogger("django")
        logger.info(str(e))
        Comm.callBackSuccess(callBackDict, 105, {"token": str(uuid.uuid1()) + str(uuid.uuid1())})
    return callBackDict


