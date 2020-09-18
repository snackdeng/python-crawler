import base64
import csv
import re, json, time
import zlib

import requests
from fake_useragent import UserAgent
import random


with open('浙江省美食.csv', 'w', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(["店铺长ID", "店铺名称", "地址", "店铺分类", "品类", "省", "市", "区", "手机"])

prox = [{"https": "122.192.226.29:4278"},
        {"https": "114.104.239.98:4270"},
        {"https": "115.213.224.153:4223"},
        {"https": "60.184.119.69:4285"},
        {"https": "121.233.160.239:4282"},
        {"https": "114.99.23.39:4232"},
        {"https": "112.114.88.218:4232"},
        {"https": "110.246.202.155:4267"},
        {"https": "123.181.147.104:4241"},
        {"https": "122.192.227.72:4278"},
        {"https": "180.109.146.92:4232"},
        {"https": "106.5.175.51:4232"},
        {"https": "183.165.32.111:4235"},
        {"https": "223.247.27.3:4216"},
        {"https": "123.186.228.209:4223"},
        {"https": "223.215.177.43:4242"},
        {"https": "125.121.170.188:4217"},
        {"https": "14.134.186.2:4272"},
        {"https": "27.191.168.9:4282"},
        {"https": "183.165.8.128:4234"}]


def get_city():
    url = "https://www.meituan.com/ptapi/getprovincecityinfo/"
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Content-Type": "application/json",
        # "Cookie": "_lxsdk_cuid=173a2d80134c8-00aed6a451569d-3323765-100200-173a2d80134c8; iuuid=A50CA613ECE9A8317FEB14F615C0F63A50F60835D5D8F53D2E3C118774D6406D; _lxsdk=A50CA613ECE9A8317FEB14F615C0F63A50F60835D5D8F53D2E3C118774D6406D; wm_order_channel=mtib; utm_source=60030; service-off=0; IJSESSIONID=12rjww0csjhwayj34g8m6mo1; __utmc=74597006; ci3=1; au_trace_key_net=default; openh5_uuid=A50CA613ECE9A8317FEB14F615C0F63A50F60835D5D8F53D2E3C118774D6406D; userId=638445496; rvct=51%2C50%2C182%2C1; uuid=c35677e47c21477fa5ee.1597116946.1.0.0; mtcdn=K; u=638445496; n=BcZ684268709; lt=PBYxDcOuNqJO-tBECHeMvNCZpOsAAAAAPAsAAJd9bXf5HYGFjKGiAvz6XTvFZOvkZxCxCigYUqUoCNqtpE4fSbStcH1GdHE1u0clow; mt_c_token=PBYxDcOuNqJO-tBECHeMvNCZpOsAAAAAPAsAAJd9bXf5HYGFjKGiAvz6XTvFZOvkZxCxCigYUqUoCNqtpE4fSbStcH1GdHE1u0clow; token=PBYxDcOuNqJO-tBECHeMvNCZpOsAAAAAPAsAAJd9bXf5HYGFjKGiAvz6XTvFZOvkZxCxCigYUqUoCNqtpE4fSbStcH1GdHE1u0clow; lsu=; token2=PBYxDcOuNqJO-tBECHeMvNCZpOsAAAAAPAsAAJd9bXf5HYGFjKGiAvz6XTvFZOvkZxCxCigYUqUoCNqtpE4fSbStcH1GdHE1u0clow; unc=BcZ684268709; isid=785ACDD2B3ADC5E2A6548EDF98BC901C; logintype=normal; oops=PBYxDcOuNqJO-tBECHeMvNCZpOsAAAAAPAsAAJd9bXf5HYGFjKGiAvz6XTvFZOvkZxCxCigYUqUoCNqtpE4fSbStcH1GdHE1u0clow; __utma=74597006.467048628.1597070107.1597071894.1597126911.3; __utmz=74597006.1597126911.3.3.utmcsr=m.baidu|utmccn=m.baidu|utmcmd=organic|utmcct=100001; cssVersion=3fee96cb; meishi_ci=51; cityid=51; p_token=PBYxDcOuNqJO-tBECHeMvNCZpOsAAAAAPAsAAJd9bXf5HYGFjKGiAvz6XTvFZOvkZxCxCigYUqUoCNqtpE4fSbStcH1GdHE1u0clow; _hc.v=83c3a596-ce70-a2b9-4c11-5009549ae202.1597126919; latlng=27.457455,112.176884,1597129146423; ci=51; cityname=%E5%AE%81%E6%B3%A2; i_extend=C_b1Gimthomepagecategory11H__a; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; client-id=7b926485-4d9c-429d-8160-9075a390c0b2; lat=29.831027; lng=121.568462; firstTime=1597131767251; _lxsdk_s=173dc2e1d3a-55-85e-62c%7C%7C149",
        "Host": "www.meituan.com",
        "Pragma": "no-cache",
        "Referer": "https://www.meituan.com/changecity/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": UserAgent().random,
    }
    response = requests.get(url, headers=headers,verify=False).json()
    for city_list in response:
        sheng = city_list["provinceName"]
        if sheng == "浙江":
            for city in city_list["cityInfoList"]:
                city_name = city["name"]  # 宁波
                acronym = city["acronym"]  # nb
                if city_name == "杭州":
                    continue
                # get_quyu(acronym)
                get_one(sheng, city_name, acronym)


