# -*- coding: utf-8 -*-
"""
Created on Mon Feb 26 17:01:35 2018

@author: Voter
"""
from Spider.Website import Website


class wwwsouthcncom(Website):
    def fromRank(self):
        for i in range(1, 40):
            if i is 1:
                self.getLinks("http://www.southcn.com/pc2016/yw/node_346416.htm")
            else:
                self.getLinks("http://www.southcn.com/pc2016/yw/node_346416_" + str(i) + ".htm")

    def getLinks(self, url):
        bs_obj = self.S.getBsObj(url)
        for div in bs_obj.findAll('div', {'class': 'j-link'}):
            for link in div.findAll('a'):
                if link.attrs['href'] not in self.pages:
                    new_page = link.attrs['href']
                    self.pages.add(new_page)

    def getTime(self, bs_obj):
        time = bs_obj.find('span', {'id': 'pubtime_baidu'}).text
        time = self.S.getTimeInfo(time)
        return time

    def getTitle(self, bs_obj):
        title = bs_obj.find('h2', {'id': 'article_title'}).text.strip()
        return title

    def getSource(self, bs_obj):
        source = bs_obj.find('span', {'id': 'source_baidu'}).text.split('：')[1]
        return source

    def getEditor(self, bs_obj):
        editor = bs_obj.find('div', {'class': 'm-editor'}).text.split('：')[1]
        return editor

    def getText(self, bs_obj):
        text = bs_obj.find('div', {'class': 'm-article'})
        return text

    def getType(self, bs_obj):
        type = bs_obj.find('a', {'class': 'crm-link'})
        if type is None or len(type) is 0:
            type = '其他'
        else:
            type = type.text
        return type

    def getImage(self, bs_obj):
        text = bs_obj.find('div', {'class': 'm-article'})
        image = text.find('img')
        if image:
            return image.attrs['src']
        else:
            return ''


if __name__ == '__main__':
    spider = wwwsouthcncom()
    spider.crawl()
