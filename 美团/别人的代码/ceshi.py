import requests
import time
from js代码 import city_url_list
from UA import USER_AGENT_LIST
import random
import pymysql, re,json,time
import parsel
db = pymysql.connect(host='localhost',
                     port=3306,
                     user='root',
                     password='snackdeng',
                     db='shop',
                     charset='utf8',
                     )

# ip_api ='http://ip.ipjldl.com/index.php/api/entry?method=proxyServer.tiqu_api_url&packid=1&fa=0&dt=&groupid=0&fetch_key=&qty=200&time=1&port=1&format=json&ss=5&css=&dt=&pro=&city=&usertype=6'
# h = requests.get(ip_api)
# ua = random.choice(USER_AGENT_LIST)
# ip_lis = json.loads(h.text)['data']
#
# ip_li = []
# for i in range(len(ip_lis)):
#     ip = ip_lis[i]['IP']
#     ip_li.append(ip)
# ip = random.choice(ip_li)
# proxies = {
#     'http':"http://"+ip,
#     'https':'https://'+ip
# }
# 随机ua库
ua = random.choice(USER_AGENT_LIST)
# 遍历js代码中的城市url
for city_url in city_url_list:
    # city_url = city_url_list[25]
    # print(city_url)
    # 添加了个cookie值
    headers = {
                'User-Agent': ua,
                'Cookie':'__mta=251035193.1596164947240.1596183174443.1596183252676.7; uuid=bbe1c0028205470a8f16.1596164930.1.0.0; _lxsdk_cuid=173a2d80134c8-00aed6a451569d-3323765-100200-173a2d80134c8; mtcdn=K; lsu=; rvct=20%2C1; iuuid=EFCCCD52484FA783961E5910376E215466E6ECF139E441A5ADE6147D3C0FA8F7; _lxsdk=EFCCCD52484FA783961E5910376E215466E6ECF139E441A5ADE6147D3C0FA8F7; _hc.v=c29d9a88-d3a0-684c-5204-1ef47dbf7e98.1596168994; __utma=74597006.1507081027.1596168746.1596168746.1596181002.2; __utmz=74597006.1596181002.2.2.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; idau=1; ci=1; cityname=%E5%8C%97%E4%BA%AC; latlng=27.456483,112.185315,1596182512187; i_extend=C_b0E236532160176830351051346367335400832255_e5925799794344954314_v5156435962457278971_a%e6%88%90%e4%ba%ba%e7%94%a8%e5%93%81GimthomepagesearchH__a100016__b2; __utmb=74597006.40.9.1596182564177; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; __mta=155958148.1596164996881.1596182820834.1596182830198.3; u=638445496; n=BcZ684268709; lt=EHPCwD_p_zmzvF965x6T2dFBdsoAAAAAHwsAAEFpXZlUPzDj5HD7w91Lrjqpgsw4gOU0g18ITdx9X-tGP53vARSeN-bWDe2-TgDaLA; mt_c_token=EHPCwD_p_zmzvF965x6T2dFBdsoAAAAAHwsAAEFpXZlUPzDj5HD7w91Lrjqpgsw4gOU0g18ITdx9X-tGP53vARSeN-bWDe2-TgDaLA; token=EHPCwD_p_zmzvF965x6T2dFBdsoAAAAAHwsAAEFpXZlUPzDj5HD7w91Lrjqpgsw4gOU0g18ITdx9X-tGP53vARSeN-bWDe2-TgDaLA; token2=EHPCwD_p_zmzvF965x6T2dFBdsoAAAAAHwsAAEFpXZlUPzDj5HD7w91Lrjqpgsw4gOU0g18ITdx9X-tGP53vARSeN-bWDe2-TgDaLA; unc=BcZ684268709; firstTime=1596183251140; _lxsdk_s=173a3cd33b3-ba7-e3d-3e6%7C%7C157'
            }
    # 睡眠3秒，防止反爬
    time.sleep(3)
    html_str = requests.get(city_url, headers=headers,timeout = 10).text
    phone_list = []
    company = re.findall('"utm_source=meituanweb">(.*?)</a>', html_str)
    add = re.findall('"address ellipsis">(.*?)<', html_str)
    uuid = re.findall('{"poiParam":{"uuid":"(.*?)",', html_str)
    cityid = re.findall('{cityid: (.*?)};', html_str)
    print(cityid)
    data = re.findall('<script>window.AppData.*?</script>', html_str)[0]
    data = re.sub('(<script>window.AppData|</script>|")', '', data)
    phone = re.findall('phone:(.*?),', data)
    su_word_ = re.match(r'(https://)(.*?)(.meituan.com/)', city_url)
    for i in range(len(company)):
        if phone[i] == '':
            phone[i]= '-'
        phone_list.append(phone[i])
    # 手机号
    print(phone_list)
    su_word = su_word_.group(2)
    cursor_c = db.cursor()
    print(su_word)
    sql = 'SELECT city_name from city where su_word="{}"'.format(su_word)
    cursor_c.execute(sql)
    city = cursor_c.fetchone()[0]
    print(city)
    cursor_c.close()
    for phone, add, company in zip(phone_list, add, company):
        print(phone)
        print(add)
        print(company)
        # 开始数据库的一系列操作
        cursor_f = db.cursor()
        sql_f = 'INSERT INTO shop(city,phone,address,company) VALUES("{}","{}","{}","{}")'.format(city, phone, add, company)
        print(sql_f)
        # 提交数据库指令
        cursor_f.execute(sql_f)
    # db.commit()
        data = parsel.Selector(html_str)
        fanye = data.css('.right-arrow.iconfont.icon-btn_right::attr(href)')
        if fanye:
            cursor_e = db.cursor()
            sql = 'SELECT city_id from city where city_id="{}"'.format(cityid[0])
            cursor_e.execute(sql)
            city_id = cursor_e.fetchone()[0]
            print(city_id)
            print('开始翻页')
            for i in range(1,15):
                # ip = random.choice(ip_li)
                # proxies = {
                #     'http': 'http://{}:{}'.format(ip['IP'], ip['Port']),
                #     'https': 'https://{}:{}'.format(ip['IP'], ip['Port'])
                # }
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.81 Safari/537.36 SE 2.X MetaSr 1.0',
                        "Cookie": "uuid=bbe1c0028205470a8f16.1596164930.1.0.0; _lxsdk_cuid=173a2d80134c8-00aed6a451569d-3323765-100200-173a2d80134c8; mtcdn=K; lsu=; rvct=20%2C1; iuuid=EFCCCD52484FA783961E5910376E215466E6ECF139E441A5ADE6147D3C0FA8F7; _lxsdk=EFCCCD52484FA783961E5910376E215466E6ECF139E441A5ADE6147D3C0FA8F7; _hc.v=c29d9a88-d3a0-684c-5204-1ef47dbf7e98.1596168994; __utma=74597006.1507081027.1596168746.1596168746.1596181002.2; __utmz=74597006.1596181002.2.2.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; ci=1; cityname=%E5%8C%97%E4%BA%AC; latlng=27.456483,112.185315,1596182512187; i_extend=C_b0E236532160176830351051346367335400832255_e5925799794344954314_v5156435962457278971_a%e6%88%90%e4%ba%ba%e7%94%a8%e5%93%81GimthomepagesearchH__a100016__b2; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; u=638445496; n=BcZ684268709; lt=7Tb0rFhOrkrvArdPgKoBaCl6SLEAAAAAPAsAAN9UMfk-4gxgmu_bXkYwvnf2HfU1Rl-nzoy5A3yK5CxhHMXaUnqpX4U31-JZDp9ChQ; mt_c_token=7Tb0rFhOrkrvArdPgKoBaCl6SLEAAAAAPAsAAN9UMfk-4gxgmu_bXkYwvnf2HfU1Rl-nzoy5A3yK5CxhHMXaUnqpX4U31-JZDp9ChQ; token=7Tb0rFhOrkrvArdPgKoBaCl6SLEAAAAAPAsAAN9UMfk-4gxgmu_bXkYwvnf2HfU1Rl-nzoy5A3yK5CxhHMXaUnqpX4U31-JZDp9ChQ; token2=7Tb0rFhOrkrvArdPgKoBaCl6SLEAAAAAPAsAAN9UMfk-4gxgmu_bXkYwvnf2HfU1Rl-nzoy5A3yK5CxhHMXaUnqpX4U31-JZDp9ChQ; unc=BcZ684268709; firstTime=1596186339421; _lxsdk_s=173a3cd33b3-ba7-e3d-3e6%7C%7C192"
                        }
                # 需要修改userid得参数   userid=858978677
                next_url = 'https://apimobile.meituan.com/group/v4/poi/pcsearch/{}?uuid={}&userid=638445496&limit=32&offset={}&cateId=-1&q=%E6%88%90%E4%BA%BA%E7%94%A8%E5%93%81'.format(city_id,uuid[0],32*i)
                print(next_url)
                html_s = requests.get(next_url,headers)
                print(html_s)
                try:
                    if html_s.status_code == 200:
                        html_s = html_s.json()
                        data = html_s.get('data')
                        results = data.get('searchResult')
                        for result in results:
                            # 写入数据库
                            company = result.get('title')
                            add = result.get('address')
                            phone = result.get('phone')
                            # city = result.get('city') //这个注释是为了解决数据库城市名有空白
                            cursor = db.cursor()
                            sql = 'INSERT INTO shop(city,phone,address,company) VALUES("{}","{}","{}","{}")'.format(city, phone, add, company)
                            cursor.execute(sql)
                        db.commit()
                    else:
                        print('未爬取任何数据')
                except Exception as e:
                    # 就是解决滑块验证码，点url进去滑动一下就可以了
                    time.sleep(20)
                    print('爬取失败')
    #     company = re.findall('"title":"(.*?)","', html_s)
    #     add = re.findall('","address":"(.*?)","', html_s)
    #     phone = re.findall('","phone":"(.*?)","full":false}', data)
    #     print(company)
    #     print(add)
    #     print(phone)
    #     if company !=[]:
    #
    #     else:
    #         break
    # db.commit()