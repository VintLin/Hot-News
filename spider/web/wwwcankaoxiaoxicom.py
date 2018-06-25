from spider.website import Website, get_xpath
import re
from lxml import etree


class wwwcankaoxiaoxicom(Website):
    def from_rank(self):
        self.rank = set()
        self.get_links("http://www.cankaoxiaoxi.com/")

    def get_links(self, url):
        x = get_xpath(url)
        links = x.xpath(".//a/@href")
        for l in links:
            if re.search('.*/[A-Za-z]*/[0-9]*/[0-9]*', l):
                self.pages.add(l)
            elif re.search('[A-Za-z]*\.cankaoxiaoxi\.com/$', l) and l not in self.rank and len(self.rank) < 50:
                self.rank.add(l)
                self.get_links(l)

    def get_time_by_x(self, x):
        time = x.xpath(".//*[@id='pubtime_baidu']/text()")[0]
        return time

    def get_title_by_x(self, x):
        title = x.xpath(".//h1[@class='h2 fz-23 YH']/text()")
        if not title:
            title = x.xpath(".//h1[@class='h2 fz-25 YH']/text()")
        return title[0]

    def get_source_by_x(self, x):
        source = x.xpath(".//*[@id='source_baidu']/a/text()")[0]
        return source

    def get_editor_by_x(self, x):
        editor = x.xpath(".//*[@id='editor_baidu']/text()")[0]
        editor = editor.split('：')[-1]
        return editor

    def get_text_by_x(self, x):
        text = x.xpath(".//*[@id='ctrlfscont']")[0]
        text = etree.tostring(text, method='html')
        return text

    def get_type_by_x(self, x):
        Type = x.xpath(".//*[@class='crumb']/a[3]/text()")
        return Type

    def get_image_by_x(self, x):
        image = x.xpath(".//*[@id='ctrlfscont']/p/a/img/@src")
        return image


if __name__ == "__main__":
    website = wwwcankaoxiaoxicom()
    # website.get_fields(" http://www.cankaoxiaoxi.com/china/20180611/2279379.shtml")
    website.crawl()
