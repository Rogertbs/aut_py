#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests, json

URL = 'http://app.com.br:8080/message/sendText/evounifytalk'
HEADERS = {
        'apikey': 'key',
        'Content-Type': 'application/json'
        }


data = {
    "number": "5516999999999",
    "options": {
        "delay": 3000,
        "presence": "composing"
    },
    "textMessage": {
        "text": "MSG"
    }
}

data = json.dumps(data)

try:
    print(f"Send Message Simulate!!!")
    response = requests.post(URL, headers=HEADERS, data=data)
    print(response.json())
except Exception as e:
    print("_httpexecute returned Unknown Error: {}".format(str(e)))
