define({ "api": [  {    "type": "get",    "url": "check/AdminCheck",    "title": "审核",    "description": "<p>NONE</p>",    "version": "0.1.0",    "name": "wxReceiveTask",    "group": "Check",    "success": {      "fields": {        "Success 200": [          {            "group": "Success 200",            "type": "String",            "optional": false,            "field": "code",            "description": "<p>1</p>"          },          {            "group": "Success 200",            "type": "String",            "optional": false,            "field": "data",            "description": "<p>业务的ID</p>"          }        ]      }    },    "error": {      "fields": {        "Error 4xx": [          {            "group": "Error 4xx",            "optional": false,            "field": "code",            "description": "<p>0</p>"          }        ]      }    },    "filename": "example/check.js",    "groupTitle": "Check",    "sampleRequest": [      {        "url": "http://134.175.44.89/ctb/check/AdminCheck"      }    ]  },  {    "type": "get",    "url": "task/adminCreateTask",    "title": "[ok]创建任务",    "description": "<p>注意只有管理员的权限可以创建，创建后status=2公开可查询进行中</p>",    "version": "0.1.0",    "name": "adminCreateTask",    "group": "Task",    "parameter": {      "fields": {        "Parameter": [          {            "group": "Parameter",            "type": "String",            "optional": false,            "field": "openId",            "description": "<p>10000默认一个管理员</p>"          },          {            "group": "Parameter",            "type": "String",            "optional": false,            "field": "userId",            "description": "<p>管理员的ID</p>"          },          {            "group": "Parameter",            "type": "String",            "optional": false,            "field": "title",            "description": "<p>任务标题</p>"          },          {            "group": "Parameter",            "type": "String",            "optional": false,            "field": "info",            "description": "<p>详细描述信息</p>"          },          {            "group": "Parameter",            "type": "String",            "optional": false,            "field": "adImgs",            "description": "<p>图片[&quot;url&quot;:&quot;http://ss&quot;]</p>"          },          {            "group": "Parameter",            "type": "String",            "optional": false,            "field": "deadline",            "description": "<p>活动的截止时间</p>"          },          {            "group": "Parameter",            "type": "Int",            "optional": false,            "field": "stickerArea",            "description": "<p>贴纸的区域，0是后窗，1是车门两侧，2是全车，3是其它</p>"          },          {            "group": "Parameter",            "type": "Int",            "optional": false,            "field": "priceMonth",            "description": "<p>每月单价,最大值是10000</p>"          },          {            "group": "Parameter",            "type": "Int",            "optional": false,            "field": "limitNum",            "description": "<p>当前任务的限制车辆数</p>"          }        ]      }    },    "success": {      "fields": {        "Success 200": [          {            "group": "Success 200",            "type": "String",            "optional": false,            "field": "code",            "description": "<p>1</p>"          },          {            "group": "Success 200",            "type": "Int",            "optional": false,            "field": "data",            "description": "<p>ID</p>"          }        ]      }    },    "error": {      "fields": {        "Error 4xx": [          {            "group": "Error 4xx",            "optional": false,            "field": "code",            "description": "<p>0</p>"          }        ]      }    },    "filename": "example/taskInfo.js",    "groupTitle": "Task",    "sampleRequest": [      {        "url": "http://134.175.44.89/ctb/task/adminCreateTask"      }    ]  },  {    "type": "get",    "url": "task/adminDelTask",    "title": "[ok]删除任务",    "description": "<p>NONE</p>",    "version": "0.1.0",    "name": "adminDelTask",    "group": "Task",    "parameter": {      "fields": {        "Parameter": [          {            "group": "Parameter",            "type": "String",            "optional": false,            "field": "openId",            "description": "<p>10000默认一个管理员</p>"          },          {            "group": "Parameter",            "type": "String",            "optional": false,            "field": "userId",            "description": "<p>管理员的ID</p>"          },          {            "group": "Parameter",            "type": "String",            "optional": false,            "field": "taskId",            "description": "<p>任务的ID</p>"          }        ]      }    },    "success": {      "fields": {        "Success 200": [          {            "group": "Success 200",            "type": "String",            "optional": false,            "field": "code",            "description": "<p>1</p>"          }        ]      }    },    "error": {      "fields": {        "Error 4xx": [          {            "group": "Error 4xx",            "optional": false,            "field": "code",            "description": "<p>0</p>"          }        ]      }    },    "filename": "example/taskInfo.js",    "groupTitle": "Task",    "sampleRequest": [      {        "url": "http://134.175.44.89/ctb/task/adminDelTask"      }    ]  },  {    "type": "get",    "url": "task/wxGetALLTask",    "title": "[ok]微信获取开放的任务",    "description": "<p>NONE</p>",    "version": "0.1.0",    "name": "wxGetALLTask",    "group": "Task",    "parameter": {      "fields": {        "Parameter": [          {            "group": "Parameter",            "type": "String",            "optional": false,            "field": "openId",            "description": "<p>微信的ID</p>"          },          {            "group": "Parameter",            "type": "String",            "optional": false,            "field": "userId",            "description": "<p>用户的ID</p>"          }        ]      }    },    "success": {      "fields": {        "Success 200": [          {            "group": "Success 200",            "type": "String",            "optional": false,            "field": "code",            "description": "<p>1</p>"          },          {            "group": "Success 200",            "type": "List",            "optional": false,            "field": "data",            "description": "<p>数据</p>"          },          {            "group": "Success 200",            "type": "Int",            "optional": false,            "field": "id",            "description": "<p>任务的id</p>"          },          {            "group": "Success 200",            "type": "String",            "optional": false,            "field": "info",            "description": "<p>详细描述信息</p>"          },          {            "group": "Success 200",            "type": "Json",            "optional": false,            "field": "adImgs",            "description": "<p>图片[&quot;url&quot;:&quot;http://ss&quot;]</p>"          },          {            "group": "Success 200",            "type": "String",            "optional": false,            "field": "deadline",            "description": "<p>活动的截止时间</p>"          },          {            "group": "Success 200",            "type": "Int",            "optional": false,            "field": "stickerArea",            "description": "<p>贴纸的区域，0是后窗，1是车门两侧，2是全车，3是其它</p>"          },          {            "group": "Success 200",            "type": "Int",            "optional": false,            "field": "priceMonth",            "description": "<p>每月单价,最大值是10000</p>"          },          {            "group": "Success 200",            "type": "Int",            "optional": false,            "field": "limitNum",            "description": "<p>当前任务的限制车辆数</p>"          },          {            "group": "Success 200",            "type": "Int",            "optional": false,            "field": "collectionsNum",            "description": "<p>当前任务已领取数</p>"          },          {            "group": "Success 200",            "type": "Int",            "optional": false,            "field": "status",            "description": "<p>当前任务的状态，0是提交审核，1是审核通过，2是公开可查询进行中，3是已经领取完成，4是已截止，-1是已删除</p>"          },          {            "group": "Success 200",            "type": "String",            "optional": false,            "field": "remark",            "description": "<p>备注描述</p>"          },          {            "group": "Success 200",            "type": "Int",            "optional": false,            "field": "billingCycle",            "description": "<p>结算周期，单位是月</p>"          },          {            "group": "Success 200",            "type": "Int",            "optional": false,            "field": "activityRange",            "description": "<p>活动范围(默认为空，设计的点是：要求在用户活动范围，多少米以内，方可领取)，后期预留</p>"          },          {            "group": "Success 200",            "type": "Int",            "optional": false,            "field": "createTime",            "description": "<p>创建时间</p>"          }        ]      }    },    "error": {      "fields": {        "Error 4xx": [          {            "group": "Error 4xx",            "optional": false,            "field": "code",            "description": "<p>0</p>"          }        ]      }    },    "filename": "example/taskInfo.js",    "groupTitle": "Task",    "sampleRequest": [      {        "url": "http://134.175.44.89/ctb/task/wxGetALLTask"      }    ]  },  {    "type": "get",    "url": "task/adminGetALLTask",    "title": "[ok]管理员获取所有的任务",    "description": "<p>NONE</p>",    "version": "0.1.0",    "name": "wxGetALLTask",    "group": "Task",    "parameter": {      "fields": {        "Parameter": [          {            "group": "Parameter",            "type": "String",            "optional": false,            "field": "openId",            "description": "<p>管理员的openID</p>"          },          {            "group": "Parameter",            "type": "String",            "optional": false,            "field": "userId",            "description": "<p>用户的ID</p>"          },          {            "group": "Parameter",            "type": "Int",            "optional": false,            "field": "status",            "description": "<p>当前任务的状态，0是提交审核，1是审核通过，2是公开可查询进行中，3是已经领取完成，4是已截止，-1是已删除</p>"          }        ]      }    },    "success": {      "fields": {        "Success 200": [          {            "group": "Success 200",            "type": "String",            "optional": false,            "field": "code",            "description": "<p>1</p>"          },          {            "group": "Success 200",            "type": "List",            "optional": false,            "field": "data",            "description": "<p>数据</p>"          },          {            "group": "Success 200",            "type": "Int",            "optional": false,            "field": "id",            "description": "<p>任务的id</p>"          },          {            "group": "Success 200",            "type": "String",            "optional": false,            "field": "info",            "description": "<p>详细描述信息</p>"          },          {            "group": "Success 200",            "type": "Json",            "optional": false,            "field": "adImgs",            "description": "<p>图片[&quot;url&quot;:&quot;http://ss&quot;]</p>"          },          {            "group": "Success 200",            "type": "String",            "optional": false,            "field": "deadline",            "description": "<p>活动的截止时间</p>"          },          {            "group": "Success 200",            "type": "Int",            "optional": false,            "field": "stickerArea",            "description": "<p>贴纸的区域，0是后窗，1是车门两侧，2是全车，3是其它</p>"          },          {            "group": "Success 200",            "type": "Int",            "optional": false,            "field": "priceMonth",            "description": "<p>每月单价,最大值是10000</p>"          },          {            "group": "Success 200",            "type": "Int",            "optional": false,            "field": "limitNum",            "description": "<p>当前任务的限制车辆数</p>"          },          {            "group": "Success 200",            "type": "Int",            "optional": false,            "field": "collectionsNum",            "description": "<p>当前任务已领取数</p>"          },          {            "group": "Success 200",            "type": "Int",            "optional": false,            "field": "status",            "description": "<p>当前任务的状态，0是提交审核，1是审核通过，2是公开可查询进行中，3是已经领取完成，4是已截止，-1是已删除</p>"          },          {            "group": "Success 200",            "type": "String",            "optional": false,            "field": "remark",            "description": "<p>备注描述</p>"          },          {            "group": "Success 200",            "type": "Int",            "optional": false,            "field": "billingCycle",            "description": "<p>结算周期，单位是月</p>"          },          {            "group": "Success 200",            "type": "Int",            "optional": false,            "field": "activityRange",            "description": "<p>活动范围(默认为空，设计的点是：要求在用户活动范围，多少米以内，方可领取)，后期预留</p>"          },          {            "group": "Success 200",            "type": "Int",            "optional": false,            "field": "createTime",            "description": "<p>创建时间</p>"          }        ]      }    },    "error": {      "fields": {        "Error 4xx": [          {            "group": "Error 4xx",            "optional": false,            "field": "code",            "description": "<p>0</p>"          }        ]      }    },    "filename": "example/taskInfo.js",    "groupTitle": "Task",    "sampleRequest": [      {        "url": "http://134.175.44.89/ctb/task/adminGetALLTask"      }    ]  },  {    "type": "get",    "url": "task/wxGetJoinTask",    "title": "[ok]小程序登录后，获取自己的任务",    "description": "<p>微信用户每次打开小程序就调用一下</p>",    "version": "0.1.0",    "name": "wxGetJoinTask",    "group": "Task",    "parameter": {      "fields": {        "Parameter": [          {            "group": "Parameter",            "type": "String",            "optional": false,            "field": "openId",            "description": "<p>微信的ID</p>"          },          {            "group": "Parameter",            "type": "String",            "optional": false,            "field": "userId",            "description": "<p>用户的ID</p>"          }        ]      }    },    "success": {      "fields": {        "Success 200": [          {            "group": "Success 200",            "type": "String",            "optional": false,            "field": "code",            "description": "<p>1</p>"          },          {            "group": "Success 200",            "type": "List",            "optional": false,            "field": "data",            "description": "<p>数据列表</p>"          },          {            "group": "Success 200",            "type": "Int",            "optional": false,            "field": "id",            "description": "<p>用户的id</p>"          },          {            "group": "Success 200",            "type": "Int",            "optional": false,            "field": "carId",            "description": "<p>车辆ID</p>"          },          {            "group": "Success 200",            "type": "Int",            "optional": false,            "field": "taskId",            "description": "<p>任务的ID</p>"          },          {            "group": "Success 200",            "type": "String",            "optional": false,            "field": "createTime",            "description": "<p>创建的时间</p>"          },          {            "group": "Success 200",            "type": "String",            "optional": false,            "field": "startdoTaskTime",            "description": "<p>开始任务的时间</p>"          },          {            "group": "Success 200",            "type": "Int",            "optional": false,            "field": "status",            "description": "<p>当前任务的状态，0是提交审核，1是审核通过（正式开始计算领取任务的时间，进行中），2是审核失败，-1是已删除</p>"          },          {            "group": "Success 200",            "type": "Json",            "optional": false,            "field": "carInfo",            "description": "<p>车辆信息</p>"          },          {            "group": "Success 200",            "type": "Int",            "optional": false,            "field": "__id",            "description": "<p>carInfo用户的id</p>"          },          {            "group": "Success 200",            "type": "String",            "optional": false,            "field": "__carNum",            "description": "<p>carInfo车牌号</p>"          },          {            "group": "Success 200",            "type": "String",            "optional": false,            "field": "__carModel",            "description": "<p>carInfo车型（例如：奥迪Q7）</p>"          },          {            "group": "Success 200",            "type": "Json",            "optional": false,            "field": "__adImgs",            "description": "<p>carInfo车辆图片[{&quot;url&quot;:&quot;http://sss&quot;},{&quot;url&quot;:&quot;http://sss&quot;}]</p>"          },          {            "group": "Success 200",            "type": "String",            "optional": false,            "field": "_remark",            "description": "<p>carInfo备注信息</p>"          },          {            "group": "Success 200",            "type": "Json",            "optional": false,            "field": "taskInfo",            "description": "<p>任务信息</p>"          },          {            "group": "Success 200",            "type": "String",            "optional": false,            "field": "__info",            "description": "<p>taskInfo详细描述信息</p>"          },          {            "group": "Success 200",            "type": "String",            "optional": false,            "field": "__deadline",            "description": "<p>taskInfo活动的截止时间</p>"          },          {            "group": "Success 200",            "type": "Int",            "optional": false,            "field": "__stickerArea",            "description": "<p>taskInfo贴纸的区域，0是后窗，1是车门两侧，2是全车，3是其它</p>"          },          {            "group": "Success 200",            "type": "Int",            "optional": false,            "field": "__priceMonth",            "description": "<p>taskInfo每月单价,最大值是10000</p>"          },          {            "group": "Success 200",            "type": "Int",            "optional": false,            "field": "__limitNum",            "description": "<p>taskInfo当前任务的限制车辆数</p>"          },          {            "group": "Success 200",            "type": "Int",            "optional": false,            "field": "__collectionsNum",            "description": "<p>taskInfo当前任务已领取数</p>"          },          {            "group": "Success 200",            "type": "Int",            "optional": false,            "field": "__status",            "description": "<p>taskInfo当前任务的状态，0是提交审核，1是审核通过，2是公开可查询进行中，3是已经领取完成，4是已截止，-1是已删除</p>"          },          {            "group": "Success 200",            "type": "String",            "optional": false,            "field": "__remark",            "description": "<p>taskInfo备注描述</p>"          },          {            "group": "Success 200",            "type": "Int",            "optional": false,            "field": "__billingCycle",            "description": "<p>taskInfo结算周期，单位是月</p>"          },          {            "group": "Success 200",            "type": "Int",            "optional": false,            "field": "__activityRange",            "description": "<p>taskInfo活动范围(默认为空，设计的点是：要求在用户活动范围，多少米以内，方可领取)，后期预留</p>"          },          {            "group": "Success 200",            "type": "Int",            "optional": false,            "field": "__createTime",            "description": "<p>taskInfo创建时间</p>"          }        ]      }    },    "error": {      "fields": {        "Error 4xx": [          {            "group": "Error 4xx",            "optional": false,            "field": "code",            "description": "<p>0</p>"          }        ]      }    },    "filename": "example/taskInfo.js",    "groupTitle": "Task",    "sampleRequest": [      {        "url": "http://134.175.44.89/ctb/task/wxGetJoinTask"      }    ]  },  {    "type": "get",    "url": "task/wxReceiveTask",    "title": "[ok]领取任务",    "description": "<p>NONE</p>",    "version": "0.1.0",    "name": "wxReceiveTask",    "group": "Task",    "parameter": {      "fields": {        "Parameter": [          {            "group": "Parameter",            "type": "String",            "optional": false,            "field": "openId",            "description": "<p>微信的ID</p>"          },          {            "group": "Parameter",            "type": "String",            "optional": false,            "field": "userId",            "description": "<p>用户的ID</p>"          },          {            "group": "Parameter",            "type": "Int",            "optional": false,            "field": "taskId",            "description": "<p>任务的ID</p>"          },          {            "group": "Parameter",            "type": "Int",            "optional": false,            "field": "carId",            "description": "<p>车辆的ID</p>"          }        ]      }    },    "success": {      "fields": {        "Success 200": [          {            "group": "Success 200",            "type": "String",            "optional": false,            "field": "code",            "description": "<p>1</p>"          },          {            "group": "Success 200",            "type": "String",            "optional": false,            "field": "data",            "description": "<p>业务的ID</p>"          }        ]      }    },    "error": {      "fields": {        "Error 4xx": [          {            "group": "Error 4xx",            "optional": false,            "field": "code",            "description": "<p>0</p>"          }        ]      }    },    "filename": "example/taskInfo.js",    "groupTitle": "Task",    "sampleRequest": [      {        "url": "http://134.175.44.89/ctb/task/wxReceiveTask"      }    ]  },  {    "type": "get",    "url": "task/wxdoTask",    "title": "[ok]做任务",    "description": "<p>NONE</p>",    "version": "0.1.0",    "name": "wxdoTask",    "group": "Task",    "parameter": {      "fields": {        "Parameter": [          {            "group": "Parameter",            "type": "String",            "optional": false,            "field": "openId",            "description": "<p>微信的ID</p>"          },          {            "group": "Parameter",            "type": "String",            "optional": false,            "field": "userId",            "description": "<p>用户的ID</p>"          },          {            "group": "Parameter",            "type": "Int",            "optional": false,            "field": "getTaskId",            "description": "<p>用户领取的任务的ID</p>"          },          {            "group": "Parameter",            "type": "String",            "optional": false,            "field": "adImgs",            "description": "<p>图片数组</p>"          },          {            "group": "Parameter",            "type": "Double",            "optional": false,            "field": "latitude",            "description": "<p>经度(可以为空)</p>"          },          {            "group": "Parameter",            "type": "Double",            "optional": false,            "field": "longitude",            "description": "<p>经度(可以为空)</p>"          }        ]      }    },    "success": {      "fields": {        "Success 200": [          {            "group": "Success 200",            "type": "String",            "optional": false,            "field": "code",            "description": "<p>1</p>"          },          {            "group": "Success 200",            "type": "String",            "optional": false,            "field": "data",            "description": "<p>业务的ID</p>"          }        ]      }    },    "error": {      "fields": {        "Error 4xx": [          {            "group": "Error 4xx",            "optional": false,            "field": "code",            "description": "<p>0</p>"          }        ]      }    },    "filename": "example/taskInfo.js",    "groupTitle": "Task",    "sampleRequest": [      {        "url": "http://134.175.44.89/ctb/task/wxdoTask"      }    ]  },  {    "type": "get",    "url": "user/wxAddCar",    "title": "[ok]用户添加车辆",    "description": "<p>None</p>",    "version": "0.1.0",    "name": "wxAddCar",    "group": "User",    "parameter": {      "fields": {        "Parameter": [          {            "group": "Parameter",            "type": "String",            "optional": false,            "field": "openId",            "description": "<p>微信的ID</p>"          },          {            "group": "Parameter",            "type": "Int",            "optional": false,            "field": "userId",            "description": "<p>用户的ID</p>"          },          {            "group": "Parameter",            "type": "String",            "optional": false,            "field": "carNum",            "description": "<p>车牌号</p>"          },          {            "group": "Parameter",            "type": "String",            "optional": false,            "field": "carModel",            "description": "<p>[null]车型（例如：奥迪Q7）</p>"          },          {            "group": "Parameter",            "type": "String",            "optional": false,            "field": "adImgs",            "description": "<p>车辆图片[{&quot;url&quot;:&quot;http://sss&quot;},{&quot;url&quot;:&quot;http://sss&quot;}]</p>"          },          {            "group": "Parameter",            "type": "String",            "optional": false,            "field": "remark",            "description": "<p>[null]备注描述</p>"          }        ]      }    },    "success": {      "fields": {        "Success 200": [          {            "group": "Success 200",            "type": "String",            "optional": false,            "field": "code",            "description": "<p>1</p>"          },          {            "group": "Success 200",            "type": "String",            "optional": false,            "field": "data",            "description": "<p>id  添加车辆的编号</p>"          }        ]      }    },    "error": {      "fields": {        "Error 4xx": [          {            "group": "Error 4xx",            "optional": false,            "field": "code",            "description": "<p>0</p>"          },          {            "group": "Error 4xx",            "optional": false,            "field": "msg",            "description": "<p>系统异常</p>"          }        ]      }    },    "filename": "example/user.js",    "groupTitle": "User",    "sampleRequest": [      {        "url": "http://134.175.44.89/ctb/user/wxAddCar"      }    ]  },  {    "type": "get",    "url": "user/wxEditCar",    "title": "[ok]编辑车辆信息",    "description": "<p>None</p>",    "version": "0.1.0",    "name": "wxEditCar",    "group": "User",    "parameter": {      "fields": {        "Parameter": [          {            "group": "Parameter",            "type": "String",            "optional": false,            "field": "openId",            "description": "<p>微信的ID</p>"          },          {            "group": "Parameter",            "type": "Int",            "optional": false,            "field": "userId",            "description": "<p>用户的ID</p>"          },          {            "group": "Parameter",            "type": "Int",            "optional": false,            "field": "carId",            "description": "<p>车辆的ID</p>"          },          {            "group": "Parameter",            "type": "String",            "optional": false,            "field": "carNum",            "description": "<p>车牌号</p>"          },          {            "group": "Parameter",            "type": "String",            "optional": false,            "field": "carModel",            "description": "<p>[null]车型（例如：奥迪Q7）</p>"          },          {            "group": "Parameter",            "type": "String",            "optional": false,            "field": "adImgs",            "description": "<p>车辆图片[{&quot;url&quot;:&quot;http://sss&quot;},{&quot;url&quot;:&quot;http://sss&quot;}]</p>"          },          {            "group": "Parameter",            "type": "String",            "optional": false,            "field": "remark",            "description": "<p>[null]备注描述</p>"          }        ]      }    },    "success": {      "fields": {        "Success 200": [          {            "group": "Success 200",            "type": "String",            "optional": false,            "field": "code",            "description": "<p>1</p>"          },          {            "group": "Success 200",            "type": "String",            "optional": false,            "field": "msg",            "description": "<p>编辑成功</p>"          }        ]      }    },    "error": {      "fields": {        "Error 4xx": [          {            "group": "Error 4xx",            "optional": false,            "field": "code",            "description": "<p>0</p>"          },          {            "group": "Error 4xx",            "optional": false,            "field": "msg",            "description": "<p>系统异常</p>"          }        ]      }    },    "filename": "example/user.js",    "groupTitle": "User",    "sampleRequest": [      {        "url": "http://134.175.44.89/ctb/user/wxEditCar"      }    ]  },  {    "type": "get",    "url": "user/wxegisterSign",    "title": "[ok]小程序登录注册",    "description": "<p>微信用户每次打开小程序就调用一下</p>",    "version": "0.1.0",    "name": "wxegisterSign",    "group": "User",    "parameter": {      "fields": {        "Parameter": [          {            "group": "Parameter",            "type": "String",            "optional": false,            "field": "openId",            "description": "<p>微信的ID</p>"          }        ]      }    },    "success": {      "fields": {        "Success 200": [          {            "group": "Success 200",            "type": "String",            "optional": false,            "field": "code",            "description": "<p>1</p>"          },          {            "group": "Success 200",            "type": "Int",            "optional": false,            "field": "id",            "description": "<p>用户的id</p>"          }        ]      }    },    "error": {      "fields": {        "Error 4xx": [          {            "group": "Error 4xx",            "optional": false,            "field": "code",            "description": "<p>0</p>"          },          {            "group": "Error 4xx",            "optional": false,            "field": "msg",            "description": "<p>系统异常</p>"          }        ]      }    },    "filename": "example/user.js",    "groupTitle": "User",    "sampleRequest": [      {        "url": "http://134.175.44.89/ctb/user/wxegisterSign"      }    ]  },  {    "type": "get",    "url": "user/wxgetCarList",    "title": "[ok]用户车辆列表",    "description": "<p>None</p>",    "version": "0.1.0",    "name": "wxegisterSign",    "group": "User",    "parameter": {      "fields": {        "Parameter": [          {            "group": "Parameter",            "type": "String",            "optional": false,            "field": "openId",            "description": "<p>微信的ID</p>"          },          {            "group": "Parameter",            "type": "Int",            "optional": false,            "field": "userId",            "description": "<p>用户的ID</p>"          }        ]      }    },    "success": {      "fields": {        "Success 200": [          {            "group": "Success 200",            "type": "String",            "optional": false,            "field": "code",            "description": "<p>1</p>"          },          {            "group": "Success 200",            "type": "List",            "optional": false,            "field": "data",            "description": "<p>数据列表</p>"          },          {            "group": "Success 200",            "type": "Int",            "optional": false,            "field": "id",            "description": "<p>用户的id</p>"          },          {            "group": "Success 200",            "type": "String",            "optional": false,            "field": "carNum",            "description": "<p>车牌号</p>"          },          {            "group": "Success 200",            "type": "String",            "optional": false,            "field": "carModel",            "description": "<p>车型（例如：奥迪Q7）</p>"          },          {            "group": "Success 200",            "type": "Json",            "optional": false,            "field": "adImgs",            "description": "<p>车辆图片[{&quot;url&quot;:&quot;http://sss&quot;},{&quot;url&quot;:&quot;http://sss&quot;}]</p>"          },          {            "group": "Success 200",            "type": "String",            "optional": false,            "field": "remark",            "description": "<p>备注信息</p>"          }        ]      }    },    "error": {      "fields": {        "Error 4xx": [          {            "group": "Error 4xx",            "optional": false,            "field": "code",            "description": "<p>0</p>"          },          {            "group": "Error 4xx",            "optional": false,            "field": "msg",            "description": "<p>系统异常</p>"          }        ]      }    },    "filename": "example/user.js",    "groupTitle": "User",    "sampleRequest": [      {        "url": "http://134.175.44.89/ctb/user/wxgetCarList"      }    ]  }] });
