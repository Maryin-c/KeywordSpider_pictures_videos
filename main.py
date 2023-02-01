from _b站__视频_专栏 import Bilibili
from _微博__实时_热门_图片 import Weibo
from _知乎__问答_文章 import Zhihu
from _今日头条__资讯_图片_微头条 import Toutiao
from _抖音__视频 import Douyin
from _快手__视频 import KuaiShou
from _Youtube__视频 import Youtube
from _微信公众号__文章 import Weixin
from tools import excel

print(excel.keywordDict)

# bili = Bilibili()
weibo = Weibo()
# zhihu = Zhihu()
# toutiao = Toutiao()
# kuaishou = KuaiShou()
# douyin = Douyin()
# youtube = Youtube()
# weixin = Weixin()

for item in excel.keywordDict["类型"]:
    print("start")

    # bili.setKeyword([item])
    # bili.article(pageNumber=2)
    # bili.video(pageNumber=2)

    weibo.setKeyword(["笔记", item])
    weibo.current(page=20)
    excel.saveExcel()
    weibo.hot(page=20)
    excel.saveExcel()
    weibo.picture(page=20)
    excel.saveExcel()

    # zhihu.setKeyword([item])
    # zhihu.searchAnswer(50)
    # zhihu.searchArticle(50)

    # toutiao.setKeyword([item])
    # toutiao.searchNews(2)
    # toutiao.searchMicro(2)
    # toutiao.searchPicture(50)

    # douyin.setKeyword([item])
    # douyin.searchVideo(10)

    # kuaishou.setKeyword([item])
    # kuaishou.searchVideo(20)

    # youtube.setKeyword([item])
    # youtube.searchVideo(20)

    # weixin.setKeyword([item])
    # weixin.searchArticle(2)

    # if i == 2:
    #     break
    # i+=1
    # break
    # excel.saveExcel()
