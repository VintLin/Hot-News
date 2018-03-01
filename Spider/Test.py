# -*- coding: utf-8 -*-
"""
Created on Wed Feb 28 16:22:32 2018

@author: 11796
"""
import os
import re
from bs4 import BeautifulSoup
from SaveToDatabase import NewsDataBase
count = 0
def test():
    news = NewsDataBase()
    news.Drop()
    news.Create()
   #getHTML('www.southcn.com')
def getHTML(path):
    dirs = [i for i in os.listdir(path)]
    print(dirs)
    findHtml(dirs, path)

def findHtml(dirList, url):
    global count
    for d in dirList:
        murl = url + '/' + d
        if os.path.isdir(murl):     
            dirL = [i for i in os.listdir(murl)]
            findHtml(dirL, murl)
        elif re.search('\.htm', d) is not None:
            with open(murl, 'r', encoding = 'utf-8') as r:
                read = r.read()
                #print(read[:100])
                bs = getBsObj(read)
                if bs.find('h2') is None:
                    print(murl)
                    print('None')
                else:
                    print(bs.find('h2').text.strip())
                    count = count + 1
    
                
def getBsObj(text):
        try:
            bsObj = BeautifulSoup(text, 'html.parser')
            return bsObj
        except:
            print('Error')
test()
print(count)