# coding: utf-8

from PIL import Image
import pytesseract
import os
import urllib.error
import urllib.parse
import urllib.request

import datetime
from bs4 import BeautifulSoup
import requests
import json
import base64

import difflib


# 去除文件中空行
def rmblank(txt):
    os.rename(txt, 'old' + txt)
    with open('old' + txt, 'r', encoding='utf-8') as fr, open(txt, 'w', encoding='utf-8') as fd:
        for text in fr.readlines():
            if text.split():
                fd.write(text)
        print('已将文件去除空行')
    os.remove('old' + txt)


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


# 图片转换文字
def imgtoword(img, txt):
    # text=pytesseract.image_to_string(Image.open('123.png'),lang='eng')  #设置为英文或阿拉伯字母的识别
    starttime = datetime.datetime.now()
    text = pytesseract.image_to_string(Image.open(img), lang='chi_sim').encode('utf-8').decode('utf-8')
    endtime = datetime.datetime.now()
    fo = open(txt, encoding='utf-8', mode='a+')
    fo.write(text)
    fo.close()
    rmblank(txt)
    print('图片转换文字成功，耗时：' + str((endtime - starttime).seconds))


# 解析处理文本内容
def analysis(txt):
    global name, amount, yesterday_profit, hold_profit, img
    fo = open(txt, encoding='utf-8', mode='r')
    line = fo.readline().encode('utf-8').decode('utf-8').replace('\n', '')
    i = 1
    fine_nums = []
    while line:
        if str(line)[0:2] == '金额':
            fine_nums.append(i)
        line = fo.readline()
        i += 1
    fo.close()
    words = result(img)  #
    for j in fine_nums:
        fo = open(txt, encoding='utf-8', mode='r')
        line = fo.readline()
        k = 1
        while line:
            if k == j - 1:
                # 名称使用百度识别，准确度较高
                quick_ratio = 0
                quick_word = line
                for word in words:
                    new_quick_ratio = difflib.SequenceMatcher(None, line, word.get('words')).quick_ratio()
                    if new_quick_ratio > quick_ratio:
                        quick_ratio = new_quick_ratio
                        quick_word = word.get('words')
                name.append(quick_word)
            elif k == j + 1:
                line = line.encode('utf-8').decode('utf-8').replace('\n', '').replace(',', '').replace('_',
                                                                                                       '.').replace('ó',
                                                                                                                    '0').replace(
                    '--', '0').replace(
                    'o', '0')  # 常见识别异常处理
                amount.append(float(line.split(' ')[0]))
                yesterday_profit.append(float(line.split(' ')[1]))
                hold_profit.append(float(line.split(' ')[2]))
            line = fo.readline()
            k += 1


# 按格式打印内容
def printmethon(code, name, money, profit, add, rate):
    print((
            '{code:<{len1}}\t' + '{name:<{len2}}\t' + '{money:<{len3}}\t' + '{add:<{len4}}\t' + '{profit:<{len5}}\t' + '{rate:<{len6}}\t').format(
        code=code,
        len1=20, name=name,
        len2=30 - len(
            name.encode(
                'GBK')) + len(
            name),
        money=money,
        len3=20,
        add=add,
        len4=5 - len(
            add.encode(
                'GBK')) + len(
            add),
        profit=profit,
        len5=20, rate=rate,
        len6=20))


# 获取单个买入费率
def rate(code):
    site = 'http://fundf10.eastmoney.com/jjfl_' + code + '.html'
    html = urllib.request.urlopen(site)
    soup = BeautifulSoup(html, 'html.parser')
    rate = soup.select('#bodydiv')[0].select('.mainFrame')[7].select('.right')[0].select('.basic-new ')[0].select(
        '.bs_jz')[0].select('.col-right')[0].select('p')[2].select('b')[1].text
    return rate


# 根据名称获取编码
def getcode(name):
    content = ''
    with open('codes.txt', encoding='utf-8', mode='r') as f:
        try:
            content = f.read()
        except:
            pass
        f.close()
    all = json.loads(content)
    for a in all:
        if str(json.loads(str(a).replace('\'', '"')).get('name')) == name:
            return str(json.loads(str(a).replace('\'', '"')).get('code'))


# 根据名称百度获取编码
def baiducode(name):
    site = 'https://www.baidu.com/s?ie=UTF-8&wd='
    html = requests.get(site + name, verify=False).content
    soup = BeautifulSoup(html, 'lxml')
    print(soup)


#
def getMoney(code, money):
    global sum
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

    # if addtrue != '':
    #     add = addtrue
    profit = float(add) * float(money)
    if len(name) > 10:
        name = name + '\t'
    if len(name) > 13:
        name = name + '\t'
    printmethon(code, name, money, '.'.join(str(profit).split('.')[:1]), add, rate(code))
    sum = profit + sum
    # 累加各基金收益


print(baiducode('诺安成长混合'))
# img = 'abc.jpg'
# sum = 0
# name = []
# amount = []
# yesterday_profit = []
# hold_profit = []
# imgtoword(img, 'jijin.txt')
# analysis('jijin.txt')
# print(name)
# printmethon('编码', '名称', '金额', '持有收益', '', '')
# fund = []
# for i in range(len(name)):
#     dict = {'code': str(getcode(name[i])), 'money': amount[i], 'name': name[i]}
#     fund.append(dict)
#
# fund = sorted(fund, key=lambda tm: (tm["money"]), reverse=True)
# print(fund)
# for i in range(0, len(fund)):
#     getMoney(fund[i].get('code'), fund[i].get('money'))
#
# printmethon('000000', name[i], amount[i], hold_profit[i], '', '')
# print(name[i] + '\t' + amount[i] + '\t' + yesterday_profit[i] + '\t' + hold_profit[i] + '\t')
