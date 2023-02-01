from _b站__视频_专栏 import Bilibili
from _微博__实时_热门_图片 import Weibo
from _知乎__问答_文章 import Zhihu
from _今日头条__资讯_图片_微头条 import Toutiao
from _抖音__视频 import Douyin
from _快手__视频 import KuaiShou
from _Youtube__视频 import Youtube
from _微信公众号__文章 import Weixin
from settings import bilibili_page, weibo_page, toutiao_page, toutiao_scroll_time, youtube_scroll_time, \
    zhihu_scroll_time, douyin_scroll_time, kuaishou_scroll_time, weixin_page
from tools import excel

def bilibili(key:str, page=5):
    bili = Bilibili()
    for item in excel.keywordDict[key]:

        bili.setKeyword(item)

        bili.article(pageNumber=page)
        excel.saveExcel()
        bili.video(pageNumber=page)
        excel.saveExcel()

def weibo(key:str, page=5):
    wei = Weibo()
    for item in excel.keywordDict[key]:

        wei.setKeyword(item)

        wei.current(page=page)
        excel.saveExcel()
        wei.hot(page=page)
        excel.saveExcel()
        wei.picture(page=page)
        excel.saveExcel()

def toutiao(key:str, page=5, scrollTime=50):
    tou = Toutiao()
    for item in excel.keywordDict[key]:

        tou.setKeyword(item)

        tou.searchNews(pageNumber=page)
        excel.saveExcel()
        tou.searchMicro(pageNumber=page)
        excel.saveExcel()
        tou.searchPicture(scrollTime=scrollTime)
        excel.saveExcel()

def youtube(key:str, scrollTime=50):
    you = Youtube()
    for item in excel.keywordDict[key]:

        you.setKeyword(item)

        you.searchVideo(scrollTime=scrollTime)
        excel.saveExcel()

def zhihu(key:str, scrollTime=50):
    zhi = Zhihu()
    for item in excel.keywordDict[key]:

        zhi.setKeyword(item)

        zhi.searchAnswer(scrollTime=scrollTime)
        excel.saveExcel()
        zhi.searchArticle(scrollTime=scrollTime)
        excel.saveExcel()

def douyin(key:str, scrollTime=50):
    dou = Douyin()
    for item in excel.keywordDict[key]:

        dou.setKeyword(item)

        dou.searchVideo(scrollTime=scrollTime)
        excel.saveExcel()

def kuaishou(key:str, scrollTime=50):
    kuai = KuaiShou()
    for item in excel.keywordDict[key]:

        kuai.setKeyword(item)

        kuai.searchVideo(scrollTime=scrollTime)
        excel.saveExcel()

def weixin(key:str, page=5):
    wei = Weixin()
    for item in excel.keywordDict[key]:

        wei.setKeyword(item)

        wei.searchArticle(pageNumber=page)
        excel.saveExcel()

if __name__ == "__main__":
    print("关键字组合        关键字")
    for key in excel.keywordDict.keys():
        print(key + "       " + str(excel.keywordDict[key]))

    keyList = input("输入使用的关键字组合：")
    print("*"*50)

    print("来源编号       来源         备注")

    print("0             bilibili       ")
    print("1             微博            ")
    print("2             今日头条         ")
    print("3             Youtube        ")

    print("4             知乎         程序第一次运行需要手动登录")
    print("5             抖音         程序第一次运行需要手动登录")
    print("6             微信公众号    程序第一次运行需要手动登录")
    print("7             快手         程序*每一次*运行都需要手动登录")

    type = int(input("输入来源编号："))
    print("*"*50)

    if type == 0:
        bilibili(keyList, page=bilibili_page)
    elif type == 1:
        weibo(keyList, page=weibo_page)
    elif type == 2:
        toutiao(keyList, page=toutiao_page, scrollTime=toutiao_scroll_time)
    elif type == 3:
        youtube(keyList, scrollTime=youtube_scroll_time)
    elif type == 4:
        zhihu(keyList, scrollTime=zhihu_scroll_time)
    elif type == 5:
        douyin(keyList, scrollTime=douyin_scroll_time)
    elif type == 6:
        weixin(keyList, page=weixin_page)
    elif type == 7:
        kuaishou(keyList, scrollTime=kuaishou_scroll_time)

