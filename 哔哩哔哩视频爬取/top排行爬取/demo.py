import requests
import pymongo

def get_json(url):
    params = {
        'page_size': 10,
        'next_offset': num,
        'tag': '今日热门',
        'platform': 'pc'
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
    }
    response = requests.get(url,headers=headers,params=params)
    return response.json()

def jiexi_parse(html):

    for i in range(0,10):
        data = html['data']["items"][i]
        user = data['user']['name']
        title = data['item']["description"]
        video_time = data['item']["video_time"]
        upload_time = data['item']["upload_time"]
        video_playurl = data['item']["video_playurl"]
        p = {
            "作者":user,
            "标题":title,
            "作品时间":video_time,
            "发布时间":upload_time,
            "web观看地址":video_playurl,
        }
        print('正在写入{}'.format(p))
        a = pymong(p)



def pymong(jiegou):
    client = pymongo.MongoClient('mongodb://admin:snackdeng@localhost:27017')
    client.bilibili.shiping.insert(jiegou)





if __name__ == '__main__':
    for i in range(0,10):
        url = 'https://api.vc.bilibili.com/board/v1/ranking/top'
        num = i*10 + 1
        print('正在爬取第{}页'.format(i))
        html = get_json(url)
        jiegou = jiexi_parse(html)


