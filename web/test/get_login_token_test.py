# -*- coding: utf-8 -*-

import requests

url = "http://127.0.0.1:8000/api/flt/get_login_token/"

payload = "t=76a02352de0abdf1e3a55ff0a1f68cf3&uid=69a658b08a6035fe80ea53867a57d1a3&sign=e7d0e96c832fd0cce6411e30f7b59539298661476e4f5a568ca8109b9bb77e09e50c93b6ea3da5d0f1db221a7413a867&fcode=6fbfe5dcfe16dd71500d2e638b794a45&register_token=76dba37c568cbfcd9c4324be48d241c85b2f5605007b8a20060d6c261d61069082671e512873b3c1490e441a15c6e49a"
headers = {
    'content-type': "application/x-www-form-urlencoded",
    }

response = requests.request("POST", url, data=payload, headers=headers)

print(response.text)
