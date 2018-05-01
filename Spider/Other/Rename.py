# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import os
import re

__COUNT = 0


def Rename():
    dirs = [i for i in os.listdir('NewsPage')]
    findHtml(dirs, 'NewsPage')


def findHtml(dirList, url):
    global __COUNT
    for d in dirList:
        murl = url + '/' + d
        if os.path.isdir(murl):
            dirL = [i for i in os.listdir(murl)]
            findHtml(dirL, murl)
        elif re.search('\.htm', d) is not None:
            newName = re.sub('\.htm$', '.html', d)
            print('Name : ', newName)
            count = count + 1
            # os.rename(url + '/' + d, url + '/' + newName)


def getType():
    context = ''
    savePath = '../../App/TypeList.txt'
    getPath = '../../HTML/WebPage'
    dr = [i for i in os.listdir(getPath)]

    for d in dr:
        context = context + d + '\n'

    with open(savePath, 'w') as f:
        f.write(context)


getType()
# Rename()
# print('count :', __COUNT)
