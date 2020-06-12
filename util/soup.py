# coding=utf-8
import requests
import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup


def soupbyurllib(url, header):
    html = urllib.request.urlopen(url)
    soup = BeautifulSoup(html, 'lxml')
    return soup


def soupbyreqs(url, header):
    html = requests.get(url).content
    soup = BeautifulSoup(html, 'lxml')
    return soup


url = 'https://www.csdn.net/'
header = ''
soup = soupbyurllib(url, header)
print(soup)
