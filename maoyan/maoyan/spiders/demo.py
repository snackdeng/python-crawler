# -*- coding: utf-8 -*-
import scrapy
from maoyan.items import MaoyanItem

class DemoSpider(scrapy.Spider):
    name = 'demo'
    allowed_domains = ['maoyan.com']
    start_urls = ['https://maoyan.com/films?showType=3']

    def parse(self, response):
        names = response.xpath('//div[@class="channel-detail movie-item-title"]/@title').extract()
        scores_div = response.xpath('//div[@class="channel-detail channel-detail-orange"]')

        scores = []
        for score in scores_div:
            # Xpath string()提取多个子节点中的文本
            scores.append(score.xpath('string(.)').extract_first())

        item = MaoyanItem()
        for name,score in zip(names,scores):
            # print(name,":",score)
            # 推送到pipelines中，只接受字典和item对象
            # 字典  yield {'name':name,'score':score}
            item['name'] = name
            item['score'] = score
            yield item
