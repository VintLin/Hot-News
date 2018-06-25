import requests

from model import Proxy
from spider.tool.Tool import SpiderTool

def crawl_proxy():
    links = get_links()
    for link in links:
        items = get_items(link)
        for item in items:
            get_proxy(item)


def get_links():
    links = []
    for i in range(1, 1814):
        links.append("http://www.xicidaili.com/wt/{}".format(str(i)))
    return links


def get_items(link):
    try:
        bs_obj = SpiderTool.getBsObj(link)
        return bs_obj.find_all('tr', {'class': 'odd'})
    except AttributeError:
        print('GET ITEM NONE TYPE')
        return []


def get_proxy(item):
    try:
        proxy = Proxy()
        td = item.find_all('td')
        proxy.country = td[0].find('img')['alt']
        proxy.ip = td[1].text
        proxy.port = td[2].text
        proxy.address = td[3].find('a').text
        proxy.status = td[5].text
        proxy.speed = td[6].find('div')['title'][:-1]
        proxy.ping = td[7].find('div')['title'][:-1]
        proxy.live_time = td[8].text
        proxy.timestamp = '20' + td[9].text + ':00'
        proxy.insert()
    except TypeError:
        print('GET PROXY NONE TYPE')


def is_useful():
    url = 'http://httpbin.org/ip'
    proxies = {
        'http': 'http://121.10.1.180:8080',
        'https': 'https://121.10.1.180:8080'
    }
    __HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Macintosh;Intel Mas OS X 10_9_5)AppleWebKit 537.36 (KHTML, like Gecko) Chrome',
        'Accept': 'text/html,application/xhtml+xml, application/xml; q=0.9, image/webp, */*, q=0.8'
    }
    r = requests.get(url, headers=__HEADERS, proxies=proxies)
    print(r.text)


if __name__ == "__main__":
    is_useful()
    #crawl_proxy()