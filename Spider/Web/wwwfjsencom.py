from urllib.error import HTTPError, URLError
from urllib.request import urlretrieve
from Spider import NewsSpider
from Model import News
import re


class wwwfjsencom:
    def __init__(self, stool, ftool):
        self.pages = set()
        self.STOOL = stool
        self.FTOOL = ftool

    def getLinks(self, pageUrl):
        bsObj = self.STOOL.getBsObj(pageUrl)
        for ul in bsObj.findAll('ul', {'class': 'list_page'}):
            for link in ul.findAll('a'):
                if link.attrs['href'] not in self.pages:
                    newPage = link.attrs['href']
                    if newPage[:4] != 'http':
                        newPage = 'http://fjnews.fjsen.com/' + newPage
                    self.pages.add(newPage)

    def getNews(self, pageUrl):
        try:
            news = News.News()
            bsObj = self.STOOL.getBsObj(pageUrl)
            head = bsObj.find('div', {'class': 'cont_head'})
            if head is None:
                head = bsObj.find('div', {'class': 'line'})
                title = head.find('div', {'class': 'big_title'}).find('h1').text
                text = bsObj.find('div', {'id': 'zoom'})
                mnue = text.find('div', {'id': 'displaypagenum'})
                if mnue is not None:
                    nextPage = mnue.find('a', text='下一页')
                    if nextPage is not None:
                        nextPage = nextPage.attrs['href']
                        nextPage = re.sub('content.*htm', nextPage, pageUrl)
                        self.getNews(nextPage)
                images = text.find_all('img')
                for img in images:
                    imgUrl = 'fjnews.fjsen.com/' + img['src'].replace('../', '')
                    self.FTOOL.makeDir(imgUrl)
                    urlretrieve('http://' + imgUrl, imgUrl)
            else:
                title = head.find('h1').text
                text = bsObj.find('div', {'class': 'cont-news'})
            content = str(head) + str(text)
            time = NewsSpider.getTimeInfo(bsObj.find('span', {'id': 'pubtime_baidu'}).text)
            news.time1 = time[0]
            news.time2 = time[1]
            news.title = title.strip()
            news.type = bsObj.find('td', {'class': 'path_tx'}).find_all('a')[-1].text
            self.FTOOL.saveFile(pageUrl, content, news)
        except AttributeError:
            print('AttributeError')
        except FileNotFoundError:
            print('FileNotFoundError')
        except (HTTPError, URLError):
            print('HTTPError')

    def CrawlPage(self):
        for i in range(1, 11):
            if i is 1:
                self.getLinks('http://fjnews.fjsen.com/fjssyw.htm')
            else:
                self.getLinks('http://fjnews.fjsen.com/fjssyw_' + str(i) + '.htm')
        for page in self.pages:
            self.getNews(page)


if __name__ == '__main__':
    spider = wwwfjsencom()
