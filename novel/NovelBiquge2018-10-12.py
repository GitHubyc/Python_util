#coding=utf-8
from bs4 import BeautifulSoup
import requests
import codecs
import sys,urllib.request,urllib.parse,urllib.error
import importlib
importlib.reload(sys)
sys.setdefaultencoding('utf-8')
#此例为爬取笔趣阁小说（条件：已知书名）

def get_url_list_biquge(url):
    html = requests.get(url)
    soup = BeautifulSoup(html.content, 'lxml')#content如果换成text会有
    # 乱码
    url_list = []
    list = soup.select("#list > dl > dd > a")
    for i in list:
        i = i.get("href")
        i = 'http://www.bequge.com' + i
        url_list.append(i)
    url_list = url_list[9:-1]
    print(url_list)
    return url_list
def get_data_biquge(book_name,url):
    html = requests.get(url)
    soup = BeautifulSoup(html.content, 'lxml')

    fo = codecs.open( book_name+'.txt', 'a+', 'utf-8');
    # 以二进制写入章节题目 需要转换为utf-8编码，否则会出现乱码
    section_name = soup.select("#wrapper > div.content_read > div > div.bookname > h1")[0].text
    print(section_name)
    fo.write(('\r\n' + section_name + '\r\n'))
    section_text = soup.select("#content")
    for x in section_text:
        a = x.text.replace('readx();', '').replace('　　','\r\t')
        fo.write((a)+ '\r\n')
    # 以二进制写入章节内容
    fo.close()  # 关闭小说文件

if '__main__' == __name__:
    # 输入书籍名称，进行格式转换拼接，获取路径
    search = '神话断章'
    url = 'http://zhannei.baidu.com/cse/search?s=1014455884157026294&entry=1&ie=gbk&q='
    name = urllib.parse.quote(search.decode(sys.stdin.encoding).encode('gbk'))
    html = requests.get(url+name) ;
    soup = BeautifulSoup(html.content, 'lxml')
    # 获取查询结果
    try:
        search_books = soup.select(' #results > div.result-list > div.result-item')
        result_num = soup.select(' #results > span')[0].text
        print(result_num)
    except ZeroDivisionError as e:
        print(e.message)
    result_bool = 0;
    for book in search_books:
        book_a = book.select(' > div.result-game-item-detail > h3 > a')[0]
        book_name = book_a.text.replace(" ", "").replace('\r', '').replace('\n', '')
        if search!=book_name:
            continue;
        result_bool = 1
        # 进入章节列表页面
        chapter_a = get_url_list_biquge(book_a.get('href'))
        for i in range(0, len(chapter_a)):
            try:
                # 传入各章节的url进行抓取
                get_data_biquge(book_name,chapter_a[i])
            except ZeroDivisionError as e:
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




