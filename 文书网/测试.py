# -*- coding:utf-8 -*-
"""
作者：snackdeng
日期：2020/08/05 爬取详情界面
"""

# __author__ = "zok" 362416272@qq.com
# Date: 2020/7/24 Python:3.7

import requests
import time
import random
import json
import base64
from datetime import datetime
from Crypto import des3


class WenShu:

    def __init__(self):
        self.js = None

    @staticmethod
    def get_now_data():
        return datetime.now().strftime('%Y%m%d')

    @staticmethod
    def random_key():
        random_str = ''
        base_str = 'ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz0123456789'
        length = len(base_str) - 1
        for i in range(24):
            random_str += base_str[random.randint(0, length)]
        return random_str

    @staticmethod
    def make_id():
        """id
        """
        return datetime.now().strftime('%Y%m%d%H%M%S')

    def make_cipher_text(self):
        time_13 = str(int(round(time.time() * 1000)))
        key = self.random_key()
        now = self.get_now_data()
        _str = des3.encryption(time_13, key, now)
        _str = key + now + _str
        new_str = ''
        for i in _str:
            if i != 1:
                new_str += " "
            new_str += str(bin(ord(i))[2:])
        return new_str.strip()

    def make_request(self,i):
        info = {
            "id": self.make_id(),
            "command": "queryDoc",
            "params": {
                "devid": "831e5aaa75c94f86a572c54dd05037ec",
                "devtype": "1",
                "ciphertext": self.make_cipher_text(),
                "pageSize": "20",
                "sortFields": "s50:desc",
                "pageNum": "1",
                "queryCondition":[{"key":"s21",
                                   "value":f"{i}"}]
            }
        }

        return info

    def to_index(self,i):
        url = 'http://wenshuapp.court.gov.cn/appinterface/rest.q4w'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 5.1.1; MI 9 Build/LMY48Z)',
            'Host': 'wenshuapp.court.gov.cn',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip',
        }
        txt = str(self.make_request(i))

        request = base64.b64encode(txt.encode('utf-8')).decode('utf-8')
        print(f"当前请求的是 :{i}")
        data = {
            'request': request
        }
        proxies = {
            "https":"58.218.200.225:6350"
        }
        response = requests.post(url, headers=headers, data=data,proxies=proxies)
        if 'HTTP Status 503' in response.text:
            print('【服务器繁忙】 爬的人太多了， 请重试')
            exit()
        data1 = json.loads(response.text)
        content = data1.get('data').get('content')
        key = data1.get('data').get('secretKey')
        iv = self.get_now_data()
        _str = des3.decrypt(content, key, iv)
        print(key,iv)
        rowkey_lists = json.loads(_str)
        rowkey_list = rowkey_lists.get("queryResult").get("resultList")
        for rowkey in rowkey_list:
            print("已经获取详细页面的："+ rowkey["rowkey"] + "正在进入.....")
            self.prase_page(rowkey["rowkey"])



    def prase_page(self,rowkey):
        info = {
            "id": self.make_id(),
            "command": "docInfoSearch",
            "params": {
                "devtype": "1",
                "ciphertext": self.make_cipher_text(),
                "devid": "831e5aaa75c94f86a572c54dd05037ec",
                "docId":f"{rowkey}"
            }
        }
        request = base64.b64encode(str(info).encode('utf-8')).decode('utf-8')
        url = 'http://wenshuapp.court.gov.cn/appinterface/rest.q4w'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 5.1.1; MI 9 Build/LMY48Z)',
            'Host': 'wenshuapp.court.gov.cn',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip',
        }
        proxies = {
            "https": "58.218.200.225:6350"
        }
        data = {
            'request': request
        }
        response = requests.post(url,headers=headers,data=data,proxies=proxies)
        if 'HTTP Status 503' in response.text:
            print('【服务器繁忙】 爬的人太多了， 请重试')
            exit()
        data1 = json.loads(response.text)
        content = data1.get('data').get('content')
        key = data1.get('data').get('secretKey')
        iv = self.get_now_data()
        _str = des3.decrypt(content, key, iv)
        self.get_data(_str)

    def get_data(self,_str):
        #这里写你的提取详细页面得逻辑
        text = json.loads(_str)
        print(text)



if __name__ == '__main__':
    ws = WenShu()
    for i in ["安徽赋力大数据处理服务有限公司","阿里巴巴"]:
        ws.to_index(i)


"""
{"id":"20200806094441","command":"docInfoSearch","params":{"ciphertext":"1101111 1000011 1000001 1101000 111000 1001011 1010100 1001011 1100101 110011 1100100 1001000 1111001 1010011 110101 110001 1100101 1001000 1011000 110011 1110101 1010010 1100111 1001001 110010 110000 110010 110000 110000 111000 110000 110110 1100011 1101010 110110 1001101 1100011 1010100 1100101 1011001 110010 1010011 1110000 1010101 1110010 101011 1011001 1010100 1000011 1101011 1011001 110011 111000 1010001 111101 111101","docId":"0f04d2ace5114866a235aba700b8c8a5","devtype":"1","devid":"831e5aaa75c94f86a572c54dd05037ec"}}"""