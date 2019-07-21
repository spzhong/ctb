# -*- coding: utf-8 -*-
import logging
from django.http import HttpResponse
import json
import sys
import time
sys.path.append('...')
from ctb.models import wdpvipUser
from ctb.models import wdpvipOrder
from .. import Comm
from .. import Jurisdiction
import uuid
import PlanningRoutes



# 创建一个规划的路线
def createPlanningRoutes(request):
    # 取得获取的值
    callBackDict = {}
    getopenId = Comm.tryTranslate(request, "openId")
    getuserId = Comm.tryTranslate(request, "userId")
    getfromlon = Comm.tryTranslate(request, "fromlon")
    getfromlat = Comm.tryTranslate(request, "fromlat")
    gettolon = Comm.tryTranslate(request, "tolon")
    gettolat = Comm.tryTranslate(request, "tolat")
    if Comm.tryTranslateNull('openId', getopenId, callBackDict) == False:
        return callBackDict
    if Comm.tryTranslateNull('userId', getuserId, callBackDict) == False:
        return callBackDict
    if Comm.tryTranslateNull('fromlon', getfromlon, callBackDict) == False:
        return callBackDict
    if Comm.tryTranslateNull('fromlat', getfromlat, callBackDict) == False:
        return callBackDict
    if Comm.tryTranslateNull('tolon', gettolon, callBackDict) == False:
        return callBackDict
    if Comm.tryTranslateNull('tolat', gettolat, callBackDict) == False:
        return callBackDict
    # 判断用户的角色及权限
    userObj = Jurisdiction.wdpJurisdictGETOpenId(request, callBackDict)
    if userObj == None:
        return callBackDict
    # 创建一个订单
    try:
        wdpvipOrderObj = wdpvipOrder.objects.create(userId=getuserId,orderNum=str(uuid.uuid4()),orderStatus='DefaultStatus',planningRoute='none',fromRouteList='[]',toRouteList='[]',requestGaoDeApi='')
        wdpvipOrderObj.fromlon = getfromlon
        wdpvipOrderObj.fromlat = getfromlat
        wdpvipOrderObj.tolon = gettolon
        wdpvipOrderObj.tolat = gettolat
        wdpvipOrderObj.createTime = int(time.time() * 1000)
        wdpvipOrderObj.save()
        # 返回订单编号
        Comm.callBackSuccess(callBackDict, 1, wdpvipOrderObj.orderNum)
    except BaseException as e:
        logger = logging.getLogger("django")
        logger.info(str(e))
        Comm.callBackFail(callBackDict,-1,"系统异常")
    return callBackDict



# 微信用户获取自己的规划路线
def getPlanningRoutes(request):
    # 取得获取的值
    callBackDict = {}
    getopenId = Comm.tryTranslate(request, "openId")
    getuserId = Comm.tryTranslate(request, "userId")
    if Comm.tryTranslateNull('openId', getopenId, callBackDict) == False:
        return callBackDict
    if Comm.tryTranslateNull('userId', getuserId, callBackDict) == False:
        return callBackDict
    # 判断用户的角色及权限
    userObj = Jurisdiction.wdpJurisdictGETOpenId(request, callBackDict)
    if userObj == None:
        return callBackDict
    list = selectWdpvipOrder(getuserId, 0, 0,None,None)
    return Comm.callBackSuccess(callBackDict, 1, list)


