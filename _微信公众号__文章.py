import json
import os
import time
import traceback

import ddddocr
import pyautogui

from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from settings import weixin_article_path, weixin_cookie_path, record_url_local, weixin_import_onnx_path, \
    weixin_charsets_path, weixin_proxy
from tools import log, getResModel, excel, download_pic


class Weixin:
    def __init__(self):
        if not os.path.exists(weixin_article_path):
            os.mkdir(weixin_article_path)

        chrome_options = webdriver.ChromeOptions()
        if weixin_proxy is not None:
            chrome_options.add_argument('--proxy-server=http://{}'.format(weixin_proxy))  # 隧道域名:端口号
        chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument("--disable-blink-features")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0')
        s = Service('./chromedriver.exe')
        self.driver = webdriver.Chrome(service=s, options=chrome_options)

        self.__updateCookie()

        self.ocr = ddddocr.DdddOcr(det=False, ocr=False, import_onnx_path=weixin_import_onnx_path, charsets_path=weixin_charsets_path)

    def __updateCookie(self):
        if not os.path.exists(weixin_cookie_path):
            self.driver.get('https://account.sogou.com/home/login')
            time.sleep(40)  # 留够时间来手动登录
            url = "https://weixin.sogou.com/weixin?ie=utf8&s_from=input&_sug_=n&_sug_type_=1&type=2&query=%E7%AC%94%E8%AE%B0&w=01015002&oq=&ri=0&sourceid=sugg&sut=0&sst0=1674291252432&lkt=0%2C0%2C0&p=40040108"
            js = "window.open('" + url + "')"
            self.driver.execute_script(js)
            time.sleep(5)
            with open(weixin_cookie_path, 'w') as f:
                # 将cookies保存为json格式在cookies.txt中
                f.write(json.dumps(self.driver.get_cookies()))
        else:
            pass

    def setKeyword(self, keywords:list):
        self.keyword = "+".join(keywords)

    def __loginAuto(self):
        self.driver.delete_all_cookies()
        with open(weixin_cookie_path, 'r') as f:
            cookies_list = json.load(f)  # 读取cookies
            for cookie in cookies_list:
                # if isinstance(cookie.get('expiry'), float):
                #     cookie['expiry'] = int(cookie['expiry'])
                if not cookie['domain'] == "account.sogou.com":
                    self.driver.add_cookie(cookie)  # 加入cookies
            self.driver.refresh()

    def searchArticle(self, pageNumber:int):
        self.driver.get('https://weixin.sogou.com/')
        self.driver.maximize_window()
        wait = WebDriverWait(self.driver, 10)
        _input = wait.until(ec.presence_of_element_located((By.NAME, 'query')))
        # 搜索框中输入内容
        _input.send_keys(self.keyword)
        self.driver.find_element(By.CLASS_NAME, "enter-input.article").click()

        self.__loginAuto()

        time.sleep(5)

        i = 0
        while i < pageNumber:
            self.__getNews()
            try:
                self.driver.find_element(By.ID, "sogou_next").click()
                time.sleep(2)
                self.driver.get("https://dev.kdlapi.com/testproxy")
                time.sleep(2)
                self.driver.back()
                time.sleep(2)
                i+=1
            # 直到不存在下一页  爬取结束
            except:
                try:
                    self.__getSeccode()
                except:
                    log(traceback.format_exc())
                    break

    def __getNews(self):
        # 全局变量  统计文章数  记序
        article_lis = self.driver.find_elements(By.XPATH, '//ul[@class="news-list"]/li')
        for article in article_lis:

            introduction = "-"
            try:
                introduction = article.find_element(By.CLASS_NAME, "txt-info").text
            except:
                pass

            article.find_element(By.XPATH, './/h3/a').click()
            all_handles = self.driver.window_handles
            # 将当前句柄定位到新打开的页面
            self.driver.switch_to.window(all_handles[-1])
            time.sleep(5)
            self.__scrollToBottom(50)
            time.sleep(5)

            if excel.checkHttpRepeat(self.driver.current_url):
                continue

            try:
                author = self.driver.find_element(By.ID, "js_name").text
                title = self.driver.find_element(By.ID, "activity-name").text

                pics = self.driver.find_element(By.ID, "img-content").find_elements(By.TAG_NAME, "img")

                for pic in pics:
                    try:
                        pic_url = pic.get_attribute("src")
                        if len(pic_url) < 5:
                            continue
                        temp = self.__divideWeixin(author=author, title=title,
                                                    introduction=introduction,
                                                    url_article=self.driver.current_url, url_pic=pic_url,
                                                    url_local=weixin_article_path + self.keyword + str(excel.nrows) + ".png")
                        print(temp)
                        download_pic(pic_url, temp[record_url_local])
                        excel.appendRecord(temp)
                    except:
                        pass
            except:
                # 文章删除
                pass

            # 关闭当前标签页（第二页）
            self.driver.close()
            self.driver.switch_to.window(all_handles[0])
            time.sleep(1)

    def __getSeccode(self):
        time.sleep(5)
        self.driver.find_element(By.ID, "seccodeImage").screenshot("code.png")
        time.sleep(1)
        with open("code.png", 'rb') as f:
            image = f.read()
        res = self.ocr.classification(image).upper()
        self.driver.find_element(By.NAME, "c").send_keys(res)
        print(res)
        time.sleep(5)
        self.driver.find_element(By.ID, "submit").click()
        time.sleep(5)
        try:
            self.driver.find_element(By.ID, "change-img").click()
        except:
            pass

    def __scrollToBottom(self, scrollTime:int):
        for i in range(scrollTime):
            pyautogui.scroll(-400)
            time.sleep(0.2)

    def __divideWeixin(self, author: str, title:str, introduction:str,
                                url_article: str, url_pic: str, url_local:str):
        res = getResModel(type='图片', source="微信公众号文章", keyword=self.keyword,
                          author=author, title=title, introduction=introduction,
                          tags=["-"], caption="-", url_article=url_article,
                          url_pic=url_pic, url_local=url_local)
        return res
