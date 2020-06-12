# coding=utf-8
import codecs
import os
import requests
import urllib.error
import urllib.parse
import urllib.request
import time

from bs4 import BeautifulSoup


def csisc():
    url = 'http://www.csisc.cn/fund-webapp/fundCode/Search_search.action'
    html = requests.get(url, verify=False);

    soup = BeautifulSoup(html.content, 'lxml')
    csiscs = soup.select('#list_form')[0].select('table')[1].select('tr')
    for csisc in csiscs:
        print(csisc.select('td')[0].text)


def eastmoney(code):
    site = 'http://fund.eastmoney.com/' + code + '.html?spm=search'
    html = urllib.request.urlopen(site)
    soup = BeautifulSoup(html, 'html.parser')
    print(code)
    # 获取基金名称
    name = \
        soup.select('.wrapper')[8].select('.wrapper_min')[0].select('.merchandiseDetail')[0].select(
            '.fundDetail-header')[
            0].select('.fundDetail-tit')[0].select('div')[0].text
    name = '('.join(name.split('(')[:1])
    if code != '000001':
        fo.write(',')
    fo.write('{\'code\':\'' + code + '\',\'name\':\'' + name + '\'' + '}')


# 先获取原文件中内容
content = ''
with open('codes.txt', encoding='utf-8', mode='r') as f:
    try:
        content = f.read()
    except:
        pass
    f.close()

fo = open('codes.txt', encoding='utf-8', mode='w+')
if content == '':
    fo.write('[')
else:
    fo.write(content.replace(']', ''))

name = []
code = '';
for i in range(3729, 5000):
    if len(str(i)) == 1:
        code = '00000' + str(i)
    elif len(str(i)) == 2:
        code = '0000' + str(i)
    elif len(str(i)) == 3:
        code = '000' + str(i)
    elif len(str(i)) == 4:
        code = '00' + str(i)
    if content.__contains__(code):
        print(code + '已存在')
        continue
    print(code)
    # 获取基金名称
    try:
        site = 'http://fund.eastmoney.com/' + code + '.html?spm=search'
        html = urllib.request.urlopen(site)
        soup = BeautifulSoup(html, 'html.parser')
        name = \
            soup.select('.wrapper')[8].select('.wrapper_min')[0].select('.merchandiseDetail')[0].select(
                '.fundDetail-header')[
                0].select('.fundDetail-tit')[0].select('div')[0].text
        name = '('.join(name.split('(')[:1])
        if code != '000001':
            fo.write(',')
        fo.write('{\'code\':\'' + code + '\',\'name\':\'' + name + '\'' + '}')
        fo.flush()
        time.sleep(1)
    except:
        continue
fo.write(']')
fo.close()