# 管理员获取所有的规划线路
def adminGetVdpOrder(request):
    # 取得获取的值
    callBackDict = {}
    # 判断用户的角色及权限
    userObj = Jurisdiction.wdpJurisAdminGETOpenId(request, callBackDict)
    if userObj == None:
        return callBackDict
    getorderStatus = Comm.tryTranslate(request, "orderStatus")
    if Comm.tryTranslateNull('orderStatus', getorderStatus, callBackDict) == False:
        return callBackDict
    getplanningRoute = Comm.tryTranslate(request, "planningRoute")
    if Comm.tryTranslateNull('planningRoute', getplanningRoute, callBackDict) == False:
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
    list = selectWdpvipOrder(None,getpage,getpageSize,getplanningRoute)
    if getorderStatus == "All":
        if getplanningRoute == 'All':
            callBackDict['totalNum'] = wdpvipOrder.objects.filter().count()
        else:
            callBackDict['totalNum'] = wdpvipOrder.objects.filter(planningRoute=getplanningRoute).count()
    else:
        if getplanningRoute == 'All':
            callBackDict['totalNum'] = wdpvipOrder.objects.filter(orderStatus=getorderStatus).count()
        else:
            callBackDict['totalNum'] = wdpvipOrder.objects.filter(orderStatus=getorderStatus,planningRoute=getplanningRoute).count()
    return Comm.callBackSuccess(callBackDict, 1, list)



# 查询出来订单
def selectWdpvipOrder(getuserId,getpage,getpageSize,getorderStatus,getplanningRoute):
    if getplanningRoute == None:
        wdpvipOrderList = wdpvipOrder.objects.filter(userId=getuserId).order_by("-createTime")
    else:
        if getorderStatus == "All":
            if getplanningRoute == 'All':
                wdpvipOrderList = wdpvipOrder.objects.filter().order_by("-createTime")[getpage*getpageSize:(getpage*getpageSize+getpageSize)]
            else:
                wdpvipOrderList = wdpvipOrder.objects.filter(planningRoute=getplanningRoute).order_by("-createTime")[getpage*getpageSize:(getpage*getpageSize+getpageSize)]
        else:
            if getplanningRoute == 'All':
                wdpvipOrderList = wdpvipOrder.objects.filter(orderStatus=getorderStatus).order_by("-createTime")[getpage*getpageSize:(getpage*getpageSize+getpageSize)]
            else:
                wdpvipOrderList = wdpvipOrder.objects.filter(orderStatus=getorderStatus,planningRoute=getplanningRoute).order_by("-createTime")[getpage*getpageSize:(getpage*getpageSize+getpageSize)]
    list = []
    for wdp in wdpvipOrderList:
        list.append({"orderNum":wdp.orderNum,"userId":wdp.userId,"fromlon":wdp.fromlon,"fromlat":wdp.fromlat,"tolon":wdp.tolon,"tolat":wdp.tolat,"createTime":wdp.createTime,"orderPrice":wdp.orderPrice,"orderStatus":wdp.orderStatus,"planningRoute":wdp.planningRoute,"fromRouteList":wdp.fromRouteList,"toRouteList":wdp.toRouteList})
    return list



