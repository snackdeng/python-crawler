# -*- coding: utf-8 -*-
import scrapy


class BkpythonSpider(scrapy.Spider):
    name = 'bkpython'
    allowed_domains = ['baike.baidu.com']
    start_urls = ['https://baike.baidu.com/item/Python%E7%BC%96%E7%A8%8B/2142769?fr=aladdin']

    def parse(self, response):
        filename = 'python.html'
        with open(filename,'wb') as fp:
            fp.write(response.body)

