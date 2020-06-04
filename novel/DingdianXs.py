# coding=utf-8
import codecs
import importlib
import sys
import os

import requests
from bs4 import BeautifulSoup

importlib.reload(sys)


# 获取章节链接集合
def get_url_list_dingdian(url):
    html = requests.get(url, verify=False);
    soup = BeautifulSoup(html.content, 'lxml')  # content如果换成text会有乱码
    url_list = []
    list = soup.select("#list > dl > dd > a")
    for i in list:
        url_list.append(url + i.get("href"))
    return url_list


# 进行章节内容获取
def get_data_dingdian(url):
    html = requests.get(url, verify=False);
    soup = BeautifulSoup(html.content, 'lxml')
    # 以二进制写入章节题目 需要转换为utf-8编码，否则会出现乱码
    section_name = soup.select(" div.bookname > h1")[0].text
    fo.write(('\r\n' + section_name + '\r\n'))
    book_content = soup.select("#content")
    for x in book_content:
        # 以二进制写入章节内容
        a = x.text.replace('readx();', '').replace('　　', '\r\t')
        fo.write((a) + '\r\n')
        fo.flush()
    print(section_name)


if '__main__' == __name__:
    search = '大主宰'
    url = 'http://www.dingdianxs.com/modules/article/search.php?searchkey='
    html = requests.get(url + search, verify=False);
    soup = BeautifulSoup(html.content, 'lxml')
    # 获取查询结果中的书籍路径
    search_books = soup.select(' #main > .novelslistss ')[0].select('li')[0].select(' span.s2 > a')
    book_a = search_books[0]
    # 比对第一个结果是否匹配
    book_name = book_a.text.replace(" ", "").replace('\r', '').replace('\n', '')
    print(book_a)
    if search != book_name:
        print('无完全匹配的书籍！要找的是不是' + book_name)
        os._exit(0)
    # 获取章节列表链接
    chapter_a = get_url_list_dingdian(book_a.get('href'))
    # 创建文件，进行写入
    fo = codecs.open(book_name + '.txt', 'a+', 'utf-8');
    for i in range(0, 100):
        get_data_dingdian(chapter_a[i])
    fo.close()  # 3 关闭小说文件
    os._exit(0)
