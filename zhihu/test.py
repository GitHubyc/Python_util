#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
"""
 @author 金全 JQ
 @version 1.0 , 2017/10/25
 @description 模拟知乎登陆
"""

import requests
import re

try:
    import http.cookiejar
except:
    import http.cookiejar as cookielib

import time
try:
    from PIL import Image
except:
    pass
import os

session = requests.session()
session.cookies = http.cookiejar.LWPCookieJar(filename="cookies.txt")

try:
    session.cookies.load(ignore_discard=True)
except:
    print("cookie加载异常")

agent = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.91 Safari/537.36"
header = {
    "HOST":"www.zhihu.com",
    "Referer":"https://www.zhihu.com",
    "User-Agent":agent
}


#获取xsrf
def get_xsrf():
    response = session.get("https://www.zhihu.com",headers= header)
    print((response.text))
    match_obj = re.findall(r'name="_xsrf" value="(.*?)"', response.text)
    if match_obj:
        return match_obj[0]
    else:
        return ""


def is_login():
    #通过个人中心判断是否为登陆状态
    inbox_url = 'http://www.zhihu.com/inbox'
    response = session.get(inbox_url,headers= header,allow_redirects=False)
    if response.status_code !=200:
        return False
    else:
        return True



def get_captcha():
    # 获取验证码
    t = str(int(time.time()*1000))
    captcha_url = 'http://www.zhihu.com/captcha.gif?r='+t+"&type=login"
    r = session.get(captcha_url,headers = header)
    with open('captcha.jpg','wb') as f :
        f.write(r.content)
        f.close()
    try:
        im = Image.open('captcha.jpg')
        im.show()
        im.close()
    except:
        print(('请到%s目录下找到captch.jpg 手动输入' %os.path.abspath('captcha.jpg')))
    captcha = eval(input('capture:'))
    return captcha


def get_index():
    response = session.get("https://www.zhihu.com/search?type=content&q=基金", headers=header)
    with open("page_index.html","wb") as f:
        f.write(response.text.encode("utf-8"))
    print("ok")


def zhihu_login(account,password):
    # 知乎手机号登陆
    match_phone = re.match("^1\d{10}$",account)
    if match_phone:
        print("手机号登陆")
        post_number = "https://www.zhihu.com/login/phone_num"
        post_data = {
            "_xsrf": get_xsrf(),
            "phone_num": account,
            "captcha":get_captcha(),
            "password":password
        }
    else:
        if "@" in account:
            print("邮箱登陆")
            post_number = "https://www.zhihu.com/login/email"
            post_data = {
                "_xsrf": get_xsrf(),
                "email": account,
                "captcha": get_captcha(),
                "password": password
            }

    response_text = session.post(post_number, data=post_data, headers=header)
    session.cookies.save()




zhihu_login("18770917652","zhihu1877091")
get_index()