# 订单状态：DefaultStatus默认待支付（用户申请路线）,PaymentedStatus支付成功（管理员确认后，路线规划中）,DeleteStatus删除订单,RefundedStatus退款状态,OverStatus订单终结
#orderStatus = models.CharField(max_length=255)
# 路线状态：已支付后，就是路线规划的状态，AutoPlanning自动规划中，AutoPlanningFail自动规划中失败，AdminConfirmPlanningOk管理员确认规划成功，AdminConfirmPlanningFail管理员确认规划失败
#planningRoute = models.CharField(max_length=255)
# 管理员修改支付的状态-修改完成后，就要进行路线规划了
def adminModifyVdpOrder(request):
    # 取得获取的值
    callBackDict = {}
    # 判断用户的角色及权限
    userObj = Jurisdiction.wdpJurisAdminGETOpenId(request, callBackDict)
    if userObj == None:
        return callBackDict
    getorderNum = Comm.tryTranslate(request, "orderNum")
    if Comm.tryTranslateNull('orderNum', getorderNum, callBackDict) == False:
        return callBackDict
    try:
        # 查询是否存在该订单
        wdpvipOrderObj = wdpvipOrder.objects.get(orderNum = getorderNum)
        # 进行处理--订单已经支付
        wdpvipOrderObj.orderStatus = 'PaymentedStatus'
        wdpvipOrderObj.planningRoute = 'AutoPlanning'
        # 进行路线的规划
        # 来取两条路线规划
        fromAotuDict = PlanningRoutes.autoAvoidRoute(wdpvipOrderObj.fromlon,wdpvipOrderObj.fromlat,wdpvipOrderObj.tolon,wdpvipOrderObj.tolat)
        toAotuDict = PlanningRoutes.autoAvoidRoute(wdpvipOrderObj.tolon,wdpvipOrderObj.tolat,wdpvipOrderObj.fromlon, wdpvipOrderObj.fromlat)
        # 来回两条路线的如果都是空
        if fromAotuDict['msg']:
            wdpvipOrderObj.planningRoute = 'AutoPlanningFail'
        else:
            wdpvipOrderObj.fromRouteList = fromAotuDict['list']
            wdpvipOrderObj.planningRoute = 'AutoPlanningFinsh'
        if toAotuDict['msg']:
            wdpvipOrderObj.planningRoute = 'AutoPlanningFail'
        else:
            wdpvipOrderObj.toRouteList = toAotuDict['list']
            wdpvipOrderObj.planningRoute = 'AutoPlanningFinsh'
        # 进行路线的保存
        wdpvipOrderObj.save()
        Comm.callBackFail(callBackDict, 1, list.append({"orderNum":wdpvipOrderObj.orderNum,"userId":wdpvipOrderObj.userId,"fromlon":wdpvipOrderObj.fromlon,"fromlat":wdpvipOrderObj.fromlat,"tolon":wdpvipOrderObj.tolon,"tolat":wdpvipOrderObj.tolat,"createTime":wdpvipOrderObj.createTime,"orderPrice":wdpvipOrderObj.orderPrice,"orderStatus":wdpvipOrderObj.orderStatus,"planningRoute":wdpvipOrderObj.planningRoute,"fromRouteList":wdpvipOrderObj.fromRouteList,"toRouteList":wdpvipOrderObj.toRouteList}))
    except BaseException as e:
        logger = logging.getLogger("django")
        logger.info(str(e))
        Comm.callBackFail(callBackDict,-1,"系统异常")
    return callBackDict



# 订单状态：DefaultStatus默认待支付（用户申请路线）,PaymentedStatus支付成功（管理员确认后，路线规划中）,DeleteStatus删除订单,RefundedStatus退款状态,OverStatus订单终结
#orderStatus = models.CharField(max_length=255)
# 路线状态：已支付后，就是路线规划的状态，AutoPlanning自动规划中，AutoPlanningFail自动规划中失败，AdminConfirmPlanningOk管理员确认规划成功，AdminConfirmPlanningFail管理员确认规划失败
#planningRoute = models.CharField(max_length=255)
# 管理员修改支付的状态-修改完成后，就要进行路线规划了
def adminModifyPlanningRouteOk(request):
    # 取得获取的值
    callBackDict = {}
    getfromRouteList = Comm.tryTranslate(request, "fromRouteList")
    if Comm.tryTranslateNull('fromRouteList 规划路线为空', getfromRouteList, callBackDict) == False:
        return callBackDict
    gettoRouteList = Comm.tryTranslate(request, "toRouteList")
    if Comm.tryTranslateNull('toRouteList 规划路线为空', gettoRouteList, callBackDict) == False:
        return callBackDict
    getorderNum = Comm.tryTranslate(request, "orderNum")
    if Comm.tryTranslateNull('orderNum 为空', getorderNum, callBackDict) == False:
        return callBackDict
    # 判断用户的角色及权限
    userObj = Jurisdiction.wdpJurisAdminGETOpenId(request, callBackDict)
    if userObj == None:
        return callBackDict
    try:
        # 查询是否存在该订单
        wdpvipOrderObj = wdpvipOrder.objects.get(orderNum = getorderNum)
        # 订单支付成功
        if wdpvipOrderObj.orderStatus == 'PaymentedStatus':
            # 进行处理--订单已经支付
            if wdpvipOrderObj.planningRoute == "AutoPlanningFinsh":
                # 管理员手动规划路线
                wdpvipOrderObj.fromRouteList = getfromRouteList
                wdpvipOrderObj.toRouteList = gettoRouteList
                # 标记订单已终结
                wdpvipOrderObj.planningRoute = 'AdminConfirmPlanningOk'
                wdpvipOrderObj.orderStatus = 'OverStatus'
                wdpvipOrderObj.save()
                # 管理员手动规划路线
                return Comm.callBackSuccess(callBackDict, 1, "已确认，路线规划完成")
            else:
                if wdpvipOrderObj.orderStatus == 'DefaultStatus':
                    return Comm.callBackFail(callBackDict, -2, "订单尚未支付")
                elif wdpvipOrderObj.orderStatus == 'DeleteStatus':
                    return Comm.callBackFail(callBackDict, -3, "订单已经删除")
                elif wdpvipOrderObj.orderStatus == 'RefundedStatus':
                    return Comm.callBackFail(callBackDict, -4, "订单退款")
                elif wdpvipOrderObj.orderStatus == 'OverStatus':
                    return Comm.callBackFail(callBackDict, -4, "订单已终结")
                else:
                    return Comm.callBackFail(callBackDict, -5, "订单异常")
        else:
            return Comm.callBackFail(callBackDict, -2, "订单尚未支付")
    except BaseException as e:
        logger = logging.getLogger("django")
        logger.info(str(e))
        Comm.callBackFail(callBackDict,-1,"系统异常")
    return callBackDict




