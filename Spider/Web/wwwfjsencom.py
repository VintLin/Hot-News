# -*- coding: utf-8 -*-
"""
Created on Mon Feb 26 17:01:35 2018

@author: Voter
"""
from Spider.Website import Website


class wwwfjsencom(Website):
    def fromRank(self):
        for i in range(1, 11):
            if i is 1:
                self.getLinks('http://fjnews.fjsen.com/fjssyw.htm')
            else:
                self.getLinks('http://fjnews.fjsen.com/fjssyw_' + str(i) + '.htm')

    def getLinks(self, url):
        bs_obj = self.S.getBsObj(url)
        for ul in bs_obj.findAll('ul', {'class': 'list_page'}):
            for link in ul.findAll('a'):
                if link.attrs['href'] not in self.pages:
                    new_page = link.attrs['href']
                    if new_page[:4] != 'http':
                        new_page = 'http://fjnews.fjsen.com/' + new_page
                    self.pages.add(new_page)

    def getTime(self, bs_obj):
        time = bs_obj.find('span', {'id': 'pubtime_baidu'}).text
        time = self.S.getTimeInfo(time)
        return time

    def getTitle(self, bs_obj):
        line = bs_obj.find('div', {'class': 'line'})
        if line is None:
            title = bs_obj.find('div', {'class': 'cont_head'}).find('h1').text
        else:
            title = line.find('div', {'class': 'big_title'}).find('h1').text
        return title.strip()

    def getSource(self, bs_obj):
        source = bs_obj.find('span', {'id': 'source_baidu'}).find('a').text
        return source

    def getEditor(self, bs_obj):
        editor = bs_obj.find('span', {'id': 'editor_baidu'}).text.split('：')[1]
        return editor

    def getText(self, bs_obj):
        text = bs_obj.find('div', {'id': 'zoom'})
        if text is None:
            text = bs_obj.find('div', {'class': 'cont-news'})
        images = text.find_all('img')
        text = text.text
        for img in images:
            text.replace(img['src'], 'fjnews.fjsen.com/{}'.format(img['src'].replace('../', '')))
        return str(text)

    def getType(self, bs_obj):
        type = bs_obj.find('td', {'class': 'path_tx'}).find_all('a')[-1].text
        return type

    def getImage(self, bs_obj):
        text = bs_obj.find('div', {'id': 'zoom'})
        if text is None:
            text = bs_obj.find('div', {'class': 'cont-news'})
        image = text.find('img')
        if image:
            return 'fjnews.fjsen.com/{}'.format(image['src'].replace('../', ''))
        else:
            return ''


if __name__ == '__main__':
    spider = wwwfjsencom()
    spider.crawl()
