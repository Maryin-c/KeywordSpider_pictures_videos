import json
import os
import time

import pyautogui
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
from settings import kuaishou_video_screen_shot_path, record_url_local
from tools import excel, download_pic, getResModel


class KuaiShou:
    def __init__(self):

        if not os.path.exists(kuaishou_video_screen_shot_path):
            os.mkdir(kuaishou_video_screen_shot_path)

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])
        chrome_options.add_argument("--disable-blink-features")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0')
        s = Service('./chromedriver.exe')
        self.browser = webdriver.Chrome(service=s, options=chrome_options)

        self.__signin()

    def __signin(self):
        self.browser.get('https://www.kuaishou.com/new-reco')
        time.sleep(40)

    def setKeyword(self, keywords:list):
        self.keyword = " ".join(keywords)

    def searchVideo(self, scrollTime:int):
        searchUrl = "https://www.kuaishou.com/search/video?searchKey=" + self.keyword
        self.browser.get(searchUrl)
        time.sleep(5)
        self.__scrollToBottom(scrollTime)

        video_cards = self.browser.find_elements(By.CLASS_NAME, 'video-card.video-item.vertical')

        for card in video_cards:
            introduction = card.find_element(By.CLASS_NAME, "video-info-title").text
            pic_url = card.find_element(By.CLASS_NAME, "poster-img").get_attribute("src")
            tags = self.__getTags(introduction)

            video = card.find_element(By.CLASS_NAME, "video-card-main")
            video.click()
            time.sleep(3)
            author = self.browser.find_element(By.CLASS_NAME, "profile-user-name-title").text
            url = self.browser.current_url
            self.browser.find_element(By.CLASS_NAME, "close-page").click()
            time.sleep(2)

            if excel.checkHttpRepeat(url):
                continue

            temp = self.__divideKuaiShou(author=author, introduction=introduction,
                                        tags=tags, url_article=url, url_pic=pic_url,
                                        url_local=kuaishou_video_screen_shot_path + self.keyword + str(excel.nrows) + ".png")
            print(temp)
            download_pic(pic_url, temp[record_url_local])
            excel.appendRecord(temp)

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

    def __divideKuaiShou(self, author: str, introduction:str, tags:list,
                            url_article: str, url_pic: str, url_local:str):
        res = getResModel(type='视频', source="快手视频", keyword=self.keyword,
                          author=author, title="-", introduction=introduction,
                          tags=tags, caption="-", url_article=url_article,
                          url_pic=url_pic, url_local=url_local)
        return res
