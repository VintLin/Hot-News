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
                newPage = newPage
                getNews(newPage)
                pages.add(newPage)
    
def getNews(pageUrl):
    try:
        bsObj = ns.getBsObj(pageUrl)
        news = bsObj.find('div', {'id':'endText'})
        time = bsObj.find('div', {'class':'post_time_source'})
        time1 = ns.getTimeInfo(time.text)[0]
        time2 = ns.getTimeInfo(time.text)[1]
        title = bsObj.find('div', {'id':'epContentLeft'}).find('h1')
        Type = re.sub('网易', '', bsObj.find('div', {'class':'post_crumb'}).find_all('a')[-1].text)
        if re.search('[\u4e00-\u9fa5]',news.text) is None:
            news = bsObj.find('div', {'class':'end-text'}).find_parents('div')
        content = str(title) + str(time) + str(news)
        params = [title.text.strip(), time1, time2, Type]
        ns.saveFile(pageUrl, content, params)
    except AttributeError:
        print('AttributeError')

def CrawlPage():
    getLinks("http://news.163.com/rank/")
CrawlPage()