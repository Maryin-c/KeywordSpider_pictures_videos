import json
import os
import time
import pyautogui
from selenium import webdriver  # 导入selenium包
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

from settings import zhihu_cookie_path, zhihu_answer_path, zhihu_article_path, record_url_local
from tools import getResModel, excel, download_pic


class Zhihu:

    def __init__(self):
        if not os.path.exists(zhihu_answer_path):
            os.mkdir(zhihu_answer_path)
        if not os.path.exists(zhihu_article_path):
            os.mkdir(zhihu_article_path)

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])
        chrome_options.add_argument("--disable-blink-features")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        s = Service('./chromedriver.exe')
        # s = Service("Driver/geckodriver.exe")
        self.driver = webdriver.Chrome(service=s, options=chrome_options)

        self.__updateCookie()

    def setKeyword(self, keywords:list):
        self.keyword = "+".join(keywords)

    def __updateCookie(self):
        self.driver.get('https://www.zhihu.com/search?type=content&q=')
        time.sleep(5)
        if not os.path.exists(zhihu_cookie_path):
            time.sleep(40)  # 留够时间来手动登录
            with open(zhihu_cookie_path, 'w') as f:
                # 将cookies保存为json格式在cookies.txt中
                f.write(json.dumps(self.driver.get_cookies()))
        else:
            self.driver.delete_all_cookies()
            with open(zhihu_cookie_path, 'r') as f:
                cookies_list = json.load(f)  # 读取cookies
                for cookie in cookies_list:
                    if isinstance(cookie.get('expiry'), float):
                        cookie['expiry'] = int(cookie['expiry'])
                    try:
                        self.driver.add_cookie(cookie)  # 加入cookies
                    except:
                        print(cookie)
            self.driver.refresh()

    def __scrollToBottom(self, scrollTime:int):
        for i in range(scrollTime):
            pyautogui.scroll(-400)
            time.sleep(0.2)

    def searchArticle(self, scrollTime=300):
        self.driver.get('https://www.zhihu.com/search?q={}&type=content&utm_id=0&vertical=article'.format(self.keyword))
        self.driver.maximize_window()

        time.sleep(2)
        self.__scrollToBottom(scrollTime)

        # number = 0
        urls = []
        introductions = []
        for article in self.driver.find_elements(By.CLASS_NAME, "ContentItem.ArticleItem"):
            title = article.find_element(By.CSS_SELECTOR, '[target="_blank"]')
            url = title.get_attribute('href')
            urls.append(url)
            introduction = article.find_element(By.CSS_SELECTOR, '[itemprop="articleBody"]').text
            introductions.append(introduction)
            print(url)
            # number+=1
        # print(number)
        # time.sleep(600)
        for i in range(len(urls)):
            self.__openArticle(urls[i], introductions[i])
            # time.sleep(600)
            # return
        time.sleep(2)
        # driver.find_element(By.ID, "Popover1-toggle").send_keys("玫瑰\n")
        return

    def searchAnswer(self, scrollTime=300):
        self.driver.get('https://www.zhihu.com/search?q={}&type=content&utm_id=0&vertical=answer'.format(self.keyword))
        self.driver.maximize_window()

        time.sleep(2)
        self.__scrollToBottom(scrollTime)

        # number = 0
        urls = []
        for answer in self.driver.find_elements(By.CLASS_NAME, "ContentItem.AnswerItem"):
            title = answer.find_element(By.CSS_SELECTOR, '[itemprop="url"]')
            url = title.get_attribute('content')
            urls.append(url)
            print(url)
            # number+=1
        # print(number)
        for url in urls:
            self.__openQuestion(url, scrollTime)
            # return
        # time.sleep(600)
        time.sleep(2)
        # driver.find_element(By.ID, "Popover1-toggle").send_keys("玫瑰\n")
        return

    def __openArticle(self, url:str, introduction:str):
        if excel.checkHttpRepeat(url):
            return

        self.driver.get(url)
        time.sleep(2)

        title = self.driver.find_element(By.CLASS_NAME, "Post-Title").text
        # introduction = "-"
        author = self.driver.find_element(By.CLASS_NAME, "UserLink.AuthorInfo-name").find_element(By.CLASS_NAME, 'UserLink-link').text

        pics_attrs = self.driver.find_element(By.CLASS_NAME, "Post-RichTextContainer").find_elements(By.TAG_NAME, "img")
        for pic_attr in pics_attrs:
            pic_url = pic_attr.get_attribute("data-original")
            if pic_url is None:
                continue
            temp = self.__divideZhihu(source="知乎文章", author=author, title=title,
                                      introduction=introduction,
                                      url_article=url, url_pic=pic_url,
                                      url_local=zhihu_article_path + self.keyword + str(excel.nrows) + ".png")
            print(temp)
            download_pic(pic_url, temp[record_url_local])
            excel.appendRecord(temp)

    def __openQuestion(self, url:str, scrollTime:int):

        if excel.checkHttpRepeat(url):
            return

        self.driver.get(url)
        time.sleep(2)

        self.__scrollToBottom(scrollTime)

        title = self.driver.find_element(By.CLASS_NAME, "QuestionHeader-title").text
        introduction = self.driver.find_element(By.CLASS_NAME, "RichText.ztext.css-1g0fqss").text

        answers = self.driver.find_elements(By.CLASS_NAME, "ContentItem.AnswerItem")
        for answer in answers:
            author = answer.find_element(By.CLASS_NAME, "AuthorInfo").find_element(By.CSS_SELECTOR, '[itemprop="name"]').get_attribute("content")
            pics_attrs = answer.find_element(By.CLASS_NAME, "RichContent-inner").find_elements(By.TAG_NAME, "img")
            for pic_attr in pics_attrs:
                pic_url = pic_attr.get_attribute("data-original")
                if pic_url is None:
                    continue
                temp = self.__divideZhihu(source="知乎问答", author=author, title=title,
                                          introduction=introduction,
                                          url_article=url, url_pic=pic_url,
                                          url_local=zhihu_answer_path + self.keyword + str(excel.nrows) + ".png")
                print(temp)
                download_pic(pic_url, temp[record_url_local])
                excel.appendRecord(temp)


    def __divideZhihu(self, source:str, author: str, title:str, introduction:str,
                                url_article: str, url_pic: str, url_local:str):
        res = getResModel(type='图片', source=source, keyword=self.keyword,
                          author=author, title=title, introduction=introduction,
                          tags=["-"], caption="-", url_article=url_article,
                          url_pic=url_pic, url_local=url_local)
        return res
