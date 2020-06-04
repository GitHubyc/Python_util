# coding=utf-8
import urllib.error
import urllib.parse
import urllib.request

from bs4 import BeautifulSoup


def rate(code):
    # 获取基金买入费率
    site = 'http://fundf10.eastmoney.com/jjfl_' + code + '.html'
    html = urllib.request.urlopen(site)
    soup = BeautifulSoup(html, 'html.parser')
    rate = soup.select('#bodydiv')[0].select('.mainFrame')[7].select('.right')[0].select('.basic-new ')[0].select(
        '.bs_jz')[0].select('.col-right')[0].select('p')[2].select('b')[1].text

    # print(soup.select('body script')[1])
    # titles = soup.select("body  script")  # CSS 选择器
    # print(titles)
    # i = 1
    # for title in titles:
    #     if i == 3:
    #         # print(title.get_text())# 标签体、标签属性
    #         str = title.get_text()
    #         break
    #     if i == 2:
    #         i = 3
    #     if i == 1:
    #         i = 2
    #
    # print(str)
    # str1 = "\"\"\"" + "<script>" + str + "</script>" + "\"\"\""
    # soup = BeautifulSoup(str1, "html.parser")
    # pattern = re.compile(r"var _url = '(.*?)';$", re.MULTILINE | re.DOTALL)
    # script = soup.find("script", text=pattern)
    # # print (pattern.search(script.text).string)
    # s = pattern.search(script.text).string
    # print(s.split('\'')[11])
    return rate


def getMoney(code, money):
    site = 'http://fund.eastmoney.com/' + code + '.html?spm=search'
    html = urllib.request.urlopen(site)
    soup = BeautifulSoup(html, 'html.parser')

    # 获取基金名称
    name = \
        soup.select('.wrapper')[8].select('.wrapper_min')[0].select('.merchandiseDetail')[0].select(
            '.fundDetail-header')[
            0].select('.fundDetail-tit')[0].select('div')[0].text
    name = '('.join(name.split('(')[:1])
    # 获取基金统计区域
    item = \
        soup.select('.wrapper')[8].select('.wrapper_min')[0].select('.merchandiseDetail')[0].select('.fundDetail-main')[
            0].select('.fundInfoItem')[0]
    # 预测涨跌幅
    add = item.select('.dataOfFund')[0].select('.dataItem01')[0].select('.dataNums')[0].select('#gz_gszzl')[
        0].text.replace('+', '').replace('', '').replace('%', '')
    # 真实涨跌幅
    addtrue = item.select('.dataOfFund')[0].select('.dataItem02')[0].select('.dataNums')[0].select('span')[
        1].text.replace('+', '').replace('', '').replace('%', '')

    global sum
    # if addtrue != '':
    #     add = addtrue
    profit = float(add) * float(money)
    if len(name) > 10:
        name = name + '\t'
    if len(name) > 13:
        name = name + '\t'
    printmethon(code, name, money, '.'.join(str(profit).split('.')[:1]), add, rate(code))
    sum = profit + sum
    # 累加各基金收益


def printmethon(code, name, money, profit, add, rate):
    print((
            '{code:<{len1}}\t' + '{name:<{len2}}\t' + '{money:<{len3}}\t' + '{add:<{len4}}\t' + '{profit:<{len5}}\t' + '{rate:<{len6}}\t').format(
        code=code,
        len1=20, name=name,
        len2=30 - len(
            name.encode(
                'GBK')) + len(
            name),
        money=money,
        len3=20,
        add=add,
        len4=5 - len(
            add.encode(
                'GBK')) + len(
            add),
        profit=profit,
        len5=20, rate=rate,
        len6=20))


def statisic():
    code = '编码'
    name = '名称'
    money = '持有'
    profit = '收益'
    add = '涨跌幅'
    rate = '买入/卖出费率'
    printmethon(code, name, money, profit, add, rate)

    fund = [
        {'code': '320007', 'money': 304.35, 'name': ''},
        {'code': '000248', 'money': 144.65, 'name': ''},
        {'code': '005224', 'money': 99.43, 'name': ''},
        {'code': '519674', 'money': 99.91, 'name': ''},
        {'code': '008282', 'money': 79.94, 'name': ''},
        {'code': '001644', 'money': 77.27, 'name': ''},
        {'code': '001579', 'money': 62.53, 'name': ''},
        {'code': '161028', 'money': 31.70, 'name': ''},
        {'code': '003096', 'money': 31.59, 'name': ''}]
    fund = sorted(fund, key=lambda tm: (tm["money"]), reverse=True)
    for i in range(0, len(fund)):
        getMoney(fund[i].get('code'), fund[i].get('money'))
    print('总收益：' + str(sum))


sum = 0
statisic()
