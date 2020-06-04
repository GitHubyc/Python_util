# coding=utf-8
import codecs
import importlib
import os
import shutil
import sys
import threading

import requests
from bs4 import BeautifulSoup

importlib.reload(sys)


# 创建文件夹
def mkdir(path):
    # 去除首位空格、去除尾部 \ 符号
    path = path.strip().rstrip("\\")
    # 判断路径是否存在进行操作
    if os.path.exists(path):
        return False
    else:
        os.makedirs(path)
        print(path + ' 创建成功')
        return True


# 删除文件夹
def rmtree(path):
    try:
        os.remove(path)
    except:
        print('路径不存在')
    try:
        project_path = os.path.dirname(os.path.abspath(__file__))  # 获取当前文件路径的上一级目录
        os.remove(project_path + r'\\' + path)
    except:
        print('不能直接删除含有文件的文件夹')
    try:
        shutil.rmtree(project_path + r'\\' + path)
        print('删除成功')
    except:
        print('删除失败')


# 遍历文件夹
def merge(file):
    for root, dirs, files in os.walk(file):
        print
    for f in files:
        print(os.path.join(root, f))
        read_Writeline(os.path.join(root, f), file + ".txt")
    for d in dirs:
        print(os.path.join(root, d))


# 文件写入
def read_Writeline(old_file, new_file):
    new = codecs.open(new_file, 'a+', 'utf-8');
    old = codecs.open(old_file, 'r', 'utf-8')  # 需要两个\\,或者用原始字符串，在引号前面加r
    try:
        new.write(old.read())
        new.flush()
    finally:
        new.close()
        old.close()


# 获取每一章链接
def get_url_list_dingdian(url):
    html = requests.get(url, verify=False);
    soup = BeautifulSoup(html.content, 'lxml')  # content如果换成text会有
    # 乱码
    url_list = []
    list = soup.select("#list > dl > dd > a")
    for i in list:
        i = i.get("href");
        i = 'https://www.dingdiann.com' + i
        url_list.append(i)
    url_list = url_list[9:-1]
    return url_list


# 进行url内容获取
def get_data_dingdian(book_name, i, url):
    html = requests.get(url, verify=False);
    soup = BeautifulSoup(html.content, 'lxml')
    mkdir(book_name)
    fo = codecs.open(book_name + '/' + str(i) + '.txt', 'a+', 'utf-8');
    # 以二进制写入章节题目 需要转换为utf-8编码，否则会出现乱码
    section_name = soup.select(" div.bookname > h1")[0].text
    print(section_name)
    fo.write(('\r\n' + section_name + '\r\n'))
    book_content = soup.select("#content")
    for x in book_content:
        a = x.text.replace('readx();', '').replace('　　', '\r\t')
        fo.write((a) + '\r\n')
    # 以二进制写入章节内容
    fo.close()  # 3 关闭小说文件


# 每个线程获取i个链接内容
def get_data_thread(book_name, num, url, thread_num):
    print(thread_num)
    for i in range(0, thread_num):
        current_num = num * thread_num + i
        print(current_num)
        if current_num >= len(url):
            break
        html = requests.get(url[current_num], verify=False);
        soup = BeautifulSoup(html.content, 'lxml')
        mkdir(book_name)
        fo = codecs.open(book_name + '/' + str(num) + '.txt', 'a+', 'utf-8');
        # 以二进制写入章节题目 需要转换为utf-8编码，否则会出现乱码
        section_name = soup.select(" div.bookname > h1")[0].text
        print(section_name)
        fo.write(('\r\n' + section_name + '\r\n'))
        book_content = soup.select("#content")
        for x in book_content:
            a = x.text.replace('readx();', '').replace('　　', '\r\t')
            fo.write((a) + '\r\n')
        # 以二进制写入章节内容
        fo.close()  # 3 关闭小说文件

if '__main__' == __name__:
    search = '超神机械师'
    url = 'https://www.dingdiann.com/searchbook.php?keyword='

    html = requests.get(url + search, verify=False);
    soup = BeautifulSoup(html.content, 'lxml')
    # 获取查询结果
    try:
        search_books = soup.select(' #main > div.novelslist2 > ul > li ')
    except ZeroDivisionError as e:
        print(e.message)
    result_bool = 0;
    for book in search_books:
        try:
            if len(book.select(' span.s2 > a')) == 0:
                continue
            book_a = book.select(' span.s2 > a')[0]
        except ZeroDivisionError as e:
            continue

        book_name = book_a.text.replace(" ", "").replace('\r', '').replace('\n', '')
        if search != book_name:
            continue;
        result_bool = 1
        # 进入章节列表页面
        chapter_a = get_url_list_dingdian('https://www.dingdiann.com' + book_a.get('href'))


        #多线程进行爬取
        problem = []
        threads = []
        for i in range(0, 100):
            if i * i > len(chapter_a):
                thread_num = i
                break
        for i in range(0, thread_num + 1):
            try:
                t = threading.Thread(target=get_data_thread, args=(book_name, i, chapter_a, thread_num))
                threads.append(t)
                t.start()
            except ZeroDivisionError as e:
                problem.append(i)

    if result_bool == 0:
        print('没有完全匹配名称的书籍')
    else:
        # # 等待所有线程任务结束。
        for t in threads:
            t.join()
        print("所有线程任务完成")
        print(str(problem) + "出现问题")
        merge(search)
        rmtree(search)