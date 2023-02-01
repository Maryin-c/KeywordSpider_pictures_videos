import json
import os

import pyautogui
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from settings import douyin_video_path, douyin_cookie_path, douyin_video_screen_shot_path, record_url_local
from tools import excel, getResModel, download_pic


class Douyin:
    def __init__(self):

        if not os.path.exists(douyin_video_screen_shot_path):
            os.mkdir(douyin_video_screen_shot_path)
        if not os.path.exists(douyin_video_path):
            os.mkdir(douyin_video_path)

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])
        chrome_options.add_argument("--disable-blink-features")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0')
        s = Service('./chromedriver.exe')
        self.browser = webdriver.Chrome(service=s, options=chrome_options)

        self.__updateCookie()

    def setKeyword(self, keywords:list):
        self.keyword = " ".join(keywords)

    def __updateCookie(self):
        self.browser.get('https://www.douyin.com')
        time.sleep(5)
        if not os.path.exists(douyin_cookie_path):
            time.sleep(40)  # 留够时间来手动登录
            with open(douyin_cookie_path, 'w') as f:
                # 将cookies保存为json格式在cookies.txt中
                f.write(json.dumps(self.browser.get_cookies()))
        else:
            self.browser.delete_all_cookies()
            with open(douyin_cookie_path, 'r') as f:
                cookies_list = json.load(f)  # 读取cookies
                for cookie in cookies_list:
                    if isinstance(cookie.get('expiry'), float):
                        cookie['expiry'] = int(cookie['expiry'])
                    try:
                        self.browser.add_cookie(cookie)  # 加入cookies
                    except:
                        print(cookie)
            self.browser.refresh()

    def searchVideo(self, scrollTime:int):
        searchUrl = "https://www.douyin.com/search/" + self.keyword
        self.browser.get(searchUrl)
        self.browser.maximize_window()
        time.sleep(5)
        self.browser.find_element(By.XPATH, "/html/body/div[2]/div/div[2]/div/div[1]/div[1]/div[2]/div[2]").click()

        self.__scrollToBottom(scrollTime)

        videos = self.browser.find_element(By.CSS_SELECTOR, '[style="display:block"]').find_elements(By.TAG_NAME, "a")
        for video in videos:
            url = video.get_attribute("href")
            if excel.checkHttpRepeat(url):
                continue
            # print(url)

            author = "-"
            try:
                author = video.find_element(By.CLASS_NAME, "OhTcPZd3").text
            except:
                pass

            introduction = "-"
            try:
                introduction = video.find_element(By.CLASS_NAME, "swoZuiEM").text
            except:
                pass

            tags = self.__getTags(introduction)
            url_pic = video.find_element(By.TAG_NAME, "img").get_attribute("src")

            temp = self.__divideDouyin(author=author, introduction=introduction,
                                        tags=tags, url_article=url, url_pic=url_pic,
                                        url_local=douyin_video_screen_shot_path + self.keyword + str(excel.nrows) + ".png")
            print(temp)
            download_pic(url_pic, temp[record_url_local])
            excel.appendRecord(temp)

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

    def __scrollToBottom(self, scrollTime:int):
        for i in range(scrollTime):
            pyautogui.scroll(-400)
            time.sleep(0.2)

    def __divideDouyin(self, author: str, introduction:str, tags:list,
                            url_article: str, url_pic: str, url_local:str):
        res = getResModel(type='视频', source="抖音视频", keyword=self.keyword,
                          author=author, title="-", introduction=introduction,
                          tags=tags, caption="-", url_article=url_article,
                          url_pic=url_pic, url_local=url_local)
        return res
