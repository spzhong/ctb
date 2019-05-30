# -*- coding: utf-8 -*-

import json
import urllib2


def aa():
    try:
        request = urllib2.Request("http://appid.985-985.com:8088/getAppConfig.php?appid=chenspeed1",timeout=5)
        request.add_header('User-Agent', 'fake-client')
        res = urllib2.urlopen(request)
        page_source = res.read().decode('utf-8')
        decode_json = json.loads(page_source)
        print(page_source)
        print(decode_json)
        mySkipUrl = decode_json['Url']
        print(mySkipUrl)
    except BaseException as e:
        print(str(e))


aa()