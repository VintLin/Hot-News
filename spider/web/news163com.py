# -*- coding: utf-8 -*-
"""
Created on Mon Feb 26 17:01:35 2018

@author: Voter
"""
from spider.website import Website, get_soup
from lxml import etree


class news163com(Website):
    def from_rank(self):
        self.get_links("http://news.163.com/rank/")

    def get_links(self, url):
        bs_obj = get_soup(url)
        for div in bs_obj.findAll('div', {'class': 'area-half'}):
            for link in div.findAll('a'):
                if link.attrs['href'] not in self.pages:
                    news_page = link.attrs['href']
                    self.pages.add(news_page)

    def get_time_by_x(self, x):
        time = x.xpath(".//*[@id='epContentLeft']/div[1]/text()")
        if not time:
            time = x.xpath(".//span[@class='info']/text()")
        return time[0]

    def get_title_by_x(self, x):
        title = x.xpath(".//*[@id='epContentLeft']/h1/text()")
        if not title:
            title = x.xpath(".//*[@id='h1title']/text()")
        return title[0]

    def get_source_by_x(self, x):
        source = x.xpath(".//*[@id='ne_article_source']/text()")
        if source:
            source = source[0]
        else:
            source = '佚名'
        return source

    def get_editor_by_x(self, x):
        editor = x.xpath(".//*[@class='ep-editor']/text()")
        if editor:
            editor = editor[0].split('：')[-1]
        else:
            editor = "佚名"
        return editor

    def get_text_by_x(self, x):
        data = x.xpath(".//*[@id='endText']")[0]
        text = etree.tostring(data, method='html')
        return text

    def get_type_by_x(self, x):
        Type = x.xpath(".//div[@class='post_crumb']/a[2]/text()")
        return Type

    def get_image_by_x(self, x):
        image = x.xpath(".//*[@id='endText']/p/img/@src")
        return image

    # def getTime(self, bs_obj):
    #     time = bs_obj.find('div', {'class': 'post_time_source'})
    #     if not time:
    #         time = bs_obj.find('span', {'class': 'info'})
    #     time = self.S.getTimeInfo(time.text)
    #     return time
    #
    # def getTitle(self, bs_obj):
    #     title = bs_obj.find('div', {'id': 'epContentLeft'}).find('h1').text.strip()
    #     return title
    #
    # def getSource(self, bs_obj):
    #     source = bs_obj.find('a', {'id': 'ne_article_source'}).text
    #     return source
    #
    # def getEditor(self, bs_obj):
    #     editor = bs_obj.find('span', {'class': 'ep-editor'}).text
    #     return editor.split('：')[-1]
    #
    # def getText(self, bs_obj):
    #     text = bs_obj.find('div', {'id': 'endText'})
    #     if re.search('[\u4e00-\u9fa5]', text.text) is None:
    #         text = bs_obj.find('div', {'class': 'end-text'}).find_parents('div')
    #     return str(text)
    #
    # def getType(self, bs_obj):
    #     type = bs_obj.find('div', {'class': 'post_crumb'}).find_all('a')[-1].text
    #     type = re.sub('(网易)|(\n)', '', type)
    #     if type is '\n' or not type:
    #         type = '其他'
    #     return type
    #
    # def getImage(self, bs_obj):
    #     text = bs_obj.find('div', {'id': 'endText'})
    #     if re.search('[\u4e00-\u9fa5]', text.text) is None:
    #         text = bs_obj.find('div', {'class': 'end-text'}).find_parents('div')
    #     image = text.find('img')
    #     if image:
    #         return image.attrs['src']
    #     else:
    #         return ''


if __name__ == '__main__':
    spider = news163com()
    spider.crawl()
    # spider.get_fields("http://lady.163.com/18/0621/11/DKQQPPIT00267VA9.html")