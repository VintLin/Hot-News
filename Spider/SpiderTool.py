# -*- coding: utf-8 -*-
"""
Created on Wed Feb 28 15:49:58 2018

@author: Voter
"""

import requests
import re
import os
from bs4 import BeautifulSoup
from datetime import datetime as dt


def makeDir(url):
    path = '.'  # 开始在本地建立相应文件夹
    print(url)
    for d in url.split('/')[:-1]:
        path = path + '/' + d
        if not os.path.exists(path):
            os.mkdir(path)
    return path + '/' + url.split('/')[-1]


class SpiderTool:
    __HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Macintosh;Intel Mas OS X 10_9_5)AppleWebKit 537.36 (KHTML, like Gecko) Chrome',
        'Accept': 'text/html,application/xhtml+xml, application/xml; q=0.9, image/webp, */*, q=0.8'
    }

    @staticmethod
    def getBsObj(pageUrl):  # 获取BeautifulSoup对象
        # try:
        r = requests.get(pageUrl, headers=SpiderTool.__HEADERS)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        bsObj = BeautifulSoup(r.text, 'html.parser')
        return bsObj

    # except:
    #     print('GET BeautifulSoup Error')

    @staticmethod
    def saveImage(imageUrl, path):
        try:
            r = requests.get(imageUrl, headers=SpiderTool.__HEADERS)
            r.raise_for_status()
            open('.' + path, 'wb').write(r.content)
        except:
            print('GET Image Error')

    @staticmethod
    def getHtml(pageUrl, params):
        try:

            r = requests.get(pageUrl, headers=SpiderTool.__HEADERS, params=params)
            r.raise_for_status()
            r.encoding = r.apparent_encoding
            return r.text
        except:
            print('GET HTML Error')

    @staticmethod
    def getTimeInfo(time):
        time1 = re.search('[0-9]+-[0-9]+-[0-9]+', time).group()
        time2 = re.search('[0-9]+:[0-9]+:[0-9]+', time)
        if time2 is None:
            time2 = re.search('[0-9]+:[0-9]+', time).group() + ':00'
        else:
            time2 = time2.group()
        return time1 + ' ' + time2

    @staticmethod
    def getContent(title, time, source, editor, text, small_title='', lead=''):
        ts = '时间 : ' + time + '   来源 : ' + source + '   编辑 : ' + editor
        content = '''
        <div class = 'news'>
            <div class = 'title'>
                <h2><strong>{}</strong><small>{}</small></h2>
            </div>
            <div class = 'post_time_source'>
                <p class='text-left text-muted'>{}
                    <span class="glyphicon glyphicon-eye-open" style="margin-left:20px"></span> {}
                    <span class="glyphicon glyphicon-thumbs-up" style="margin-left:20px"></span> {}
                    <span class="glyphicon glyphicon-folder-open" style="margin-left:20px"></span> {}
                </p>
            </div>
            <p class="lead">
                {}
            </p>
            <div class = 'content'>
                <h4>{}</h4>
            </div>
        </div>
                '''.format(title, small_title, ts,
                           '{{operand.browse}}',
                           '{{operand.thumb}}',
                           '{{operand.collect}}', lead, text)
        return content


class FileTool:
    __INITFLAG = False
    __NOWTIME = dt.now().strftime('%Y-%m-%d')

    @staticmethod
    def setInitFlag():
        FileTool.__INITFLAG = True

    @staticmethod
    def saveFile(url, content, image, news):
        if FileTool.__INITFLAG or FileTool.__NOWTIME == news.time[:10]:
            url = re.sub('http://', '', url)
            news.website = url.split('/')[0]
            news.filename = re.sub('\?.*|#.*', '', url.split('/')[-1])
            FileTool.handle_static_page(content, news)
            FileTool.handle_image(image, news)
            news.insert_without_return()
            print('Save Success')
            return True
        else:
            return False

    @staticmethod
    def handle_image(url, news):
        if url:
            imagePath = re.sub('\?.*|#.*', '', url.split('/')[-1])
            news.image = makeDir('news_image/{}/{}/{}'.format(news.type, news.time[:10], imagePath)).replace('./', '/')
            SpiderTool.saveImage(url, news.image)
        else:
            news.image = ''

    @staticmethod
    def handle_static_page(content, news):
        news.path = makeDir('page/{}/{}/{}'.format(news.type, news.time[:10], news.filename)).replace('./', '/')
        with open('.' + news.path, 'w', encoding='utf-8') as w:
            w.write(content)


if __name__ == '__main__':
    for i in range(1, 80):
        index = SpiderTool.getBsObj('http://www.voterlin.cn/time/' + str(i))
        for a in index.find_all('a', {'class': 'list-group-item'}):
            print(a['href'])
            page = SpiderTool.getBsObj('http://www.voterlin.cn/' + a['href'])