# 在列表面获取详细页面的参数
def get_one(sheng, city_name, acronym):
    i = 1
    while True:
        url = f"https://{acronym}.meituan.com/meishi/api/poi/getPoiList"
        headers = {
            "Accept": "application/json",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Connection": "keep-alive",
            "Content-Type": "application/json",
            "Cookie": "_lxsdk_cuid=173a2d80134c8-00aed6a451569d-3323765-100200-173a2d80134c8; iuuid=A50CA613ECE9A8317FEB14F615C0F63A50F60835D5D8F53D2E3C118774D6406D; _lxsdk=A50CA613ECE9A8317FEB14F615C0F63A50F60835D5D8F53D2E3C118774D6406D; wm_order_channel=mtib; utm_source=60030; mtcdn=K; lsu=; __utma=74597006.467048628.1597070107.1597071894.1597126911.3; __utmz=74597006.1597126911.3.3.utmcsr=m.baidu|utmccn=m.baidu|utmcmd=organic|utmcct=100001; _hc.v=83c3a596-ce70-a2b9-4c11-5009549ae202.1597126919; latlng=27.457455,112.176884,1597129146423; cityname=%E5%AE%81%E6%B3%A2; i_extend=C_b1Gimthomepagecategory11H__a; ci=50; rvct=50%2C51%2C182%2C1; client-id=c7fb0c59-7e16-4778-aa32-ee020aa38353; uuid=462c74e4dce74185ae24.1597192814.1.0.0; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; __mta=53802391.1597069990249.1597190167263.1597192815592.12; lat=30.480392; lng=120.191836; userTicket=yvUhyHpCQwHbfGhAukqZMAyDpnDmLdrWLwaoizJL; u=638445496; n=BcZ684268709; lt=77VHOjZ56P0vpZuT-E2wWqvruCoAAAAAVgsAACIgt39yYWa22RsS4PgjA91xqX8bvX1lrjSf8xqULjv23bMZsuw4omh-JK6iYNOAtw; mt_c_token=77VHOjZ56P0vpZuT-E2wWqvruCoAAAAAVgsAACIgt39yYWa22RsS4PgjA91xqX8bvX1lrjSf8xqULjv23bMZsuw4omh-JK6iYNOAtw; token=77VHOjZ56P0vpZuT-E2wWqvruCoAAAAAVgsAACIgt39yYWa22RsS4PgjA91xqX8bvX1lrjSf8xqULjv23bMZsuw4omh-JK6iYNOAtw; token2=77VHOjZ56P0vpZuT-E2wWqvruCoAAAAAVgsAACIgt39yYWa22RsS4PgjA91xqX8bvX1lrjSf8xqULjv23bMZsuw4omh-JK6iYNOAtw; unc=BcZ684268709; firstTime=1597192937573; _lxsdk_s=173e01c3f6d-88a-f57-e4c%7C%7C15",
            "Referer": f"https://{acronym}.meituan.com/meishi/",
            "Host": "meishi.meituan.com",
            "Origin": "http://meishi.meituan.com",
            "User-Agent": UserAgent().random,
            "x-requested-with": "XMLHttpRequest",
        }
        params = {
            "cityName": city_name,
            "cateId": "0",
            "areaId": "0",
            "sort": "",
            "dinnerCountAttrId": "",
            "page": i,
            "userId": "638445496",
            "uuid": "c35677e47c21477fa5ee.1597116946.1.0.0",
            "platform": "1",
            "partner": "126",
            "originUrl": f"https://{acronym}.meituan.com/meishi/",
            "riskLevel": "1",
            "optimusCode": "10",
            "_token": encrypt_token(acronym, city_name),
        }
        # proxies = random.choice(prox) proxies=proxies,
        try:
            response = requests.get(url, headers=headers, params=params)
        except requests.exceptions.ProxyError as e:
            print("代理错误",e)
            time.sleep(1)
            continue
        else:
            shop_id_list = response.json()["data"]["poiInfos"]
            if shop_id_list:
                # print(shop_id_list)
                for shop_id in shop_id_list:
                    id = shop_id["poiId"]

                    get_data(id, sheng, city_name, acronym)
                with open(f'{sheng}省美食.csv', 'rt',
                          encoding='utf-8')as fin:  # 读有空行的csv文件，舍弃空行
                    lines = ''
                    for line in fin:
                        if line != '\n':
                            lines += line
                with open(f'{sheng}省美食.csv', 'wt',
                          encoding='utf-8')as fout:  # 再次文本方式写入，不含空行
                    fout.write(lines)
                print("第%d页爬取完毕" % i)
                i += 1
            else:break

