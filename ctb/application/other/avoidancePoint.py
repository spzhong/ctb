# -*- coding: utf-8 -*-
import json
import random
import time
import math
import sys
import urllib2
import httplib
import logging
from .. import Comm


# 初始化启动
def initStart(origin_lon,origin_lat,destination_lon,destination_lat):
    # 半径的距离
    radius = math.sqrt(pow(abs(origin_lon-destination_lon),2) + pow(abs(origin_lat-destination_lat),2))/2
    radiusList = [radius/2]
    position = ''  #相对起点，终点的方位
    if origin_lon - destination_lon > 0:
        if origin_lat - destination_lat < 0 :
            position = '西北'
        else:
            position = '西南'
    else:
        if origin_lat - destination_lat < 0 :
            position = '东北'
        else:
            position = '东南'
    # 搜索和筛选规避的点
    allAvoidanceList = getAllAvoidancePoints()
    if allAvoidanceList == None:
        return '获取配置避让点的文件为空'
    # 进行筛选 - 查找适合的半径距离
    fitRadiusaPolygonsList = None
    # 获得修正后的坐标
    correct_lonlatList = amendedLonLat(position,radius/4,origin_lon,origin_lat,destination_lon,destination_lat)
    # 查询避让点
    for radiusOne in radiusList:
        # 得到修正后的矩形，判断避让点是否包含所在的修正后的矩形
        avoidpolygonsCount = 0
        fitRadiusaPolygonsList = []
        for dict in allAvoidanceList:
            # 判断避让点是否在包含所在的修正的矩形中
            if includedInRectangle(position,correct_lonlatList[0],correct_lonlatList[1],correct_lonlatList[2],correct_lonlatList[3],dict) == True:
                avoidpolygonsCount += 1
                # 记录避让点
                fitRadiusaPolygonsList.append(dict)
#            # 最多采用30个避让点
#            if avoidpolygonsCount > 30:
#                break
    # 得到所有符合范围的避让点，进行避让点的拼装
    avoidpolygons=''
    for dict in fitRadiusaPolygonsList:
        avoidpolygons += rectanglesize(dict['lon'],dict['lat'])
    if len(fitRadiusaPolygonsList) < 32:
        # 请求高德规划的路线
        page_source = httpLoadGD(str(origin_lon) + "," + str(origin_lat), str(destination_lon) + "," + str(destination_lat),
                   avoidpolygons)
        if page_source == None:
            return "高德API请求异常"
        # 分析高德地图的规划路线
        # 得到规划的路线
        try:
            stepsList = analysisGDJsonData(page_source)
            return [stepsList,len(fitRadiusaPolygonsList)]
        except:
            return "解析避让道路异常"
    else:
        return "查询避让点:" + str(len(fitRadiusaPolygonsList)) + "个,超过了32个，没有高德API的请求"


# 得到修正后的坐标
def amendedLonLat(position,radiusOne,origin_lon,origin_lat,destination_lon,destination_lat):
    correctOrigin_lon = origin_lon
    correctOrigin_lat = origin_lat
    correctDestination_lon = destination_lon
    correctDestination_lat = destination_lat
    if position == '西北':
        correctOrigin_lon += radiusOne*2/math.sqrt(2)
        correctOrigin_lat -= radiusOne*2/math.sqrt(2)
        correctDestination_lon -= radiusOne*2/math.sqrt(2)
        correctDestination_lat += radiusOne*2/math.sqrt(2)
    elif position == '西南':
        correctOrigin_lon += radiusOne*2/math.sqrt(2)
        correctOrigin_lat += radiusOne*2/math.sqrt(2)
        correctDestination_lon -= radiusOne*2/math.sqrt(2)
        correctDestination_lat -= radiusOne*2/math.sqrt(2)
    elif position == '东北':
        correctOrigin_lon -= radiusOne*2/math.sqrt(2)
        correctOrigin_lat -= radiusOne*2/math.sqrt(2)
        correctDestination_lon += radiusOne*2/math.sqrt(2)
        correctDestination_lat += radiusOne*2/math.sqrt(2)
    elif position == '东南':
        correctOrigin_lon -= radiusOne*2/math.sqrt(2)
        correctOrigin_lat += radiusOne*2/math.sqrt(2)
        correctDestination_lon += radiusOne*2/math.sqrt(2)
        correctDestination_lat -= radiusOne*2/math.sqrt(2)
    return [correctOrigin_lon,correctOrigin_lat,correctDestination_lon,correctDestination_lat]



