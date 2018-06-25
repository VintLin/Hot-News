# -*- coding: utf-8 -*-
"""
Created on Sat Mar  3 15:00:13 2018

@author: 11796
"""
# import sys
# sys.path.append('..')
# ^server have

import time
from multiprocessing import Pool
from spider.website import Website


def crawl():
    start_time = time.time()
    subs = Website.__subclasses__()
    p = Pool(len(subs))
    for s in subs:
        p.apply_async(s().crawl)
    p.close()
    p.join()
    end_time = time.time()
    print('Time : ', end_time - start_time)


def crawl_one_by_one():
    subs = Website.__subclasses__()
    clazz = []
    for s in subs:
        clazz.append(s())
    for c in clazz:
        c.crawl()


if __name__ == '__main__':
    crawl_one_by_one()