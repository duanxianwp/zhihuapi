import time
from io import BytesIO
from PIL import Image
from wordcloud import WordCloud
import jieba
import requests
from db import MongoTools, OssUtils
from bs4 import BeautifulSoup
import numpy as np
import random
from config import settings

'''取数据,去空格'''


class CleanData(object):
    url_token = None
    stop_words_list = {}

    def __init__(self):
        url = settings.WORD_CLOUD_STOP_WORD_URL
        self.stop_words_list = set(requests.get(url).text.split('\n'))

    def get_answer_word_data(self):
        token = MongoTools.get_analyze_token()
        if not token:
            return
        self.url_token = token
        answers = MongoTools.get_all_answer_word(token)
        return ''.join(BeautifulSoup(answer, 'lxml').text for answer in answers)

    '''分词'''

    def participle(self, article):
        word_list = (' '.join(jieba.cut(article.strip(), cut_all=False))).split(' ')  # seg_list为str类型
        final_word_list = []

        for word in word_list:
            if word not in self.stop_words_list:
                final_word_list.append(word)

        return ' '.join(final_word_list)

    '''统计词频'''

    def word_count(self, words):
        word_dict = {}
        word_list = words.split(' ')
        for item in word_list:
            if item not in word_dict:
                word_dict[item] = 1
            else:
                word_dict[item] += 1
        return dict(sorted(word_dict.items(), key=lambda item: item[1], reverse=True))  # 按照词频从大到小排序

    '''制作词云'''

    def make_word_cloud(self, words):
        index = random.randint(settings.WORD_CLOUD_BACK_TEMPLATE_START, settings.WORD_CLOUD_BACK_TEMPLATE_END)
        template_url = settings.WORD_CLOUD_BACK_TEMPLATE_URL.format(index)
        content = BytesIO(requests.get(template_url).content)
        image = Image.open(content)
        background_image = np.array(image, dtype=np.uint8)
        my_wordcloud = WordCloud(
            background_color=settings.WORD_CLOUD_BACKGROUND_COLOR,
            mask=background_image,
            font_path=settings.WORD_CLOUD_FONT_PATH,
            stopwords=self.stop_words_list,
            max_words=settings.WORD_CLOUD_MAX_WORDS,
            max_font_size=settings.WORD_CLOUD_MAX_FONT_SIZE,  # 字体最大值
            min_font_size=settings.WORD_CLOUD_MIN_FONT_SIZE,
            random_state=settings.WORD_CLOUD_RANDOM_STATE
        ).generate(words)
        img = my_wordcloud.to_image()
        return OssUtils.upload_img(img)


def run():
    obj = CleanData()
    # 获取数据集
    data = obj.get_answer_word_data()
    if not data:
        return
    # 分词 获得分词且去除stopWord的词组（以空格分开）
    words = obj.participle(data)
    # 制作词云 并上传至阿里云
    img_name = obj.make_word_cloud(words)
    # 统计词频
    # kvs = obj.word_count(words)
    # 更改状态 并存储对应数据
    word_cloud_item = {
        'url_token': obj.url_token,
        'img_url': settings.OSS_URL.format(img_name),
        #  'word_count': json.dumps(kvs),
        'created_at': time.time()
    }
    MongoTools.finish_data_anlyaze(word_cloud_item)
