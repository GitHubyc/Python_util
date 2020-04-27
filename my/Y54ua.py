#coding=utf-8
import requests
from bs4 import BeautifulSoup
import codecs
import os
import sys
import importlib
importlib.reload(sys)
sys.setdefaultencoding('utf-8')

#首页
url = 'http://www.54ua.com/'
r = requests.get(url)
soup = BeautifulSoup(r.content,'html.parser') #html.parser是解析器
div = soup.findAll('div', attrs={'class': 'menu'})[1]
a = div.findAll('a')
menu_num = 0
fo = codecs.open('10.txt'.decode('utf-8'), 'a+', 'utf-8')
for i in a:
    menu_num = menu_num + 1
    if menu_num < 10:
        continue
    fo.write(i.text + '\n')
    r1 = requests.get(url + i.get("href"))
    soup1 = BeautifulSoup(r1.content, 'html.parser')  # html.parser是解析器
    bord_mtop = soup1.find('div', attrs={'class': 'bord mtop'}).select('> strong')[0].text.replace('1/', '')
    zhang = 0
    for i1 in range(int(bord_mtop) - 1):
        url1 = str(i.get("href"))
        r2 = ''
        if i1 == 0:
            r2 = requests.get(url + url1)
        else:
            url1 = url1.replace('index', 'list_1')
            # print url1.split('_')[0] + '_' + str(i1) + '.html'
            r2 = requests.get(url + url1.split('_')[0] + '_' + str(i1) + '.html')
        soup2 = BeautifulSoup(r2.content, 'html.parser')  # html.parser是解析器
        div2 = soup2.find('div', attrs={'class': 'typelist'})
        ul = div2.select('> ul')
        for i2 in ul:
            zhang = zhang + 1
            r3 = requests.get(url + i2.select('> li > a')[0].get("href"))
            soup3 = BeautifulSoup(r3.content, 'html.parser')  # html.parser是解析器
            title = soup3.findAll('div', attrs={'class': 'mtop'})[1].select('> h3 > a > font')[0].text
            div3 = soup3.findAll('div', attrs={'class': 'mtop'})[2]
            content = str(div3).replace('<div class="mtop" id="view2">\n', '')
            content = content.replace('<br/>', '')
            content = content.replace('<p>', '')
            content = content.replace('.', '')
            content = content.replace('</p>', '')
            content = content.replace('</div>', '')
            fo.write("第" + str(zhang) + "章 " + title + '\n' + content + '\n')
            print("第" + str(zhang) + "章\r",title)
    break
fo.close()

