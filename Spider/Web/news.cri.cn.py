# -*- coding: utf-8 -*-
"""
Created on Mon Feb 26 17:01:35 2018

@author: 11796
"""
import sys
sys.path.append('..')
import NewsSpider as ns

pages = set()
count = 0
def getLinks(pageUrl):
    global pages
    bsObj = ns.getBsObj(pageUrl)
    for div in bsObj.findAll('div', {'class':'tit-list'}):
        for link in div.findAll('a'):
            if link.attrs['href'] not in pages:
                newPage = link.attrs['href']
                if newPage[:4] != 'http':
                    newPage = 'http://news.cri.cn' + newPage
                    print(newPage)
                    getNews(newPage)
                    pages.add(newPage)
    
def getNews(pageUrl):
    try:
        bsObj = ns.getBsObj(pageUrl)
        news = bsObj.find('div', {'id':'abody'})
        title = bsObj.find('h1', {'id':'goTop'})
        info = bsObj.find('div', {'class':'info'})
        content = str(title) + str(info) + str(news)
        ns.saveFile(pageUrl, content)
    except AttributeError:
        print('AttributeError')

def CrawlPage():
    for i in range(1,11):
        print("count :", i)
        if i is 1:
            getLinks("http://news.cri.cn/roll")
        else:
            getLinks("http://news.cri.cn/roll-"+str(i)+"")
    print("webpage : ", count)