# 是否包含在矩形中
def includedInRectangle(position,correctOrigin_lon,correctOrigin_lat,correctDestination_lon,correctDestination_lat,dict):
    if position == '西北':
        if dict['lon'] > correctDestination_lon and dict['lon'] < correctOrigin_lon and dict['lat'] < correctDestination_lat and dict['lat'] > correctOrigin_lat and isInSubSiseRect(correctDestination_lon,correctOrigin_lat,abs(correctOrigin_lon-correctDestination_lon), abs(correctDestination_lat-correctOrigin_lat),dict):
            return True
    elif position == '西南':
        if dict['lon'] > correctDestination_lon and dict['lon'] < correctOrigin_lon and dict['lat'] < correctOrigin_lat and dict['lat'] > correctDestination_lat and isInSubSiseRect(correctDestination_lon,correctDestination_lat,abs(correctOrigin_lon-correctDestination_lon), abs(correctDestination_lat-correctOrigin_lat),dict):
            return True
    elif position == '东北':
        if dict['lon'] > correctOrigin_lon and dict['lon'] < correctDestination_lon and dict['lat'] < correctOrigin_lat and dict['lat'] > correctDestination_lat and isInSubSiseRect(correctOrigin_lon,correctOrigin_lat,abs(correctOrigin_lon-correctDestination_lon), abs(correctDestination_lat-correctOrigin_lat),dict):
            return True
    elif position == '东南':
        if dict['lon'] > correctOrigin_lon and dict['lon'] < correctDestination_lon and dict['lat'] < correctOrigin_lat and dict['lat'] > correctDestination_lat and isInSubSiseRect(correctOrigin_lon,correctDestination_lat,abs(correctOrigin_lon-correctDestination_lon), abs(correctDestination_lat-correctOrigin_lat),dict):
            return True
    return False



# 判断是否在区域内
def isInSubSiseRect(x,y,w,h,dict):
    if dict['lon'] < x + w/2 and dict['lat'] < y+h/2:
        return False
    if dict['lon'] > x + w/2 and dict['lat'] > y+h/2:
        return False
    return True


# 避让矩形
def rectanglesize(lon,lat):
    radius = 0.002000
    avoidpolygonOne = ''
    # left
    avoidpolygonOne += "{0:.6f}".format(lon-radius) + "," + "{0:.6f}".format(lat) + ";"
    # down
    avoidpolygonOne += "{0:.6f}".format(lon) + "," + "{0:.6f}".format(lat-radius) + ";"
    # right
    avoidpolygonOne += "{0:.6f}".format(lon+radius) + "," + "{0:.6f}".format(lat) + ";"
    # up
    avoidpolygonOne += "{0:.6f}".format(lon) + "," + "{0:.6f}".format(lat+radius)
    return avoidpolygonOne+"|"



# 请求高德规划的路线
def httpLoadGD(origin,destination,avoidpolygons):
    try:
        url = 'https://restapi.amap.com/v3/direction/driving?'
        url += "origin="
        url += origin   # 起点经度
        url += "&destination="
        url += destination   # 起点维度
        url += "&extensions=base"
        url += "&strategy=0"    #0，速度优先，不考虑当时路况，此路线不一定距离最短
        #1，费用优先，不走收费路段，且耗时最少的路线
        #2，距离优先，不考虑路况，仅走距离最短的路线，但是可能存在穿越小路/小区的情况
        #3，速度优先，不走快速路，例如京通快速路（因为策略迭代，建议使用13）
        #4，躲避拥堵，但是可能会存在绕路的情况，耗时可能较长
        #5，多策略（同时使用速度优先、费用优先、距离优先三个策略计算路径）。
        #其中必须说明，就算使用三个策略算路，会根据路况不固定的返回一~三条路径规划信息。
        #6，速度优先，不走高速，但是不排除走其余收费路段
        #7，费用优先，不走高速且避免所有收费路段
        #8，躲避拥堵和收费，可能存在走高速的情况，并且考虑路况不走拥堵路线，但有可能存在绕路和时间较长
        #9，躲避拥堵和收费，不走高速
        # 增加避让点
        if avoidpolygons:
            url += "&avoidpolygons="+avoidpolygons[:-1]  #截取从头开始到倒数第一个字符之前
        url += "&ferry=1"       #不使用渡轮
        url += "&key=49521b5942bff4d41e5495698ab5bcb6"
        res = urllib2.urlopen(url, timeout=5)
        page_source = res.read().decode('utf-8')
        return page_source
    except:
        return None


# 分析高德返回的数据
def analysisGDJsonData(page_source):
    try:
        jsonData = json.loads(page_source)
        pathsList = jsonData['route']['paths']
        steps = None
        for path in pathsList:
            steps = []
            for oneStep in path['steps']:
                steps.append(oneStep)
        return steps
            # strTimes = ''
            # for stepOne in steps:
            #     polyLineList = stepOne['polyline'].split(';')
            #     strTimes += "new AMap.LngLat("+polyLineList[-1]+"),\n"
            #     #print(polyLineList[-1])
            # print("关键坐标长度:"+str(len(steps)) + "\n避让点数：" + str(fitRadiusaPolygonsList) + "\n关键经纬度如下：\n"+strTimes)
    except BaseException as e:
        return "解析数据异常"


def bdToGaoDe(lon, lat):
    PI = 3.14159265358979324 * 3000.0 / 180.0
    x = lon - 0.0065
    y = lat - 0.006
    z = math.sqrt(x * x + y * y) - 0.00002 * math.sin(y * PI)
    theta = math.atan2(y, x) - 0.000003 * math.cos(x * PI)
    lon = z * math.cos(theta)
    lat = z * math.sin(theta)
    return lon, lat


