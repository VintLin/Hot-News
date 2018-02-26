from bs4 import BeautifulSoup
import requests
import re
import os

pages = set()
def getLinks(pageUrl):
    global pages
    bsObj = getBsObj(pageUrl)
    for div in bsObj.findAll('div', {'class':'area-half'}):
        for link in div.findAll('a'):
            if link.attrs['href'] not in pages:
                newPage = link.attrs['href']
                newPage = 'http://news.cri.cn' + newPage
                print(newPage)
                getNews(newPage)
                pages.add(newPage)
    
def getNews(pageUrl):
    try:
        bsObj = getBsObj(pageUrl)
        news = bsObj.find('div', {'id':'endText'})
        time = bsObj.find('div', {'class':'post_time_source'})
        title = bsObj.find('div', {'id':'epContentLeft'}).find('h1')
        if re.search('[\u4e00-\u9fa5]',news.text) is None:
            news = bsObj.find('div', {'class':'end-text'}).find_parents('div')
        content = str(title) + str(time) + str(news)
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

getLinks("http://news.163.com/rank/")
