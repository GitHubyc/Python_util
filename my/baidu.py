import requests

import urllib.parse

from requests.exceptions import RequestException

from urllib.parse import urljoin

from lxml import etree
import re
import json

# 百度搜索接口

def format_url(url, params: dict=None) -> str:
    query_str = urllib.parse.urlencode(params)
    return f'{ url }?{ query_str }'

def get_url(keyword):
    params = {
        'wd': str(keyword)
    }
    url = "https://www.baidu.com/s"
    url = format_url(url, params)
    # print(url)

    return url

def get_page(url):
    try:

        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, compress',
            'Accept-Language': 'en-us;q=0.5,en;q=0.3',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'
        }  # 定义头文件，伪装成浏览器

        response = requests.get(url,headers=headers)
        # 更改编码方式，否则会出现乱码的情况
        response.encoding = "utf-8"
        print(response.status_code)
        # print(response.text)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None

def parse_page(url,page):

    for i in range(1,int(page)+1):
        print(("正在爬取第{}页....".format(i)))
        title = ""
        sub_url = ""
        abstract = ""
        flag = 11
        if i == 1:
            flag = 10
        html = get_page(url)
        content = etree.HTML(html)
        for j in range(1,flag):
            data = {}
            res_title = content.xpath('//*[@id="%d"]/h3/a' % ((i - 1) * 10 + j))
            if res_title:
                title = res_title[0].xpath('string(.)')

            sub_url = content.xpath('//*[@id="%d"]/h3/a/@href' % ((i - 1) * 10 + j))
            if sub_url:
                sub_url = sub_url[0]

            res_abstract = content.xpath('//*[@id="%d"]/div[@class="c-abstract"]'%((i-1)*10+j))
            if res_abstract:
                abstract = res_abstract[0].xpath('string(.)')
            else:
                res_abstract = content.xpath('//*[@id="%d"]/div/div[2]/div[@class="c-abstract"]'%((i-1)*10+j))
                if res_abstract:
                    abstract = res_abstract[0].xpath('string(.)')
                    # res_abstract = content.xpath('//*[@id="%d"]/div/div[2]/p[1]'%((i-1)*10+j))
            # if not abstract:
            #     abstract = content.xpath('//*[@id="%d"]/div/div[2]/p[1]'%((i-1)*10+j))[0].xpath('string(.)')
            data['title'] = title
            data['sub_url'] = sub_url
            data['abstract'] = abstract


            rel_url = content.xpath('//*[@id="page"]/a[{}]/@href'.format(flag))
            if rel_url:
                url = urljoin(url, rel_url[0])
            else:
                print("无更多页面！～")
                return
            yield data

def main():
    keyword = eval(input("输入关键字:"))
    page = eval(input("输入查找页数:"))
    url = get_url(keyword)

    results = parse_page(url,page)
    # 写入文件
    file = open("data.json", 'w+', encoding='utf-8')
    for result in results:
        print(result)
        file.write(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == '__main__':
    main()
