# -*- coding: utf-8 -*-
import scrapy
from ..items import YangguangzhengwuItem

class DemoSpider(scrapy.Spider):
    name = 'demo'
    allowed_domains = ['sun0769.com']
    start_urls = ['http://wz.sun0769.com/political/index/politicsNewest?id=1&type=4&page=0']

    def parse(self, response):
        # 分组
        # li_list = response.css('.title-state-ul')
        print("----")
        li_list = response.xpath('//ul[@class="title-state-ul"]/li')
        for li in li_list:
            item = YangguangzhengwuItem()
            item["title"] = li.xpath('.//a[@class="color-hover"]/text()').extract_first()
            item["href"] = li.xpath('.//a[@class="color-hover"]/@href').extract_first()
            item["publish_date"] = li.xpath('./span[last()]/text()').extract_first()
            nexts_url = 'http://wz.sun0769.com'+ item["href"]
            yield scrapy.Request(nexts_url,callback=self.parse_detail,meta={"item":item})
        next_url = response.xpath('//a[@class="arrow-page prov_rota"]/@href').extract_first()
        if next_url is not None:
            next_url = 'http://wz.sun0769.com' + next_url
            yield scrapy.Request(next_url,callback=self.parse)

    def parse_detail(self,response):
        print('-----------------')
        item = response.meta["item"]
        item["content"] = response.xpath('//div[@class="details-box"]/pre/text()').extract()
        item["content_img"] = response.xpath('//div[@class="clear details-img-list Picture-img"]/img/@src').extract()
        yield item
