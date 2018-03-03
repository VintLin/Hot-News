# -*- coding: utf-8 -*-
"""
Created on Mon Feb 26 17:01:35 2018

@author: 11796
"""
import Web.NewsSpider as ns

pages = set()
def getLinks(pageUrl):
    global pages
    global count
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
        if title is None or info is None:
            info = bsObj.find('div', {'class':'slider-top'})
            title = info.find('h3')
            time = ns.getTimeInfo(info.find('div', {'class':'slider-tinfo-left'}).find('span').text)
            content = str(info) + str(news)
            Type = '全国两会'
        else :
            time = ns.getTimeInfo(bsObj.find('span', {'id':'acreatedtime'}).text)        
            Type = bsObj.find('div', {'class':'crumbs'})
            if Type is not None:
                Type = Type.find_all('a')[1].text
            else:
                Type = ''
            content = str(title) + str(info) + str(news)  
        params = [title.text.strip(), time[0], time[1], Type]
        ns.saveFile(pageUrl, content, params)
    except AttributeError:
        print('AttributeError')

def CrawlPage():
    for i in range(1,11):
        if i is 1:
            getLinks("http://news.cri.cn/roll")
        else:
            return
            getLinks("http://news.cri.cn/roll-"+str(i)+"")