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


# 车辆信息
class carInfo(models.Model):
    userId = models.IntegerField(default=0,db_index=True)
    # 车牌号
    carNum = models.CharField(max_length=64,unique=True)
    # 车型（例如：奥迪Q7）
    carModel = models.CharField(max_length=512,null=True)
    # 图片jsonString结构[]
    adImgs = models.CharField(max_length=1024,null=True)
    remark = models.CharField(max_length=1024,null=True)


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


# 领取任务(一个任务，一个辆车只能领取一次)
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
    # 开始任务的时间
    startdoTaskTime = models.BigIntegerField(default=0)



# 做任务（至少两次，方才有效，动态扫描这个表，计算收入的流水）
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
    # 领取任务的ID
    getTask = models.IntegerField(default=0, db_index=True)
    createTime = models.BigIntegerField(default=0)
    # 收入的钱
    money = models.IntegerField(default=0)


# 支出流水
class outStream(models.Model):
    # 验证的用户信息
    userId = models.IntegerField(default=0, db_index=True)
    openId = models.CharField(max_length=64, db_index=True)
    # 领取任务的ID
    getTaskId = models.IntegerField(default=0, db_index=True)
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


