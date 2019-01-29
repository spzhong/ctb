# -*- coding: utf-8 -*-
import logging
from django.http import HttpResponse
import json
import Comm
import sys
sys.path.append('..')
from ctb.models import user


# 判断用户角色信息
def jurisdictGETOpenId(request,callBackDict):
    # 取得获取的值
    getopneId = Comm.tryTranslate(request,"opneId")
    getuserId = Comm.tryTranslate(request,"userId")
    if Comm.tryTranslateNull('opneId',getopneId,callBackDict) == False:
        return None
    if Comm.tryTranslateNull('userId',getuserId,callBackDict) == False:
        return None
    try:
        userList = user.objects.filter(opneId=getopneId, id=getuserId)
        if len(userList) == 0:
            callBackDict['code'] = -2
            callBackDict['msg'] = "用户不存在"
            return callBackDict
        # 查询出来了用户了
        return userList[0]
    except BaseException as e:
        callBackDict['code'] = -1
        callBackDict['msg'] = "用户异常"
        logger = logging.getLogger("django")
        logger.info(str(e))
        return None


