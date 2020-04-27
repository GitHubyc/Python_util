#coding=utf-8

import request
import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import _thread
import codecs
import sys
import importlib
importlib.reload(sys)
# sys.setdefaultencoding('utf-8')

o = 0
def getDomain(i):
    try:
        url = 'http://www.' + str(i) + '.com'
        html = urllib.request.urlopen(url)
        page = html.read()
        soup = BeautifulSoup(page, 'html.parser')
        # title = soup.findAll('title')[0].text
        titles = soup.findAll('title')
        if len(titles) == 0:
            return
        title = titles[0].text
    except IOError:
        html = '1'
        # print '网站http://www.' + str(i) + '.com' + '不存在'
    else:
        string1 = '404'
        string2 = '403'
        string3 = '500'
        string4 = 'Not Found'
        string5 = '出售'
        string6 = '建设中'
        string7 = '转让'

        if string1 in title or string2 in title or string3 in title \
                or string4 in title or string5 in title or string5 in title \
                or string6 in title or string7 in title:
            return
            # print '网站http://www.' + str(i) + '.com' + '不存在,' + str(title).replace('\n', '')
        else:
            print('网站http://www.' + str(i) + '.com' + '存在,' + str(title).replace('\n', ''))
            fo.write('网站http://www.' + str(i) + '.com' + '存在,' + str(title).replace('\n', ';') + '\n')
            fo.flush()

def two_thread(a,i, j):
    try:
        for m in a:
            for n in a:
                for k in range(int(j)):
                    _thread.start_new_thread(getDomain, (str(int(i) + k) + str(m) + str(n),))
    except:
        print("Error: unable to start thread")
    while 1:
        pass

a = []
a.append('a');a.append('b');a.append('c');a.append('d');a.append('e');a.append('f');a.append('g');a.append('h');a.append('i')
a.append('j');a.append('k');a.append('l');a.append('m');a.append('n');a.append('o');a.append('p');a.append('q');a.append('r')
a.append('s');a.append('t');a.append('u');a.append('v');a.append('w');a.append('x');a.append('y');a.append('z')
fo = open('50-59.txt', 'a+', encoding='utf-8');
two_thread(a, '48', '2')#参数一为起始，参数二为数量
fo.close()





