#coding=utf-8
from bs4 import BeautifulSoup
import requests
import codecs
import sys,urllib.request,urllib.parse,urllib.error
import time
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
        i = i
        url_list.append(i)
    url_list = url_list[9:-1]
    return url_list
def get_data_biquge(book_name,url):
    try:
        html = requests.get(url)
        soup = BeautifulSoup(html.content, 'lxml')

        fo = codecs.open('1' + '.txt', 'a+', 'utf-8');
        # 以二进制写入章节题目 需要转换为utf-8编码，否则会出现乱码
        section_name = soup.select(' #wrapper > div.content_read > div.box_con > div.bookname > h1')[0].text
        print(section_name)
        fo.write(('\r\n' + section_name + '\r\n'))
        section_text = soup.select("#content")
        for x in section_text:
            a = x.text.replace('readx();', '').replace('　　','\r\t')
            fo.write((a) + '\r\n')
        # 以二进制写入章节内容
        fo.close()  # 关闭小说文件
    except ZeroDivisionError as e:
        fo.close()  # 关闭小说文件
        print(section_text+'错误')
        return ''
if '__main__' == __name__:
    # 输入书籍名称，进行格式转换拼接，获取路径
    search = '侏罗纪恐龙霸王'
    url = 'https://www.biquge5200.cc/modules/article/search.php?searchkey='
    # name = urllib.quote(search.decode(sys.stdin.encoding).encode('gbk'))
    html = requests.get(url+search) ;
    soup = BeautifulSoup(html.content, 'lxml')
    # 获取查询结果
    try:
        search_books = soup.select(' #wrapper > #main > #hotcontent > table.grid > tr')
    except ZeroDivisionError as e:
        print(e.message)
    result_bool = 1;
    # 进入章节列表页面
    chapter_a = get_url_list_biquge("https://www.biquge5200.cc/118_118840/")
    for i in range(0, 5):
        try:
            # 传入各章节的url进行抓取
            get_data_biquge(search,chapter_a[i])
            time.sleep(0.5)
        except ZeroDivisionError as e:
            print(e.message)
            if i > 0:
                i=i-1
                continue
            else:
                continue
    if result_bool==0:
        print('没有完全匹配名称的书籍')
    else:
        print('下载完成')




