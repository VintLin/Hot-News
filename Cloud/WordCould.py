# -*- coding: utf-8 -*-
"""
Created on Mon Mar  5 16:05:13 2018

@author: 11796
"""
from scipy.misc import imread
import matplotlib.pyplot as plt
from wordcloud import WordCloud, ImageColorGenerator
import jieba.posseg as pseg
import operator
import xlwt
import json
import os
import re


def GetWordCould(path):
    count = 0
    text = GetText(path)
    # jbObj = jieba.cut(text, cut_all = False)
    jbObj = pseg.cut(text)
    wordsToExc = {}
    WordsToImg = {}
    for word, flag in jbObj:
        if re.search('x|(wp)|(ws)|(eng)|m|(ns)', flag) or len(word) == 1:
            continue
        if word in wordsToExc.keys():
            wordsToExc[word][0] = wordsToExc[word][0] + 1
        else:
            wordsToExc[word] = [1, flag]
        count = count + 1
    for key, value in wordsToExc.items():
        WordsToImg[key] = value[0]
    # print(WordsToImg)
    MakeDir('Save')
    SaveToExcel(wordsToExc, count)
    SaveToJSON(wordsToExc, count)
    SaveToImage(WordsToImg)


def MakeDir(path):
    p = '.'
    for d in path.split('/'):
        p = p + '/' + d
        if not os.path.exists(p):
            os.mkdir(p)


def SaveToExcel(words, count):
    print('SaveToExcel')
    sort_words = sorted(words.items(), key=operator.itemgetter(1, 1), reverse=True)
    words = dict(sort_words)
    wb = xlwt.Workbook()
    sheet = wb.add_sheet('sheet1', cell_overwrite_ok=True)
    sheet.write(0, 0, '词语')
    sheet.write(0, 1, '次数')
    sheet.write(0, 2, '词频')
    sheet.write(0, 3, '词性')
    index = 0
    for key, value in words.items():
        # print(key, value)
        sheet.write(index, 0, key)
        sheet.write(index, 1, str(value[0]))
        sheet.write(index, 2, str(int(value[0]) / count)[:20])
        sheet.write(index, 3, value[1])
        index = index + 1
    try:
        wb.save('Save/WordFrequency.xls')
    except Exception:
        print('Exception')


def SaveToJSON(words, count):
    sort_words = sorted(words.items(), key=operator.itemgetter(1, 1), reverse=True)
    words = dict(sort_words)
    wordDict = dict()
    for key, value in words.items():
        wordDict[key] = {'count': str(value[0]),
                         'frequency': str(int(value[0]) * 12345 / count)[:5]}
    jn = json.dumps(wordDict)
    with open('../App/info/Frequency.json', 'w', encoding='utf-8') as f:
        f.write(jn)


def SaveToImage(words):
    print('SaveToImage')
    d = os.path.dirname(__file__)
    imgname1 = "Save/WordCloudDefautColors.png"  # 保存的图片名字(按照背景图片形状和颜色)
    back_coloring_path = "Image/map1.jpg"  # 设置背景图片路径
    back_coloring = imread(os.path.join(d, back_coloring_path))  # 设置背景图片
    font_path = 'simhei.ttf'  # 为matplotlib设置中文字体路径没
    wc = WordCloud(font_path=font_path,  # 设置字体
                   background_color="white",  # 背景颜色
                   max_words=2000,  # 词云显示的最大词数
                   mask=back_coloring,  # 设置背景图片
                   max_font_size=100,  # 字体最大值
                   random_state=42,
                   width=1000, height=776, margin=2,  # 设置图片默认的大小,但是如果使用背景图片的话,那么保存的图片大小将会按照其大小保存,margin为词语边缘距离
                   )
    # 生成词云, 可以用generate输入全部文本(wordcloud对中文分词支持不好,建议启用中文分词),也可以我们计算好词频后使用generate_from_frequencies函数
    # wc.generate(text)
    wc.generate_from_frequencies(words)
    # words例子为{'词a': 100,'词b': 90,'词c': 80}
    image_colors = ImageColorGenerator(back_coloring)
    plt.imshow(wc.recolor(color_func=image_colors))  # 将颜色重置为背景图片中颜色
    plt.axis("off")  # 关闭横纵轴
    plt.show()
    wc.to_file(os.path.join(d, imgname1))  # 保存图片


def GetText(path):
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()
    return text


if __name__ == '__main__':
    GetWordCould('Text/newsTitle.txt')
