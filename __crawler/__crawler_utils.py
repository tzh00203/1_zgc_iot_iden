import json
import requests

PROXY_POOL_URL = 'http://127.0.0.1:5010'

def get_proxy():
    try:
        response = requests.get(PROXY_POOL_URL)
        if response.status_code == 200:
            return response.text
    except ConnectionError:
        return None


def delete_proxy(proxy):
    requests.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy))


def load_keywords_from_tfidf(json_file_path: str = None, json_str: str = None):
    """
    从标准格式json文件或json字符串中加载tfidf识别出的关键词，返回关键词二维列表
    :param json_file_path: str
    :param json_str: str
    :return: list
    """
    if json_file_path:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    elif json_str:
        data = json.loads(json_str)
    else:
        raise ValueError("json_file_path or json_str must be provided")
    data = list(data.values())
    keywords = []
    for item in data:
        if item not in keywords:
            keywords.append(item)
    return keywords