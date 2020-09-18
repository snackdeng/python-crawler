# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json

# 之所以不用with open这个方法，是因为加一次数据就要打开一次文件，所以使用方法即可以一直打开文件

class MaoyanPipeline(object):
    def open_spider(self,spider):
        self.filename = open('movie.txt','a',encoding='utf-8')

    def process_item(self, item, spider):
        # with open('movie.txt','a',encoding='utf-8') as f:
        #     f.write(json.dumps(item,ensure_ascii=False))
        # print(item)
        # 如果它提示序列化错误，就是没有转化为字典
        self.filename.write(json.dumps(dict(item),ensure_ascii=False) + '\n')
        return item

    def close_spider(self,spider):
        self.filename.close()