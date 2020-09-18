import requests
import jsonpath

class DouYu(object):
    def __init__(self):
        url = "https://www.douyu.com/gapi/rkc/directory/2_1/1"
        headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
    }
        self.url = url
        self.headers = headers

    def get_html(self):
        response = requests.get(url = self.url,headers = self.headers).json()
        #
        # print(response)
        return response

    def get_data(self,response):
        names = jsonpath.jsonpath(response,'$..nn')  #返回的是一个列表
        ols = jsonpath.jsonpath(response,'$..ol')
        items = []
        for name,ol in zip(names,ols):
            item= {
                "主播名字":name,
                "粉丝量":ol
            }
            items.append(item)
        # print(items)
        return items


    def refine(self,items):
        paiming = sorted(items,key=lambda x:x['粉丝量'], reverse=True)
        return paiming

    def zhanshi(self,item):
        for index,item in enumerate(item):
            print("第{}名======是{}======人气值是{}".format(index+1,item['主播名字'],item['粉丝量']))

    def run(self):
        response = self.get_html()
        items = self.get_data(a)
        item = self.refine(b)
        self.zhanshi(c)

if __name__ == "__main__":
    spider = DouYu()