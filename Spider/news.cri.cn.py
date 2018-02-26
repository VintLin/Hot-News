# -*- coding: utf-8 -*-
"""
Created on Mon Feb 26 17:01:35 2018

@author: 11796
"""

from bs4 import BeautifulSoup
import requests
import re
import os

pages = set()
count = 0
def getLinks(pageUrl):
    global pages
    bsObj = getBsObj(pageUrl)
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
        bsObj = getBsObj(pageUrl)
        news = bsObj.find('div', {'id':'abody'})
        title = bsObj.find('h1', {'id':'goTop'})
        info = bsObj.find('div', {'class':'info'})
        content = str(title) + str(info) + str(news)
        saveFile(pageUrl, content)
    except AttributeError:
        print('AttributeError')

def getBsObj(pageUrl):
    try:
        r = requests.get(pageUrl)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        bsObj = BeautifulSoup(r.text, 'html.parser')
        return bsObj
    except:
        print('Error')

def saveFile(dirUrl, content):
    global count
    if dirUrl[:4] == 'http':
        dirUrl = re.sub('http:.*\.cn/','',dirUrl)
    alldirUrl = ''
    for d in dirUrl.split('/')[:-1]:
        alldirUrl = alldirUrl +'/'+ d
        if not os.path.exists('.'+alldirUrl):
            os.mkdir('.'+alldirUrl)
    alldirUrl = '.' + alldirUrl
    print(alldirUrl)
    file = re.sub('?.*','',dirUrl.split('/')[-1])
    with open(alldirUrl + '/'+ file,'w',encoding='utf-8') as w:
            w.write(content)
            count = count + 1
    return True
for i in range(1,11):
    print("count :", i)
    if i is 1:
        getLinks("http://news.cri.cn/roll")
    else:
        getLinks("http://news.cri.cn/roll-"+str(i)+"")
print("webpage : ", count)
