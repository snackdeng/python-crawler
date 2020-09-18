# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class XiaoshuoPipeline(object):
    def open_spider(self, spider):
        self.file = open('龙族5悼亡者的归来.txt', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        title = item['title']
        content = item['content']
        info = title + '\n' + content + '\n'
        self.file.write(info)
        return item

    def close_spider(self, spider):
        self.file.close()

