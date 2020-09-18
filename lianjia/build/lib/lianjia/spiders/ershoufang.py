# -*- coding: utf-8 -*-
import scrapy
import re


class ErshoufangSpider(scrapy.Spider):
    name = 'ershoufang'
    allowed_domains = ['lianjia.com']
    start_urls = ['https://qd.lianjia.com/ershoufang/pg{}/'.format(num) for num in range(1,101)]

    def parse(self, response):
        urls = response.xpath('//div[@class="info clear"]/div[@class="title"]/a/@href').extract()
        for url in urls:
            yield scrapy.Request(url,callback=self.info_pare)

    def info_pare(self,response):
        # concat 使两个xpath结合在一起
        total = response.xpath('concat(//span[@class="total"]/text(),//span[@class="unit"]/span/text())').extract_first()
        total = re.findall(r'\d+\.?\d*',total)
        unitPriceValue = response.xpath('string(//span[@class="unitPriceValue"])').extract_first()
        unitPriceValue = re.findall(r'\d+\.?\d*', unitPriceValue)
        # a = response.xpath('//div[@class="brokerInfoText"]/div[@class="phone"]/text()').extract()
        # tel = "转".join(a)
        xiao_qu = response.xpath('//div[@class="communityName"]/a[1]/text()').extract_first()
        qu_yu = response.xpath('//div[@class="areaName"]/span[@class="info"]/a[1]').extract_first()

        base = response.xpath('//div[@class="base"]//ul')
        hu_xing = base.xpath('./li[1]/text()').extract_first()
        lou_ceng = base.xpath('./li[2]/text()').extract_first()
        mian_ji = base.xpath('./li[3]/text()').extract_first()
        mian_ji = re.findall(r'\d+\.?\d*', mian_ji)
        zhuang_xiu = base.xpath('./li[9]/text()').extract_first()
        dian_hu = base.xpath('./li[10]/text()').extract_first()
        dian_ti = base.xpath('./li[last()-1]/text()').extract_first()
        chan_quan = base.xpath('./li[last()-0]/text()').extract_first()

        transaction = response.xpath('//div[@class="transaction"]//ul')
        yong_tu = transaction.xpath('./li[4]/span[2]/text()').extract_first()
        nian_xian = transaction.xpath('./li[5]/span[2]/text()').extract_first()
        di_ya = transaction.xpath('./li[7]/span[2]/text()').extract_first().strip()

        yield {
            '房价/万':total,
            # '电话':tel,
            '单价元/平米':unitPriceValue,
            '所在小区':xiao_qu,
            '所在区域':qu_yu,
            # '户型':hu_xing,
            '楼层':lou_ceng,
            '面积M^2':mian_ji,
            '装修':zhuang_xiu,
            # '梯户比':dian_hu,
            '电梯':dian_ti,
            # '产权':chan_quan,
            # '用途':yong_tu,
            # '年限':nian_xian,
            # '抵押':di_ya
        }
