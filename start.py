import datetime
import time
from spider import crawl
from pipeline.pipeline import transfer


def start():
    """h表示设定的小时，m为设定的分钟"""
    while True:
        # 判断是否达到设定时间，例如0:00
        while True:
            now = datetime.datetime.now()
            if now.hour == 7 and now.minute == 0:
                break
            if now.hour == 11 and now.minute == 0:
                break
            time.sleep(35)
        try:
            crawl.crawl()
        except:
            print("ERROR SPIDER")
        finally:
            transfer()


if __name__ == "__main__":
    start()
    transfer()