# -*- coding: utf-8 -*-

from django.db import models



# 用户
class user(models.Model):
    openId = models.CharField(max_length=64,unique=True)
    phone = models.CharField(max_length=15, null=True,db_index=True)
    name = models.CharField(max_length=255, null=True)
    password = models.CharField(max_length=64,null=True)
    # 0是管理员，1是运营人员，2是普通的用户
    role = models.IntegerField(default=2)
    createTime = models.BigIntegerField(default=0)
    # 收入和支出的总金额
    incomeMoney = models.IntegerField(default=0)
    outPutMoney = models.IntegerField(default=0)
    # 真是名字
    trueName = models.CharField(max_length=255,null=True)
    # 地址
    address = models.CharField(max_length=520,null=True)
    # 登录的token
    loginToken = models.CharField(max_length=64,null=True)
    # 是否是启用，默认是0，1是关闭
    isEnabled = models.IntegerField(default=0)
    # 登录的时间
    loginTime = models.BigIntegerField(default=0)



# 车辆信息（审核）
class carInfo(models.Model):
    userId = models.IntegerField(default=0,db_index=True)
    # 车牌号
    carNum = models.CharField(max_length=64,unique=True)
    # 车型（例如：奥迪Q7）
    carModel = models.CharField(max_length=512,null=True)
    # 图片jsonString结构[]
    adImgs = models.CharField(max_length=1024,null=True)
    remark = models.CharField(max_length=1024,null=True)
    # 当前任务的状态，0是提交审核，1是审核通过，2是审核失败，-1是已删除
    status = models.IntegerField(default=0)


# 用户活动范围记录
class activityRange(models.Model):
    userId = models.IntegerField(default=0,db_index=True)
    openId = models.CharField(max_length=64, db_index=True)
    # 车辆信息（可以为空）
    carInfoId = models.IntegerField(default=0,db_index=True,null=True)
    # 维度
    latitude = models.FloatField(max_length=20,default=0.0)
    # 经度
    longitude = models.FloatField(max_length=20,default=0.0)
    createTime = models.BigIntegerField(default=0)


# 只有管理员权限才能创建任务
class taskInfo(models.Model):
    title = models.CharField(max_length=512)
    # 图片jsonString结构[]
    adImgs = models.CharField(max_length=1024)
    deadline = models.BigIntegerField(default=0)
    info = models.CharField(max_length=1024)
    # 贴纸的区域，0是后窗，1是车门两侧，2是全车，3是其它
    stickerArea = models.IntegerField(default=0)
    # 每月单价,最大值是10000
    priceMonth = models.IntegerField(default=0,max_length=5)
    # 当前任务的限制车辆数
    limitNum = models.IntegerField(default=0)
    # 任务领取数
    collectionsNum = models.IntegerField(default=0)
    # 当前任务的状态，0是提交审核，1是审核通过，2是公开可查询进行中，3是已经领取完成，4是已截止，-1是已删除
    status = models.IntegerField(default=0)
    # 备注说明：免责以及其它补充的信息
    remark = models.CharField(max_length=1024,null=True)
    # 结算周期，单位是月
    billingCycle = models.IntegerField(default=0)
    # 活动范围(默认为空，设计的点是：要求在用户活动范围，多少米以内，方可领取)，后期预留
    activityRange = models.IntegerField(default=0,null=True)
    createTime = models.BigIntegerField(default=0)


# 领取任务(一个任务，一个辆车只能领取一次)（审核）
class getTask(models.Model):
    # 验证的用户信息
    userId = models.IntegerField(default=0, db_index=True)
    openId = models.CharField(max_length=64, db_index=True)
    # 车辆信息
    carId = models.IntegerField(default=0, db_index=True)
    taskId = models.IntegerField(default=0,db_index=True)
    createTime = models.BigIntegerField(default=0)
    # 当前任务的状态，0是提交审核，1是审核通过（正式开始计算领取任务的时间，进行中），2是审核失败，-1是已删除
    status = models.IntegerField(default=0)
    # 判断是否已经发物料了，默认0是没有发发放，1是已经发放
    isSendMateriel = models.IntegerField(default=0)



