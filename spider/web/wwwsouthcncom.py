# -*- coding: utf-8 -*-
"""
Created on Mon Feb 26 17:01:35 2018

@author: Voter
"""
from spider.website import Website, get_soup
from lxml import etree


class wwwsouthcncom(Website):
    def from_rank(self):
        for i in range(1, 40):
            if i is 1:
                self.get_links("http://www.southcn.com/pc2016/yw/node_346416.htm")
            else:
                self.get_links("http://www.southcn.com/pc2016/yw/node_346416_" + str(i) + ".htm")

    def get_links(self, url):
        bs_obj = get_soup(url)
        for div in bs_obj.findAll('div', {'class': 'itm'}):
            for link in div.findAll('a'):
                if link.attrs['href'] not in self.pages:
                    new_page = link.attrs['href']
                    self.pages.add(new_page)

    def get_time_by_x(self, x):
        time = x.xpath(".//span[@id='pubtime_baidu']/text()")[0]
        return time

    def get_title_by_x(self, x):
        title = x.xpath(".//h2[@id='article_title']/text()")[0].strip()
        return title

    def get_source_by_x(self, x):
        source = x.xpath(".//span[@id='source_baidu']/text()")[0].split('：')[1]
        return source

    def get_editor_by_x(self, x):
        editor = x.xpath(".//div[@class='m-editor']/text()")[0].split('：')[1]
        return editor

    def get_text_by_x(self, x):
        data = x.xpath(".//div[@id='content']")[0]
        text = etree.tostring(data, method='html')
        return text

    def get_type_by_x(self, x):
        type = x.xpath(".//a[@class=crm-link]/text()")
        if type:
            type = type[0]
        else:
            type = '其他'
        return type

    def get_image_by_x(self, x):
        image = x.xpath(".//div[class='m-article']/p/img/@src")
        return image

    # def getTime(self, bs_obj):
    #     time = bs_obj.find('span', {'id': 'pubtime_baidu'}).text
    #     time = self.S.getTimeInfo(time)
    #     return time
    #
    # def getTitle(self, bs_obj):
    #     title = bs_obj.find('h2', {'id': 'article_title'}).text.strip()
    #     return title
    #
    # def getSource(self, bs_obj):
    #     source = bs_obj.find('span', {'id': 'source_baidu'}).text.split('：')[1]
    #     return source
    #
    # def getEditor(self, bs_obj):
    #     editor = bs_obj.find('div', {'class': 'm-editor'}).text.split('：')[1]
    #     return editor
    #
    # def getText(self, bs_obj):
    #     text = bs_obj.find('div', {'class': 'm-article'})
    #     return text
    #
    # def getType(self, bs_obj):
    #     type = bs_obj.find('a', {'class': 'crm-link'})
    #     if type is None or len(type) is 0:
    #         type = '其他'
    #     else:
    #         type = type.text
    #     return type
    #
    # def getImage(self, bs_obj):
    #     text = bs_obj.find('div', {'class': 'm-article'})
    #     image = text.find('img')
    #     if image:
    #         return image.attrs['src']
    #     else:
    #         return ''


if __name__ == '__main__':
    spider = wwwsouthcncom()
    spider.crawl()