# 深圳避让点
# 注意，传入的经纬度是，是经度在前，维度在后
# 另外，注意是float类型，小数点最后最多6位数
def getAllAvoidancePoints():
    logger = logging.getLogger("django")
    f = open("/srv/ctb/ctb/application/other/index.json", "r")  # 打开文件
    fr = f.read()  # 读取文件
    try:
        jsonData = eval(fr)
        list = []
        for dict in jsonData['RECORDS']:
            list.append({"lon":float(dict['longitude']),"lat":float(dict['latitude'])})
        return list
    except BaseException as e:
        logger.info('1_2' + str(e))
        return None



# 获取避让的道路
def getAvoidRoute(request):
    callBackDict = {}
    #首先的判断当前项目的情况
    getbundleIdentifier = Comm.tryTranslate(request, "sessionId")
    s_lonlat = Comm.tryTranslate(request, "s_lonlat")
    e_lonlat = Comm.tryTranslate(request, "e_lonlat")
    #if Comm.tryTranslateNull("sessionId 为空", getbundleIdentifier, callBackDict) == False:
    #    return callBackDict
    if Comm.tryTranslateNull("起点纬纬度为空", s_lonlat, callBackDict) == False:
        return callBackDict
    if Comm.tryTranslateNull("结束经纬度为空", e_lonlat, callBackDict) == False:
        return callBackDict
    try:
        slist = s_lonlat.split(',')
        elist = e_lonlat.split(',')
        s_lon = slist[0]
        s_lat = slist[1]
        e_lon = elist[0]
        e_lat = elist[1]
        # 开启计算
        stepsMsgArray = initStart(float(s_lon), float(s_lat), float(e_lon), float(e_lat))
        if type(stepsMsgArray) is list:
            steps = []
            stepstr = ''
            steps.append(str(s_lon) + "," + str(s_lat))
            stepstr += "[[" + str(s_lon) +","+str(s_lat) + "],"
            for step in stepsMsgArray[0]:
                try:
                    polylineStr = step['polyline']
                    polyLineList = polylineStr.split(';')
                    steps.append(polyLineList[0])
                    stepstr += "[" + polyLineList[0] + "],"
                    stepstr += "[" + polyLineList[len(polyLineList) - 1] + "],"
                    steps.append(polyLineList[len(polyLineList) - 1])
                    #steps.append({"road": step['road'], "instruction": step['instruction'], "orientation": step['orientation'],
                    #             "action": step['action'], "polyline":polyLineList[len(polyLineList) - 1]})
                except:
                    continue
            steps.append(str(e_lon) + "," + str(e_lat))
            stepstr += "[" + str(e_lon) + "," + str(e_lat) + "]]"
            return Comm.callBackSuccess(callBackDict, 1, {"start":s_lonlat,"end":e_lonlat,"avoidAreasCount":str(stepsMsgArray[1]),"listStr":stepstr})
        else:
            return Comm.callBackFail(callBackDict, 0, stepsMsgArray)
    except BaseException as e:
        logger = logging.getLogger("django")
        logger.info(str(e))
        return Comm.callBackFail(callBackDict, 0, "输入的经纬度异常")

    # # 测试用
    # testList = getAllAvoidancePoints()
    # if testList == None:
    #     return Comm.callBackFail(callBackDict, 0, "获取经纬度配置异常")


# # 执行程序的入口
# def main(argv):
#     try:
#         slist = argv[1].split(',')
#         elist = argv[2].split(',')
#
#         s_lon = slist[0]
#         s_lat = slist[1]
#
#         e_lon = elist[0]
#         e_lat = elist[1]
#
#         print("\n起始经纬度：" + "new AMap.LngLat({0:.6f}".format(float(s_lon)) + "," + "{0:.6f}".format(float(s_lat)) + "),");
#         print("new AMap.LngLat({0:.6f}".format(float(e_lon))+","+"{0:.6f}".format(float(e_lat))+"),");
#         initStart(float(s_lon),float(s_lat),float(e_lon),float(e_lat))
#
#         #initStart(113.943511,22.549537, 113.880579,22.582984)
#         # # 随机经纬度
#         # for num in range(0,1):
#         #     s_lon = random.uniform(113.793640, 114.310684)
#         #     s_lat = random.uniform(22.592458, 22.715390)
#         #     e_lon = random.uniform(113.793640, 114.310684)
#         #     e_lat = random.uniform(22.592458, 22.715390)
#         #     print("\n起终点:\n"+"new AMap.LngLat({0:.6f}".format(s_lon)+","+"{0:.6f}".format(s_lat)+")",);
#         #     print("new AMap.LngLat({0:.6f}".format(e_lon)+","+"{0:.6f}".format(e_lat)+")");
#         #     initStart(s_lon,s_lat,e_lon,e_lat)
#     except BaseException as e:
#         print("传入起始经纬度异常:" + str(e))
#         exit(0)
#
# if __name__ == "__main__":
#     main(sys.argv)




