# -*- coding: utf-8 -*-
from scrapy import Spider,Request
import json

from zhihuuser.items import UserItem

class ExampleSpider(Spider):
    name = 'example'
    allowed_domains = ['zhihu.com']
    start_urls = ['http://www.zhihu.com']

    user_url = 'https://www.zhihu.com/api/v4/members/{user}/relations/mutuals?include={include}'
    user_query = 'data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics'

    start_user = 'silent1226'

    follows_url = 'https://www.zhihu.com/api/v4/members/{user}/followees?include={include}&offset={offset}&limit={limit}'
    follows_query = 'data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics'

    def start_requests(self):
        yield Request(self.user_url.format(user=self.start_user,include = self.user_query),self.parse_user)
        yield Request(self.follows_url.format(user=self.start_user,include=self.follows_query,offset=0,limit=20),callback = self.parse_follows)

    def parse_user(self, response):
        result = json.loads(response.text)
        item = UserItem()
        for field in item.fields:
            if field in result.key():
                item[field] = result.get(field)
        yield item
        yield Request(self.follows_url.format(user=result.get('url_token'),include= self.follows_query,limit=20,offset=0),self.parse_follows)

    def parse_follows(self,response):
        results = json.loads(response.text)

        if 'data' in results.keys():
            for result in results.get('data'):
                yield Request(self.user_url.format(user= result.get('url_token'),include=self.user_query),self.parse_user)

        if 'paging' in results.keys() and results.get('paging').get('is_end')== False:
            next_page = results.get('paging').get('next')
            yield Request(next_page,self.parse_follows)
