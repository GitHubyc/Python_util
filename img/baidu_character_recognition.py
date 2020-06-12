# encoding:utf-8
import requests
import json
import base64

import difflib


# 百度文字识别 返回识别出的文字集合
def result(img):
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=51ntFe2CokOIA5l1LcXq3KHS&client_secret=D2uOXGKu7Cc9G9Kgh4N8HGGiGMiiakoN'
    response = requests.get(host)
    if response:
        request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic"
        f = open(img, 'rb')
        img = base64.b64encode(f.read())
        params = {"image": img}
        access_token = json.loads(response.text).get("access_token")
        request_url = request_url + "?access_token=" + access_token
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        response = requests.post(request_url, data=params, headers=headers)
        if response:
            return response.json().get('words_result')
    return []


# 遍历替换集合内容为匹配度更高的百度识别内容
def ratio(strs):
    words = result('abc.jpg')
    for str in strs:
        quick_ratio = 0
        quick_word = str
        for word in words:
            new_quick_ratio = difflib.SequenceMatcher(None, str, word.get('words')).quick_ratio()
            if new_quick_ratio > quick_ratio:
                quick_ratio = new_quick_ratio
                quick_word = word.get('words')
        print(quick_word)
