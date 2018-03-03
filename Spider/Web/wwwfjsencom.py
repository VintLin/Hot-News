from urllib.error import HTTPError, URLError
from urllib.request import urlretrieve
import re
import Web.NewsSpider as ns

pages = set()
def getLinks(pageUrl):
    global pages
    bsObj = ns.getBsObj(pageUrl)
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
        bsObj = ns.getBsObj(pageUrl)
        head = bsObj.find('div', {'class':'cont_head'})
        if head is None:
            head = bsObj.find('div', {'class':'line'})
            title = head.find('div', {'class':'big_title'}).find('h1').text
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
                imgUrl = 'fjnews.fjsen.com/' + img['src'].replace('../','')
                ns.makeDir(imgUrl)
                urlretrieve('http://'+imgUrl, imgUrl)
        else:
            title = head.find('h1').text
            news = bsObj.find('div', {'class':'cont-news'})
        Type = bsObj.find('td',{'class':'path_tx'}).find_all('a')[-1].text
        time = ns.getTimeInfo(bsObj.find('span', {'id':'pubtime_baidu'}).text)
        content = str(head) + str(news)
        params = [title.strip(), time[0], time[1], Type]
        ns.saveFile(pageUrl, content, params)
    except AttributeError:
        print('AttributeError')
    except (HTTPError, URLError):
        print('HTTPError')

def CrawlPage():
    for i in range(1,11):
        if i is 1:
            getLinks('http://fjnews.fjsen.com/fjssyw.htm')
        else:
            getLinks('http://fjnews.fjsen.com/fjssyw_'+str(i)+'.htm')

