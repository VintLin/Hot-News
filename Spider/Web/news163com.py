# -*- coding: utf-8 -*-
"""
Created on Mon Feb 26 17:01:35 2018

@author: Voter
"""
from Spider.Website import Website
import re


class news163com(Website):
    def fromRank(self):
        self.getLinks("http://news.163.com/rank/")

    def getLinks(self, url):
        bs_obj = self.S.getBsObj(url)
        for div in bs_obj.findAll('div', {'class': 'area-half'}):
            for link in div.findAll('a'):
                if link.attrs['href'] not in self.pages:
                    news_page = link.attrs['href']
                    self.pages.add(news_page)

    def getTime(self, bs_obj):
        time = bs_obj.find('div', {'class': 'post_time_source'})
        if not time:
            time = bs_obj.find('span', {'class': 'info'})
        time = self.S.getTimeInfo(time.text)
        return time

    def getTitle(self, bs_obj):
        title = bs_obj.find('div', {'id': 'epContentLeft'}).find('h1').text.strip()
        return title

    def getSource(self, bs_obj):
        source = bs_obj.find('a', {'id': 'ne_article_source'}).text
        return source

    def getEditor(self, bs_obj):
        editor = bs_obj.find('span', {'class': 'ep-editor'}).text
        return editor

    def getText(self, bs_obj):
        text = bs_obj.find('div', {'id': 'endText'})
        if re.search('[\u4e00-\u9fa5]', text.text) is None:
            text = bs_obj.find('div', {'class': 'end-text'}).find_parents('div')
        return str(text)

    def getType(self, bs_obj):
        type = bs_obj.find('div', {'class': 'post_crumb'}).find_all('a')[-1].text
        type = re.sub('(网易)|(\n)', '', type)
        if type is '\n' or not type:
            type = '其他'
        return type

    def getImage(self, bs_obj):
        text = bs_obj.find('div', {'id': 'endText'})
        if re.search('[\u4e00-\u9fa5]', text.text) is None:
            text = bs_obj.find('div', {'class': 'end-text'}).find_parents('div')
        image = text.find('img')
        if image:
            return image.attrs['src']
        else:
            return ''


if __name__ == '__main__':
    spider = news163com()
    spider.getParams("http://home.163.com/18/0528/07/DISICLPS001081EI.html")
