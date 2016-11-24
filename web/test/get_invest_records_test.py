# -*- coding: utf-8 -*-

import requests
import urllib

url = "http://127.0.0.1:8000/api/flt/get_invest_records/"

querystring = {"start_time": "2015-10-10",
               "end_time": "2015-10-11",
               "t": "1440328485",
               "sign": "7d20243c5443fb468248146bf0cc7554",
               }

payload = urllib.urlencode(querystring)
headers = {
    'content-type': "application/x-www-form-urlencoded",
    }

response = requests.request("GET", url, data=payload, headers=headers, params=querystring)

print(response.text)

print "%s?%s" % (url, payload)
