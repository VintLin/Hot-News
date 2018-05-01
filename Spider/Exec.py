# -*- coding: utf-8 -*-
"""
Created on Sat Mar  3 15:00:13 2018

@author: 11796
"""
import os
import time
from multiprocessing import Pool
from Spider import NewsSpider
import Spider.Web.news163com as web1
import Spider.Web.newscricn as web2
import Spider.Web.wwwfjsencom as web3
import Spider.Web.wwwsouthcncom as web4


def Crawl(stool, ftool):
    print('Parent process %s.' % os.getpid())
    p = Pool()
    spider1 = web1.news163com(stool, ftool)
    spider2 = web2.newscricn(stool, ftool)
    spider3 = web3.wwwfjsencom(stool, ftool)
    spider4 = web4.wwwsouthcncom(stool, ftool)

    p.apply_async(spider1.CrawlPage)
    p.apply_async(spider2.CrawlPage)
    p.apply_async(spider3.CrawlPage)
    p.apply_async(spider4.CrawlPage)
    print('Waiting for all subprocesses done...')
    p.close()
    p.join()
    print('All subprocesses done.')


def CrawlWeb(stool, ftool):
    print('BEGIN')
    spider1 = web1.news163com(stool, ftool)
    spider2 = web2.newscricn(stool, ftool)
    spider3 = web3.wwwfjsencom(stool, ftool)
    spider4 = web4.wwwsouthcncom(stool, ftool)

    spider1.CrawlPage()
    spider2.CrawlPage()
    spider3.CrawlPage()
    spider4.CrawlPage()


def Exec():
    start_time = time.time()
    stool = NewsSpider.SpiderTool()
    if os.path.exists('page'):
        print('Run Again')
        ftool = NewsSpider.FileTool(flag=False)
    else:
        print('Init Web Model')
        ftool = NewsSpider.FileTool(flag=True)
        ftool.createDataBase()
    CrawlWeb(stool, ftool)
    end_time = time.time()
    print('Time : ', end_time - start_time)


if __name__ == '__main__':
    Exec()
