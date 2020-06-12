# coding=utf-8
import urllib.request, urllib.parse, urllib.error
import _thread
import re
import requests
from time import ctime
from bs4 import BeautifulSoup
import os


def getPM25(cityname):
    site = 'https://baike.baidu.com/item/%E6%98%8E%E6%9C%9D/141291?fromtitle=%E6%98%8E&fromid=9473149&fr=aladdin'
    html = urllib.request.urlopen(site)
    soup = BeautifulSoup(html, 'lxml')

    city = soup.select('.body-wrapper')[0].select('.content-wrapper')[0].select('.content')[0].select(
        '.main-content')[0].select('table')[3].select('tr')
    title = city[0]
    try:
        for i in city:
            td = i.select('td')
            if len(td) <= 1:
                print()
            else:
                print(td[2].text.replace('\r', '').replace('\n', ''))
                print('(',td[3].text.replace('\r', '').replace('\n', ''))
                print(title.select('th')[5].text, td[5].text.replace('\r', '').replace('\n', ''))
                print(title.select('th')[0].text, td[0].text.replace('\r', '').replace('\n', ''))
                print(title.select('th')[1].text, td[1].text.replace('\r', '').replace('\n', ''))
                print(title.select('th')[4].text, td[4].text.replace('\r', '').replace('\n', ''))
                print(')')
    except ZeroDivisionError as e:
        os._exit(0)

    # aqi = soup.find('a', {'class', 'bi_aqiarea_num'})
    # quality = soup.select(".bi_aqiarea_right span")
    # result = soup.find('div', class_='bi_aqiarea_bottom').find('p')
    # result1 = soup.find('p', class_='bi_aqiarea_right')
    # # print result1.text
    # # print aqi.text
    # # print quality[0].text

    # print '*' * 3 + ctime() + '*' * 3 + result.text


def one_thread():
    print('One_thread Start:' + ctime() + '\n')
    getPM25('jian')
    getPM25('nanchang')
    getPM25('xianyang')
    getPM25('shenzhen')
    getPM25('beijing')
    getPM25('shanghai')
    getPM25('hangzhou')
    getPM25('nanjing')
    getPM25('suzhou')


def two_thread():
    try:
        getPM25(1)
    except:
        print("Error: unable to start thread")

    while 1:
        pass
    # threads.append(t1)
    # t2 = threading.Thread(target=getPM25, arg=('nanchang',))
    # threads.append(t2)
    # t3 = threading.Thread(target=getPM25, arg=('xianyang',))
    # threads.append(t3)
    # t4 = threading.Thread(target=getPM25, arg=('shenzhen',))
    # threads.append(t4)
    # t5 = threading.Thread(target=getPM25, arg=('beijing',))
    # threads.append(t5)
    # t6 = threading.Thread(target=getPM25, arg=('shanghai',))
    # threads.append(t6)
    # t7 = threading.Thread(target=getPM25, arg=('hangzhou',))
    # threads.append(t7)
    # t8 = threading.Thread(target=getPM25, arg=('nanjing',))
    # threads.append(t8)
    # t9 = threading.Thread(target=getPM25, arg=('suzhou',))
    # threads.append(t9)

    # for t in threads:
    #     # t.setDaemon(true)
    #     t.start()


# one_thread()
two_thread()