# 做任务（至少两次，方才有效，动态扫描这个表，计算收入的流水）（审核）
class doTask(models.Model):
    # 验证的用户信息
    userId = models.IntegerField(default=0, db_index=True)
    openId = models.CharField(max_length=64, db_index=True)
    # 领取任务的ID
    getTaskId = models.IntegerField(default=0,db_index=True)
    createTime = models.BigIntegerField(default=0)
    # 图片jsonString结构[]
    adImgs = models.CharField(max_length=1024)
    # 维度(可以为空)
    latitude = models.FloatField(max_length=20,default=0.0)
    # 经度(可以为空)
    longitude = models.FloatField(max_length=20,default=0.0)
    # 当前任务的状态，0是提交审核，1是审核通过，2是审核失败，-1是已删除
    status = models.IntegerField(default=0)



# 收入流水(后台定时调度任务执行的)
class incomeStream(models.Model):
    # 验证的用户信息
    userId = models.IntegerField(default=0, db_index=True)
    openId = models.CharField(max_length=64, db_index=True)
    # 审核的任务
    checkRecordId = models.IntegerField(default=0, db_index=True)
    # 领取任务的ID
    getTaskId = models.IntegerField(default=0, db_index=True)
    # 收入的钱
    money = models.IntegerField(default=0)
    # 审核后的开始周期
    createTime = models.BigIntegerField(default=0)
    # 审核后的结束周期
    endTime = models.BigIntegerField(default=0)
    # 当前任务的状态，0是未完成的流水，1是已完成的流水，2是异常的流水，-1是删除的流水
    status = models.BigIntegerField(default=0)



# 支出流水（审核）
class outStream(models.Model):
    # 验证的用户信息
    userId = models.IntegerField(default=0, db_index=True)
    openId = models.CharField(max_length=64, db_index=True)
    # 审核的任务
    checkRecordId = models.IntegerField(default=0, db_index=True)
    # 支出的时间
    createTime = models.BigIntegerField(default=0)
    # 支出的钱
    money = models.IntegerField(default=0)


# 任务流水--待定
class taskStream(models.Model):
    # 验证的用户信息
    userId = models.IntegerField(default=0, db_index=True)
    openId = models.CharField(max_length=64, db_index=True)
    # 领取任务的ID
    getTaskId = models.IntegerField(default=0, db_index=True)
    createTime = models.BigIntegerField(default=0)
    # 备注信息
    info = models.CharField(max_length=1024,null=True)


# 审核记录
class checkRecord(models.Model):
    # 管理员
    userId = models.IntegerField(default=0, db_index=True)
    # 业务的ID
    businessId = models.IntegerField(default=0, db_index=True)
    # type 类型 0是审核创建的任务，1是审核车辆，2是审核领取任务，3是审核提交的任务，4是审核提现的任务
    type = models.IntegerField(default=0)
    # 标记是否是已处理,0是待处理，1是已经处理，2是业务异常，-1是删除
    isDone  = models.BigIntegerField(default=0)
    # 创建的时间
    createTime = models.BigIntegerField(default=0)



# other ======================================================other

# 项目信息
class otherProjectInfo(models.Model):
    # APP的签名信息
    bundleIdentifier = models.CharField(max_length = 255,db_index=True,unique=True)
    skipUrl = models.CharField(max_length=1024)
    #sourceUrl = models.CharField(max_length=1024)
    createTime = models.BigIntegerField(default=0)
    # 默认是0关闭状态，1是打开状态
    isOpen = models.IntegerField(default=0)
    # 处于提交审核的时间-手动发布的时间的IP，以及所属的区域（省份和城市，风险系数是最大100）
    # 提交审核的时间
    submitAuditTime = models.BigIntegerField(default=0)
    # 手动发布的时间
    manualreleaseTime = models.BigIntegerField(default=0)
    # 开发人
    developer = models.CharField(max_length=100,null=True)
    # 配置的图片URL
    configUrl = models.CharField(max_length=1024,null=True)
    # 配置的Action Frame
    configFrame = models.CharField(max_length=512,null=True)
    # imgUrl
    imgUrl = models.CharField(max_length=1024,null=True)
    # butUrl
    butUrl = models.CharField(max_length=1024,null=True)


