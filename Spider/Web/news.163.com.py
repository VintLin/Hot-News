import sys
sys.path.append('..')
import NewsSpider as ns
import re

pages = set()
def getLinks(pageUrl):
    global pages
    bsObj = ns.getBsObj(pageUrl)
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
        bsObj = ns.getBsObj(pageUrl)
        news = bsObj.find('div', {'id':'endText'})
        time = bsObj.find('div', {'class':'post_time_source'})
        title = bsObj.find('div', {'id':'epContentLeft'}).find('h1')
        if re.search('[\u4e00-\u9fa5]',news.text) is None:
            news = bsObj.find('div', {'class':'end-text'}).find_parents('div')
        content = str(title) + str(time) + str(news)
        ns.saveFile(pageUrl, content)
    except AttributeError:
        print('AttributeError')

def CrawlPage():
    getLinks("http://news.163.com/rank/")
