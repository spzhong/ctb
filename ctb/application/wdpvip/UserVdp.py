# -*- coding: utf-8 -*-
import logging
from django.http import HttpResponse
import json
import sys
import time
sys.path.append('...')
from ctb.models import wdpvipUser
from .. import Comm
from .. import Jurisdiction
import uuid

# 微信登录注册认证
def wxegisterSign(request):
    # 取得获取的值
    callBackDict = {}
    getopenId = Comm.tryTranslate(request, "openId")
    if Comm.tryTranslateNull('openId', getopenId, callBackDict) == False:
        return callBackDict
    try:
        # 查询判断用户是否已经存在的
        userList = wdpvipUser.objects.filter(openId=getopenId)
        createTime = int(time.time() * 1000)
        if len(userList) > 0:
            dict = {}
            dict['userId'] =  userList[0].id
            dict['name'] = userList[0].name
            dict['address'] = userList[0].address
            dict['trueName'] = userList[0].trueName
            dict['phone'] = userList[0].phone
            dict['isEnabled'] = userList[0].isEnabled
            dict['loginTime'] = createTime
            # 保存最后一次登录的时间
            userList[0].loginTime = createTime
            userList[0].save()
            Comm.callBackSuccess(callBackDict, 1,dict)
            return callBackDict
        if getopenId == '10000':
            userObj = wdpvipUser.objects.create(openId=getopenId, role=0,loginTime = createTime, createTime=createTime)
        else:
            userObj = wdpvipUser.objects.create(openId=getopenId, role=2, loginTime = createTime,createTime=createTime)
        userObj.save()
        dict = {}
        dict['userId'] = userObj.id
        dict['isEnabled'] = 0
        Comm.callBackSuccess(callBackDict, 1, dict)
    except BaseException as e:
        logger = logging.getLogger("django")
        logger.info(str(e))
        Comm.callBackFail(callBackDict,-1,"系统异常")
    return callBackDict



# 查询所有的用户
def adminGetAllUsers(request):
    # 取得获取的值
    callBackDict = {}
    # 验证用户的openID
    userObj = Jurisdiction.wdpJurisdictGETOpenId(request, callBackDict)
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
    userList = wdpvipUser.objects.all().order_by("-loginTime")[getpage*getpageSize:(getpage*getpageSize+getpageSize)]
    list = []
    for oneuser in userList:
        list.append({"isEnabled":oneuser.isEnabled,"loginTime":oneuser.loginTime,"createTime":oneuser.createTime,"openId":oneuser.openId,"trueName":oneuser.trueName,"name":oneuser.name,"address":oneuser.address,"phone":oneuser.phone,"role":oneuser.role})
    callBackDict['totalNum'] = wdpvipUser.objects.all().count()
    return Comm.callBackSuccess(callBackDict, 1, list)



# 完善用户信息
def perfectUserInfo(request):
    # 取得获取的值
    callBackDict = {}
    getphone = Comm.tryTranslate(request, "phone")
    getaddress = Comm.tryTranslate(request, "address")
    gettrueName = Comm.tryTranslate(request, "trueName")
    # 验证用户的openID
    userObj = Jurisdiction.wdpJurisdictGETOpenId(request, callBackDict)
    if userObj == None:
        return callBackDict
    try:
        if getphone:
            userObj.phone = getphone
        if getaddress:
            userObj.address = getaddress
        if gettrueName:
            userObj.trueName = gettrueName
        userObj.save()
        return Comm.callBackSuccess(callBackDict, 1, userObj.id)
    except BaseException as e:
        logger = logging.getLogger("django")
        logger.info(str(e))
        return Comm.callBackFail(callBackDict,-1,"系统异常")



# web端登录
def webSign(request):
    # 取得获取的值
    callBackDict = {}
    getphone = Comm.tryTranslate(request, "phone")
    getpassword = Comm.tryTranslate(request, "password")
    if Comm.tryTranslateNull('phone', getphone, callBackDict) == False:
        return callBackDict
    if Comm.tryTranslateNull('password', getpassword, callBackDict) == False:
        return callBackDict
    # hash = hashlib.md5()
    # hash.update(str(getpassword).encode("utf-8"))
    # md = hash.hexdigest()
    # hash2 = hashlib.md5()
    # hash2.update(str(md).encode("utf-8"))
    # newgetpassword = str(hash2.hexdigest())
    try:
        # 查询判断用户是否已经存在的
        userList = wdpvipUser.objects.filter(phone=getphone,password=getpassword,role=0)
        if len(userList) > 0:
            userList[0].loginToken = str(uuid.uuid1()).replace("-","")
            userList[0].save()
            dict = {}
            dict['userId'] =  userList[0].id
            dict['name'] = userList[0].name
            dict['address'] = userList[0].address
            dict['trueName'] = userList[0].trueName
            dict['phone'] = userList[0].phone
            dict['token'] = userList[0].loginToken
            Comm.callBackSuccess(callBackDict, 1,dict)
            return callBackDict
        Comm.callBackFail(callBackDict, -1, "登录失败")
    except BaseException as e:
        logger = logging.getLogger("django")
        logger.info(str(e))
        Comm.callBackFail(callBackDict,-1,"系统异常")
    return callBackDict



def adminisEnabledUser(request):
    # 取得获取的值
    callBackDict = {}
    # 验证用户的openID
    userObj = Jurisdiction.wdpJurisAdminGETOpenId(request, callBackDict)
    if userObj == None:
        return callBackDict
    getisEnabled = Comm.tryTranslate(request, "isEnabled")
    getcurUserId = Comm.tryTranslate(request, "curUserId")
    if Comm.tryTranslateNull('isEnabled', getisEnabled, callBackDict) == False:
        return callBackDict
    if Comm.tryTranslateNull('curUserId', getcurUserId, callBackDict) == False:
        return callBackDict
    try:
        userObj = wdpvipUser.objects.get(id=getcurUserId)
        userObj.isEnabled = getisEnabled
        userObj.save()
        Comm.callBackSuccess(callBackDict, 1, None)
        return callBackDict
    except BaseException as e:
        logger = logging.getLogger("django")
        logger.info(str(e))
        Comm.callBackFail(callBackDict,-1,"系统异常")
    return callBackDict