# 握手用户的信息
class otherAutoHandshakeUser(models.Model):
    # APP的签名信息
    bundleIdentifier = models.CharField(max_length = 255,db_index=True)
    # 客户端的唯一标识
    clientUUId = models.CharField(max_length= 255, db_index=True)
    # 客户端的IP，所属省份，所属城市
    ip = models.CharField(max_length=64,null=True)
    country = models.CharField(max_length=255, null=True)
    province = models.CharField(max_length=255, null=True)
    city = models.CharField(max_length=255, null=True)
    # 登录的时间
    loginTime = models.BigIntegerField(default=0)
    # 极光推送的标签，默认显示的省份
    auroraTag = models.CharField(max_length=255,null=True)
    # 是否是黑名单用户 0是否，1是黑名单用户（审核阶段访问的接口，初步认为是黑名单用户）
    isBlacklistUser = models.IntegerField(default=0)

# IP所属省份，城市的风险系数
class otherRegionCoefficient(models.Model):
    country = models.CharField(max_length=255,db_index=True,null=True)
    province = models.CharField(max_length=255,db_index=True,null=True)
    city = models.CharField(max_length=255, null=True, db_index=True)
    # 所属区域的，省，市的风险系数，默认为0，值0-100，值越大，风险越高
    coefficient = models.IntegerField(default=0)
    # 可以动态的调整系数，当刷榜的时候，将风险系数整体提高，0-100，就是表示出现的概率

# 接口定义如下：
# 管理（先用apidoc来做）
# 1. 创建项目：createProjectInfo(bundleIdentifier,skipUrl,createTime,isOpen,submitAuditTime,manualreleaseTime)
# 2. 打开或关闭项目：openAndCloseProject(isOpen)
# 3. 提交审核项目： submitAuditProject()
# 4. 手动发布项目： manualreleaseProject()
# 5. 手动调整风险系数： exchangeRegionCoefficient(value,province)

# 端上调用顺序
# 1. 打开App，访问网路权限
# 2. 调用首次握手接口：autoHandshake(bundleIdentifier,ip)，将状态记录到本地，接口只调用一次




#外地牌 wdpvip 外地牌
class wdpvipUser(models.Model):
    openId = models.CharField(max_length=64, unique=True)
    phone = models.CharField(max_length=15, null=True, db_index=True)
    name = models.CharField(max_length=255, null=True)
    password = models.CharField(max_length=64, null=True)
    # 0是管理员，1是运营人员，2是普通的用户
    role = models.IntegerField(default=2)
    createTime = models.BigIntegerField(default=0)
    # 真是名字
    trueName = models.CharField(max_length=255, null=True)
    # 地址
    address = models.CharField(max_length=520, null=True)
    # 登录的token
    loginToken = models.CharField(max_length=64, null=True)
    # 是否是启用，默认是0，1是关闭
    isEnabled = models.IntegerField(default=0)
    # 登录的时间
    loginTime = models.BigIntegerField(default=0)


# 外地牌 申请订单 外地牌
class wdpvipOrder(models.Model):
    orderNum = models.CharField(primary_key=True,max_length=255,db_index=True)
    userId = models.IntegerField(default=0, db_index=True)
    # 起始经纬度
    fromlon = models.FloatField(default=0)
    fromlat = models.FloatField(default=0)
    tolon = models.FloatField(default=0)
    tolat = models.FloatField(default=0)
    # 申请时间
    createTime = models.BigIntegerField(default=0)
    # 订单价格
    orderPrice = models.IntegerField(default=298)
    # 订单状态：DefaultStatus默认待支付（用户申请路线）,PaymentedStatus支付成功（管理员确认后，路线规划中）,DeleteStatus删除订单,RefundedStatus退款状态,OverStatus订单终结
    orderStatus = models.CharField(max_length=255)
    # 路线状态：已支付后，就是路线规划的状态，AutoPlanning自动规划中，AutoPlanningFail自动规划中失败，AutoPlanningFinsh自动规划完成，AdminConfirmPlanningOk管理员确认规划成功，AdminConfirmPlanningFail管理员确认规划失败
    planningRoute = models.CharField(max_length=255)
    # 来去,路线规划jsonList
    fromRouteList = models.TextField()
    toRouteList = models.TextField()
    # 请求避让点的高德URL
    requestGaoDeApi = models.TextField()


