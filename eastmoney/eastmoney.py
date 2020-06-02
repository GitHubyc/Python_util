# coding=utf-8
import urllib.request, urllib.parse, urllib.error
import _thread
import re
import requests
from time import ctime
from bs4 import BeautifulSoup

sum = 0;


def getMoney(code, money):
    site = 'http://fund.eastmoney.com/' + code + '.html?spm=search'
    html = urllib.request.urlopen(site)
    soup = BeautifulSoup(html, 'html.parser')

    # 获取基金名称
    name = \
        soup.select('.wrapper')[8].select('.wrapper_min')[0].select('.merchandiseDetail')[0].select(
            '.fundDetail-header')[
            0].select('.fundDetail-tit')[0].select('div')[0].text
    name = '('.join(name.split('(')[:1])
    # 获取基金统计区域
    item = \
        soup.select('.wrapper')[8].select('.wrapper_min')[0].select('.merchandiseDetail')[0].select('.fundDetail-main')[
            0].select('.fundInfoItem')[0]
    # 预测涨跌幅
    add = item.select('.dataOfFund')[0].select('.dataItem01')[0].select('.dataNums')[0].select('#gz_gszzl')[
        0].text.replace('+', '').replace('', '').replace('%', '')
    # 真实涨跌幅
    addtrue = item.select('.dataOfFund')[0].select('.dataItem02')[0].select('.dataNums')[0].select('span')[
        1].text.replace('+', '').replace('', '').replace('%', '')

    global sum
    if addtrue != '':
        add = addtrue
    profit = float(add) * float(money)
    profit1 = '.'.join(str(profit).split('.')[:1])
    if len(name) > 10:
        name = name + '\t'
    if len(name) > 13:
        name = name + '\t'
    print((
            '{code:<{len1}}\t' + '{name:<{len2}}\t' + '{money:<{len3}}\t' + '{add:<{len4}}\t' + '{profit:<{len5}}\t').format(
        code=code,
        len1=6, name=name,
        len2=30 - len(
            name.encode(
                'GBK')) + len(
            name),
        money=money,
        len3=12,
        add=add,
        len4=10 - len(
            add.encode(
                'GBK')) + len(
            add),
        profit=profit1,
        len5=20))
    sum = profit + sum
    # 累加各基金收益


def getAll():
    codes = ['320007', '000248', '005224', '519674', '008282', '001644', '001579', '161028', '003096']
    moneys = ['304.35', '144.65', '99.43', '99.91', '79.94', '77.27', '62.53', '31.70', '31.59']

    code = '编码'
    name = '名称'
    money = '持有(百)'
    profit = '收益(元)'
    add = '涨跌幅(%)'

    print((
            '{code:<{len1}}\t' + '{name:<{len2}}\t' + '{money:<{len3}}\t' + '{add:<{len4}}\t' + '{profit:<{len5}}\t').format(
        code=code,
        len1=6, name=name,
        len2=30 - len(
            name.encode(
                'GBK')) + len(
            name),
        money=money,
        len3=12,
        add=add,
        len4=10 - len(
            add.encode(
                'GBK')) + len(
            add),
        profit=profit,
        len5=20))
    for i in range(0, len(codes)):
        getMoney(codes[i], moneys[i])
    print('今日收益：' + str(sum))


def getA():
    site = 'http://favor.fund.eastmoney.com/'
    html = urllib.request.urlopen(site)
    soup = BeautifulSoup(html, 'html.parser')

    print(soup.select('#quotePanel')[0].select('.em-grids')[0].select('.em-grid-20')[0].select('#quotePanel')[0])


# getA()
getAll()
