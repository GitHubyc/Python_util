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

    return rate


def getMoney(code, name, money, currentprofit):
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
    printmethon(code, name, rate(code), str(money), '.'.join(str(profit).split('.')[:1]), str(add), str(currentprofit),
                str(currentprofit + float(add))[0:4])
    sum = profit + sum
    # 累加各基金收益


def printmethon(code, name, rate, money, profit, add, currentprofit, todayprofit):
    print((
            '{code:<{len1}}\t' + '{name:<{len2}}\t' + '{rate:<{len3}}\t' + '{money:<{len4}}\t' + '{add:<{len5}}\t' + '{profit:<{len6}}\t' + '{currentprofit:<{len7}}\t' + '{todayprofit:<{len8}}\t').format(
        code=code,
        len1=10, name=name,
        len2=30 - len(
            name.encode(
                'GBK')) + len(
            name), rate=rate,
        len3=5 - len(
            rate.encode(
                'GBK')) + len(
            rate),
        money=money,
        len4=15 - len(
            money.encode(
                'GBK')) + len(
            money),
        add=add,
        len5=5 - len(
            add.encode(
                'GBK')) + len(
            add),
        profit=profit,
        len6=5 - len(
            profit.encode(
                'GBK')) + len(
            profit), currentprofit=currentprofit,
        len7=5 - len(
            currentprofit.encode(
                'GBK')) + len(
            currentprofit), todayprofit=todayprofit,
        len8=20))


def statisic():
    code = '编码'
    name = '名称'
    rate = '买入卖出'
    money = '持有'
    profit = '收益'
    add = '涨跌幅'
    currentprofit = '当前收益'
    todayprofit = '累计今日'
    printmethon(code, name, rate, money, profit, add, currentprofit, todayprofit)

    fund = [
        {'code': '320007', 'money': 355.53, 'name': '诺安', 'currentprofit': 0.37},
        {'code': '000248', 'money': 116, 'name': '汇添富消费', 'currentprofit': 3.29},
        {'code': '001644', 'money': 107.17, 'name': '汇丰晋信智造', 'currentprofit': 8.08},
        {'code': '519674', 'money': 100, 'name': '银河', 'currentprofit': -1.02},
        {'code': '005224', 'money': 98.75, 'name': '基建', 'currentprofit': -1.31},
        {'code': '001579', 'money': 82.12, 'name': '农业', 'currentprofit': 2.76},
        {'code': '008282', 'money': 81.38, 'name': '半导体', 'currentprofit': 0.63},
        {'code': '003096', 'money': 12, 'name': '医疗', 'currentprofit': 1.54}]
    fund = sorted(fund, key=lambda tm: (tm["money"]), reverse=True)
    for i in range(0, len(fund)):
        getMoney(fund[i].get('code'), fund[i].get('name'), fund[i].get('money'), fund[i].get('currentprofit'))
    print('总收益：' + str(int(sum)))


sum = 0
statisic()
