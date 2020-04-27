#coding=utf-8
import requests
from bs4 import BeautifulSoup
import codecs
# import StudyThread
import time

import sys
import importlib
importlib.reload(sys)
sys.setdefaultencoding('utf-8')
#此例为顶点小说爬取

def one_book(path):
    r = requests.get('http://www.23us.so/xiaoshuo/' + path + '.html')
    soup = BeautifulSoup(r.content, 'html.parser')  # html.parser是解析器
    div = soup.find('div', attrs={'class': 'bdsub'})
    book_info = div.select(' > dl > dd')[1].select(' > div')[1].select('table')[0]
    brief_introduction = div.select(' > dl > dd')[3].select(' > p')[1]#内容简介

    book_name = div.select(' > dl > dd')[0].text.split(' ')[0]
    book_type = book_info.select(' > tr')[0].select(' > td')[0].text
    word_of_number = book_info.select(' > tr')[1].select(' > td')[1].text.split('字')[0]
    collection = book_info.select(' > tr')[1].select(' > td')[0].text
    click_totle = book_info.select(' > tr')[2].select(' > td')[0].text
    click_mouth = book_info.select(' > tr')[2].select(' > td')[1].text
    click_weeked = book_info.select(' > tr')[2].select(' > td')[1].text
    Recommend_totle = book_info.select(' > tr')[3].select(' > td')[0].text
    Recommend_mouth = book_info.select(' > tr')[3].select(' > td')[1].text
    Recommend_weeked = book_info.select(' > tr')[3].select(' > td')[2].text
    # 根据条件获取书籍信息
    # if int(collection) < 500 or int(Recommend_totle) < 1000:
    #     return
    print(("第几本：%-5s 名称:%-10s 类别:%-10s 字数:%-10s 收藏数:%-5s 总点击数:%-15s 本月点击:%-15s 本周点击:%-10s 总推荐数:%-10s 本月推荐:%-10s 本周推荐:%-10s 内容简介:%-10s" % (
        (path),
        (book_name),
        (book_type),
        (word_of_number),
        (collection),
        (click_totle),
        (click_mouth),
        (click_weeked),
        (Recommend_totle),
        (Recommend_mouth),
        (Recommend_weeked),
        ('\n' + brief_introduction.text))));
    # 爬取书籍内容
    fo = codecs.open(book_name + '.txt'.decode('utf-8'), 'a+', 'utf-8')
    # 目录页面
    div4 = soup.find('p', attrs={'class': 'btnlinks'})
    a1 = div4.select(' > a')[0]
    r4 = requests.get(a1.get("href"))
    soup4 = BeautifulSoup(r4.content, 'html.parser')  # html.parser是解析器
    table = soup4.find("table")
    table_book = table.select(' > tr')
    zhangnum = 0;  # 循环章节进行写入文本
    fo.write('内容简介:\n' + brief_introduction.text + '\r\n')
    for book_a1 in table_book:
        book_a2 = book_a1.select('> td > a')
        for zhangjie in book_a2:
            zhangnum = zhangnum + 1
            book_content_page = requests.get(zhangjie.get("href"))
            book_content_soup = BeautifulSoup(book_content_page.content, 'html.parser')  # html.parser是解析器
            book_content = book_content_soup.find('div', attrs={'class': 'bdsub'})
            book_content1 = book_content.select(' > dl > dd')[2]
            book_content1 = str(book_content1).replace('<dd id="contents">', '')
            book_content1 = book_content1.replace('</dd>', '')
            book_content1 = book_content1.replace('<br/>\n<br/>', '  ')
            print(book_name + zhangjie.text)  # 当前章节
            fo.write(zhangjie.text + '\r\n')
            fo.write(book_content1 + '\r\n')
        # if zhangnum == 10:#控制下载章节数目
        #     break;
    fo.close()
    print(book_name + '爬取完成！！！')

# 为线程定义一个函数
def print_time(threadName, delay):
    count = 0
    while count < 5:
        time.sleep(delay)
        count += 1
        print("%s: %s" % (threadName, time.ctime(time.time())))


# 创建线程
try:
    # for i in range(10000):
    #     i = i + 1
    #     StudyThread.start_new_thread(one_book, (str(i),))
    one_book('15738')
except:
    print("Error: unable to start thread")

while 1:
    pass