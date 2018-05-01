from flask import render_template, session, redirect, url_for, current_app
from Database import SaveToDatabase
from . import main
from . import Froms
import json

__ND = SaveToDatabase.NewsDataBase()


@main.route('/', methods=['GET', 'POST'])
def index():
    with open('info/TypeToTitle.json', 'r', encoding='utf-8') as f:
        typeDict = json.loads(f.read())
    with open('info/Frequency.json', 'r', encoding='utf-8') as f:
        wordDict = json.loads(f.read())
    typeList = []
    newsList = []
    for k, v in typeDict.items():
        typeList.append(k)
        newsList.append(v)
    count = len(typeList)
    form = Froms.SearchForm()
    if form.validate_on_submit():
        wd = form.search.data
        return redirect('/search/{}/1'.format(wd))
    return render_template('index.html',
                           typeList=typeList,
                           newsList=newsList,
                           wordDict=wordDict,
                           len=count,
                           form=form)


@main.route('/search/<wd>/<int:page>', methods=['GET', 'POST'])
def search(wd, page):
    form = Froms.SearchForm()
    if form.validate_on_submit():
        nwd = form.search.data
        return redirect('/search/{}/1'.format(nwd))
    if wd is not None:
        form.search.data = wd
    newsList, totalItem = __ND.SelectAndGetRows("select SQL_CALC_FOUND_ROWS  * from news where title like '%{}%' order "
                                                "by id asc limit {}, 20;".format(wd, (page - 1) * 20))
    pages = totalItem // 20 + 1
    hasPrev = page is not 1
    hasNext = page is not pages
    return render_template('search.html',
                           newsList=newsList,
                           wd=wd,
                           form=form,
                           page=page,
                           prevNum=page - 1,
                           nextNum=page + 1,
                           hasPrev=hasPrev,
                           hasNext=hasNext,
                           pages=pages)


@main.route('/<type>', methods=['GET'])
def typePage(type):
    with open('info/type/' + type + '.json', 'r', encoding='utf-8') as f:
        titleDict = json.loads(f.read())
    itemList = []
    for item in titleDict.values():
        itemList.append(item)
    return render_template('type.html', itemList=itemList, type=type)


@main.route('/time/<int:page>', methods=['GET'])
def timePage(page):
    with open('info/Times.json', 'r', encoding='utf-8') as f:
        timesDict = json.loads(f.read())
    timeList = []
    newsList = []
    pages = len(timesDict) // 2
    if pages > page:
        for i in range(page * 2 - 2, page * 2):
            timeList.append(timesDict[str(i)])
            with open('info/time/{}.json'.format(timesDict[str(i)]), 'r', encoding='utf-8') as f:
                timeDict = json.loads(f.read())
            newsList.append(timeDict)
    hasPrev = page is not 1
    hasNext = page is not pages - 1
    return render_template('time.html',
                           timeList=timeList,
                           newsList=newsList,
                           len=2,
                           page=page,
                           prevNum=page - 1,
                           nextNum=page + 1,
                           hasPrev=hasPrev,
                           hasNext=hasNext,
                           pages=pages)


@main.route('/page/<type>/<time>/<filename>', methods=['GET'])
def staticPage(type, time, filename):
    url = '/page/{}/{}/{}'.format(type, time, filename)
    with open('info/time/{}.json'.format(time), 'r', encoding='utf-8') as f:
        timeDict = json.loads(f.read())
    with open('info/type/{}.json'.format(type), 'r', encoding='utf-8') as f:
        typeDict = json.loads(f.read())
    timeList = []
    timeLen = len(timeDict)
    typeList = []
    typeLen = len(typeDict)
    for i in range(10):
        if i < timeLen:
            timeList.append(timeDict[str(i)])
        if i < typeLen:
            typeList.append(typeDict[str(i)])
    return render_template(url, timeList=timeList, typeList=typeList, time=time, type=type)
