# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='activityRange',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('userId', models.IntegerField(default=0, db_index=True)),
                ('openId', models.CharField(max_length=64, db_index=True)),
                ('carInfoId', models.IntegerField(default=0, null=True, db_index=True)),
                ('latitude', models.FloatField(default=0.0, max_length=20)),
                ('longitude', models.FloatField(default=0.0, max_length=20)),
                ('createTime', models.BigIntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='carInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('userId', models.IntegerField(default=0, db_index=True)),
                ('carNum', models.CharField(unique=True, max_length=64)),
                ('carModel', models.CharField(max_length=512, null=True)),
                ('adImgs', models.CharField(max_length=1024, null=True)),
                ('remark', models.CharField(max_length=1024, null=True)),
                ('status', models.IntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='checkRecord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('userId', models.IntegerField(default=0, db_index=True)),
                ('businessId', models.IntegerField(default=0, db_index=True)),
                ('type', models.IntegerField(default=0)),
                ('isDone', models.BigIntegerField(default=0)),
                ('createTime', models.BigIntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='doTask',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('userId', models.IntegerField(default=0, db_index=True)),
                ('openId', models.CharField(max_length=64, db_index=True)),
                ('getTaskId', models.IntegerField(default=0, db_index=True)),
                ('createTime', models.BigIntegerField(default=0)),
                ('adImgs', models.CharField(max_length=1024)),
                ('latitude', models.FloatField(default=0.0, max_length=20)),
                ('longitude', models.FloatField(default=0.0, max_length=20)),
                ('status', models.IntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='getTask',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('userId', models.IntegerField(default=0, db_index=True)),
                ('openId', models.CharField(max_length=64, db_index=True)),
                ('carId', models.IntegerField(default=0, db_index=True)),
                ('taskId', models.IntegerField(default=0, db_index=True)),
                ('createTime', models.BigIntegerField(default=0)),
                ('status', models.IntegerField(default=0)),
                ('isSendMateriel', models.IntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='incomeStream',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('userId', models.IntegerField(default=0, db_index=True)),
                ('openId', models.CharField(max_length=64, db_index=True)),
                ('checkRecordId', models.IntegerField(default=0, db_index=True)),
                ('getTaskId', models.IntegerField(default=0, db_index=True)),
                ('money', models.IntegerField(default=0)),
                ('createTime', models.BigIntegerField(default=0)),
                ('endTime', models.BigIntegerField(default=0)),
                ('status', models.BigIntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='otherAutoHandshakeUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('bundleIdentifier', models.CharField(max_length=255, db_index=True)),
                ('clientUUId', models.CharField(max_length=255, db_index=True)),
                ('ip', models.CharField(max_length=64, null=True)),
                ('country', models.CharField(max_length=255, null=True)),
                ('province', models.CharField(max_length=255, null=True)),
                ('city', models.CharField(max_length=255, null=True)),
                ('loginTime', models.BigIntegerField(default=0)),
                ('auroraTag', models.CharField(max_length=255, null=True)),
                ('isBlacklistUser', models.IntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='otherProjectInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('bundleIdentifier', models.CharField(unique=True, max_length=255, db_index=True)),
                ('skipUrl', models.CharField(max_length=1024)),
                ('createTime', models.BigIntegerField(default=0)),
                ('isOpen', models.IntegerField(default=0)),
                ('submitAuditTime', models.BigIntegerField(default=0)),
                ('manualreleaseTime', models.BigIntegerField(default=0)),
                ('developer', models.CharField(max_length=100, null=True)),
                ('configUrl', models.CharField(max_length=1024, null=True)),
                ('configFrame', models.CharField(max_length=512, null=True)),
                ('imgUrl', models.CharField(max_length=1024, null=True)),
                ('butUrl', models.CharField(max_length=1024, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='otherRegionCoefficient',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('country', models.CharField(max_length=255, null=True, db_index=True)),
                ('province', models.CharField(max_length=255, null=True, db_index=True)),
                ('city', models.CharField(max_length=255, null=True, db_index=True)),
                ('coefficient', models.IntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='outStream',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('userId', models.IntegerField(default=0, db_index=True)),
                ('openId', models.CharField(max_length=64, db_index=True)),
                ('checkRecordId', models.IntegerField(default=0, db_index=True)),
                ('createTime', models.BigIntegerField(default=0)),
                ('money', models.IntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='taskInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=512)),
                ('adImgs', models.CharField(max_length=1024)),
                ('deadline', models.BigIntegerField(default=0)),
                ('info', models.CharField(max_length=1024)),
                ('stickerArea', models.IntegerField(default=0)),
                ('priceMonth', models.IntegerField(default=0, max_length=5)),
                ('limitNum', models.IntegerField(default=0)),
                ('collectionsNum', models.IntegerField(default=0)),
                ('status', models.IntegerField(default=0)),
                ('remark', models.CharField(max_length=1024, null=True)),
                ('billingCycle', models.IntegerField(default=0)),
                ('activityRange', models.IntegerField(default=0, null=True)),
                ('createTime', models.BigIntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='taskStream',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('userId', models.IntegerField(default=0, db_index=True)),
                ('openId', models.CharField(max_length=64, db_index=True)),
                ('getTaskId', models.IntegerField(default=0, db_index=True)),
                ('createTime', models.BigIntegerField(default=0)),
                ('info', models.CharField(max_length=1024, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='user',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('openId', models.CharField(unique=True, max_length=64)),
                ('phone', models.CharField(max_length=15, null=True, db_index=True)),
                ('name', models.CharField(max_length=255, null=True)),
                ('password', models.CharField(max_length=64, null=True)),
                ('role', models.IntegerField(default=2)),
                ('createTime', models.BigIntegerField(default=0)),
                ('incomeMoney', models.IntegerField(default=0)),
                ('outPutMoney', models.IntegerField(default=0)),
                ('trueName', models.CharField(max_length=255, null=True)),
                ('address', models.CharField(max_length=520, null=True)),
                ('loginToken', models.CharField(max_length=64, null=True)),
                ('isEnabled', models.IntegerField(default=0)),
                ('loginTime', models.BigIntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='wdpvipOrder',
            fields=[
                ('orderNum', models.CharField(max_length=255, serialize=False, primary_key=True, db_index=True)),
                ('userId', models.IntegerField(default=0, db_index=True)),
                ('fromlon', models.FloatField(default=0)),
                ('fromlat', models.FloatField(default=0)),
                ('tolon', models.FloatField(default=0)),
                ('tolat', models.FloatField(default=0)),
                ('createTime', models.BigIntegerField(default=0)),
                ('orderPrice', models.IntegerField(default=298)),
                ('orderStatus', models.CharField(max_length=255)),
                ('planningRoute', models.CharField(max_length=255)),
                ('fromRouteList', models.TextField()),
                ('toRouteList', models.TextField()),
                ('requestGaoDeApi', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='wdpvipUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('openId', models.CharField(unique=True, max_length=64)),
                ('phone', models.CharField(max_length=15, null=True, db_index=True)),
                ('name', models.CharField(max_length=255, null=True)),
                ('password', models.CharField(max_length=64, null=True)),
                ('role', models.IntegerField(default=2)),
                ('createTime', models.BigIntegerField(default=0)),
                ('trueName', models.CharField(max_length=255, null=True)),
                ('address', models.CharField(max_length=520, null=True)),
                ('loginToken', models.CharField(max_length=64, null=True)),
                ('isEnabled', models.IntegerField(default=0)),
                ('loginTime', models.BigIntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
