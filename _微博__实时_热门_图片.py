import os
import traceback
from urllib import parse
import requests
import json

from bs4 import BeautifulSoup
from settings import weibo_current_path, weibo_hot_path, weibo_pic_path, record_url_local
from tools import download_pic, log, excel, getResModel

requests.DEFAULT_RETRIES = 5  # 增加重试连接次数

class Weibo:
    def __init__(self):
        if not os.path.exists(weibo_current_path):
            os.mkdir(weibo_current_path)
        if not os.path.exists(weibo_hot_path):
            os.mkdir(weibo_hot_path)
        if not os.path.exists(weibo_pic_path):
            os.mkdir(weibo_pic_path)

    def setKeyword(self, keywords:list):
        self.keyword = "+".join(keywords)

    def __pic(self, mblog:dict, source:str, base_path:str):
        if 'pics' in mblog.keys():
            tags = self.__getTages(mblog['text'])
            excel.appendTagsFromList(tags)
            for pic_url in mblog['pics']:
                if 'large' in pic_url.keys():
                    temp = self.__divideWeibo(mblog=mblog, source=source, tags=tags, url=pic_url['large']['url'], base_path=base_path)
                    excel.appendRecord(temp)
                    download_pic(pic_url['large']['url'], temp[record_url_local])
                else:
                    temp = self.__divideWeibo(mblog=mblog, source=source, tags=tags, url=pic_url['url'], base_path=base_path)
                    excel.appendRecord(temp)
                    download_pic(pic_url['url'], temp[record_url_local])

    def __getTages(self, text:str):
        tags = []
        soup = BeautifulSoup(text, 'html.parser')
        # print(soup)
        for i in soup.find_all(class_='surl-text'):
            tags.append(i.text.replace("#", ""))
        # print(tags)
        return tags

    def __getText(self, text:str):
        soup = BeautifulSoup(text, 'html.parser')
        return soup.text

    def __divideWeibo(self, mblog:dict, source:str, tags:list, url:str, base_path:str):
        res = getResModel(type='图片', source=source, keyword=self.key,
                          author=mblog['user']['screen_name'], title="-",
                          introduction=self.__getText(mblog['text']),
                          tags=tags, caption="-",
                          url_article='https://m.weibo.cn/detail/' + mblog['id'],
                          url_pic=url,
                          url_local=base_path + self.key + str(excel.nrows) + ".png")
        return res

    def __currentAnalysis(self, page:int):
        url = "https://m.weibo.cn/api/container/getIndex?containerid=100103type" + parse.quote("=61&q={}&t=".format(self.key)) + "&page_type=searchall&page={}".format(page)
        # print(url)
        data = self.__request(url)
        for card in data['data']['cards']:
            if excel.checkHttpRepeat('https://m.weibo.cn/detail/' + card['mblog']['id']):
                continue
            print(card['mblog']['id'])
            self.__pic(mblog=card['mblog'], source="微博实时动态", base_path=weibo_current_path)

    def __hotAnalysis(self, page:int):
        url = "https://m.weibo.cn/api/container/getIndex?containerid=100103type" + parse.quote("=60&q={}&t=".format(self.key)) + "&page_type=searchall&page={}".format(page)
        # print(url)
        data = self.__request(url)
        for card in data['data']['cards']:
            if 'mblog' in card.keys():
                if excel.checkHttpRepeat('https://m.weibo.cn/detail/' + card['mblog']['id']):
                    continue
                print(card['mblog']['id'])
                self.__pic(mblog=card['mblog'], source="微博热门动态", base_path=weibo_hot_path)
            elif 'card_group' in card.keys():
                for card_group in card['card_group']:
                    if 'mblog' in card_group.keys():
                        if excel.checkHttpRepeat('https://m.weibo.cn/detail/' + card_group['mblog']['id']):
                            continue
                        print(card_group['mblog']['id'])
                        self.__pic(mblog=card_group['mblog'], source="微博热门动态", base_path=weibo_hot_path)
            else:
                print(card)

    def __picAnalysis(self, page:int):
        url = "https://m.weibo.cn/api/container/getIndex?containerid=100103type" + parse.quote("=63&q={}&t=".format(self.key)) + "&page_type=searchall&page={}".format(page)
        # print(url)
        data = self.__request(url)
        for cards in data['data']['cards']:
            for card_group in cards['card_group']:
                if 'mblog' in card_group['left_element'].keys():
                    if excel.checkHttpRepeat('https://m.weibo.cn/detail/' + card_group['left_element']['mblog']['id']):
                        continue
                    print(card_group['left_element']['mblog']['id'])
                    self.__pic(mblog=card_group['left_element']['mblog'], source="微博图片动态", base_path=weibo_pic_path)
                if 'mblog' in card_group['right_element'].keys():
                    if excel.checkHttpRepeat('https://m.weibo.cn/detail/' + card_group['left_element']['mblog']['id']):
                        continue
                    print(card_group['right_element']['mblog']['id'])
                    self.__pic(mblog=card_group['right_element']['mblog'], source="微博图片动态", base_path=weibo_pic_path)

    def __request(self, url:str):
        # url = "https://m.weibo.cn/api/container/getIndex?containerid=100103type%3D21%26q%3D%E7%AC%94%E8%AE%B0%26t%3D&page_type=searchall"
        s = requests.session()
        s.keep_alive = False  # 关闭多余连接
        response = s.get(url=url).text
        data = json.loads(response)
        return data

    def current(self, page=5):
        for i in range(1, page):
            try:
                self.__currentAnalysis(i)
            except:
                log(traceback.format_exc())
                break

    def hot(self, page=5):
        for i in range(1, page):
            try:
                self.__hotAnalysis(i)
            except:
                log(traceback.format_exc())
                break

    def picture(self, page=5):
        for i in range(1, page):
            try:
                self.__picAnalysis(i)
            except:
                log(traceback.format_exc())
                break
