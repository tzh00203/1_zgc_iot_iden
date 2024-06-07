import json
import requests
import re

from __utils.__filter_util import filter_dictionary_string
from __utils.__unicode_util import unicode_filter

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


def proxy_request(search_url, retry_count: int = 5):

    # 隧道域名:端口号
    tunnel = "t715.kdltpspro.com:15818"

    # 用户名密码方式
    username = "t11765165139962"
    password = "7ur5ie7p"
    proxies = {
        "http": "http://%(user)s:%(pwd)s@%(proxy)s/" % {"user": username, "pwd": password, "proxy": tunnel},
        "https": "http://%(user)s:%(pwd)s@%(proxy)s/" % {"user": username, "pwd": password, "proxy": tunnel}
    }

    # 白名单方式（需提前设置白名单）
    # proxies = {
    #     "http": "http://%(proxy)s/" % {"proxy": tunnel},
    #     "https": "http://%(proxy)s/" % {"proxy": tunnel}
    # }

    # 要访问的目标网页
    target_url = search_url

    # 使用隧道域名发送请求
    response = requests.get(target_url, proxies=proxies)

    # 获取页面内容
    if response.status_code == 200:
        print(response.text)  # 请勿使用keep-alive复用连接(会导致隧道不能切换IP)


def common_request(search_url, retry_count: int = 5):
    search_results = None
    tunnel = "t715.kdltpspro.com:15818"

    # 用户名密码方式
    username = "t11765165139962"
    password = "7ur5ie7p"
    proxies = {
        "http": "http://%(user)s:%(pwd)s@%(proxy)s/" % {"user": username, "pwd": password, "proxy": tunnel},
        "https": "http://%(user)s:%(pwd)s@%(proxy)s/" % {"user": username, "pwd": password, "proxy": tunnel}
    }
    while retry_count > 0:
        try:
            response = requests.get(search_url)
            if response.status_code == 200 and response.text is not None:
                search_results = response.text
                break
            else:
                retry_count -= 1
        except Exception as e:
            print(e)
            retry_count -= 1

    return search_results


def word_product_re_pattern(ori_word):
    import re
    text = " " + ori_word + " "
    # 定义正则表达式模式
    pattern_num_cha = r'(?=.*\d)(?=.*[a-zA-Z])'
    pattern1 = r' [a-zA-Z0-9]+-[a-zA-Z0-9]+ '
    pattern2 = r' [a-zA-Z]+[0-9]+ '

    # 示例字符串
    text1 = "Here are some examples: rt-ac86u  A1-B2 , xYz-123, and no-match-here."
    text2 = "Example strings:  rt-ac86u abc-!def123-ghi∧1234XYZ, test-456-abc∧12AB."

    # 使用 re.findall 进行匹配
    matches1 = re.findall(pattern1, text)
    matches2 = re.findall(pattern2, text)
    if matches1 and re.search(pattern_num_cha, matches1[0]) and len(ori_word) > 4:

        return ori_word

    elif matches2 and len(ori_word) > 4:

        return ori_word
    return None


def crawler_html_filter(link, html_content):

    from bs4 import BeautifulSoup

    # 使用BeautifulSoup解析HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    # 获取标题
    title = soup.title.string if soup.title else 'No title found'

    # 获取所有文本信息
    text = soup.get_text()

    # 去除多余的空白字符
    cleaned_text = ' '.join(text.split())

    html_result = {
        "uri": link,
        "title": title,
        "web_info": cleaned_text
    }

    return html_result


if __name__ == "__main__":
    if word_product_re_pattern("dcs-5020l"):
        print(word_product_re_pattern("dcs-5020l"))
    else:
        print(666)
    re1 = requests.get("https://www.dlink.com/uk/en/products/dcs-5000l-wi-fi-pan-tilt-day-night-camera")
    rr = re1.text
    dict1 = crawler_html_filter(rr)
    dict1.update({"link": "sasaas"})
    print(dict1)
