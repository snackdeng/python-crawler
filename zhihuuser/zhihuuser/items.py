# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item,Field


class UserItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    id = Field()
    name = Field()
    avatar_url = Field()
    url_token=Field()
    use_default_avatar=Field()
    avatar_url_template=Field()
    type=Field()
    url=Field()
    user_type=Field()
    headline=Field()
    follower_count=Field()
    answer_count=Field()
    articles_count=Field()
