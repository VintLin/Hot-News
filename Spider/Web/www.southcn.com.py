import sys
sys.path.append('..')
import NewsSpider as ns

pages = set()
count = 0
def getLinks(pageUrl):
    global pages
    bsObj = ns.getBsObj(pageUrl)
    for div in bsObj.findAll('div', {'class':'j-link'}):
        for link in div.findAll('a'):
            if link.attrs['href'] not in pages:
                newPage = link.attrs['href']
                print(newPage)
                getNews(newPage)
                pages.add(newPage)
    
def getNews(pageUrl):
    try:
        bsObj = ns.getBsObj(pageUrl)
        news = bsObj.find('div', {'class':'m-article'})
        content = str(news)
        ns.saveFile(pageUrl, content)
    except AttributeError:
        print('AttributeError')

def CrawlPage():
    for i in range(39,51):
        print('count : ', i)
        if i is 1:
            getLinks("http://www.southcn.com/pc2016/yw/node_346416.htm")
        else:
            getLinks("http://www.southcn.com/pc2016/yw/node_346416_"+str(i)+".htm")
    print('webpage : ', count)
