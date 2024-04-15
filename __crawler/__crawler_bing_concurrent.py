"""
并发地通过tfidf筛选出的高频词汇进行bing引擎信息爬虫搜索
"""
from __utils.__path_util import global_path
from __utils.__sort_util import sort_dict
from __utils.__save_file_util import save_dict_to_json, save_str_file, save_list_to_csv
from __utils.__similarity_util import similarity
from __logs.__log import log_init, log_init_reverse_shell
from __crawler_bing_util import bing_search
import json
import re
from multiprocessing import Process

tfidf_path = global_path.__crawler_tfidf_path__
search_query, search_index = None, None


def load_tfidf():
    """
    加载search_query, 返回关键词及其索引列表=>二维
    :return:
    """
    tfidf_dict = eval(open(tfidf_path, "r", encoding="utf-8").read())
    tfidf_search_query_list = list(tfidf_dict.values())
    tfidf_search_index_list = list(tfidf_dict.keys())
    print(len(tfidf_search_query_list))
    return tfidf_search_index_list, tfidf_search_query_list


def crawler_concurrent(search_query, search_index, start:int, end:int):
    """
    search_query一部分进行bing引擎搜索，得到每次搜索前十结果uri_web
    [ [search_query_1], [search_query_2], [search_query_3], ... ]
    :param search_query:
    :param search_index:
    :param start: 线程数据index起始
    :param end:   线程数据index末尾+1
    :return:d
    """

    all_data_part = search_query[start: end+1]
    all_index_part = search_index[start: end+1]
    logger_path = global_path.__crawler_search_result_path__ + f"search_log/search_uri_{start}_{end}.log"
    poc_logger = log_init(logFilename=logger_path)

    for index in range(len(all_data_part)):
        search_list, line_index = all_data_part[index], all_index_part[index]
        uri_query = " ".join(search_list)
        uri_list = bing_search(uri_query)
        for uri in uri_list:
            poc_logger.info(f"{line_index} line in sanitization.json :search uri: {uri}")


if __name__ == "__main__":

    search_index_, search_query_ = load_tfidf()
    total_number = len(search_query_)
    process_number = 2
    delta = int(total_number / process_number)
    for i in range(process_number):
        start, end = i*delta, (i+1)*delta - 1
        if end >= total_number:
            end = total_number - 1
        p = Process(target=bing_search, args=(search_query_, search_index_, start, end))
        p.start()



