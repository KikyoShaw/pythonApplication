# -*- coding: utf-8 -*-

__author__ = 'fff_zrx'

import requests

import base64

# 获取access_token

# client_id 为官网获取的AK， client_secret 为官网获取的SK

host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=your ak&client_secret=your sk'

header = {'Content-Type': 'application/json; charset=UTF-8'}

response1 = requests.post(url=host, headers=header)  # <class 'requests.models.Response'>

json1 = response1.json()  # <class 'dict'>

access_token = json1['access_token']

# 转换图片格式

filepath = 'zrx.jpg'

f = open(r'%s' % filepath, 'rb')

pic = base64.b64encode(f.read())

f.close()

base64 = str(pic, 'utf-8')

print(base64)

# 访问人脸检测api

request_url = "https://aip.baidubce.com/rest/2.0/face/v3/detect"

params = {"image": base64, "image_type": "BASE64", "face_field": "faceshape,facetype,beauty,"}

header = {'Content-Type': 'application/json'}

request_url = request_url + "?access_token=" + access_token

response1 = requests.post(url=request_url, data=params, headers=header)  # <class 'requests.models.Response'>

json1 = response1.json()  # <class 'dict'>

print(json1)

print("颜值评分为")

print(json1["result"]["face_list"][0]['beauty'], '分/100分')