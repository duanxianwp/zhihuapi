import pymongo
import time
from config import settings

'''添加一个新任务'''


def insert_collect_task(token):
    client = pymongo.MongoClient(settings.MONGO_URI)
    tb = client.get_database(settings.MONGO_DATABASE).get_collection('collect_task')
    item = {
        'token': token,
        'status': 'INIT',
        'created_at': time.time()
    }
    data = tb.find_one({'token': token})
    client.close()
    if data and (time.time() - data['created_at'] < 3 * 24 * 60 * 60):
        return False
    else:
        tb.insert_one(item)
        return True


'''获取task的状态'''


def get_task_status(token):
    client = pymongo.MongoClient(settings.MONGO_URI)
    tb = client.get_database(settings.MONGO_DATABASE).get_collection('collect_task')
    data = tb.find_one({'token': token})
    client.close()
    if data:
        # 如果超过30天,认为其未进行过采集
        if time.time() - data['created_at'] > 30 * 24 * 60 * 60:
            return None
        else:
            return data['status']
    else:
        return None


'''获取一个待分析task的用户token'''


def get_analyze_token():
    client = pymongo.MongoClient(settings.MONGO_URI)
    tb = client.get_database(settings.MONGO_DATABASE).get_collection('collect_task')
    result = tb.find_and_modify({'status': 'ANALYZE_WAIT'}, {'$set': {'status': "ANALYZING"}})
    client.close()
    if result:
        return result['token']
    else:
        return None


'''获取用户所有回复内容'''


def get_all_answer_word(token):
    client = pymongo.MongoClient(settings.MONGO_URI)
    tb = client.get_database(settings.MONGO_DATABASE).get_collection('answer')
    result = tb.find({'url_token': token})
    client.close()
    return map(lambda data: data.get('content'), result)


'''存储清分析的数据'''


def finish_data_anlyaze(item):
    client = pymongo.MongoClient(settings.MONGO_URI)
    tb = client.get_database(settings.MONGO_DATABASE).get_collection('word_cloud_item')
    tb.insert_one(item)
    tb = client.get_database(settings.MONGO_DATABASE).get_collection('collect_task')
    tb.update_one({'token': item['url_token']}, {'$set': {'status': 'FINISHED'}}, True)
    client.close()
