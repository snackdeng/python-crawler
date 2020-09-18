# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from pymysql import connect

class LianjiaPipeline(object):
    def open_spider(self,spider):
        self.client = pymongo.MongoClient('mongodb://admin:snackdeng@localhost:27017')

    def process_item(self, item, spider):
        self.client.room.lianjia.insert(item)
        return item

    def close_spider(self, spider):
        self.client.close()

class MysqlPipeline(object):
    def open_spider(self, spider):
        self.client = connect(host='localhost',user='root',password='snackdeng',port=3306,db='room',charset='utf8')
        self.cursor = self.client.cursor()

    def process_item(self, item, spider):
        args = [item['房价/万'],
                # item['电话'],
                item['单价元/平米'],
                item['所在小区'],
                item['所在区域'],
                # item['户型'],
                item['楼层'],
                item['面积M^2'],
                item['装修'],
                # item['梯户比'],
                item['电梯'],
                # item['产权'],
                # item['用途'],
                # item['年限'],
                # item['抵押'],
]
        sql = 'insert into lianjia VALUES (0,%s,%s,%s,%s,%s,%s,%s,%s)'
        self.cursor.execute(sql,args)
        self.client.commit()
        return item

    def close_spider(self, spider):
        self.cursor.close()
        self.client.close()
