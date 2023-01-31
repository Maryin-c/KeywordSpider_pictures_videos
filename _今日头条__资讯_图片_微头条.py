import os
import traceback

import pyautogui
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from tools import download_pic, excel, getResModel, log
from settings import toutiao_micro_path, toutiao_pic_path, toutiao_news_path, record_url_local


class Toutiao:
    def __init__(self):

        if not os.path.exists(toutiao_micro_path):
            os.mkdir(toutiao_micro_path)
        if not os.path.exists(toutiao_pic_path):
            os.mkdir(toutiao_pic_path)
        if not os.path.exists(toutiao_news_path):
            os.mkdir(toutiao_news_path)

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])
        chrome_options.add_argument("--disable-blink-features")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0')
        s = Service('./chromedriver.exe')
        self.browser = webdriver.Chrome(service=s, options=chrome_options)

    def setKeyword(self, keywords:list):
        self.keyword = " ".join(keywords)

    def searchNews(self, pageNumber=5):
        for i in range(pageNumber):
            try:
                self.__searchNews(i)
            except:
                log(traceback.format_exc())
                break

    def searchMicro(self, pageNumber=5):
        for i in range(pageNumber):
            try:
                self.__searchMicro(i)
            except:
                log(traceback.format_exc())
                break

    def searchPicture(self, scrollTime=300):
        self.browser.get('https://so.toutiao.com/search?dvpf=pc&source=search_subtab_switch&keyword={}&pd=atlas&action_type=search_subtab_switch&page_num=0&search_id=&from=gallery&cur_tab_title=gallery'.format(self.keyword))
        time.sleep(5)

        self.__scrollToBottom(scrollTime)

        imgs = self.browser.find_elements(By.CLASS_NAME, 'cs-view.cs-view-block.cs-image.margin-bottom-8.img_3eheVv')
        urls = []
        titles = []
        for img in imgs:
            url = img.find_element(By.TAG_NAME, "img").get_attribute("src")
            title = img.find_element(By.CLASS_NAME, "cs-view.margin-bottom-1.cs-view-block.cs-text.align-items-center.text_2NW5ID").get_attribute("title")
            urls.append(url)
            titles.append(title)
            print(url)
            print(title)

        for i in range(len(urls)):
            if excel.checkHttpRepeat(urls[i]):
                continue

            temp = self.__divideToutiao(source="今日头条图片", author="-", title=titles[i],
                                            introduction="-", caption="-",
                                            url_article=urls[i], url_pic=urls[i],
                                            url_local=toutiao_pic_path + self.keyword + str(excel.nrows) + ".png")
            print(temp)
            download_pic(urls[i], temp[record_url_local])
            excel.appendRecord(temp)

    def __scrollToBottom(self, scrollTime:int):
        for i in range(scrollTime):
            pyautogui.scroll(-400)
            time.sleep(0.2)

    def __searchMicro(self, page:int):
        self.browser.get('https://so.toutiao.com/search?dvpf=pc&source=search_subtab_switch&keyword={}&pd=weitoutiao&action_type=search_subtab_switch&page_num={}&search_id=&from=weitoutiao&cur_tab_title=weitoutiao'.format(self.keyword, page))
        time.sleep(5)

        cards = self.browser.find_elements(By.CLASS_NAME, 'cs-view.cs-view-block.cs-card-content')
        urls = []
        introductions = []
        for card in cards:
            url = card.find_element(By.XPATH, "./div[1]/a[1]").get_attribute("href")
            urls.append(url)
            print(url)
            introduction = "-"
            try:
                introduction = card.find_element(By.XPATH, "./div[1]/a[1]").find_element(By.CLASS_NAME, "text-underline-hover").text
            except:
                pass
            introductions.append(introduction)
            print(introduction)

        for i in range(len(urls)):
            if excel.checkHttpRepeat(urls[i]):
                continue
            self.browser.get(urls[i])
            time.sleep(5)

            title = "-"
            author = self.browser.find_element(By.CLASS_NAME, "author-info").find_element(By.CLASS_NAME, "name").text

            pics_attrs = self.browser.find_element(By.TAG_NAME, "article").find_elements(By.TAG_NAME, "img")
            for pic_attr in pics_attrs:
                pic_url = pic_attr.get_attribute("src")
                temp = self.__divideToutiao(source="今日头条微头条", author=author, title=title,
                                            introduction=introductions[i], caption="-",
                                            url_article=urls[i], url_pic=pic_url,
                                            url_local=toutiao_micro_path + self.keyword + str(excel.nrows) + ".png")
                print(temp)
                download_pic(pic_url, temp[record_url_local])
                excel.appendRecord(temp)

    def __searchNews(self, page:int):
        self.browser.get('https://so.toutiao.com/search?dvpf=pc&source=search_subtab_switch&keyword={}&pd=information&action_type=search_subtab_switch&page_num={}&search_id=&from=news&cur_tab_title=news'.format(self.keyword, page))
        time.sleep(5)
        # print(self.browser.page_source)
        cards = self.browser.find_elements(By.CLASS_NAME, 'cs-view.cs-view-block.cs-card-content')
        urls = []
        introductions = []
        for card in cards:
            url = card.find_element(By.CLASS_NAME, 'text-ellipsis.text-underline-hover').get_attribute("href")
            urls.append(url)
            print(url)
            introduction = "-"
            try:
                introduction = card.find_elements(By.CLASS_NAME, "cs-view.cs-view-block.cs-text.align-items-center")[1].find_element(By.CLASS_NAME, "text-underline-hover").text
            except:
                pass
            introductions.append(introduction)
            # print(introduction)

        for i in range(len(urls)):
            if excel.checkHttpRepeat(urls[i]):
                continue
            self.browser.get(urls[i])
            time.sleep(5)

            title = self.browser.find_element(By.CLASS_NAME, "article-content").find_element(By.TAG_NAME, "h1").text
            author = self.browser.find_element(By.CLASS_NAME, "article-content").find_element(By.CLASS_NAME, "name").find_element(By.TAG_NAME, "a").text

            pics_attrs = self.browser.find_element(By.CLASS_NAME, "syl-article-base.tt-article-content.syl-page-article.syl-device-pc").find_elements(By.TAG_NAME, "img")
            for pic_attr in pics_attrs:
                pic_url = pic_attr.get_attribute("src")
                temp = self.__divideToutiao(source="今日头条资讯", author=author, title=title,
                                            introduction=introductions[i], caption="-",
                                            url_article=urls[i], url_pic=pic_url,
                                            url_local=toutiao_news_path + self.keyword + str(excel.nrows) + ".png")
                print(temp)
                download_pic(pic_url, temp[record_url_local])
                excel.appendRecord(temp)

    def __divideToutiao(self, source:str, author: str, title:str, introduction:str, caption:str,
                                url_article: str, url_pic: str, url_local:str):
        res = getResModel(type='图片', source=source, keyword=self.keyword,
                          author=author, title=title, introduction=introduction,
                          tags=["-"], caption=caption, url_article=url_article,
                          url_pic=url_pic, url_local=url_local)
        return res
