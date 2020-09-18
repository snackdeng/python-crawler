import requests
from lxml import etree
import pymysql
import pymongo
import time


class GuokeSpider():
    def __init__(self):
        self.start_url = "https://www.guokr.com/ask/highlight/?page={}"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36"
        }
        self.db = pymysql.connect(host='localhost',user='root',password='snackdeng',port=3306,db='spiders')
        self.client = pymongo.MongoClient('mongodb://admin:snackdeng@localhost:27017')

    def get_page(self, url):
        response = requests.get(url=url, headers=self.headers)
        return response.content.decode()


    def get_data(self,response):
        html = etree.HTML(response)
        ask_lists = html.xpath('//ul[@class="ask-list-cp"]/li')
        data = []
        for ask_list in ask_lists:
            items = {}
            items['ask'] = ask_list.xpath('.//a[@target="_blank"]/text()')[0]
            items['ans'] = ask_list.xpath('.//p[@class="ask-list-summary"]/text()')[0].strip()
            items['url'] = ask_list.xpath('.//a[@target="_blank"]/@href')[0]
            data.append(items)
        return data

    def save_mysql(self, data):
        # print(data)
        for i in data:

            print(i)
            cursor = self.db.cursor()
            table = 'guo_ke_wen_da'
            keys = ','.join(i.keys())
            values = ', '.join(['%s'] * len(i))
            sql = 'INSERT INTO {table}({keys}) VALUES ({values})'.format(table=table, keys=keys, values=values)
            try:
                if cursor.execute(sql, tuple(i.values())):
                    print('Successful')
                    # 对于数据库的增删改查，需要调用commit（）方法
                    self.db.commit()
            except:
                print('Failed')
                # 保存就回滚
                self.db.rollback()

    def save_mongo(self,data):
        for i in data:
            db = self.client.spider
            collection = db.guo_ke_wen_da
            result = collection.insert(i)
            print('正在写入mongo数据库')


    def run(self):
        # start_url
        for i in range(1, 101):
            time.sleep(1)
            url = self.start_url.format(i)
            print('正在爬{}页'.format(i))
        # 请求这个网址
            response = self.get_page(url)

        # 获取想要的信息
            data = self.get_data(response)
            # print(data)
        # 保存资料
            self.save_mysql(data)
            self.save_mongo(data)

        self.db.close()
        print('爬虫结束，正在关闭mysql数据库')
        self.client.close()
        print('爬虫结束，正在关闭mongodb数据库')


if __name__ == "__main__":
    spider = GuokeSpider()
    spider.run()