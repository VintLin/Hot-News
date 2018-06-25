# -*- coding: utf-8 -*-
"""
Created on Mon Mar  5 16:05:13 2018

@author: 11796
"""
from model.model import Frequency, Website, News, now
from jieba import posseg
import operator
import json
import re

not_this_word = ['发展', '习近平', '工作', '建设', '精神', '合作', '今年', '推进', '全面', '我国']
not_this_pos = ['x', 'wp', 'eng', 'm', 'ns', 'v', 'vd', 'vn']


def is_in(not_this, field):
    s = '({})|'
    condition = ''
    for l in not_this:
        condition = condition + s.format(l)
    return re.search(condition[:-1], field)


def get_word_frequency(time=now(1)):
    time = time + ' 00:00:00'
    text = ''
    words = {}
    count = 1
    news = News().set_period(field='time', time_slot='-24:0:0', moment=time).select()
    for n in news:
        text = text + n.title
    be_cut = posseg.cut(text)
    for word, pos in be_cut:
        if is_in(not_this_word, word) or is_in(not_this_pos, pos) or len(word) == 1:
            continue
        if word in words.keys():
            words[word][0] = words[word][0] + 1
        else:
            words[word] = [1, pos]
        count = count + 1
    words = dict(sorted(words.items(), key=operator.itemgetter(1, 1), reverse=True))
    save_to_sql(words, count, time)
    if time[:10] == now(1):
        save_to_json(count)


def init_word_frequency(time):
    f = Frequency(time=time).select(getone=True)
    if f.id:
        return False
    else:
        get_word_frequency(time)


def save_to_sql(words, count, time):
    for key, value in words.items():
        frequency = Frequency()
        frequency.word = key
        if value[0] < 2:
            break
        frequency.times = value[0]
        frequency.pos = value[1]
        id = frequency.is_record(time[:10])
        if id:
            frequency.id = id
            frequency.update()
        else:
            frequency.insert()
    Website(word_times=count).init_insert(time=time[:10])


def save_to_json(count):
    print('Save To JSON')
    frequency = Frequency.get_now_list()
    wordDict = dict()
    for item in frequency:
        wordDict[item.word] = {'count': item.times, 'frequency': str(100 * item.times / count )[:6]}
    jn = json.dumps(wordDict)
    with open('App/info/Frequency.json', 'w', encoding='utf-8') as f:
        f.write(jn)


if __name__ == '__main__':
    pass
