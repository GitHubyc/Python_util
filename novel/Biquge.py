# coding=utf-8
import codecs
import os
import requests
from bs4 import BeautifulSoup


# 此例为爬取笔趣阁小说
def get_url_list(url):
    html = requests.get(url)
    soup = BeautifulSoup(html.content, 'lxml')  # content如果换成text会有乱码
    url_list = []
    list = soup.select("#list > dl > dd > a")
    for i in list:
        url_list.append(url + i.get("href"))
    print('共' + str(len(url_list)) + '章')
    return url_list


def get_data(url):
    html = requests.get(url)
    soup = BeautifulSoup(html.content, 'lxml')
    # 以二进制写入章节题目 需要转换为utf-8编码，否则会出现乱码
    section_name = soup.select("#wrapper > div.content_read > div > div.bookname > h1")[0].text
    print(section_name)
    fo.write(('\r\n' + section_name + '\r\n'))
    section_text = soup.select("#content")
    for x in section_text:
        # 以二进制写入章节内容
        a = x.text.replace('readx();', '').replace('　　', '\r\t').replace('http://www.biquge5200.com/2_2244/1642949', '')
        fo.write((a) + '\r\n')
        fo.flush()


if '__main__' == __name__:
    search = '史上最强炼气期'
    url = 'http://www.biquge.info/modules/article/search.php?searchkey='
    html = requests.get(url + search, verify=False);

    soup = BeautifulSoup(html.content, 'lxml')
    # 获取查询结果中的书籍路径
    # search_books = soup.select(' #main > #content > #checkform > table.grid > tbody > tr ')
    search_books = soup.select('#wrapper > .grid')[0].select('tr')[1].select('a')
    book_a = search_books[0].get('href')
    print(book_a)
    # 比对第一个结果是否匹配
    book_name = search_books[0].text.replace(" ", "").replace('\r', '').replace('\n', '')
    if search != book_name:
        print('无完全匹配的书籍！要找的是不是' + book_name)
        os._exit(0)
    # 获取章节列表链接

    url_list = get_url_list("http://www.biquge.info" + book_a)
    fo = codecs.open(book_name + '.txt', 'a+', 'utf-8');
    for n in url_list:
        get_data(n)
    fo.close()  # 关闭小说文件
