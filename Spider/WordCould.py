# -*- coding: utf-8 -*-
"""
Created on Mon Mar  5 16:05:13 2018

@author: 11796
"""
import re
import jieba.posseg as pseg
import operator
def GetText(path):
    text = ''
    with open(path, 'r', encoding = 'utf-8') as f:
        text = f.read()
    return text
def MakeCould(path):
    text = GetText(path)
    #jbObj = jieba.cut(text, cut_all = False)
    jbObj = pseg.cut(text)
    words = {}
    for word, flag in jbObj:
        if re.search('x|(wp)|(ws)|(eng)|m', flag):
            continue
        if word in words.keys():
            words[word][0] = words[word][0] + 1
        else:
            words[word] = [1, flag]
    #for key, value in words.items():
        #print(key, value)
    sort_words = sorted(words.items(), key = operator.itemgetter(1,1))
    words = dict(sort_words)
    print(words)
    

MakeCould('newsTitle.txt')
