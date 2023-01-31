import json
import os
import traceback

from bs4 import BeautifulSoup
from settings import bilibili_video_path, bilibili_video_screen_shot_path, bilibili_article_picture_path, \
    record_url_pic, record_url_local, record_tags
from tools import log, getResModel, download_pic, excel, download_video
import requests
requests.DEFAULT_RETRIES = 5  # 增加重试连接次数

# bilibili
class Bilibili:
    bilibili_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
            'Referer': "https://search.bilibili.com"
        }

    def __init__(self):
        # self.keyword = " ".join(keyword)
        if not os.path.exists(bilibili_video_path):
            os.mkdir(bilibili_video_path)
        if not os.path.exists(bilibili_video_screen_shot_path):
            os.mkdir(bilibili_video_screen_shot_path)
        if not os.path.exists(bilibili_article_picture_path):
            os.mkdir(bilibili_article_picture_path)

    def setKeyword(self, keywords:list):
        self.keyword = " ".join(keywords)

    def video(self, pageNumber=5):
        for i in range(1, pageNumber):
            try:
                self.__searchBilibiliVideos(i)
            except:
                log(traceback.format_exc())
                break

    def article(self, pageNumber=5):
        for i in range(1, pageNumber):
            try:
                self.__searchBilibiliArticle(i)
            except:
                log(traceback.format_exc())
                break

    def __getValueFromDict(self, aimDict: dict, key: str):
        if key in aimDict.keys():
            return aimDict[key]

    def __getValueFromVideo(self, aimDict: dict, key: str):
        title = self.__getValueFromDict(aimDict, key)
        return title.replace("<em class=\"keyword\">", "").replace("</em>", "")

    def __getTagsFromVideo(self, aimDict: dict, key: str):
        tags = self.__getValueFromVideo(aimDict, key)
        return tags.split(',')

    def __divideBilibiliArticle(self, information: dict, author: str,
                                tags: list, url_article: str, url: str, caption:str):
        res = getResModel(type='图片', source='bilibili专栏', keyword=self.keyword, author=author,
                          title=self.__getValueFromVideo(information, 'title'),
                          introduction=self.__getValueFromVideo(information, 'desc'),
                          tags=tags, caption=caption,
                          url_article=url_article, url_pic=url, url_local=bilibili_article_picture_path + self.keyword + str(excel.nrows) + ".png")
        return res

    def __divideBilibiliVideo(self, information: dict):
        res = getResModel(type='视频', source='bilibili视频', keyword=self.keyword, author=self.__getValueFromVideo(information, 'author'),
                          title=self.__getValueFromVideo(information, 'title'),
                          introduction=self.__getValueFromVideo(information, 'description'),
                          tags=self.__getTagsFromVideo(information, 'tag'), caption='-',
                          url_article=self.__getValueFromVideo(information, 'arcurl'),
                          url_pic="http:" + self.__getValueFromVideo(information, 'pic'),
                          url_local=bilibili_video_screen_shot_path + self.keyword + str(excel.nrows) + ".png")
        return res

    def __getBilibiliCookie(self):
        url = "https://bilibili.com"
        res = requests.get(url)
        return res.cookies

    def __recordData(self, resDict: dict):
        download_pic(resDict[record_url_pic], resDict[record_url_local])
        excel.appendRecord(resDict)

    def __request(self, url: str):
        cookie = self.__getBilibiliCookie()
        s = requests.session()
        s.keep_alive = False  # 关闭多余连接
        response = s.get(url=url, headers=self.bilibili_headers, cookies=cookie).text
        return response

    def __searchBilibiliVideos(self, page: int):
        url = "https://api.bilibili.com/x/web-interface/search/all/v2?page={}&keyword={}"

        response = self.__request(url.format(page, self.keyword))
        data = json.loads(response)

        for record in data['data']['result']:
            if record['result_type'] == 'video':
                for video in record['data']:
                    # print(videoB)
                    if excel.checkHttpRepeat(video['arcurl']):
                        continue
                    temp = self.__divideBilibiliVideo(video)
                    print(temp)
                    excel.appendTagsFromList(temp[record_tags])
                    # download_video(video['arcurl'], bilibili_video_path, self.keyword + str(excel.nrows))
                    self.__recordData(temp)

    def __analysisArticle(self, information: dict):

        url_article = "https://www.bilibili.com/read/cv" + str(information['id'])
        if excel.checkHttpRepeat(url_article):
            return

        html = requests.get(url_article).text
        soup = BeautifulSoup(html, 'html.parser')

        author = soup.find_all(class_="up-info__name")
        author = author[0]['title']

        tag_attr = soup.find_all(class_="tag-item")
        tags = []
        for attr in tag_attr:
            tags.append(attr.text.strip())
        excel.appendTagsFromList(tags)

        img_attr = soup.find_all(class_="img-box")
        for i in img_attr:
            url = "https:" + i.find("img")["data-src"]
            caption = i.find(class_="caption")
            if caption is not None:
                caption = caption.text
            if caption is None:
                caption = "-"
            # print(caption)
            temp = self.__divideBilibiliArticle(information, author, tags, url_article, url, caption)
            # print(temp)
            self.__recordData(temp)

    def __searchBilibiliArticle(self, page: int):
        url = "https://api.bilibili.com/x/web-interface/search/type?search_type=article&page={}&keyword={}"

        response = self.__request(url.format(page, self.keyword))
        data = json.loads(response)

        for record in data['data']['result']:
            print(record)
            # log(record)
            self.__analysisArticle(record)
