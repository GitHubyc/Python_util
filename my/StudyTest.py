#coding=utf-8

#1、文件抬头：
#coding=utf-8

#2、引用中文编码
# import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')

#3、解析网页乱码：（查看网页抬头编码）
# soup3 = BeautifulSoup(r3.content.decode('GBK'), 'html.parser')

#4、建立文件：w为可读可写的意思，a+指在原先文本后追加新写内容
# file = open('C:/Users/Administrator/Desktop/a/b.txt','w') #a文件夹必须存在
# 写入文字：
# file.write('你好，\n  世界。')

#5、想使用lxml解析需要先安装lxml插件

#6、多线程
# # 为线程定义一个函数
# def print_time(threadName, delay):
#     count = 0
#     while count < 5:
#         time.sleep(delay)
#         count += 1
#         print "%s: %s" % (threadName, time.ctime(time.time()))
# # 创建两个线程
# try:
#     thread.start_new_thread(print_time, ("Thread-1", 2,))
#     thread.start_new_thread(print_time, ("Thread-2", 4,))
# except:
#     print "Error: unable to start thread"
# while 1:
#     pass

#7、带请求头
# import urllib2
# header={
#     "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:43.0) Gecko/20100101 Firefox/43.0",
#     "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#     "Host":"aljun.me"
# }
# request=urllib2.request("http://xxx.com",header=header)
# response=urllib2.urlopen(request)

#8、带cookie
# import urllib2
# import cookielib
#
# cookie={"bdshare_firstime":1455378744638}
# cookie = cookielib.CookieJar()
#
# opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
#
# urllib2.install_opener(opener)
#
# response=urllib2.urlopen("http://xxx.com")

#9、带参数
# import urllib2
#
# data={
#     "username":"xxx"
#     "password":"xxx"
# }
# request=urllib2.request("http://xxx.com",data)
# response=urllib2.urlopen(request)

#10、爬图片
# import urllib2
#
# response=urllib2.urlopen("http://zhaduixueshe.com/static/pic/discovery.png")
#
# with open("xxx.png","wb") as f:
#     f.write(response.read())

#11、爬图片，借助缓存
# import urllib2
# import stringIO
#
# response=urllib.urlopen("http://zhaduixueshe.com/static/pic/discovery.png")
#
# response=stringIO.stringIO(response.read())
#
# with open("xxx.png","wb") as f:
#     f.write(response)

#12、最好方法
# import urllib
#
# path="xxx.png"
# url="http://zhaduixueshe.com/static/pic/discovery.png"
#
# urllib.urlretrieve(url,path)

#13、正则匹配
# import urllib2
# import re
#
# reg=r'http.(d+).jpg'
# reg=re.compile(reg)
# response=urllib2.urlopen("http://xxx.com")
# result=re.findall(response.read(),reg)

#14、输入汉字
# raw_input()函数
# input()函数只能输入整型或浮点型


#15、两个字母
# a = []
# a.append('a');a.append('b');a.append('c');a.append('d');a.append('e');a.append('f');a.append('g');a.append('h');a.append('i')
# a.append('j');a.append('k');a.append('l');a.append('m');a.append('n');a.append('o');a.append('p');a.append('q');a.append('r')
# a.append('s');a.append('t');a.append('u');a.append('v');a.append('w');a.append('x');a.append('y');a.append('z')
# for i in a:
#     for j in a:
#         print i+j

#按格式输出字符串
input_str = '1、企业;2、物业'
a = []
input_strs = input_str.split(';')
for i in input_strs:
    a.append(i)
for i1 in a:
    str1 = str(i1).split('、')
    id = str1[0]
    content = str1[1]
    print("insert into table values('" + id + "','" + content + "');")
# output_str = input_str.replace(';','insert into table() values('+'')

