# -*- coding: utf-8 -*-
"""
Created on Wed Feb 28 15:49:58 2018

@author: 11796
"""
import sys
sys.path.append('..')
from bs4 import BeautifulSoup
from SaveToDatabase import NewsDataBase
import requests
import re
import os

count = 0
def getBsObj(pageUrl):
    try:
        headers = {'User-Agent':'Mozilla/5.0 (Macintosh;Intel Mas OS X 10_9_5)AppleWebKit 537.36 (KHTML, like Gecko) Chrome',
           'Accept':'text/html,application/xhtml+xml, application/xml; q=0.9, image/webp, */*, q=0.8'}
        r = requests.get(pageUrl, headers=headers)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        bsObj = BeautifulSoup(r.text, 'html.parser')
        return bsObj
    except:
        print('Error')

def saveFile(URL, content, params):
    URL = re.sub('http://','',URL)
    #去掉 http:// 之后可用网页路径做本地路径
    filename = re.sub('\?.*|#.*', '', URL.split('/')[-1])
    #去掉url路径后的？#开头的参数
    website = URL.split('/')[0]
    #取该网站的网址
    path = makeDir(URL) + '/' + filename
    
    with open(path ,'w',encoding='utf-8') as w:
        w.write(content)
    
    params = [filename, path, website] + params
    saveToDataBase(params)
    return True

def getTimeInfo(string):
    time1 = re.search('[0-9]+-[0-9]+-[0-9]+', string).group()
    time2 = re.search('[0-9]+:[0-9]+:[0-9]+', string).group()
    return [time1, time2]

def makeDir(URL):
    path = '.'#开始在本地建立相应文件夹
    for d in URL.split('/')[:-1]:
        path = path +'/'+ d
        if not os.path.exists(path):
            os.mkdir(path)
    print('makeDir', path)
    return path

def createDataBase():
    nd = NewsDataBase()
    nd.Drop()
    nd.Create()
    
def saveToDataBase(params):
    global count
    count = count + 1
    nd = NewsDataBase()
    nd.Insert(params)
    print(params)
    
def getCount():
    global count
    print(count)
#createDataBase()