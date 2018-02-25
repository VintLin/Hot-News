from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
import os
import re

pages = set()
def getLinks(pageUrl):
    global pages
    html = urlopen(pageUrl)
    bsObj = BeautifulSoup(html, 'html.parser')
    for ul in bsObj.findAll('ul', {'class':'list_page'}):
        for link in ul.findAll('a'):
            if link.attrs['href'] not in pages:
                newPage = link.attrs['href']
                if newPage[:4] != 'http':
                    newPage = 'http://fjnews.fjsen.com/' + newPage
                    print(newPage)
                    getNews(newPage)
                    pages.add(newPage)
                
def getNews(pageUrl):
    html = urlopen(pageUrl)
    bsObj = BeautifulSoup(html, 'html.parser')
    try:
        head = bsObj.find('div', {'class':'cont_head'})
        news = bsObj.find('div', {'class':'cont-news'})
        time = bsObj.find('span',{'id':'pubtime_baidu'}).text[:10]
        title = head.find('h1').text.strip()
        title = re.sub('[<>?|"\\\/*:]', '', title)
        #images = news.find_all('img')
    
        month = time[:7]
        day = time.split('-')[-1]
        content = str(head) + str(news)
    
        dirUrl = re.sub('http:.*\.com/','',pageUrl)
        print(dirUrl)
        alldirUrl = ''
        for d in dirUrl.split('/')[:-1]:
                alldirUrl = alldirUrl +'/'+ d
                if not os.path.exists('.'+alldirUrl):
                    os.mkdir('.'+alldirUrl)
        with open('.'+alldirUrl + '/'+title+'.txt','w',encoding='utf-8') as w:
            w.write(content)
    except AttributeError:
        print('AttributeError')
        
        
'''
    if not os.path.exists(month):
        os.mkdir(month)
    if not os.path.exists(month+'/'+day):
        os.mkdir(month+'/'+day)
    for img in images:
        imgUrl = img['src'].replace('../','')
        image = imgUrl.split('/')[-1]
        allImgUrl = ''
        for d in imgUrl.split('/')[:-1]:
            allImgUrl = allImgUrl +'/'+ d
            if not os.path.exists('.'+allImgUrl):
                os.mkdir('.'+allImgUrl)
        urlretrieve('http://news.fjsen.com/'+imgUrl, imgUrl)
'''
        
    
    
for i in range(2,10):
    print("count : ",i)
    if i is 1:
        getLinks('http://fjnews.fjsen.com/fjssyw.htm')
    else:
        getLinks('http://fjnews.fjsen.com/fjssyw_'+str(i)+'.htm')
    
    

