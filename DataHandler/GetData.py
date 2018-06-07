# import sys
# sys.path.append('..')
# ^ server have

from Model.model import News
from Spider import SpiderTool as ns
import Cloud.WordCould as wc
import re
import os
import json
import shutil

__TEXTPATH = '../Cloud/Text/newsTitle.txt'
__TYPES = '../App/info/Types.json'  # 新闻类型
__TIMES = '../App/info/Times.json'  # 时刻
__TYPEPATH = '../App/info/TypeToTitle.json'  # 新闻类型 : { 标题: 路径 }
__TIMEPATH = '../App/info/TimeToTitle.json'  # 时间 : { 标题: 路径}
__PATH = '../App/info/'


def saveInfo(textPath, types, times):
    print('SAVE INFO')
    text = ''
    newsList = News().select(oderby='time', isasc=False)
    print(len(newsList))
    newsType = set()
    newsTime = []

    for news in newsList:
        text = text + news.title
        newsType.add(news.type)
        time = str(news.time)[:10]
        if time not in newsTime:
            newsTime.append(time)

    ns.makeDir(textPath)
    with open(textPath, 'w', encoding='utf-8') as n:
        n.write(text)

    context = {}
    for i in range(len(newsTime)):
        context[i] = newsTime[i]

    jn = json.dumps(context)
    with open(times, 'w') as f:
        f.write(jn)

    context = {}
    for i in range(len(newsType)):
        context[i] = newsType.pop()

    jn = json.dumps(context)
    with open(types, 'w') as f:
        f.write(jn)


def saveTypeToTitle(typePath, types):
    print("SAVE TYPE : TITLE")
    typeToInfo = dict()
    with open(types, 'r', encoding='utf-8') as f:
        typeDict = json.loads(f.read())
    for v in typeDict.values():
        newsList = News(type=v).select(oderby='time', isasc=False)
        titleToUrl = dict()
        count = 0
        for news in newsList:
            count = count + 1
            titleToUrl[news.title] = news.path
            if count is 5:
                break
        typeToInfo[v] = titleToUrl
    jn = json.dumps(typeToInfo)
    with open(typePath, 'w') as f:
        f.write(jn)


def saveTimeToTitle(timePath, times):
    print("SAVE TYPE : TITLE")
    timeToInfo = dict()
    with open(times, 'r', encoding='utf-8') as f:
        timeDict = json.loads(f.read())
    for v in timeDict.values():
        newsList = News().set_period(field='time', time_slot='+24:0:0', moment=v+' 00:00:00').\
            select(oderby='time', isasc=False, limit=5)
        titleToUrl = dict()
        for news in newsList:
            titleToUrl[news.title] = news.path
        timeToInfo[v] = titleToUrl
    jn = json.dumps(timeToInfo)
    with open(timePath, 'w') as f:
        f.write(jn)


def saveUrlWithType(path, types):
    print("SAVE URL : TYPE")
    with open(types, 'r', encoding='utf-8') as f:
        urlDict = json.loads(f.read())
    for t in urlDict.values():
        typeDict = dict()
        itemDict = dict()
        newsList = News(type=t).select(oderby='time', isasc=False)
        for i in range(len(newsList)):
            itemDict['title'] = newsList[i].title
            itemDict['path'] = newsList[i].path
            itemDict['time'] = str(newsList[i].time)[:10]
            typeDict[i] = itemDict.copy()
        jn = json.dumps(typeDict)
        with open(path + 'type/' + t + '.json', 'w') as f:
            f.write(jn)


def saveUrlWithTime(path, times):
    print("SAVE URL : TIME")
    with open(times, 'r', encoding='utf-8') as f:
        urlDict = json.loads(f.read())
    for t in urlDict.values():
        timeDict = dict()
        itemDict = dict()
        newsList = News().set_period(field='time', time_slot='+24:0:0', moment=t+' 00:00:00').\
            select(oderby='time', isasc=False)
        for i in range(len(newsList)):
            itemDict['title'] = newsList[i].title
            itemDict['path'] = newsList[i].path
            itemDict['type'] = newsList[i].type
            timeDict[i] = itemDict.copy()
        jn = json.dumps(timeDict)
        with open(path + 'time/' + t + '.json', 'w') as f:
            f.write(jn)


def savePageWithTime(path):
    print("SAVE PAGE : TIME")
    times = []
    page_dict = {}
    p = News().set_pagination(1, 30).select(oderby='time', isasc=False).pages
    for i in range(1, p):
        pages = News().set_pagination(i, 30).select(oderby='time', isasc=False)
        for item in pages.items:
            time = str(item.time)[:10]
            if not times:
                page_dict[i] = {}
            if time not in times:
                times.append(time)
                page_dict[i][time] = [{'title': item.title, 'path': item.path, 'type': item.type}]
            else:
                page_dict[i][time].append({'title': item.title, 'path': item.path, 'type': item.type})
        times.clear()

    for k, v in page_dict.items():
        with open(path + 'times/' + str(k) + '.json', 'w') as f:
            jn = json.dumps(v)
            f.write(jn)


def rmTree(path):
    if os.path.exists(path):
        shutil.rmtree(path)


def copyTree(opath, npath):
    rmTree(npath)
    shutil.copytree(opath, npath)


def removeInfo():
    rmTree('../App/info')
    copyTree('page', '../App/templates/page')
    copyTree('news_image', '../App/static/news_image')

    ns.makeDir(__TEXTPATH)
    ns.makeDir(__PATH + '/type/')
    ns.makeDir(__PATH + '/time/')
    ns.makeDir(__PATH + '/times/')

    saveInfo(textPath=__TEXTPATH, types=__TYPES, times=__TIMES)
    saveTypeToTitle(typePath=__TYPEPATH, types=__TYPES)
    saveTimeToTitle(timePath=__TIMEPATH, times=__TIMES)
    saveUrlWithType(path=__PATH, types=__TYPES)
    saveUrlWithTime(path=__PATH, times=__TIMES)
    savePageWithTime(path=__PATH)
    getImage('../App/info/image.txt')
    reBuild('../App/templates/page')


def getImage(path):
    news = News().select(limit=100, oderby='time', isasc=False)
    for n in news:
        if n.image and len(n.image.split('/')[-1]) > 20:
            print(n.image)
            with open(path, 'a', encoding='utf-8') as f:
                f.write(str(n.id) + '\n')


BASE = '''{% extends "newsbase.html" %} 
{% import "bootstrap/wtf.html" as wtf %} 
{% block title %}HotNews{% endblock %} 
{% block page_content %}
@ 
{% endblock %}'''


def reBuild(url):
    dirList = [i for i in os.listdir(url)]
    for d in dirList:
        murl = url + '/' + d
        if os.path.isdir(murl):
            reBuild(murl)
        elif re.search('\.htm', d) is not None:
            with open(murl, 'r', encoding='utf-8') as f:
                context = f.read()
            with open(murl, 'w', encoding='utf-8') as f:
                f.write(BASE.replace('@', context))


def Exec():
    print('BEGIN')
    removeInfo()
    wc.GetWordCould(__TEXTPATH)
    print('END')


if __name__ == '__main__':
    Exec()