# 获取详情页面的信息
def get_data(id, sheng, city_name, acronym):
    for _ in range(10):
        url = f"https://www.meituan.com/meishi/{id}/"
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Cookie": "_lxsdk_cuid=173a2d80134c8-00aed6a451569d-3323765-100200-173a2d80134c8; iuuid=A50CA613ECE9A8317FEB14F615C0F63A50F60835D5D8F53D2E3C118774D6406D; _lxsdk=A50CA613ECE9A8317FEB14F615C0F63A50F60835D5D8F53D2E3C118774D6406D; wm_order_channel=mtib; utm_source=60030; mtcdn=K; lsu=; __utma=74597006.467048628.1597070107.1597071894.1597126911.3; __utmz=74597006.1597126911.3.3.utmcsr=m.baidu|utmccn=m.baidu|utmcmd=organic|utmcct=100001; _hc.v=83c3a596-ce70-a2b9-4c11-5009549ae202.1597126919; latlng=27.457455,112.176884,1597129146423; cityname=%E5%AE%81%E6%B3%A2; i_extend=C_b1Gimthomepagecategory11H__a; client-id=7b926485-4d9c-429d-8160-9075a390c0b2; __mta=49567129.1597144318361.1597144318361.1597144318361.1; ci=50; rvct=50%2C51%2C182%2C1; uuid=462c74e4dce74185ae24.1597192814.1.0.0; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; lat=30.480392; lng=120.191836; userTicket=yvUhyHpCQwHbfGhAukqZMAyDpnDmLdrWLwaoizJL; u=638445496; n=BcZ684268709; lt=77VHOjZ56P0vpZuT-E2wWqvruCoAAAAAVgsAACIgt39yYWa22RsS4PgjA91xqX8bvX1lrjSf8xqULjv23bMZsuw4omh-JK6iYNOAtw; mt_c_token=77VHOjZ56P0vpZuT-E2wWqvruCoAAAAAVgsAACIgt39yYWa22RsS4PgjA91xqX8bvX1lrjSf8xqULjv23bMZsuw4omh-JK6iYNOAtw; token=77VHOjZ56P0vpZuT-E2wWqvruCoAAAAAVgsAACIgt39yYWa22RsS4PgjA91xqX8bvX1lrjSf8xqULjv23bMZsuw4omh-JK6iYNOAtw; token2=77VHOjZ56P0vpZuT-E2wWqvruCoAAAAAVgsAACIgt39yYWa22RsS4PgjA91xqX8bvX1lrjSf8xqULjv23bMZsuw4omh-JK6iYNOAtw; firstTime=1597192899333; unc=BcZ684268709; _lxsdk_s=173e01c3f6d-88a-f57-e4c%7C%7C10",
            "Referer": f"https://{acronym}.meituan.com/meishi/",
            "Host": "www.meituan.com",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": UserAgent().random,
        }
        # proxies = random.choice(prox) proxies=proxies
        try :
            response = requests.get(url, headers=headers,
                                )
        except requests.exceptions.ProxyError as e:
            print("详细页面，代理错误",e)
            time.sleep(1)
            continue
        try:
            json_data = json.loads(re.findall(
                '</script><script>window._appState = (.*?);</script><script src=',
                response.text)[0])
        except  :
            print("验证码来了")
            time.sleep(10)
            continue
        else:
            id = id
            # print(json_data)
            title = json_data["detailInfo"]["name"]
            address = json_data["detailInfo"]["address"]
            sheng = sheng + "省"
            shi = city_name + "市"
            phone = re.findall(r'"phone":"(.*?)",', response.text, re.S)[0]
            type = json_data["crumbNav"][2]["title"]
            if type:
                type = type.replace(f"{city_name}", "")
            else:
                type = "炒菜"
            if re.findall(r'(.*?)区', address, re.S):
                qu = re.findall(r'(.*?)区', address, re.S)[0] + "区"
            elif re.findall(r'(.*?)市', address, re.S):
                qu = re.findall(r'(.*?)市', address, re.S)[0] + "市"
            elif re.findall(r'(.*?)县', address, re.S):
                qu = re.findall(r'(.*?)县', address, re.S)[0] + "县"
            else:
                qu = "余杭区"
            print(id, title, address, "餐饮", type, sheng, shi, qu, phone)
            with open(f'{sheng}美食.csv', 'a', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(
                    [id, title, address, "餐饮", type, sheng, city_name, qu,
                     phone])
            break


# 算法信息
def sign(acronym, city_name):
    """生成sign参数"""
    # 默认编码
    # coding = sys.getdefaultencoding()
    # areaId=0&cateId=0&cityName=杭州&dinnerCountAttrId=&optimusCode=10&originUrl=https://hz.meituan.com/meishi/&page=1&partner=126&platform=1&riskLevel=1&sort=&userId=&uuid=27f3e6c637e04344b7cb.1597157544.1.0.0
    _params = f"areaId=0&cateId=0&cityName={city_name}&dinnerCountAttrId=&optimusCode=10&originUrl=https://{acronym}.meituan.com/meishi/&page=1&partner=126&platform=1&riskLevel=1&sort=&userId=&uuid=27f3e6c637e04344b7cb.1597157544.1.0.0"
    # 二进制压缩
    binary_data = zlib.compress(_params.encode())
    # base64编码
    base64_data = base64.b64encode(binary_data)
    # 返回utf8编码的字符串
    # print("sign",base64_data.decode())
    return base64_data.decode()


def encrypt_token(acronym, city_name):
    """生成_token参数"""
    ts = int(time.time() * 1000)  # time.time()返回1970年至今的时间(以秒为单位)
    token_data = {
        "rId": 100900,
        "ver": "1.0.6",
        "ts": ts,
        "cts": ts + random.randint(100, 120),  # 经测,cts - ts 的差值大致在 90-130 之间
        "brVD": [1366, 625],
        "brR": [[1366, 768], [1366, 728], 24, 24],
        "bI": [f'https://{acronym}.meituan.com/meishi/',
               f'https://{acronym}.meituan.com/'],
        "mT": [],
        "kT": [],
        "aT": [],
        "tT": [],
        "aM": "",
        "sign": sign(acronym, city_name)
    }
    # 二进制压缩
    binary_data = zlib.compress(str(token_data).encode())
    # base64编码
    base64_data = base64.b64encode(binary_data)
    return base64_data.decode()


if __name__ == '__main__':
    city_name = get_city()
