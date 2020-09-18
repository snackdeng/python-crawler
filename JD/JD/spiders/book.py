# -*- coding: utf-8 -*-
import scrapy
from JD.items import JdItem
import re
# 1.导入分布式爬虫类
from scrapy_redis.spiders import RedisSpider

# 2.继承分布式爬虫类
class BookSpider(RedisSpider):
    name = 'book'
    # 3.注销start_urls & allowed-domains
    # allowed_domains = ['jd.com']
    # # 修改起始的url
    # start_urls = ['https://book.jd.com/booksort.html']

    # 4.设置redis-key
    redis_key = 'py21'

    # 5.设置__init__
    def __init__(self,*args,**kwargs):
        domain = kwargs.pop("domain", '')
        self.allowed_domain = list(filter(None, domain.split(',')))
        super(BookSpider, self).__init__(*args,**kwargs)


    def parse(self, response):
        # 获取所以大分类节点列表
        big_node_list = response.xpath('//*[@id="booksort"]/div[2]/dl/dt/a')
        for big_node in big_node_list:
            big_category = big_node.xpath('./text()').extract_first()
            big_category_link = response.urljoin(
                big_node.xpath('./@href').extract_first())
            # 获取小分类节点
            small_node_list = big_node.xpath('../following-sibling::dd[1]/em/a')
            for small_node in small_node_list:
                temp = {}
                temp["big_category"] = big_category
                temp["big_category_link"] = big_category_link
                temp["big_category_link"] = big_category_link
                temp["small_category"] = small_node.xpath(
                    './text()').extract_first()
                temp["small_category_link"] = response.urljoin(
                    small_node.xpath('./@href').extract_first())
                # 模拟点击小分类连接
                yield scrapy.Request(
                    url=temp["small_category_link"],
                    callback=self.parse_book_list,
                    meta={"py21": temp}
                )

    def parse_book_list(self, response):
        temp = response.meta['py21']
        book_list = response.xpath('//*[@id="J_goodsList"]/ul/li/div')
        data = ""
        for book in book_list:
            item = JdItem()
            item['big_category'] = temp["big_category"]
            item['big_category_link'] = temp["big_category_link"]
            item['small_category'] = temp["small_category"]
            item['small_category_link'] = temp["small_category_link"]

            item['bookname'] = book.xpath(
                './div[3]/a/em/text()').extract_first()
            item['author'] = book.xpath(
                './div[4]/span[1]/a/text()').extract_first()
            item['link'] = book.xpath('./div[1]/a/@href').extract_first()
            item['price'] = book.xpath(
                './div[2]/strong/i/text()').extract_first()
            yield item

            next_url = book.xpath('.//i[@class="promo-words"]/@id').extract_first().split(
                '_')[-1]
            data += next_url + ','
        cat = response.url.split('=')[-1].replace(",", "%2c")

        yield scrapy.Request(
            url=f'https://list.jd.com/listNew.php?cat={cat}&page=2&s=27&scrolling=y&tpl=2_M&isList=1&show_items={data[:-1]}',
            callback=self.parse_book_list_one,
            meta={"py21": temp},
            headers={
                "referer": "https://list.jd.com/list.html?cat=1713,3258,3297"}
        )

    def parse_book_list_one(self, response):
        temp = response.meta['py21']
        book_list = response.xpath('//li[@class="gl-item"]')
        for book in book_list:
            item = JdItem()
            item['big_category'] = temp["big_category"]
            item['big_category_link'] = temp["big_category_link"]
            item['small_category'] = temp["small_category"]
            item['small_category_link'] = temp["small_category_link"]

            item['bookname'] = book.xpath(
                './/div[@class="p-name"]/a/em/text()').extract_first()
            item['author'] = book.xpath(
                './/div[@class="p-bookdetails"]/span[1]/a/text()').extract_first()
            item['link'] = book.xpath(
                './/div[@class="p-name"]/a/@href').extract_first()
            item['price'] = book.xpath(
                './/div[@class="p-price"]/strong/i/text()').extract_first()

            yield item