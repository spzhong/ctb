# -*- coding: utf-8 -*-

import json
import urllib.request

import schedule
import time

def job():
    f = urllib.request.urlopen('http://appid.985-985.com:8088/getAppConfig.php?appid=chenspeed2')
    print(f.read().decode('utf-8'))
    # 根据打印的信息
    # 调用我们自己的接口

# 定时任务1分钟，取得一下数据
schedule.every(0.1).minutes.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)

