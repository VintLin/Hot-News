# -*- coding: utf-8 -*-
"""
Created on Wed Feb 28 15:49:58 2018

@author: 11796
"""
from bs4 import BeautifulSoup
import requests
import re
import os

def getBsObj(pageUrl):
    try:
        r = requests.get(pageUrl)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        bsObj = BeautifulSoup(r.text, 'html.parser')
        return bsObj
    except:
        print('Error')

def saveFile(dirUrl, content):
    if dirUrl[:4] == 'http':
        dirUrl = re.sub('http://','',dirUrl)
        #去掉 http:// 之后可用网页路径做本地路径
    if re.search('\?|#', dirUrl.split('/')[-1]) is not None:
        file = re.sub('\?.*|#.*', '', dirUrl.split('/')[-1])
        #去掉url路径后的？#开头的参数
    alldirUrl = ''#开始在本地建立相应文件夹
    for d in dirUrl.split('/')[:-1]:
        alldirUrl = alldirUrl +'/'+ d
        if not os.path.exists('.'+alldirUrl):
            os.mkdir('.'+alldirUrl)
    alldirUrl = '.' + alldirUrl
    print(alldirUrl)
    with open(alldirUrl + '/'+ file,'w',encoding='utf-8') as w:
            w.write(content)
    return True