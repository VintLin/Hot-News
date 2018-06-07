# -*- coding: utf-8 -*-
"""
Created on Mon Feb 26 17:01:35 2018

@author: Voter
"""
from Spider.Website import Website


class newscricn(Website):
    def fromRank(self):
        for i in range(1, 11):  # 1-11
            if i is 1:
                self.getLinks("http://news.cri.cn/roll")
            else:
                self.getLinks("http://news.cri.cn/roll-" + str(i) + "")

    def getLinks(self, url):
        bs_obj = self.S.getBsObj(url)
        for div in bs_obj.findAll('div', {'class': 'tit-list'}):
            for link in div.findAll('a'):
                if link.attrs['href'] not in self.pages:
                    new_page = link.attrs['href']
                    if new_page[:4] != 'http':
                        new_page = 'http://news.cri.cn' + new_page
                    self.pages.add(new_page)

    def getTime(self, bs_obj):
        time = bs_obj.find('span', {'id': 'acreatedtime'}).text
        time = self.S.getTimeInfo(time)
        return time

    def getTitle(self, bs_obj):
        title = bs_obj.find('h1', {'id': 'goTop'}).text
        return title

    def getSource(self, bs_obj):
        source = bs_obj.find('span', {'id': 'asource'})
        if source.find('a') is None:
            source = source.text.split('：')[1]
        else:
            source = source.find('a').text
        return source

    def getEditor(self, bs_obj):
        editor = bs_obj.find('span', {'id': 'aeditor'}).text.split('：')[1]
        return editor

    def getText(self, bs_obj):
        text = bs_obj.find('div', {'id': 'abody'})
        return str(text)

    def getType(self, bs_obj):
        type = bs_obj.find('div', {'class': 'crumbs'})
        if type is not None:
            type = type.find_all('a')[1].text
        else:
            type = '其他'
        return type

    def getImage(self, bs_obj):
        text = bs_obj.find('div', {'id': 'abody'})
        image = text.find('img')
        if image:
            return image.attrs['src']
        else:
            return ''


if __name__ == '__main__':
        spider = newscricn()
        spider.crawl()