# 订单状态：DefaultStatus默认待支付（用户申请路线）,PaymentedStatus支付成功（管理员确认后，路线规划中）,DeleteStatus删除订单,RefundedStatus退款状态,OverStatus订单终结
#orderStatus = models.CharField(max_length=255)
# 路线状态：已支付后，就是路线规划的状态，AutoPlanning自动规划中，AutoPlanningFail自动规划中失败，AdminConfirmPlanningOk管理员确认规划成功，AdminConfirmPlanningFail管理员确认规划失败
#planningRoute = models.CharField(max_length=255)
# 管理员修改支付的状态-修改完成后，就要进行路线规划了
def adminModifyPlanningRouteFail(request):
    # 取得获取的值
    callBackDict = {}
    getorderNum = Comm.tryTranslate(request, "orderNum")
    if Comm.tryTranslateNull('orderNum', getorderNum, callBackDict) == False:
        return callBackDict
    # 判断用户的角色及权限
    userObj = Jurisdiction.wdpJurisAdminGETOpenId(request, callBackDict)
    if userObj == None:
        return callBackDict
    try:
        # 查询是否存在该订单
        wdpvipOrderObj = wdpvipOrder.objects.get(orderNum = getorderNum)
        # 订单支付成功
        if wdpvipOrderObj.orderStatus == 'PaymentedStatus':
            # 进行处理--订单已经支付
            if wdpvipOrderObj.planningRoute == "AutoPlanningFinsh":
                # 标记订单-处于退款的状态
                wdpvipOrderObj.planningRoute = 'AdminConfirmPlanningFail'
                wdpvipOrderObj.orderStatus = 'RefundedStatus'
                wdpvipOrderObj.save()
                # 管理员手动规划路线
                return Comm.callBackSuccess(callBackDict, 1, "已标记路线规划失败，设置为退款状态")
            else:
                return Comm.callBackFail(callBackDict, -1, "路线尚未规划完成，请重新规划")
        else:
            if wdpvipOrderObj.orderStatus == 'DefaultStatus':
                return Comm.callBackFail(callBackDict, -2, "订单尚未支付")
            elif wdpvipOrderObj.orderStatus == 'DeleteStatus':
                return Comm.callBackFail(callBackDict, -3, "订单已经删除")
            elif wdpvipOrderObj.orderStatus == 'RefundedStatus':
                return Comm.callBackFail(callBackDict, -4, "订单退款")
            elif wdpvipOrderObj.orderStatus == 'OverStatus':
                return Comm.callBackFail(callBackDict, -4, "订单已终结")
            else:
                return Comm.callBackFail(callBackDict, -5, "订单异常")
    except BaseException as e:
        logger = logging.getLogger("django")
        logger.info(str(e))
        Comm.callBackFail(callBackDict,-1,"系统异常")
    return callBackDict

