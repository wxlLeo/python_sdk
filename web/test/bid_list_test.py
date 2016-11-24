# -*- coding: utf-8 -*-

import requests
import urllib

url = "http://127.0.0.1:8000/api/flt/get_bid_list/"

querystring = {"pageCount": 10,
               "pageIndex": 1,
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
