# coding=utf-8
import urllib.error
import urllib.parse
import urllib.request

from bs4 import BeautifulSoup

content='12121213121212'
if content.__contains__('14'):
    print('已存在')