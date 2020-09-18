import requests
import xml.etree.ElementTree as ET
from xml.parsers.expat import ParserCreate

class DefaultSaxHandler(object):
    def __init__(self,prvinces):
        self.provinces = provinces

    def start_element(selfself,name,attrs):
        if name != "map":
            name = attrs['title']
            number = attrs['href']
            self.provinces.append((name,number))

    def end_element(selfself,name):
        pass

    def char_data(self,text):
        pass


def get_province_entry(url):
    content = requests.get(url).content.decode("gb2312")
    #print(content)
    start = content.find('<map name="map_86" id="map_86">')
    end = content.find('</map>')
    content = content[start:end + len('</map>')].strip()
    #print(content)
    provinces = []
    handler = DefaultSaxHandler(provinces)
    parser = ParserCreate()
    parser.StartElementHandler = handler.start_element
    parser.EndElementHandler = handler.end_element()
    parser.CharacterDataHandler = handler.char_data
    parser.Parse(content)
    return provinces

provinces = get_province_entry("http://www.ip138.com/post")
print(provinces)