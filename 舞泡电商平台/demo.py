import requests
from lxml import etree
from PIL import Image
import io
from urllib.parse import urljoin
import pytesseract

url = "https://shop.5pao.com/tmallIndexNew-3------------------------------1.html"
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
}
response = requests.get(url=url,headers=headers).text
html = etree.HTML(response)
title = html.xpath('//span[@class="layui-inline title"]/@title')
main = html.xpath('//ul[@class="shopAttr"]/li[1]/span[2]/text()')
city = html.xpath('//ul[@class="shopAttr"]/li[3]/span[2]/text()')
Mall_type = html.xpath('//ul[@class="shopAttr"]/li[5]/span[2]/text()')
Tax_qualification = html.xpath('//ul[@class="shopAttr"]/li[7]/span[2]/text()')
image_name = html.xpath('//div[@class="price"]/img/@src')[0]
image_url = urljoin(url,image_name)
# 获取二进制文件
image_boby = requests.get(image_url).content
# 获取对象
image_stream = Image.open(io.BytesIO(image_boby))
# 打印结果
print(pytesseract.image_to_string(image_stream))


