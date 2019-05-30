# -*- coding: utf-8 -*-

import json
import urllib2

aa()

def aa():
    try:
        res = urllib2.urlopen("http://appid.985-985.com:8088/getAppConfig.php?appid=chenspeed1", timeout=5)
        page_source = res.read().decode('utf-8')
        decode_json = json.loads(page_source)
        print(page_source)
        print(decode_json)
        mySkipUrl = decode_json['Url']
        print(mySkipUrl)
    except BaseException as e:
        print(str(e))

