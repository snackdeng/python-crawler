# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class ZwwSpider(CrawlSpider):
    name = 'zww'
    allowed_domains = ['81zw.us']
    start_urls = ['https://www.81zw.us/book/25483/']

    rules = (
        # //dl/dd[10]/a 只需要定位在这一行就行了，不需要精准定位其中的属性
        Rule(LinkExtractor(restrict_xpaths=r'//dl/dd[10]/a'), callback='parse_item', follow=True),
        Rule(LinkExtractor(restrict_xpaths=r'//div[@class="bottem1"]/a[4]'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        title = response.xpath('//h1/text()').extract_first()
        # 因为返回的是一个列表，即需要把列表拼接在一起
        content = ''.join(response.xpath('//div[@id="content"]/text()').extract()).replace('\r\n\r\n','\n')
        yield {
            'title': title,
            'content': content
        }



