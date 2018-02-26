from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from urllib.request import urlretrieve
from bs4 import BeautifulSoup
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
    try:
        html = urlopen(pageUrl)
        bsObj = BeautifulSoup(html, 'html.parser')
        head = bsObj.find('div', {'class':'cont_head'})
        if head is None:
            head = bsObj.find('div', {'class':'line'})
            news = bsObj.find('div', {'id':'zoom'})
            mnue = news.find('div', {'id':'displaypagenum'})
            if mnue is not None:
                nextPage = mnue.find('a', text='下一页')                
                if nextPage is not None:
                    nextPage = nextPage.attrs['href']
                    nextPage = re.sub('content.*htm', nextPage, pageUrl)
                    getNews(nextPage)
            images = news.find_all('img')
            for img in images:
                imgUrl = img['src'].replace('../','')
                mkDirs(imgUrl)
                urlretrieve('http://fjnews.fjsen.com/'+imgUrl, imgUrl)
        else:
            news = bsObj.find('div', {'class':'cont-news'})
        content = str(head) + str(news)
        saveFile(pageUrl, content)
    except AttributeError:
        print('AttributeError')
    except (HTTPError, URLError):
        print('HTTPError')

def mkDirs(dirUrl):
    alldirUrl = ''
    for d in dirUrl.split('/')[:-1]:
        alldirUrl = alldirUrl +'/'+ d
        if not os.path.exists('.'+alldirUrl):
            os.mkdir('.'+alldirUrl)
    return '.' + alldirUrl

def saveFile(dirUrl, content):
    if dirUrl[:4] == 'http':
        dirUrl = re.sub('http:.*\.com/','',dirUrl)
    alldirUrl = ''
    for d in dirUrl.split('/')[:-1]:
        alldirUrl = alldirUrl +'/'+ d
        if not os.path.exists('.'+alldirUrl):
            os.mkdir('.'+alldirUrl)
    alldirUrl = '.' + alldirUrl
    print(alldirUrl)
    with open(alldirUrl + '/'+dirUrl.split('/')[-1],'w',encoding='utf-8') as w:
            w.write(content)
    return True

for i in range(1,11):
    print("count : ",i)
    if i is 1:
        getLinks('http://fjnews.fjsen.com/fjssyw.htm')
    else:
        getLinks('http://fjnews.fjsen.com/fjssyw_'+str(i)+'.htm')
    
    

