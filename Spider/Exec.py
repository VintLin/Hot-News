# -*- coding: utf-8 -*-
"""
Created on Sat Mar  3 15:00:13 2018

@author: 11796
"""
from multiprocessing import Pool
import time, os
import Web.news163com as web1
import Web.newscricn as web2
import Web.wwwfjsencom as web3
import Web.wwwsouthcncom as web4
def Crawl():
    print('Parent process %s.' % os.getpid())
    p = Pool()
    p.apply_async(web1.CrawlPage)
    p.apply_async(web2.CrawlPage)
    p.apply_async(web3.CrawlPage)
    p.apply_async(web4.CrawlPage)
    print('Waiting for all subprocesses done...')
    p.close()
    p.join()
    print('All subprocesses done.')

if __name__ == '__main__':
   start_time = time.time()
   Crawl()
   end_time = time.time()
   print('Time : ', end_time - start_time)
   