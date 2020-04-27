#coding:utf-8
import urllib.request, urllib.error, urllib.parse
import urllib.request, urllib.parse, urllib.error
import http.cookiejar
from bs4 import BeautifulSoup
posturl = 'https://www.zhihu.com/login/phone_num'
headers={
    'User-Agent':'user-agent: Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
    'Referer':'https://www.zhihu.com/signin?next=%2Fsearch'
}
value = {
    'password':'zhihu1877091',
    'remember_me':True,
    'phone_num':'187709179652',
    '_xsrf':'sXcKbW7DyRdCy9O0rWhGq6bn0PHPCmXf'
}
data=urllib.parse.urlencode(value)
#初始化一个CookieJar来处理Cookie
cookieJar=http.cookiejar.CookieJar()
cookie_support = urllib.request.HTTPCookieProcessor(cookieJar)
#实例化一个全局opener
opener=urllib.request.build_opener(cookie_support)
request = urllib.request.Request(posturl, data, headers)
result=opener.open(request)
# page=opener.open(r'https://www.zhihu.com/search?type=content&q=licai'.encode())
# content = page.read().decode('utf-8')

html = urllib.request.urlopen(r'https://www.zhihu.com/search?type=content&q=licai'.encode())
soup = BeautifulSoup(html, 'lxml')
div = soup.findAll('div', class_='List-item')
for i in div:
    print(i)


# name = scrapy.Field()
# url = scrapy.Field()
# keywords = scrapy.Field()
# answer_count = scrapy.Field()
# comment_count = scrapy.Field()
# flower_count = scrapy.Field()
# date_created = scrapy.Field()




# print result.read()