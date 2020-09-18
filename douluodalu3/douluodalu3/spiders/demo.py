# -*- coding: utf-8 -*-
import scrapy


class DemoSpider(scrapy.Spider):
    name = 'demo'
    allowed_domains = ['biquge.info']
    start_urls = ['http://www.biquge.info/22_22522/8096674.html']

    def parse(self, response):
        title = response.xpath('//h1/text()').extract_first()
        content = ''.join(response.xpath('//div[@id="content"]/text()').extract()).replace('    ','\n')
        yield {
            'title':title,
            'content':content
        }
        next_url = response.xpath('//div[@class="bottem1"]/a[4]/@href').extract_first()
        if next_url.find('.html')!=-1:
            yield scrapy.Request(next_url,callback=self.parse)