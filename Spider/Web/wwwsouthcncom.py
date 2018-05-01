from Spider import NewsSpider
from Model import News


class wwwsouthcncom:
    def __init__(self, stool, ftool):
        self.pages = set()
        self.STOOL = stool
        self.FTOOL = ftool

    def getLinks(self, pageUrl):
        bsObj = self.STOOL.getBsObj(pageUrl)
        for div in bsObj.findAll('div', {'class': 'j-link'}):
            for link in div.findAll('a'):
                if link.attrs['href'] not in self.pages:
                    newPage = link.attrs['href']
                    self.pages.add(newPage)
                    print(newPage)

    def getNews(self, pageUrl):
        try:
            news = News.News()
            bsObj = self.STOOL.getBsObj(pageUrl)
            text = bsObj.find('div', {'class': 'm-article'})
            time = NewsSpider.getTimeInfo(bsObj.find('span', {'id': 'pubtime_baidu'}).text)
            Type = bsObj.find('a', {'class': 'crm-link'})
            if Type is None or len(Type) is 0:
                Type = '其他'
            else:
                Type = Type.text
            content = str(text)
            news.title = bsObj.find('h2', {'id': 'article_title'}).text.strip()
            news.time1 = time[0]
            news.time2 = time[1]
            news.type = Type
            self.FTOOL.saveFile(pageUrl, content, news)
        except AttributeError:
            print('AttributeError')

    def CrawlPage(self):
        for i in range(1, 50):
            if i is 1:
                self.getLinks("http://www.southcn.com/pc2016/yw/node_346416.htm")
            else:
                self.getLinks("http://www.southcn.com/pc2016/yw/node_346416_" + str(i) + ".htm")
        for page in self.pages:
            self.getNews(page)


if __name__ == '__main__':
    spider = wwwsouthcncom()
