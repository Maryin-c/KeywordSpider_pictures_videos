# 图片下载间隔
picture_download_interval = 0.5

# 连接等待时长
requests_timeout = 30

# 是否下载视频
download_video_check = False

# excel 路径
excel_path = "全部记录.xlsx"

# excel 每列名称
record_type = '类型'
record_source = '来源'
record_keyword = '关键词'
record_author = '作者'
record_title = '标题'
record_introduction = '简介'
record_tags = '标签'
record_caption = '图注'
record_url_article = '原文链接'
record_url_pic = '图片链接'
record_url_local = '本地链接'

# 日志目录
log_path = 'log.txt'

# bilibili 存储目录
bilibili_video_screen_shot_path = "./b站视频封面/"
bilibili_video_path = "./b站视频/"
bilibili_article_picture_path = "./b站专栏/"
# bilibili 爬取页数
bilibili_page = 5

# 微博 存储目录
weibo_current_path = "./微博实时动态/"
weibo_hot_path = "./微博热门动态/"
weibo_pic_path = "./微博图片动态/"
# 微博 爬取页数
weibo_page = 5

# 知乎cookie目录
zhihu_cookie_path = "./知乎cookies.txt"
# 知乎 存储目录
zhihu_answer_path = "./知乎问答/"
zhihu_article_path = "./知乎文章/"
# 知乎 鼠标滚轮滑动时长
zhihu_scroll_time = 50

# 今日头条 存储目录
toutiao_news_path = "./今日头条咨询/"
toutiao_pic_path = "./今日头条图片/"
toutiao_micro_path = "./今日头条微咨询/"
# 今日头条 爬取页数
toutiao_page = 5
# 今日头条 鼠标滚轮滑动时长
toutiao_scroll_time = 50

# 抖音cookie目录
douyin_cookie_path = "./抖音cookies.txt"
# 抖音 存储目录
douyin_video_path = "./抖音视频/"
douyin_video_screen_shot_path = "./抖音视频封面/"
# 抖音 鼠标滚轮滑动时长
douyin_scroll_time = 50

# 快手 存储目录
kuaishou_video_screen_shot_path = "./快手视频封面/"
# 快手 鼠标滚轮滑动时长
kuaishou_scroll_time = 50

# youtube 存储目录
youtube_video_screen_shot_path = "./youtube视频封面/"
youtube_video_path = "./youtube视频/"
# youtube 鼠标滚轮滑动时长
youtube_scroll_time = 50

# 搜狗微信 验证码深度学习模型
weixin_import_onnx_path = "./model/sougou_1.0_21_113000_2023-01-22-05-53-19.onnx"
weixin_charsets_path = "./model/charsets.json"
# 搜狗微信cookie目录
weixin_cookie_path = "./微信cookies.txt"
# 搜狗微信 存储目录
weixin_article_path = "./微信公众号文章/"
# 搜狗微信 爬取页数
weixin_page = 5
# 搜狗微信 代理IP 使用快代理的隧道代理服务，可以不设置，但是爬取过多时可能会导致封IP
weixin_proxy = None # "XXX.XXX.com:XXXXX"
