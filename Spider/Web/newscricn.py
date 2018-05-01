# -*- coding: utf-8 -*-
"""
Created on Mon Feb 26 17:01:35 2018

@author: Voter
"""
from Model import News
from Spider import NewsSpider


class newscricn:
    def __init__(self, stool, ftool):
        self.pages = set()
        self.STOOL = stool
        self.FTOOL = ftool

    def getLinks(self, pageUrl):
        bsObj = self.STOOL.getBsObj(pageUrl)
        for div in bsObj.findAll('div', {'class': 'tit-list'}):
            for link in div.findAll('a'):
                if link.attrs['href'] not in self.pages:
                    newPage = link.attrs['href']
                    if newPage[:4] != 'http':
                        newPage = 'http://news.cri.cn' + newPage
                    self.pages.add(newPage)

    def getNews(self, pageUrl):
        try:
            news = News.News()
            bsObj = self.STOOL.getBsObj(pageUrl)
            text = bsObj.find('div', {'id': 'abody'})
            title = bsObj.find('h1', {'id': 'goTop'})
            info = bsObj.find('div', {'class': 'info'})
            if title is None or info is None:
                info = bsObj.find('div', {'class': 'slider-top'})
                title = info.find('h3')
                time = info.find('div', {'class': 'slider-tinfo-left'}).find('span').text
                content = str(info) + str(text)
                Type = '全国两会'
            else:
                time = bsObj.find('span', {'id': 'acreatedtime'}).text
                Type = bsObj.find('div', {'class': 'crumbs'})
                if Type is not None:
                    Type = Type.find_all('a')[1].text
                else:
                    Type = '其他'
                content = str(title) + str(info) + str(text)
            time = NewsSpider.getTimeInfo(time)
            news.time1 = time[0]
            news.time2 = time[1]
            news.title = title.text.strip()
            news.type = Type
            self.FTOOL.saveFile(pageUrl, content, news)
        except AttributeError:
            print('AttributeError')

    def CrawlPage(self):
        for i in range(1, 11):  # 1-11
            if i is 1:
                self.getLinks("http://news.cri.cn/roll")
            else:
                self.getLinks("http://news.cri.cn/roll-" + str(i) + "")
        for page in self.pages:
            self.getNews(page)


if __name__ == '__main__':
    spider = newscricn()