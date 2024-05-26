"""
并发地通过搜索引擎爬取到的uri列表获取设备网页信息描述--html格式
1. 加载uri_log文件 数据处理与分析
2. requests_get words对应的 webpage页面信息
3. 将html信息进行字符串处理 使用_3_data_processing中模块 过滤得到关键字词/使用IoT-Assets-Library做字词匹配扩充资产标签
"""
from multiprocessing import Process

from __logs.__log import log_init
from __utils.__path_util import global_path
from __utils.__save_file_util import save_dict_to_json
from __crawler_utils import common_request
from _3_data_processing._3_data_sanitization import sanitization_string


def load_iot_assets_library():
    iot_assets_path =global_path.__assets_library_path__
    vendor_list = open(iot_assets_path + "vendor.txt", "r", encoding="utf-8").readlines()
    type_list = open(iot_assets_path + "type.txt", "r", encoding="utf-8").readlines()

    type_vendor_list = type_list + vendor_list
    new_type_vendor_list = []
    for word in type_vendor_list:
        new_type_vendor_list.append(word.strip().lower())
    if "" in type_vendor_list:
        new_type_vendor_list.remove("")
    if " " in type_vendor_list:
        new_type_vendor_list.remove(" ")
    print(new_type_vendor_list, len(new_type_vendor_list))
    return new_type_vendor_list


def load_uri_log():
    """
    加载uri_api搜索的log文件并进行数据处理
    返回sanitization文件中对应的行号字符串所对应的web page uri list
    :return: dict{ str[line1_line2]: list[webpage1, webpage2] }
    """
    import os
    import re

    uri_log_path = global_path.__crawler_search_result_path__ + "search_log/"
    pattern = r"INFO\s+(\S+)\s+line.*?:search\s+uri:\s+(\S+)"
    webpage_uri_dict = {}
    log_list = os.listdir(uri_log_path)
    for log_name in log_list:
        filepath = os.path.join(uri_log_path, log_name)
        lines = open(filepath, "r", encoding="utf-8").readlines()
        for line in lines:
            match = re.search(pattern, line)
            if not match:
                continue
            sanitization_line_str = match.group(1)
            uri = match.group(2)
            if sanitization_line_str not in webpage_uri_dict:
                webpage_uri_dict[sanitization_line_str] = [uri]
            else:
                webpage_uri_dict[sanitization_line_str].append(uri)
    webpage_line = list(webpage_uri_dict.keys())
    webpage_uri = list(webpage_uri_dict.values())

    num = 0
    for uris in webpage_uri:
        num += len(uris)
    print("all uri num:", num)
    return webpage_line, webpage_uri


def webpage_concurrent(webpage_line, webpage_uri, iot_library_list, start: int, end: int):
    """
    搜索
    :param webpage_line: sanitization中行号
    :param webpage_uri: webpage uri list
    :param iot_library_list: 厂商和产品类型列表
    :param start: 线程数据index起始
    :param end:   线程数据index末尾+1
    :return:
    """

    webpage_uri_part = webpage_uri[start: end + 1]
    webpage_line_part = webpage_line[start: end + 1]
    logger_path = global_path.__crawler_search_result_path__ + f"webpage_log/webpage_uri_{start}_{end}.log"
    poc_logger = log_init(logFilename=logger_path)

    fail_num = 0
    result_path = global_path.__crawler_search_result_path__ + f"webpage_log/webpage_sanitization_{start}_{end}.json"
    result_str = {}     # 清洗过后的网页html信息
    result_words = {}   # 需要对比library筛选的字词信息

    cnt = 1
    for index in range(len(webpage_uri_part)):
        uri_list_tmp = webpage_uri_part[index]
        line_str = webpage_line_part[index]
        poc_logger.info(f"================={cnt}==================")
        cnt += 1
        for uri_ in uri_list_tmp:
            response_html = common_request(uri_)
            if response_html is None:
                fail_num += 1
                poc_logger.info(f"failed {line_str} webpage uri: "+uri_)
                continue
            poc_logger.info(f"succeed {line_str} webpage uri: "+uri_)
            sanitization_res_html = sanitization_string(response_html)
            if line_str in result_str:
                result_str[line_str] += " " + sanitization_res_html
            else:
                result_str[line_str] = sanitization_res_html

    from __utils.__filter_util import filter_keyword_list_string
    for line_str in result_str:
        html_sanitization_string = result_str[line_str]
        keywords_tmp = (filter_keyword_list_string(iot_library_list, html_sanitization_string))
        result_words[line_str] = keywords_tmp

    poc_logger.info(f"total failed uri num:"+str(fail_num)+"total uri num:"+str(end-start+1))
    save_dict_to_json(result_path, result_words)


if __name__ == "__main__":
    iot_library_list = load_iot_assets_library()
    search_webpage_line, search_webpage_uri = load_uri_log()
    total_number = len(search_webpage_line)

    print(f"The total webpage cnt: {total_number}")
    process_number = 5

    delta = int(total_number / process_number)
    for i in range(process_number):
        start, end = i * delta, (i + 1) * delta - 1
        if end >= total_number:
            end = total_number - 1
        p = Process(target=webpage_concurrent, args=(search_webpage_line, search_webpage_uri, iot_library_list, start, end))
        p.start()

