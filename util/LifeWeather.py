#coding=utf-8
import urllib.request, urllib.parse, urllib.error
import _thread
import re
import requests
from time import ctime
from bs4 import BeautifulSoup
import sys
import importlib
importlib.reload(sys)
sys.setdefaultencoding('utf-8')

#今日天气
def getPM25(cityname):
    site = 'http://www.tianqi.com/' + cityname + '.html'
    html = urllib.request.urlopen(site)
    soup = BeautifulSoup(html, 'lxml')

    weather_info = soup.find('dl', class_='weather_info')
    name = str(weather_info.findAll('dd')[0].text).split('[')[0]
    weather = str(weather_info.findAll('dd')[2].findAll('span')[0].text).replace('\n', '')
    shidu = str(weather_info.findAll('dd')[3].text).replace('\n', '')
    kongqi = str(weather_info.findAll('dd')[4].text).replace('\n', '')

    site1 = 'http://www.pm25.com/' + cityname + '.html'
    html1 = urllib.request.urlopen(site1)
    soup1 = BeautifulSoup(html1, 'lxml')

    city = soup1.find(class_='bi_loaction_city')
    aqi = soup1.find('a', {'class', 'bi_aqiarea_num'})
    quality = soup1.select(".bi_aqiarea_right span")
    result = soup1.find('div', class_='bi_aqiarea_bottom').find('p')
    result1 = soup1.find('p', class_='bi_aqiarea_right')

    print(name, weather, '\n\t' + shidu)
    if name == '吉水':
        return
    print('\tAQI指数：' + aqi.text + '；空气质量：' + quality[0].text + '；' + result.text)

#15天预报
def yubao(cityname):
    site = 'http://www.tianqi.com/' + cityname + '/15/'
    html = urllib.request.urlopen(site)
    soup = BeautifulSoup(html, 'lxml')
    div = soup.find('div', class_='box_day').findAll('div')
    name = soup.find('div', class_='more_day').findAll('a')[0].text
    print(name + '15天')
    for i in div:
        print(i.find('h3').text + '\t' + str(i.find('ul').text).replace('\n',' '))

def one_thread():
    getPM25('jishui')
    getPM25('nanchang')
    getPM25('xianyang')
    getPM25('shenzhen')
    getPM25('beijing')
    getPM25('shanghai')
    getPM25('hangzhou')
    getPM25('nanjing')
    getPM25('suzhou')

    yubao('jishui')
    yubao('nanchang')
    yubao('xianyang')
    yubao('shenzhen')
    yubao('beijing')
    yubao('shanghai')
    yubao('hangzhou')
    yubao('nanjing')
    yubao('suzhou')

def two_thread():
    try:
        _thread.start_new_thread(getPM25, ('hefei',))
        _thread.start_new_thread(getPM25, ('nanchang',))
        _thread.start_new_thread(getPM25, ('xianyang',))
        _thread.start_new_thread(getPM25, ('shenzhen',))
        _thread.start_new_thread(getPM25, ('beijing',))
        _thread.start_new_thread(getPM25, ('shanghai',))
        _thread.start_new_thread(getPM25, ('hangzhou',))
        _thread.start_new_thread(getPM25, ('nanjing',))
        _thread.start_new_thread(getPM25, ('beijing',))
        _thread.start_new_thread(getPM25, ('suzhou',))
    except:
        print("Error: unable to start thread")
    while 1:
        pass
one_thread()
# two_thread()