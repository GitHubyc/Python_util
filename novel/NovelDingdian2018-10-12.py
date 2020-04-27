#coding=utf-8
import requests
from bs4 import BeautifulSoup
import codecs
# import StudyThread
import time
import sys,urllib.request,urllib.parse,urllib.error
import importlib
importlib.reload(sys)
sys.setdefaultencoding('utf-8')
#此例为顶点小说爬取

def get_url_list_dingdian(url):
    html = requests.get(url,verify=False);
    soup = BeautifulSoup(html.content, 'lxml')#content如果换成text会有
    # 乱码
    url_list = []
    list = soup.select("#list > dl > dd > a")
    for i in list:
        i = i.get("href");
        i = 'https://www.dingdiann.com' + i
        url_list.append(i)
    url_list = url_list[9:-1]
    print(url_list)
    return url_list
def get_data_dingdian(book_name,url):
    html = requests.get(url,verify=False);
    soup = BeautifulSoup(html.content, 'lxml')

    fo = codecs.open(book_name + '.txt', 'a+', 'utf-8');
    # 以二进制写入章节题目 需要转换为utf-8编码，否则会出现乱码
    section_name = soup.select(" div.bookname > h1")[0].text
    print(section_name)
    fo.write(('\r\n' + section_name + '\r\n'))
    book_content = soup.select("#content")
    for x in book_content:
        a = x.text.replace('readx();', '').replace('　　','\r\t')
        fo.write((a)+ '\r\n')
    # 以二进制写入章节内容
    fo.close()  #3 关闭小说文件
if '__main__' == __name__:
    # for i in range(10000):
    #     i = i + 1
    #     StudyThread.start_new_thread(one_book, (str(i),))
    # 输入书籍名称，进行格式转换拼接，获取路径
    search = '超神机械师'
    #、、
    url = 'https://www.dingdiann.com/searchbook.php?keyword='
    name = urllib.parse.quote(search.decode(sys.stdin.encoding).encode('gbk'))
    html = requests.get(url + search,verify=False);
    soup = BeautifulSoup(html.content, 'lxml')
    # 获取查询结果
    try:
        search_books = soup.select(' #main > div.novelslist2 > ul > li ')
    except ZeroDivisionError as e:
        print(e.message)
    result_bool = 0;
    for book in search_books:
        try:
            if len(book.select(' > span.s2 > a'))==0:
                continue
            book_a = book.select(' > span.s2 > a')[0]
        except ZeroDivisionError as e:
            continue

        book_name = book_a.text.replace(" ", "").replace('\r', '').replace('\n', '')
        if search!=book_name:
            continue;
        result_bool = 1
        # 进入章节列表页面
        chapter_a = get_url_list_dingdian('https://www.dingdiann.com'+book_a.get('href'))
        # for i in range(0, len(chapter_a)):
        for i in range(1170, len(chapter_a)):
            try:
                # 传入各章节的url进行抓取
                get_data_dingdian(book_name,chapter_a[i])
                time.sleep(1)
            except ZeroDivisionError as e:
                print(i)
                print(e.message)
                if i > 0:
                    i=i-1
                    continue
                else:
                    continue
        break;
    if result_bool==0:
        print('没有完全匹配名称的书籍')
    else:
        print('下载完成')