# -*- coding:utf-8 -*-
"""
作者：snackdeng
日期：2020/06/14
"""
import requests
from urllib.parse import urljoin
import re,os
from lxml import etree
import time


def page_get(url):
    headers = {
        "Cookie": "searchtime=1592115718; Hm_lvt_672e68bf7e214b45f4790840981cdf99=1592115673; UM_distinctid=172b17d37241a3-0b938fc5fa3b16-f7d123e-100200-172b17d3725578; CNZZDATA1277874215=1970258464-1592110379-%7C1592110379; Hm_lpvt_672e68bf7e214b45f4790840981cdf99=1592115712",
        "Host": "www.mm131.net",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"
    }
    time.sleep(0.5)
    res = requests.get(url, headers=headers, allow_redirects=False)
    html = res.content.decode('gbk')
    return html


def scrape_html():
    key = input('请输入你要输入的词：')
    n = 1
    number = 100
    while n <= number:
        url = f'https://www.mm131.net/search/?key={key}&page={n}'
        htmls = page_get(url)
        html = etree.HTML(htmls)
        try :
            next_url = html.xpath('//ul[@class="newpage"]/a[@class="all"]/@href')[0]
        except IndexError:
            time.sleep(0.5)
        finally:
            print(next_url)
            number = int(next_url.split('=')[-1])
            # print(number)
            print(url)
            lis = html.xpath('//ul[@class="e2"]/li')
            for li in lis:
                detail_url = li.xpath('./a[@class="preview"]/@href')[0]

                name = li.xpath('./a/text()')[0]
                os.mkdir(f'./图片/{name}')
                num = detail_url.split('/')[-1].split('.')[0]
                print(f'正在爬取的是第{n}页的网址是{detail_url}')
                detail_html(detail_url, num, name)
        n += 1


def detail_html(url, num, name):
    text = page_get(url)
    number = re.findall('<span class="page-ch">共(.*?)页</span>', text)
    print(f'此url共{number}张图片')
    for i in range(1, int(number[0]) + 1):
        img_url = f'https://img1.mmmw.net/pic/{num}/{i}.jpg'
        headers = {
            "Referer": url,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"
        }
        time.sleep(0.5)
        response = requests.get(img_url, headers=headers).content
        print(f'正在保存此url下的{i}张照片', img_url)
        files = './图片/{0}/'
        with open(files.format(name) + '{0}.jpg'.format(i), 'wb') as f:
            f.write(response)


def run():
    scrape_html()


if __name__ == '__main__':
    run()
