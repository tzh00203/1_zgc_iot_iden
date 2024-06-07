"""
并发地通过搜索引擎爬取到的uri列表获取设备网页信息描述--html格式
1. 加载uri_log文件 数据处理与分析
2. requests_get words对应的 webpage页面信息
3. 将html信息进行字符串处理 使用_3_data_processing中模块 过滤得到关键字词/使用IoT-Assets-Library做字词匹配扩充资产标签
"""
from multiprocessing import Process
from pprint import pprint

from __logs.__log import log_init
from __utils.__path_util import global_path
from __utils.__save_file_util import save_dict_to_json
from __crawler_utils import common_request, crawler_html_filter
from _3_data_processing._3_data_sanitization import sanitization_string


def load_iot_assets_library():
    iot_assets_path =global_path.__assets_library_path__
    vendor_list = open(iot_assets_path + "vendor.csv", "r", encoding="latin-1").readlines()
    type_list = open(iot_assets_path + "type.txt", "r", encoding="utf-8").readlines()

    new_type_list,new_vendor_list = [], []
    for vendor in vendor_list:
        vendor_tmp = vendor.split(",")[-1].strip().lower()
        new_vendor_list.append(vendor_tmp)
    for type_ in type_list:
        type_tmp = type_.strip().lower()
        new_type_list.append(type_tmp)

    return new_type_list, new_vendor_list


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


def webpage_concurrent(webpage_line, webpage_uri, start: int, end: int):
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

    result_str_path = global_path.__crawler_search_result_path__ + f"webpage_log/webpage_sanitization_{start}_{end}.json"
    result_str_path_a = global_path.__crawler_search_result_path__ + f"webpage_log/webpage_asanitization_{start}_{end}.txt"
    _ = open(result_str_path_a, "w", encoding="utf-8")
    sanitization_json = open(result_str_path_a, "a", encoding="utf-8")
    sanitization_json.write("{\n")
    result_str = {}     # 清洗过后的网页html信息

    cnt = 1
    fail_num = 0
    for index in range(len(webpage_uri_part)):
        uri_list_tmp = webpage_uri_part[index][:5]   # 只爬取前5个uri
        line_str = webpage_line_part[index]
        poc_logger.info(f"=============={cnt}=======fail_number:{fail_num}==============")
        cnt += 1
        each_index_uri_flag = 0
        for uri_ in uri_list_tmp:
            response_html = common_request(uri_)
            sanitization_res_html_dict = {
                "uri": uri_,
                "title": "null",
                "web_info": "null"
            }
            if response_html is None:
                poc_logger.info(f"failed {line_str} webpage uri: "+uri_)
            else:
                each_index_uri_flag = 1
                poc_logger.info(f"succeed {line_str} webpage uri: "+uri_)
                sanitization_res_html_dict = crawler_html_filter(uri_, response_html)

            if line_str in result_str:
                result_str[line_str].append(sanitization_res_html_dict)
            else:
                result_str[line_str] = [sanitization_res_html_dict]
        if each_index_uri_flag == 0:
            fail_num += 1
        try:
            sanitization_json.write("\t\"" + line_str + "\": \"" + str(result_str[line_str]) + "\",\n")
        except:
            pass

    save_dict_to_json(result_str_path, result_str)
    poc_logger.info(f"total failed uri num:"+str(fail_num)+"total index_line num:"+str(end-start+1))
    sanitization_json.write("}")


def webpage_keyword_match(vendor_list, type_list, start: int, end: int):
    """
    匹配每一个sanitization中的关键字词信息
    保存到webpage_log/webpage_words_{start}_{end}.json中
    :param vendor_list: iot-assets-library中的vendor名称
    :param type_list: iot-assets-library中的type名称
    :param start:
    :param end:
    """

    from __utils.__filter_util import filter_keyword_list_string
    result_words = {}   # 需要对比library筛选的字词信息
    sanitization_str_path = global_path.__crawler_search_result_path__ + f"webpage_log/webpage_sanitization_{start}_{end}.json"
    sanitization_str_lines = open(sanitization_str_path, "r", encoding="utf-8").readlines()
    result_words_path = global_path.__crawler_search_result_path__ + f"webpage_match_log/webpage_words_{start}_{end}.json"

    for sanitization_str_dict in sanitization_str_lines:
        if ":" not in sanitization_str_dict:
            continue
        dict_tmp = eval( "{" + sanitization_str_dict[:-1] + "}")
        line_index = list(dict_tmp.keys())[0]
        sanitization_str = list(dict_tmp.values())[0]

        keyword_vendor_list_tmp = []
        keyword_type_list_tmp = []
        for word_ in sanitization_str.strip().split():
            if word_ in type_list:
                keyword_type_list_tmp.append(word_)
            if word_ in vendor_list:
                keyword_vendor_list_tmp.append(word_)

        # keywords_tmp = (filter_keyword_list_string(iot_library_list, sanitization_str))
        result_words[line_index] = [keyword_type_list_tmp, keyword_vendor_list_tmp]
    save_dict_to_json(result_words_path, result_words)

    from __utils.__similarity_util import similarity
    result_further_words = {}   # 需要对比library筛选的字词信息

    result_words_path = global_path.__crawler_search_result_path__ + f"webpage_log/webpage_words_{start}_{end}.json"
    result_words_dict = eval(open(result_words_path, "r", encoding="utf-8").read())
    result_further_path = global_path.__crawler_search_result_path__ + f"webpage_log/webpage_words_further_{start}_{end}.json"
    for line_str in result_words_dict:
        words_list_tmp = result_words_dict[line_str]
        for keyword_word in words_list_tmp:
            key_, word_ = keyword_word.split("_")[-1]
            _, value = similarity(word_, key_)
            if value > 0.9 and key_ in word_:
                if line_str in result_further_words:
                    result_further_words[line_str].append(key_+"_"+word_)
                else:
                    result_further_words[line_str] = [ key_+"_"+word_ ]

    save_dict_to_json(result_further_path, result_further_words)


