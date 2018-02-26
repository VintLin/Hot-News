from bs4 import BeautifulSoup
import requests
import re
import os

pages = set()
count = 0
def getLinks(pageUrl):
    global pages
    bsObj = getBsObj(pageUrl)
    for div in bsObj.findAll('div', {'class':'j-link'}):
        for link in div.findAll('a'):
            if link.attrs['href'] not in pages:
                newPage = link.attrs['href']
                print(newPage)
                getNews(newPage)
                pages.add(newPage)
    
def getNews(pageUrl):
    try:
        bsObj = getBsObj(pageUrl)
        news = bsObj.find('div', {'class':'m-article'})
        content = str(news)
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
        dirUrl = re.sub('http://.*?/','',dirUrl)
    alldirUrl = ''
    for d in dirUrl.split('/')[:-1]:
        alldirUrl = alldirUrl +'/'+ d
        if not os.path.exists('.'+alldirUrl):
            os.mkdir('.'+alldirUrl)
    alldirUrl = '.' + alldirUrl
    print(alldirUrl)
    file = re.sub('\?.*','',dirUrl.split('/')[-1])
    with open(alldirUrl + '/'+file,'w',encoding='utf-8') as w:
            w.write(content)
            count = count + 1
    return True

for i in range(39,51):
    print('count : ', i)
    if i is 1:
        getLinks("http://www.southcn.com/pc2016/yw/node_346416.htm")
    else:
        getLinks("http://www.southcn.com/pc2016/yw/node_346416_"+str(i)+".htm")
print('webpage : ', count)
