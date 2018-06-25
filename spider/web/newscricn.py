# -*- coding: utf-8 -*-
"""
Created on Mon Feb 26 17:01:35 2018

@author: Voter
"""
from spider.website import Website, get_soup
from lxml import etree


class newscricn(Website):
    def from_rank(self):
        for i in range(1, 11):  # 1-11
            if i is 1:
                self.get_links("http://news.cri.cn/roll")
            else:
                self.get_links("http://news.cri.cn/roll-" + str(i) + "")

    def get_links(self, url):
        bs_obj = get_soup(url)
        for div in bs_obj.findAll('div', {'class': 'tit-list'}):
            for link in div.findAll('a'):
                if link.attrs['href'] not in self.pages:
                    new_page = link.attrs['href']
                    if new_page[:4] != 'http':
                        new_page = 'http://news.cri.cn' + new_page
                    self.pages.add(new_page)

    def get_time_by_x(self, x):
        time = x.xpath(".//*[@id='acreatedtime']/text()")
        return time[0]

    def get_title_by_x(self, x):
        title = x.xpath(".//*[@id='goTop']/text()")
        return title[0]

    def get_source_by_x(self, x):
        source = x.xpath(".//*[@id='asource']/a/text()")
        if not source:
            source = x.xpath(".//*[@id='asource']/text()")
            source = source[0].split('：')[1]
        else:
            source = source[0]
        return source

    def get_editor_by_x(self, x):
        editor = x.xpath(".//*[@id='aeditor']/text()")[0].split("：")[1]
        return editor

    def get_text_by_x(self, x):
        data = x.xpath(".//*[@id='abody']")[0]
        text = etree.tostring(data, method='html')
        return text

    def get_type_by_x(self, x):
        Type = x.xpath(".//div[@class='crumbs']/a[2]/text()")
        return Type

    def get_image_by_x(self, x):
        image = x.xpath(".//*[@id='abody']/p/img/@src")
        return image

    # def getTime(self, bs_obj):
    #     time = bs_obj.find('span', {'id': 'acreatedtime'}).text
    #     time = self.S.getTimeInfo(time)
    #     return time

    # def getTitle(self, bs_obj):
    #     title = bs_obj.find('h1', {'id': 'goTop'}).text
    #     return title
    #
    # def getSource(self, bs_obj):
    #     source = bs_obj.find('span', {'id': 'asource'})
    #     if source.find('a') is None:
    #         source = source.text.split('：')[1]
    #     else:
    #         source = source.find('a').text
    #     return source
    #
    # def getEditor(self, bs_obj):
    #     editor = bs_obj.find('span', {'id': 'aeditor'}).text.split('：')[1]
    #     return editor
    #
    # def getText(self, bs_obj):
    #     text = bs_obj.find('div', {'id': 'abody'})
    #     return str(text)
    #
    # def getType(self, bs_obj):
    #     type = bs_obj.find('div', {'class': 'crumbs'})
    #     if type is not None:
    #         type = type.find_all('a')[1].text
    #     else:
    #         type = '其他'
    #     return type
    #
    # def getImage(self, bs_obj):
    #     text = bs_obj.find('div', {'id': 'abody'})
    #     image = text.find('img')
    #     if image:
    #         return image.attrs['src']
    #     else:
    #         return ''


if __name__ == '__main__':
        spider = newscricn()
        # spider.getParams(" http://news.cri.cn/20180611/361770dd-9d77-4e1e-efdf-5e17e97dc250.html")
        spider.crawl()
