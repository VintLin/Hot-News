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
import Web.NewsSpider as ns
import WordCould as wc
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
    
def CrawlWeb():
    print('BEGIN')
    web1.CrawlPage()
    web2.CrawlPage()
    web3.CrawlPage()
    web4.CrawlPage()
if __name__ == '__main__':
   start_time = time.time()
   ns.createDataBase()
   CrawlWeb()
   wc.GetWordCould('Cloud/newsTitle.txt')
   end_time = time.time()
   print('Time : ', end_time - start_time)
   