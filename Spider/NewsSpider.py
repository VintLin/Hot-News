# -*- coding: utf-8 -*-
"""
Created on Wed Feb 28 15:49:58 2018

@author: Voter
"""

import requests
import re
import os
from bs4 import BeautifulSoup
from datetime import datetime as dt
from Database.SaveToDatabase import NewsDataBase
# from Spider import Translate


def getTimeInfo(string):
    time1 = re.search('[0-9]+-[0-9]+-[0-9]+', string).group()
    time2 = re.search('[0-9]+:[0-9]+:[0-9]+', string)
    if time2 is None:
        time2 = re.search('[0-9]+:[0-9]+', string).group() + ':00'
    else:
        time2 = time2.group()
    return [time1, time2]


def makeDir(url):
    path = '.'  # 开始在本地建立相应文件夹
    for d in url.split('/')[:-1]:
        path = path + '/' + d
        if not os.path.exists(path):
            os.mkdir(path)
    return path + '/' + url.split('/')[-1]


class SpiderTool:
    def __init__(self):
        self.__HEADERS = {
            'User-Agent': 'Mozilla/5.0 (Macintosh;Intel Mas OS X 10_9_5)AppleWebKit 537.36 (KHTML, like Gecko) Chrome',
            'Accept': 'text/html,application/xhtml+xml, application/xml; q=0.9, image/webp, */*, q=0.8'
        }

    def getBsObj(self, pageUrl):  # 获取BeautifulSoup对象
        try:
            r = requests.get(pageUrl, headers=self.__HEADERS, )
            r.raise_for_status()
            r.encoding = r.apparent_encoding
            bsObj = BeautifulSoup(r.text, 'html.parser')
            return bsObj
        except:
            print('Error')

    def getHtml(self, pageUrl, params):
        try:

            r = requests.get(pageUrl, headers=self.__HEADERS, params=params)
            r.raise_for_status()
            r.encoding = r.apparent_encoding
            return r.text
        except:
            print('Error')


class FileTool:
    def __init__(self, flag=False):
        self.__INITFLAG = flag
        self.__NOWTIME = dt.now().strftime('%Y-%m-%d')
        self.__ND = NewsDataBase()

    def setInitFlag(self, flag=False):
        self.__INITFLAG = flag

    def saveFileOnUrl(self, url, content, news):  # 将抓取的网页保存在本地(以网页路径)
        url = re.sub('http://', '', url)
        # 去掉 http:// 之后可用网页路径做本地路径
        news.filename = re.sub('\?.*|#.*', '', url.split('/')[-1])
        # 去掉url路径后的？#开头的参数
        news.website = url.split('/')[0]
        # 取该网站的网址
        news.path = makeDir(url)

        with open(news.path, 'w', encoding='utf-8') as w:
            w.write(content)

        self.__ND.Insert(news)
        return True

    def saveFile(self, url, content, news):
        if self.__INITFLAG or self.__NOWTIME == news.time1:
            url = re.sub('http://', '', url)
            if news.type is '':
                news.type = '其他'
            news.website = url.split('/')[0]
            news.filename = re.sub('\?.*|#.*', '', url.split('/')[-1])
            news.path = makeDir('page/{}/{}/{}'.format(news.type, news.time1, news.filename)).replace('./', '/')

            with open('.' + news.path, 'w', encoding='utf-8') as w:
                w.write(content)
            print(news.title, news.path)
            self.__ND.Insert(news)
            return True
        else:
            return False

    def createDataBase(self):
        self.__ND.Drop()
        self.__ND.Create()


if __name__ == '__main__':
    file = FileTool()
    spider = SpiderTool()
