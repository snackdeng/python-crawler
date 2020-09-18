# -*- coding:utf-8 -*-
"""
作者：snackdeng
日期：2020/08/11
"""
# -*- coding:utf-8 -*-
import random
import re
import csv
import time
import zlib
import base64
import requests
from fake_useragent import UserAgent


session = requests.Session()

with open('浙江省美食.csv', 'w', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(["店铺长ID", "店铺名称", "地址", "店铺分类", "品类", "省", "市", "区", "手机"])

prox = [{"https": "58.218.200.229:9184"},
{"https": "58.218.200.229:8796"},
{"https": "58.218.200.237:11845"},
{"https": "58.218.200.237:11803"},
{"https": "58.218.200.229:8751"},
{"https": "58.218.200.229:9031"},
{"https": "58.218.200.248:9076"},
{"https": "58.218.200.237:11887"},
{"https": "58.218.200.248:9066"},
{"https": "58.218.200.237:11896"},
{"https": "58.218.200.229:9072"},
{"https": "58.218.200.229:9008"},
{"https": "58.218.200.229:9023"},
{"https": "58.218.200.248:9003"},
{"https": "58.218.200.248:9002"},
]

# def get_uuid(acronym):
#     headers = {
#         'User-Agent': UserAgent().random,
#         'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
#         'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
#         'Connection': 'keep-alive',
#         'Upgrade-Insecure-Requests': '1',
#         'Pragma': 'no-cache',
#         'Cache-Control': 'no-cache',
#         # "Cookie": "_lxsdk_cuid=173a2d80134c8-00aed6a451569d-3323765-100200-173a2d80134c8; iuuid=A50CA613ECE9A8317FEB14F615C0F63A50F60835D5D8F53D2E3C118774D6406D; _lxsdk=A50CA613ECE9A8317FEB14F615C0F63A50F60835D5D8F53D2E3C118774D6406D; wm_order_channel=mtib; utm_source=60030; service-off=0; userId=638445496; mtcdn=K; lsu=; isid=785ACDD2B3ADC5E2A6548EDF98BC901C; logintype=normal; __utma=74597006.467048628.1597070107.1597071894.1597126911.3; __utmz=74597006.1597126911.3.3.utmcsr=m.baidu|utmccn=m.baidu|utmcmd=organic|utmcct=100001; _hc.v=83c3a596-ce70-a2b9-4c11-5009549ae202.1597126919; latlng=27.457455,112.176884,1597129146423; cityname=%E5%AE%81%E6%B3%A2; i_extend=C_b1Gimthomepagecategory11H__a; ci=50; rvct=50%2C51%2C182%2C1; client-id=c7fb0c59-7e16-4778-aa32-ee020aa38353; uuid=0c34e8acc722452e9098.1597148140.1.0.0; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; __mta=53802391.1597069990249.1597144842143.1597148142952.3; userTicket=zqacjZNVailqzymsfNMlSNyhgmnlzuyhDFIxvhlF; u=638445496; n=BcZ684268709; lt=AADcTzibDDdSh3XYzFUM1Ys80D8AAAAAVgsAAM1Aqo1aaz5ogVaNvsMjK_7OXbU58nvdxMpDMrSOIyrBL0xhvuhkARZ0hiC__jHNmg; mt_c_token=AADcTzibDDdSh3XYzFUM1Ys80D8AAAAAVgsAAM1Aqo1aaz5ogVaNvsMjK_7OXbU58nvdxMpDMrSOIyrBL0xhvuhkARZ0hiC__jHNmg; token=AADcTzibDDdSh3XYzFUM1Ys80D8AAAAAVgsAAM1Aqo1aaz5ogVaNvsMjK_7OXbU58nvdxMpDMrSOIyrBL0xhvuhkARZ0hiC__jHNmg; token2=AADcTzibDDdSh3XYzFUM1Ys80D8AAAAAVgsAAM1Aqo1aaz5ogVaNvsMjK_7OXbU58nvdxMpDMrSOIyrBL0xhvuhkARZ0hiC__jHNmg; firstTime=1597148198918; unc=BcZ684268709; _lxsdk_s=173dd7297fe-ae5-9b-232%7C%7C7",
#     }
#     response = session.get(f'https://{acronym}.meituan.com/meishi/', headers=headers, timeout=3)
#     UUID = response.cookies.get_dict().get("uuid")
#     print(response.cookies.get_dict().get("uuid"))
#     return UUID


def sign(uuid,acronym,city_name):
    """生成sign参数"""
    # 默认编码
    # coding = sys.getdefaultencoding()
                #areaId=0&cateId=0&cityName=杭州&dinnerCountAttrId=&optimusCode=10&originUrl=https://hz.meituan.com/meishi/&page=1&partner=126&platform=1&riskLevel=1&sort=&userId=&uuid=27f3e6c637e04344b7cb.1597157544.1.0.0
    _params = f"areaId=0&cateId=0&cityName={city_name}&dinnerCountAttrId=&optimusCode=10&originUrl=https://{acronym}.meituan.com/meishi/&page=1&partner=126&platform=1&riskLevel=1&sort=&userId={uuid}&uuid=27f3e6c637e04344b7cb.1597157544.1.0.0"
    # 二进制压缩
    binary_data = zlib.compress(_params.encode())
    # base64编码
    base64_data = base64.b64encode(binary_data)
    # 返回utf8编码的字符串
    # print("sign",base64_data.decode())
    return base64_data.decode()

def encrypt_token( uuid,acronym,city_name):
    """生成_token参数"""
    ts = int(time.time() * 1000)  # time.time()返回1970年至今的时间(以秒为单位)
    token_data = {
        "rId": 100900,
        "ver": "1.0.6",
        "ts": ts,
        "cts": ts + random.randint(100, 120),  # 经测,cts - ts 的差值大致在 90-130 之间
        "brVD": [1366, 625],
        "brR": [[1366, 768], [1366, 728], 24, 24],
        "bI": [f'https://{acronym}.meituan.com/meishi/', f'https://{acronym}.meituan.com/'],
        "mT": [],
        "kT": [],
        "aT": [],
        "tT": [],
        "aM": "",
        "sign": sign(uuid,acronym,city_name)
    }
    # 二进制压缩
    binary_data = zlib.compress(str(token_data).encode())
    # base64编码
    base64_data = base64.b64encode(binary_data)
    return base64_data.decode()

def get_all_url( uuid, token,acronym,city_name,sheng):
        for i in range(2,202):
            params = (
                ('cityName', city_name),
                ('cateId', '0'),
                ('areaId', '0'),
                ('sort', ''),
                ('dinnerCountAttrId', ''),
                ('page', i),
                ('userId', ''),
                ('uuid',"27f3e6c637e04344b7cb.1597157544.1.0.0"),
                ('platform', '1'),
                ('partner', '126'),
                ('originUrl', f'https://{acronym}.meituan.com/meishi/pn{i}/'),
                ('riskLevel', '1'),
                ('optimusCode', '10'),
                ('_token', token),
            )
            for _ in range(10):
                url = f'https://{acronym}.meituan.com/meishi/api/poi/getPoiList'
                headers = {
                    "Accept": "*/*",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Accept-Language": "zh-CN,zh;q=0.9",
                    "Cache-Control": "no-cache",
                    "Connection": "keep-alive",
                    "Content-Type": "application/json",
                    # "Cookie": "_lxsdk_cuid=173a2d80134c8-00aed6a451569d-3323765-100200-173a2d80134c8; iuuid=A50CA613ECE9A8317FEB14F615C0F63A50F60835D5D8F53D2E3C118774D6406D; _lxsdk=A50CA613ECE9A8317FEB14F615C0F63A50F60835D5D8F53D2E3C118774D6406D; wm_order_channel=mtib; utm_source=60030; service-off=0; IJSESSIONID=12rjww0csjhwayj34g8m6mo1; __utmc=74597006; ci3=1; au_trace_key_net=default; openh5_uuid=A50CA613ECE9A8317FEB14F615C0F63A50F60835D5D8F53D2E3C118774D6406D; userId=638445496; rvct=51%2C50%2C182%2C1; uuid=c35677e47c21477fa5ee.1597116946.1.0.0; mtcdn=K; u=638445496; n=BcZ684268709; lt=PBYxDcOuNqJO-tBECHeMvNCZpOsAAAAAPAsAAJd9bXf5HYGFjKGiAvz6XTvFZOvkZxCxCigYUqUoCNqtpE4fSbStcH1GdHE1u0clow; mt_c_token=PBYxDcOuNqJO-tBECHeMvNCZpOsAAAAAPAsAAJd9bXf5HYGFjKGiAvz6XTvFZOvkZxCxCigYUqUoCNqtpE4fSbStcH1GdHE1u0clow; token=PBYxDcOuNqJO-tBECHeMvNCZpOsAAAAAPAsAAJd9bXf5HYGFjKGiAvz6XTvFZOvkZxCxCigYUqUoCNqtpE4fSbStcH1GdHE1u0clow; lsu=; token2=PBYxDcOuNqJO-tBECHeMvNCZpOsAAAAAPAsAAJd9bXf5HYGFjKGiAvz6XTvFZOvkZxCxCigYUqUoCNqtpE4fSbStcH1GdHE1u0clow; unc=BcZ684268709; isid=785ACDD2B3ADC5E2A6548EDF98BC901C; logintype=normal; oops=PBYxDcOuNqJO-tBECHeMvNCZpOsAAAAAPAsAAJd9bXf5HYGFjKGiAvz6XTvFZOvkZxCxCigYUqUoCNqtpE4fSbStcH1GdHE1u0clow; __utma=74597006.467048628.1597070107.1597071894.1597126911.3; __utmz=74597006.1597126911.3.3.utmcsr=m.baidu|utmccn=m.baidu|utmcmd=organic|utmcct=100001; cssVersion=3fee96cb; meishi_ci=51; cityid=51; p_token=PBYxDcOuNqJO-tBECHeMvNCZpOsAAAAAPAsAAJd9bXf5HYGFjKGiAvz6XTvFZOvkZxCxCigYUqUoCNqtpE4fSbStcH1GdHE1u0clow; _hc.v=83c3a596-ce70-a2b9-4c11-5009549ae202.1597126919; latlng=27.457455,112.176884,1597129146423; ci=51; cityname=%E5%AE%81%E6%B3%A2; i_extend=C_b1Gimthomepagecategory11H__a; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; client-id=7b926485-4d9c-429d-8160-9075a390c0b2; lat=29.831027; lng=121.568462; firstTime=1597131767251; _lxsdk_s=173dc2e1d3a-55-85e-62c%7C%7C149",
                    "Referer": f"https://{acronym}.meituan.com/meishi/",
                    "Host": "www.meituan.com",
                    "Pragma": "no-cache",
                    "Referer": "https://www.meituan.com/changecity/",
                    "Sec-Fetch-Dest": "empty",
                    "Sec-Fetch-Mode": "cors",
                    "Sec-Fetch-Site": "same-origin",
                    "User-Agent": UserAgent().random,
                }
                proxies = random.choice(prox)
                try:
                    response = session.get(url,headers=headers,params=params,proxies=proxies,timeout=3)
                except requests.exceptions.ProxyError as e:
                    print("代理错误")
                    continue
                else:
                    print("正在使用的是",UserAgent().random,proxies)
                    if response.json()["code"] == 406:
                        print(response.text)
                        print("报错了,验证码来了")
                        time.sleep(2)
                        continue
                    print(date)
                    result = response.json().get("data").get("poiInfos")
                    if result:
                        get_phone(result, i,acronym,city_name,sheng)
                        time.sleep(2)


def get_phone(result, page,acronym,city_name,sheng):
    sheng = sheng+"省"
    city_name = city_name+"市"
    for i in result:
        title = i.get("title")
        address = i.get("address")
        id = str(i.get("poiId"))
        url = "https://www.meituan.com/meishi/" + id + "/"
        try:
            ua = random.choice(USER_AGENT_LIST)
            headers = {
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "zh-CN,zh;q=0.9",
                "Cache-Control": "max-age=0",
                "Connection": "keep-alive",
                # "Cookie": "_lxsdk_cuid=173a2d80134c8-00aed6a451569d-3323765-100200-173a2d80134c8; iuuid=A50CA613ECE9A8317FEB14F615C0F63A50F60835D5D8F53D2E3C118774D6406D; _lxsdk=A50CA613ECE9A8317FEB14F615C0F63A50F60835D5D8F53D2E3C118774D6406D; wm_order_channel=mtib; utm_source=60030; service-off=0; IJSESSIONID=12rjww0csjhwayj34g8m6mo1; __utmc=74597006; ci3=1; au_trace_key_net=default; openh5_uuid=A50CA613ECE9A8317FEB14F615C0F63A50F60835D5D8F53D2E3C118774D6406D; userId=638445496; rvct=51%2C50%2C182%2C1; uuid=c35677e47c21477fa5ee.1597116946.1.0.0; mtcdn=K; u=638445496; n=BcZ684268709; lt=PBYxDcOuNqJO-tBECHeMvNCZpOsAAAAAPAsAAJd9bXf5HYGFjKGiAvz6XTvFZOvkZxCxCigYUqUoCNqtpE4fSbStcH1GdHE1u0clow; mt_c_token=PBYxDcOuNqJO-tBECHeMvNCZpOsAAAAAPAsAAJd9bXf5HYGFjKGiAvz6XTvFZOvkZxCxCigYUqUoCNqtpE4fSbStcH1GdHE1u0clow; token=PBYxDcOuNqJO-tBECHeMvNCZpOsAAAAAPAsAAJd9bXf5HYGFjKGiAvz6XTvFZOvkZxCxCigYUqUoCNqtpE4fSbStcH1GdHE1u0clow; lsu=; token2=PBYxDcOuNqJO-tBECHeMvNCZpOsAAAAAPAsAAJd9bXf5HYGFjKGiAvz6XTvFZOvkZxCxCigYUqUoCNqtpE4fSbStcH1GdHE1u0clow; unc=BcZ684268709; isid=785ACDD2B3ADC5E2A6548EDF98BC901C; logintype=normal; oops=PBYxDcOuNqJO-tBECHeMvNCZpOsAAAAAPAsAAJd9bXf5HYGFjKGiAvz6XTvFZOvkZxCxCigYUqUoCNqtpE4fSbStcH1GdHE1u0clow; __utma=74597006.467048628.1597070107.1597071894.1597126911.3; __utmz=74597006.1597126911.3.3.utmcsr=m.baidu|utmccn=m.baidu|utmcmd=organic|utmcct=100001; cssVersion=3fee96cb; meishi_ci=51; cityid=51; p_token=PBYxDcOuNqJO-tBECHeMvNCZpOsAAAAAPAsAAJd9bXf5HYGFjKGiAvz6XTvFZOvkZxCxCigYUqUoCNqtpE4fSbStcH1GdHE1u0clow; _hc.v=83c3a596-ce70-a2b9-4c11-5009549ae202.1597126919; latlng=27.457455,112.176884,1597129146423; ci=51; cityname=%E5%AE%81%E6%B3%A2; i_extend=C_b1Gimthomepagecategory11H__a; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; client-id=7b926485-4d9c-429d-8160-9075a390c0b2; firstTime=1597132983040; lat=29.808786; lng=121.561317; _lxsdk_s=173dc2e1d3a-55-85e-62c%7C%7C174",
                "Referer":f"https://{acronym}.meituan.com/meishi/",
                "Host": "www.meituan.com",
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "none",
                "Sec-Fetch-User": "?1",
                "Upgrade-Insecure-Requests": "1",
                "User-Agent": UserAgent().random,
            }
            proxies = random.choice(prox)
            response = session.get(url, headers=headers, proxies=proxies, timeout=3)
            # print(response.text)
            phone = re.findall(r'"phone":"(.*?)",', response.text, re.S)[0]
            #type = re.findall(r'{"title":"杭州美食","url":"http://hz.meituan.com/meishi/"},{"title":"(.*?)",',response.text, re.S)
            type = re.findall(r'{"title":"\W+美食","url":"http://\w+.meituan.com/meishi/"},{"title":"(.*?)",',response.text, re.S)


            if type:
                # type = type[0].replace("杭州", "")
                type = type[0].replace(f"{acronym}", "")
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
            # print(id, title, address, "餐饮", type, "浙江省", "杭州市", qu, phone)
            print(id, title, address, "餐饮", type, sheng, city_name, qu, phone)
            with open(f'{sheng}美食.csv', 'a', encoding='utf-8') as f:
                writer = csv.writer(f)
                # writer.writerow([id, title, address, "餐饮", type, "浙江省", "杭州市", qu, phone])
                writer.writerow([id, title, address, "餐饮", type, sheng, city_name, qu, phone])
        except:
            print(url)
            time.sleep(10)
            pass
    with open(f'{sheng}美食.csv', 'rt', encoding='utf-8')as fin:  # 读有空行的csv文件，舍弃空行
        lines = ''
        for line in fin:
            if line != '\n':
                lines += line
    with open(f'{sheng}美食.csv', 'wt', encoding='utf-8')as fout:  # 再次文本方式写入，不含空行
        fout.write(lines)
    print("第%d页爬取完毕" % page)

def get_city():
    url = "https://www.meituan.com/ptapi/getprovincecityinfo/"
    headers = {
        'User-Agent': UserAgent().random,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        # "Cookie": "_lxsdk_cuid=173a2d80134c8-00aed6a451569d-3323765-100200-173a2d80134c8; iuuid=A50CA613ECE9A8317FEB14F615C0F63A50F60835D5D8F53D2E3C118774D6406D; _lxsdk=A50CA613ECE9A8317FEB14F615C0F63A50F60835D5D8F53D2E3C118774D6406D; wm_order_channel=mtib; utm_source=60030; service-off=0; userId=638445496; mtcdn=K; lsu=; isid=785ACDD2B3ADC5E2A6548EDF98BC901C; logintype=normal; __utma=74597006.467048628.1597070107.1597071894.1597126911.3; __utmz=74597006.1597126911.3.3.utmcsr=m.baidu|utmccn=m.baidu|utmcmd=organic|utmcct=100001; _hc.v=83c3a596-ce70-a2b9-4c11-5009549ae202.1597126919; latlng=27.457455,112.176884,1597129146423; cityname=%E5%AE%81%E6%B3%A2; i_extend=C_b1Gimthomepagecategory11H__a; ci=50; rvct=50%2C51%2C182%2C1; client-id=c7fb0c59-7e16-4778-aa32-ee020aa38353; uuid=0c34e8acc722452e9098.1597148140.1.0.0; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; __mta=53802391.1597069990249.1597144842143.1597148142952.3; userTicket=zqacjZNVailqzymsfNMlSNyhgmnlzuyhDFIxvhlF; u=638445496; n=BcZ684268709; lt=AADcTzibDDdSh3XYzFUM1Ys80D8AAAAAVgsAAM1Aqo1aaz5ogVaNvsMjK_7OXbU58nvdxMpDMrSOIyrBL0xhvuhkARZ0hiC__jHNmg; mt_c_token=AADcTzibDDdSh3XYzFUM1Ys80D8AAAAAVgsAAM1Aqo1aaz5ogVaNvsMjK_7OXbU58nvdxMpDMrSOIyrBL0xhvuhkARZ0hiC__jHNmg; token=AADcTzibDDdSh3XYzFUM1Ys80D8AAAAAVgsAAM1Aqo1aaz5ogVaNvsMjK_7OXbU58nvdxMpDMrSOIyrBL0xhvuhkARZ0hiC__jHNmg; token2=AADcTzibDDdSh3XYzFUM1Ys80D8AAAAAVgsAAM1Aqo1aaz5ogVaNvsMjK_7OXbU58nvdxMpDMrSOIyrBL0xhvuhkARZ0hiC__jHNmg; firstTime=1597148198918; unc=BcZ684268709; _lxsdk_s=173dd7297fe-ae5-9b-232%7C%7C7",
    }
    response = requests.get(url, headers=headers).json()
    for city_list in response:
        sheng = city_list["provinceName"]
        if sheng == "浙江":
            for city in city_list["cityInfoList"]:
                city_name = city["name"] #全称中文 例如宁波
                acronym = city["acronym"] # 简写 nb
                if city_name == "杭州":
                    continue
                yield acronym,city_name,sheng


def main():
    for acronym,city_name,sheng in get_city():
        uuid = get_uuid(acronym)
        token = encrypt_token(uuid,acronym,city_name)
        print(acronym,city_name,sheng)
        get_all_url(uuid, token,acronym,city_name,sheng)
        break
    print("ok")


if __name__ == '__main__':
    main()
