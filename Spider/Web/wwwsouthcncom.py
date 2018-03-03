import Web.NewsSpider as ns

pages = set()
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
        title = bsObj.find('h2', {'id':'article_title'}).text.strip()
        time = ns.getTimeInfo(bsObj.find('span', {'id':'pubtime_baidu'}).text)
        Type = bsObj.find('div', {'id':'2014_ad01'}).find_all('a')[-1].text
        params = [title, time[0], time[1], Type]
        content = str(news)
        ns.saveFile(pageUrl, content, params)
    except AttributeError:
        print('AttributeError')

def CrawlPage():
    for i in range(39,51):
        if i is 1:
            getLinks("http://www.southcn.com/pc2016/yw/node_346416.htm")
        else:
            getLinks("http://www.southcn.com/pc2016/yw/node_346416_"+str(i)+".htm")
