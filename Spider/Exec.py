# -*- coding: utf-8 -*-
"""
Created on Sat Mar  3 15:00:13 2018

@author: 11796
"""
# import sys
# sys.path.append('..')
# ^server have

import os
import time
from multiprocessing import Pool
from Spider.Website import Website
from Spider import SpiderTool


def Crawl():
    print('Parent process %s.' % os.getpid())
    p = Pool()
    subs = Website.__subclasses__()
    for s in subs:
        p.apply_async(s().crawl())
    print('Waiting for all subprocesses done...')
    p.close()
    p.join()
    print('All subprocesses done.')


def CrawlWeb():
    print('BEGIN')
    subs = Website.__subclasses__()
    for s in subs:
        s().crawl()


def Exec():
    start_time = time.time()
    if os.path.exists('page'):
        print('Run Again')
    else:
        print('INIT WEB MODEL')
        SpiderTool.FileTool.setInitFlag()
    CrawlWeb()
    end_time = time.time()
    print('Time : ', end_time - start_time)


if __name__ == '__main__':
    Exec()
