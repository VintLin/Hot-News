# -*- coding: utf-8 -*-
"""
Created on Mon Feb 26 17:01:35 2018

@author: Voter
"""
import requests
import re
from lxml import etree
from bs4 import BeautifulSoup
from abc import abstractmethod
from requests import HTTPError
from model.model import News
from pipeline.image_dispose import save_image
from pipeline.data_dispose import save_file

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh;Intel Mas OS X 10_9_5)AppleWebKit 537.36 (KHTML, like Gecko) Chrome',
    'Accept': 'text/html,application/xhtml+xml, application/xml; q=0.9, image/webp, */*, q=0.8'
}
BASE = '''
        {% extends "newsbase.html" %} 
        {% import "bootstrap/wtf.html" as wtf %} 
        {% block title %}HotNews{% endblock %} 
        {% block page_content %}
        @ 
        {% endblock %}
        '''
TEMPLATE = '''
        <div class = 'news'>
            <div class = 'title'>
                <h2><strong>{}</strong><small>{}</small></h2>
            </div>
            <div class = 'post_time_source'>
                <p class='text-left text-muted'>{}
                    <span class="glyphicon glyphicon-eye-open" style="margin-left:20px"></span> {}
                    <span class="glyphicon glyphicon-thumbs-up" style="margin-left:20px"></span> {}
                    <span class="glyphicon glyphicon-folder-open" style="margin-left:20px"></span> {}
                </p>
            </div>
            <p class="lead">
                {}
            </p>
            <div class = 'content'>
                <h4>{}</h4>
            </div>
        </div>
                '''


def get_html(url, params=''):
    try:
        if params:
            r = requests.get(url, headers=HEADERS, params=params)
        else:
            r = requests.get(url, headers=HEADERS)
        r.raise_for_status()
        if r.encoding != 'utf-8':
            r.encoding = r.apparent_encoding
        return r.text
    except:
        print('GET HTML Error')


def get_xpath(url):
    try:
        r = get_html(url)
        x = etree.HTML(r)
        return x
    except:
        print('GET XPATH ERROR')


def get_soup(url):  # 获取BeautifulSoup对象
    try:
        r = get_html(url)
        soup = BeautifulSoup(r, 'html.parser')
        return soup
    except:
        print('GET SOUP ERROR')


class Website(object):
    def __init__(self):
        self.pages = set()

    def get_fields(self, url):
        print('url : ', url)
        try:
            news = News()
            x = get_xpath(url)
            url = re.sub('http://', '', url)
            news.website = url.split('/')[0].strip()
            news.filename = re.sub('\..*htm.*', '.html', url.split('/')[-1])
            news.time = self.format_time(x)
            news.title = self.get_title_by_x(x)
            news.source = self.get_source_by_x(x)
            news.editor = self.get_editor_by_x(x)
            news.type = self.get_type(x)
            if not news.is_in_table():
                path = '/{}/{}/'.format(news.type, news.time[:10])
                news.path = '/page' + path + news.filename
                news.img_path = '/news_image' + path
                news.img_filename = self.get_image(news.img_path, x)
                self.get_content(news, x)
                news.insert_without_return()
                print("success save")
            else:
                print("the news is in table")
            return True
        except AttributeError:
            print('WEBSITE: Attribute Error')
        except IndexError:
            print('WEBSITE: Index Error')
        # except UnicodeEncodeError:
        #     print("WEBSITE: Unicode Encode Error")
        except HTTPError:
            print('WEBSITE: HTTP Error')

    def crawl(self):
        self.from_rank()
        for page in self.pages:
            self.get_fields(page)

    def format_time(self, x):
        time = self.get_time_by_x(x)
        time1 = re.search('[0-9]+-[0-9]+-[0-9]+', time).group()
        time2 = re.search('[0-9]+:[0-9]+:[0-9]+', time)
        if time2 is None:
            time2 = re.search('[0-9]+:[0-9]+', time).group() + ':00'
        else:
            time2 = time2.group()
        return time1 + ' ' + time2

    def get_image(self, path, x):
        image_url = self.get_image_by_x(x)
        filename = ''
        if image_url and isinstance(image_url, list):
            image_url = image_url[0]
        elif not image_url:
            image_url = ""
        if image_url:
            print(image_url)
            r = requests.get(image_url, headers=HEADERS)
            r.raise_for_status()
            filename = re.sub('\?.*|#.*', '', image_url.split('/')[-1])
            save_image(r.content, path + filename, path + '200X-' + filename)
        return filename

    def get_content(self, news, x, small_title='', lead=''):
        text = self.get_text_by_x(x)
        text = str(text).replace('\\r', '').replace('\\n', '\n').replace('\\t', '\t')[2:-1]
        ts = '时间 : {}   来源 : {}   编辑 : {}   '.format(news.time, news.source, news.editor)
        content = TEMPLATE.format(news.title, small_title, ts,
                                  '{{operand.browse}}', '{{operand.thumb}}', '{{operand.collect}}',
                                  lead, text)
        content = BASE.replace('@', content)
        save_file(content, news.path)
        return content

    def get_type(self, x):
        Type = self.get_type_by_x(x)
        if Type and isinstance(Type, list):
            Type = Type[0]
        elif not Type:
            Type = "其他"
        return Type

    @abstractmethod
    def get_links(self, url):
        pass

    @abstractmethod
    def from_rank(self):
        pass

    @abstractmethod
    def get_time_by_x(self, x):
        pass

    @abstractmethod
    def get_title_by_x(self, x):
        pass

    @abstractmethod
    def get_source_by_x(self, x):
        pass

    @abstractmethod
    def get_editor_by_x(self, x):
        pass

    @abstractmethod
    def get_text_by_x(self, x):
        pass

    @abstractmethod
    def get_type_by_x(self, x):
        pass

    @abstractmethod
    def get_image_by_x(self, x):
        pass

    # def get_by_soup(self, url):
    #     bs_obj = self.S.getBsObj(url)
    #     time = self.getTime(bs_obj)
    #     title = self.getTitle(bs_obj)
    #     source = self.getSource(bs_obj)
    #     editor = self.getEditor(bs_obj)
    #     text = self.getText(bs_obj)
    #     type = self.getType(bs_obj)
    #     image = self.getImage(bs_obj)
    #     content = self.S.getContent(title=title, time=time, source=source, editor=editor, text=text)
    #     news = News(title=title, time=time, type=type)
    #     self.F.saveFile(url, content, image, news)
    #     return True

    # @abstractmethod
    # def getTime(self, bs_obj): pass
    #
    # @abstractmethod
    # def getTitle(self, bs_obj): pass
    #
    # @abstractmethod
    # def getSource(self, bs_obj): pass
    #
    # @abstractmethod
    # def getEditor(self, bs_obj): pass
    #
    # @abstractmethod
    # def getText(self, bs_obj): pass
    #
    # @abstractmethod
    # def getType(self, bs_obj): pass
    #
    # @abstractmethod
    # def getImage(self, bs_obj): pass
