#coding=utf-8
import urllib.request, urllib.parse, urllib.error
import _thread
import re
import requests
from time import ctime
from bs4 import BeautifulSoup

def getPM25(cityname):
    site = 'http://www.pm25.com/' + cityname + '.html'
    html = urllib.request.urlopen(site)
    soup = BeautifulSoup(html, 'lxml')

    city = soup.find(class_='bi_loaction_city')
    aqi = soup.find('a', {'class', 'bi_aqiarea_num'})
    quality = soup.select(".bi_aqiarea_right span")
    result = soup.find('div', class_='bi_aqiarea_bottom').find('p')
    result1 = soup.find('p', class_='bi_aqiarea_right')
    # print result1.text
    # print aqi.text
    # print quality[0].text
    print(city.text + ':' + 'AQI指数：' + aqi.text + '；空气质量：' + quality[0].text + '；' + result.text)

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