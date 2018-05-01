from Database.SaveToDatabase import NewsDataBase
from Spider import NewsSpider as ns
import Cloud.WordCould as wc
import re
import os
import json
import shutil

__ND = NewsDataBase()
__TEXTPATH = '../Cloud/Text/newsTitle.txt'
__TYPES = '../App/info/Types.json'  # 新闻类型
__TIMES = '../App/info/Times.json'  # 时刻
__TYPEPATH = '../App/info/TypeToTitle.json'  # 新闻类型 : { 标题: 路径 }
__TIMEPATH = '../App/info/TimeToTitle.json'  # 时间 : { 标题: 路径}
__PATH = '../App/info/'


def saveInfo(textPath, types, times):
    text = ''
    newsType = set()
    newsTime = set()

    ns.makeDir(textPath)
    newsList = __ND.Select('select * from news')
    for news in newsList:
        text = text + news.title
        newsType.add(news.type)
        newsTime.add(news.time1)

    with open(textPath, 'w', encoding='utf-8') as n:
        n.write(text)

    timeList = []
    for i in range(len(newsTime)):
        timeList.append(newsTime.pop())
    context = sortTimeList(timeList)
    jn = json.dumps(context)
    with open(times, 'w') as f:
        f.write(jn)

    context = {}
    for i in range(len(newsType)):
        context[i] = newsType.pop()
    jn = json.dumps(context)
    with open(types, 'w') as f:
        f.write(jn)


def sortTimeList(timeList):
    tList = []
    for s in timeList:
        sl = s.split('-')
        tList.append((int(sl[0]), int(sl[1]), int(sl[2])))
    tList = sorted(tList, key=lambda x: x[2], reverse=True)
    tList = sorted(tList, key=lambda x: x[1], reverse=True)
    tList = sorted(tList, key=lambda x: x[0], reverse=True)
    toStr = lambda x: '0' + str(x) if len(str(x)) is 1 else str(x)
    tDict = {}
    for i in range(len(tList)):
        tDict[i] = '{}-{}-{}'.format(toStr(tList[i][0]), toStr(tList[i][1]), toStr(tList[i][2]))
    return tDict


def saveTypeToTitle(typePath, types):
    typeToInfo = dict()
    with open(types, 'r', encoding='utf-8') as f:
        typeDict = json.loads(f.read())

    for v in typeDict.values():
        newsList = __ND.Select('select * from news where TYPE = "{}"'.format(v))
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
    timeToInfo = dict()
    with open(times, 'r', encoding='utf-8') as f:
        timeDict = json.loads(f.read())

    for v in timeDict.values():
        newsList = __ND.Select('select * from news where TIME1 = "{}" order by id asc limit 5'.format(v))
        titleToUrl = dict()
        for news in newsList:
            titleToUrl[news.title] = news.path
        timeToInfo[v] = titleToUrl
    jn = json.dumps(timeToInfo)
    with open(timePath, 'w') as f:
        f.write(jn)


def saveUrlWithType(path, types):
    with open(types, 'r', encoding='utf-8') as f:
        urlDict = json.loads(f.read())
    for t in urlDict.values():
        typeDict = dict()
        itemDict = dict()
        newsList = __ND.Select('select * from news where TYPE = "{}"'.format(t))
        for i in range(len(newsList)):
            itemDict['title'] = newsList[i].title
            itemDict['path'] = newsList[i].path
            itemDict['time'] = newsList[i].time1
            typeDict[i] = itemDict.copy()
        jn = json.dumps(typeDict)
        with open(path + 'type/' + t + '.json', 'w') as f:
            f.write(jn)


def saveUrlWithTime(path, times):
    with open(times, 'r', encoding='utf-8') as f:
        urlDict = json.loads(f.read())
    for t in urlDict.values():
        timeDict = dict()
        itemDict = dict()
        newsList = __ND.Select('select * from news where TIME1 = "{}"'.format(t))
        for i in range(len(newsList)):
            itemDict['title'] = newsList[i].title
            itemDict['path'] = newsList[i].path
            itemDict['type'] = newsList[i].type
            timeDict[i] = itemDict.copy()
        jn = json.dumps(timeDict)
        with open(path + 'time/' + t + '.json', 'w') as f:
            f.write(jn)


def rmTree(path):
    if os.path.exists(path):
        shutil.rmtree(path)


def copyTree(opath, npath):
    rmTree(npath)
    shutil.copytree(opath, npath)


def removeInfo():
    rmTree('../App/info')
    copyTree('../Spider/page', '../App/templates/page')

    ns.makeDir(__TEXTPATH)
    ns.makeDir(__PATH + '/type/')
    ns.makeDir(__PATH + '/time/')

    saveInfo(textPath=__TEXTPATH, types=__TYPES, times=__TIMES)
    saveTypeToTitle(typePath=__TYPEPATH, types=__TYPES)
    saveTimeToTitle(timePath=__TIMEPATH, times=__TIMES)
    saveUrlWithType(path=__PATH, types=__TYPES)
    saveUrlWithTime(path=__PATH, times=__TIMES)
    reBuild('../App/templates/page')


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


if __name__ == '__main__':
    print('BEGIN')
    # saveInfo(textPath=__TEXTPATH, types=__TYPES, times=__TIMES)
    removeInfo()
    wc.GetWordCould(__TEXTPATH)
    print('END')
