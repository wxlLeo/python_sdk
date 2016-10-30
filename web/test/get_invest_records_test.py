# -*- coding: utf-8 -*-

import requests

url = "http://127.0.0.1:8000/api/flt/get_invest_records/"

querystring = {"fcode":"fanlitou","start_time":"2015-10-10","end_time":"2015-10-11","t":"1477839611","sign":"13b71f00db7e5c4e1d88feaa638244f7"}

payload = "phone_num=69a658b08a6035fe80ea53867a57d1a3&t=76a02352de0abdf1e3a55ff0a1f68cf3&serial_num=1&uid=69a658b08a6035fe80ea53867a57d1a3&sign=1fbc415e3cf13ee3683bd223dd7af4dd&fcode=fanlitou&register_token=69a658b08a6035fe80ea53867a57d1a3"
headers = {
    'content-type': "application/x-www-form-urlencoded",
    }

response = requests.request("GET", url, data=payload, headers=headers, params=querystring)

print(response.text)
