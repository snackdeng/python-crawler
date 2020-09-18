# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JdItem(scrapy.Item):
    # define the fields for your item here like:
    big_category = scrapy.Field()
    big_category_link = scrapy.Field()
    small_category = scrapy.Field()
    small_category_link = scrapy.Field()
    bookname = scrapy.Field()
    author = scrapy.Field()
    link = scrapy.Field()
    price = scrapy.Field()
    pass
