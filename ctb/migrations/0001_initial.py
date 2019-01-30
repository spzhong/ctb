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
                ('startdoTaskTime', models.BigIntegerField(default=0)),
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
                ('getTaskId', models.IntegerField(default=0, db_index=True)),
                ('createTime', models.BigIntegerField(default=0)),
                ('money', models.IntegerField(default=0)),
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
                ('getTaskId', models.IntegerField(default=0, db_index=True)),
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
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
