# -*- coding: utf-8 -*-
"""
Created on Mon Feb 26 17:01:35 2018

@author: Voter
"""
from abc import abstractmethod
from Spider import SpiderTool
from Model.model import News


class Website(object):
    def __init__(self):
        self.pages = set()
        self.S = SpiderTool.SpiderTool
        self.F = SpiderTool.FileTool

    def getParams(self, url):
        try:
            print('url : ', url)
            bs_obj = self.S.getBsObj(url)
            time = self.getTime(bs_obj)
            title = self.getTitle(bs_obj)
            source = self.getSource(bs_obj)
            editor = self.getEditor(bs_obj)
            text = self.getText(bs_obj)
            type = self.getType(bs_obj)
            image = self.getImage(bs_obj)
            content = self.S.getContent(title=title, time=time, source=source, editor=editor, text=text)
            news = News(title=title, time=time, type=type)
            print(title, time, source, type, image)
            self.F.saveFile(url, content, image, news)
        except AttributeError:
            print('AttributeError')
        except IndexError:
            print('IndexError')

    def crawl(self):
        self.fromRank()
        for page in self.pages:
            self.getParams(page)

    @abstractmethod
    def getLinks(self, url): pass

    @abstractmethod
    def fromRank(self): pass

    @abstractmethod
    def getTime(self, bs_obj): pass

    @abstractmethod
    def getTitle(self, bs_obj): pass

    @abstractmethod
    def getSource(self, bs_obj): pass

    @abstractmethod
    def getEditor(self, bs_obj): pass

    @abstractmethod
    def getText(self, bs_obj): pass

    @abstractmethod
    def getType(self, bs_obj): pass

    @abstractmethod
    def getImage(self, bs_obj): pass
