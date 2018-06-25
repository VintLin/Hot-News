# import sys
# sys.path.append('..')
# ^ server have

from model.model import News
from pipeline.word_frequency import init_word_frequency
import re
import os
import json
import shutil


PATH = 'App/info/'


def make_dir(url):
    path = '.'  # 开始在本地建立相应文件夹
    for d in url.split('/')[:-1]:
        path = path + '/' + d
        if not os.path.exists(path):
            os.mkdir(path)
    return path + '/' + url.split('/')[-1]


def save_file(content, path):
    path = make_dir('./packup/' + path)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)


def rm_tree(path):
    if os.path.exists(path):
        shutil.rmtree(path)


def copy_tree(opath, npath):
    rm_tree(npath)
    shutil.copytree(opath, npath)


def save(path, content):
    make_dir(path)
    with open(path, 'w', encoding='utf-8') as n:
        n.write(content)


def save_to_json(path, jzon):
    jzon = json.dumps(jzon)
    with open(path, 'w') as f:
        f.write(jzon)


def read_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.loads(f.read())


def save_type_time():
    print('SAVE TYPE TIME')
    type_path = PATH + 'Types.json'
    time_path = PATH + 'Times.json'
    news_list = News().select(oderby='time', isasc=False)
    news_type = set()
    news_time = []
    
    for news in news_list:
        news_type.add(news.type)
        time = str(news.time)[:10]
        if time not in news_time:
            news_time.append(time)
            init_word_frequency(time)

    times = {}
    for i in range(len(news_time)):
        times[i] = news_time[i]

    types = {}
    for i in range(len(news_type)):
        types[i] = news_type.pop()

    save_to_json(time_path, times)
    save_to_json(type_path, types)


def save_news_by_type():
    print("SAVE TYPE : TITLE")
    type_path = PATH + 'Types.json'
    to_path = PATH + 'TypeToTitle.json'
    type_title = dict()
    type_dict = read_json(type_path)
    for v in type_dict.values():
        title_url = dict()
        news_list = News(type=v).select(oderby='time', limit=5, isasc=False)
        for news in news_list:
            title_url[news.title] = news.path
        type_title[v] = title_url
    save_to_json(to_path, type_title)


def save_news_by_time():
    print("SAVE TYPE : TITLE")
    time_path = PATH + 'Times.json'
    to_path = PATH + 'TimeToTitle.json'
    time_title = dict()
    time_dict = read_json(time_path)
    for v in time_dict.values():
        title_url = dict()
        news_list = News().set_period(field='time', time_slot='+24:0:0', moment=v+' 00:00:00').\
            select(oderby='time', isasc=False, limit=5)
        for news in news_list:
            title_url[news.title] = news.path
        time_title[v] = title_url
    save_to_json(to_path, time_title)


def save_type_news_list():
    print("SAVE URL : TYPE")
    type_path = PATH + 'Types.json'
    to_path = PATH + 'type/{}.json'
    url_dict = read_json(type_path)
    for t in url_dict.values():
        type_dict = dict()
        item_dict = dict()
        news_list = News(type=t).select(oderby='time', isasc=False)
        for i in range(len(news_list)):
            item_dict['title'] = news_list[i].title
            item_dict['path'] = news_list[i].path
            item_dict['time'] = str(news_list[i].time)[:10]
            type_dict[i] = item_dict.copy()
        save_to_json(to_path.format(t), type_dict)


def save_time_news_list():
    print("SAVE URL : TIME")
    time_path = PATH + 'Times.json'
    to_path = PATH + 'time/{}.json'
    url_dict = read_json(time_path)
    for t in url_dict.values():
        time_dict = dict()
        item_dict = dict()
        news_list = News().set_period(field='time', time_slot='+24:0:0', moment=t+' 00:00:00').\
            select(oderby='time', isasc=False)
        for i in range(len(news_list)):
            item_dict['title'] = news_list[i].title
            item_dict['path'] = news_list[i].path
            item_dict['type'] = news_list[i].type
            time_dict[i] = item_dict.copy()
        save_to_json(to_path.format(t), time_dict)


def save_time_page():
    print("SAVE PAGE : TIME")
    to_path = PATH + 'times/{}.json'
    time_list = []
    page_dict = {}
    pages = int(News().select(iscount=True) / 30)
    for i in range(1, pages):
        pages = News().set_pagination(i, 30).select(oderby='time', isasc=False)
        for item in pages.items:
            time = str(item.time)[:10]
            if not time_list:
                page_dict[i] = {}
            if time not in time_list:
                time_list.append(time)
                page_dict[i][time] = [{'title': item.title, 'path': item.path, 'type': item.type}]
            else:
                page_dict[i][time].append({'title': item.title, 'path': item.path, 'type': item.type})
        time_list.clear()
    for k, v in page_dict.items():
        save_to_json(to_path.format(str(k)), v)


def re_build(url):
    dir_list = [i for i in os.listdir(url)]
    for d in dir_list:
        path = url + '/' + d
        if os.path.isdir(path):
            re_build(path)
        elif re.search('\.htm', d) is not None:
            with open(path, 'r', encoding='utf-8') as f:
                context = f.read()
            with open(path, 'w', encoding='utf-8') as f:
                f.write(context)


if __name__ == '__main__':
    pass
