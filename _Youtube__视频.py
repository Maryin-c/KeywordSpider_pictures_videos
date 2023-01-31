import os
import time
import traceback

from settings import youtube_video_screen_shot_path, youtube_video_path, record_url_local
import pyautogui
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By

from tools import excel, getResModel, download_pic, log


class Youtube:
    def __init__(self):

        if not os.path.exists(youtube_video_screen_shot_path):
            os.mkdir(youtube_video_screen_shot_path)
        if not os.path.exists(youtube_video_path):
            os.mkdir(youtube_video_path)

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])
        chrome_options.add_argument("--disable-blink-features")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0')
        s = Service('./chromedriver.exe')
        self.browser = webdriver.Chrome(service=s, options=chrome_options)

    def setKeyword(self, keywords:list):
        self.keyword = "+".join(keywords)

    def searchVideo(self, scrollTime=300):
        try:
            searchUrl = "https://www.youtube.com/results?search_query={}&sp=EgIQAQ%253D%253D".format(self.keyword)
            self.browser.get(searchUrl)
            time.sleep(5)

            # self.__scrollToBottom(scrollTime)

            video_cards = self.browser.find_elements(By.TAG_NAME, 'ytd-video-renderer')

            for card in video_cards:
                title = card.find_element(By.ID, 'video-title').get_attribute("title")
                url = card.find_element(By.ID, 'video-title').get_attribute("href")
                author = card.find_elements(By.CLASS_NAME, "yt-simple-endpoint.style-scope.yt-formatted-string")[1].text
                # print(author)
                # time.sleep(600)
                introduction = "-"
                try:
                    introduction = card.find_element(By.CLASS_NAME, "metadata-snippet-text.style-scope.ytd-video-renderer").text
                except:
                    pass
                pic_url = card.find_element(By.TAG_NAME, "yt-image").find_element(By.TAG_NAME, "img").get_attribute("src")
                tags = self.__getTags(introduction)

                if excel.checkHttpRepeat(url):
                    continue

                temp = self.__divideYoutube(author=author, title=title, introduction=introduction,
                                            tags=tags, url_article=url, url_pic=pic_url,
                                            url_local=youtube_video_screen_shot_path + self.keyword + str(excel.nrows) + ".png")
                print(temp)
                download_pic(pic_url, temp[record_url_local])
                excel.appendRecord(temp)
        except:
            log(traceback.format_exc())

    def __scrollToBottom(self, scrollTime:int):
        for i in range(scrollTime):
            pyautogui.scroll(-400)
            time.sleep(0.2)

    def __getTags(self, text:str):
        list=[]
        word = ""
        status = 0
        for c in text:
            if status == 0 and c == '#':
                status = 1
                word = ""
            elif status == 1:
                if c == " ":
                    list.append(word)
                    status = 0
                    word = ""
                elif c == "#":
                    list.append(word)
                    word = ""
                else:
                    word += c
        if len(word) > 0:
            list.append(word)
        return list

    def __divideYoutube(self, author: str, title:str, introduction:str, tags:list,
                            url_article: str, url_pic: str, url_local:str):
        res = getResModel(type='视频', source="youtube视频", keyword=self.keyword,
                          author=author, title=title, introduction=introduction,
                          tags=tags, caption="-", url_article=url_article,
                          url_pic=url_pic, url_local=url_local)
        return res
