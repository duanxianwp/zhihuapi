MONGO_URI = 'localhost'
MONGO_DATABASE = 'zhihu'
# 停用词
WORD_CLOUD_STOP_WORD_URL = 'https://ip/stop_word.txt'
# 模版url
WORD_CLOUD_BACK_TEMPLATE_URL = 'https://ip/template/{}.png'
# 模版索引
WORD_CLOUD_BACK_TEMPLATE_START = 1
WORD_CLOUD_BACK_TEMPLATE_END = 1

# 渲染背景颜色
WORD_CLOUD_BACKGROUND_COLOR = 'white'
# 渲染字体路径
WORD_CLOUD_FONT_PATH = '/Library/Fonts/Songti.ttc'
# 要显示的词的最大个数
WORD_CLOUD_MAX_WORDS = 1000
WORD_CLOUD_MAX_FONT_SIZE = 100  # 字体最大值
WORD_CLOUD_MIN_FONT_SIZE = 10
WORD_CLOUD_RANDOM_STATE = 42

# OSS Key Secret
OSS_KEY = 'key'
OSS_SECRET = 'secret'
OSS_AREA = 'http://oss-cn-shanghai.aliyuncs.com'
OSS_BUCKET = 'bucket'
OSS_PATH = 'wordcloud/out/'
OSS_URL = 'https://ip/out/{}'
