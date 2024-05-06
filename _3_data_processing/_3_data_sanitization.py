
import re
from __utils.__path_util import global_path
from __utils.__save_file_util import save_dict_to_json, save_str_file, save_list_to_csv
from __utils.__similarity_util import similarity
from __utils.__unicode_util import unicode_calc_proportion, unicode_filter
from __utils.__filter_util import html_filter, filter_dictionary_string
import json
from multiprocessing import Process

global_path = global_path
root_path = global_path.__2_response_pattern_result_path__


def extract_status_code(response_text):
    # 使用正则表达式匹配 HTTP 响应
    match = re.match(r'HTTP/1\.1 (\d+) ', response_text)

    if match:
        status_code = match.group(1)
        return status_code
    else:
        return None


response_data = []
data_count = 0
http_count = 0
http_unfilter_list = [
    "Server:", "Set-Cookie:", "X-Powered-By:"
]

http_filter_list = [
    "Content-Type:", "HTTP/1.1", "Expires:", "Cache-Control:", "Pragma:", "Vary:",
    "Content-Security-Policy:", "Location:", ...
]


# TODO 数据过滤规则完善：
def sanitization_string(str_):

    bad_str_ = ""
    # 对responseData进行过滤操作
    if str_ == "":
        return bad_str_

    # 处理http/https协议的responseData
    if str_.startswith("HTTP/"):
        # 将状态码为3XX和5XX的过滤掉
        if str_[len("HTTP/1.1 ")] in ['3', '5']:
            print("\thttp bad")
            return bad_str_
        else:
            str_ = html_filter(str_)

    str_ = unicode_filter(str_)
    # 对所有response作统一过滤
    str_ = re.sub(r'<\s*p\s*>(.*?)<\s*/\s*p\s*>', ' ', str_)
    str_ = re.sub(r'\\x[0-9a-fA-F]{2}', ' ', str_)  # 将\\xff十六进制过滤
    str_ = re.sub(r'x[0-9a-fA-F]{2}', ' ', str_)    # 将xff十六进制过滤
    str_ = re.sub(r'\s+', ' ', str_)                # 多个空格匹配成为一个空格
    str_ = re.sub(r'-+', '-', str_)                 # 多个破折号匹配成为一个破折

    '''处理.符号问题 多. 边缘.等'''
    str_ = re.sub(r'\.+', '.', str_)
    str_ = re.sub(r'\s*\.\s', ' ', str_)
    str_ = re.sub(r'\s\.\s*', ' ', str_)
    str_ = re.sub(r'\s*\.$', ' ', str_)
    str_ = re.sub(r'^\.\s*', ' ', str_)

    str_ = ' '.join([char for char in str_.strip().split() if len(char) > 1])  # 匹配两侧空格字符串并将其删除
    str_ = str_.lower()
    # 去除stop words
    str_ = filter_dictionary_string(str_)
    return str_


def load_data():
    raw_data_path = global_path.__raw_data_path__ + "all_response_dichotomy_v1.json"

    raw_data = open(raw_data_path, "r", encoding="utf-8").read()
    raw_data_list = eval(raw_data)["natural language"]
    result_dict = {"sanitization_data": []}
    cnt_ = 1
    for line in raw_data_list:
        print(cnt_)
        cnt_ += 1
        clean_data = sanitization_string(line)
        result_dict["sanitization_data"].append(clean_data)

    save_dict_to_json(global_path.__raw_data_path__ + "all_response_sanitization_v3.json", result_dict)


if __name__ == "__main__":
    print(sanitization_string("HTTP/1.1 404 Not Found\r\nServer: kong/2.8.1\r\nDate: Mon, 18 Dec 2023 08:21:15 GMT\r\nContent-Type: application/json; charset=utf-8\r\nContent-Length: 48\r\nX-Kong-Response-Latency: 0\r\nConnection: close\r\n\r\n{\"message\":\"no Route matched with those values\"}"))
    # load_data()














