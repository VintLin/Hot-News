from Spider import NewsSpider
from Model import News
import re


class news163com:
    def __init__(self, stool, ftool):
        self.pages = set()
        self.STOOL = stool
        self.FTOOL = ftool

    def getLinks(self, pageUrl):
        bsObj = self.STOOL.getBsObj(pageUrl)
        for div in bsObj.findAll('div', {'class': 'area-half'}):
            for link in div.findAll('a'):
                if link.attrs['href'] not in self.pages:
                    newPage = link.attrs['href']
                    self.pages.add(newPage)

    def getNews(self, pageUrl):
        try:
            news = News.News()
            bsObj = self.STOOL.getBsObj(pageUrl)
            text = bsObj.find('div', {'id': 'endText'})
            if re.search('[\u4e00-\u9fa5]', text.text) is None:
                text = bsObj.find('div', {'class': 'end-text'}).find_parents('div')
            time = bsObj.find('div', {'class': 'post_time_source'})
            title = bsObj.find('div', {'id': 'epContentLeft'}).find('h1')
            content = str(title) + str(time) + str(text)  # <div class="lead">

            time = NewsSpider.getTimeInfo(time.text)
            news.time1 = time[0]
            news.time2 = time[1]
            news.type = re.sub('网易', '', bsObj.find('div', {'class': 'post_crumb'}).find_all('a')[-1].text)
            news.title = title.text.strip()

            self.FTOOL.saveFile(pageUrl, content, news)
        except AttributeError:
            print('AttributeError')

    def CrawlPage(self):
        self.getLinks("http://news.163.com/rank/")
        for page in self.pages:
            self.getNews(page)


if __name__ == '__main__':
    spider = news163com()