def local_dependency_match(vendor_list, type_list, start: int, end: int):
    """
    使用 vendor-type-product 的依赖关系匹配每一个网页sanitization中的关键字词信息
    保存到webpage_log/webpage_words_{start}_{end}.json中
    :param vendor_list: iot-assets-library中的vendor名称
    :param type_list: iot-assets-library中的type名称
    :param start:
    :param end:
    """
    from __crawler_utils import word_product_re_pattern
    result_words = {}   # 需要对比library筛选的字词信息
    sanitization_str_path = global_path.__crawler_search_result_path__ + f"webpage_log/webpage_sanitization_{start}_{end}.json"
    sanitization_str_lines = open(sanitization_str_path, "r", encoding="utf-8").readlines()
    result_words_path = global_path.__crawler_search_result_path__ + f"webpage_match_log/webpage_words_{start}_{end}.json"

    for sanitization_str_dict in sanitization_str_lines:
        if ":" not in sanitization_str_dict:
            continue
        dict_tmp = eval( "{" + sanitization_str_dict[:-1] + "}")
        line_index = list(dict_tmp.keys())[0]
        sanitization_str = list(dict_tmp.values())[0]

        keyword_tmp = {}

        sanitization_str_words_list_tmp = sanitization_str.strip().split()
        word_index = 0
        while word_index < len(sanitization_str_words_list_tmp):
            word_ = sanitization_str_words_list_tmp[word_index]

            # dependency : vendor_type_product /  vendor_product_type
            # 注意 大于等于2才开始计算
            for flag, iot_list1, iot_list2 in ((1, vendor_list, type_list), (2, type_list, vendor_list)):
                if word_ in iot_list1 and word_index + 1 < len(sanitization_str_words_list_tmp):
                    word_next = sanitization_str_words_list_tmp[word_index+1]
                    word_index += 1
                    if word_next in iot_list2:
                        words_vendor_type = word_ + "(vendor)_" + word_next + "(type)" if flag == 1 else word_ + "(type)_" + word_next + "(vendor)"
                        words_assets_tmp = words_vendor_type
                        if word_index + 1 < len(sanitization_str_words_list_tmp) and word_product_re_pattern(sanitization_str_words_list_tmp[word_index+1]):
                            words_assets_tmp += "_" + sanitization_str_words_list_tmp[word_index+1] + "(product)"
                            word_index += 1
                        if words_assets_tmp not in keyword_tmp:
                            keyword_tmp[words_assets_tmp] = 1
                        else:
                            keyword_tmp[words_assets_tmp] += 1
                    elif word_product_re_pattern(word_next):
                        words_vendor_product = word_ + "(vendor)_" + word_next + "(product)" if flag == 1 else word_ + "(type)_" + word_next + "(product)"
                        words_assets_tmp = words_vendor_product
                        if word_index + 1 < len(sanitization_str_words_list_tmp) and sanitization_str_words_list_tmp[word_index+1] in iot_list2:
                            words_assets_tmp += "_" + sanitization_str_words_list_tmp[word_index+1] + "(type)" if flag == 1 else "_" + sanitization_str_words_list_tmp[word_index+1] + "(vendor)"
                            word_index += 1
                        if words_assets_tmp not in keyword_tmp:
                            keyword_tmp[words_assets_tmp] = 1
                        else:
                            keyword_tmp[words_assets_tmp] += 1
                word_index += 1

        # keywords_tmp = (filter_keyword_list_string(iot_library_list, sanitization_str))
        keyword_tmp = dict(sorted(keyword_tmp.items(), key=lambda item: item[1], reverse=True))
        result_words[line_index] = keyword_tmp
        pprint(line_index)
        pprint(keyword_tmp)


if __name__ == "__main__":
    type_list, vendor_list = load_iot_assets_library()
    search_webpage_line, search_webpage_uri = load_uri_log()
    total_number = len(search_webpage_line)

    print(f"The total webpage cnt: {total_number}")
    process_number = 10

    delta = int(total_number / process_number)
    for i in range(process_number):
        start, end = i * delta, (i + 1) * delta - 1
        if end >= total_number:
            end = total_number - 1
        p = Process(target=webpage_concurrent, args=(search_webpage_line, search_webpage_uri, start, end))
        p.start()

