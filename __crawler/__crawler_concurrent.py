"""
并发地通过tfidf筛选出的高频词汇进行bing引擎信息爬虫搜索
"""
from multiprocessing import Process
from __crawler_bing_util import bing_api_search
from __crawler_google_util import google_api_search
from __logs.__log import log_init
from __utils.__path_util import global_path

tfidf_path = global_path.__crawler_tfidf_path__


def load_tfidf():
    """
    加载search_query, 返回关键词及其索引列表=>二维
    :return:
    """
    tfidf_dict = eval(open(tfidf_path, "r", encoding="utf-8").read())
    tfidf_search_query_list = list(tfidf_dict.values())
    tfidf_search_index_list = list(tfidf_dict.keys())
    tfidf_search_words_dict = {}
    for index_ in tfidf_dict:
        words_ = str(tfidf_dict[index_])
        if words_ not in tfidf_search_words_dict:
            tfidf_search_words_dict[words_] = [index_]
        else:
            tfidf_search_words_dict[words_].append(index_)
    tfidf_search_query_list_ = list(tfidf_search_words_dict.keys())
    tfidf_search_index_list_ = list(tfidf_search_words_dict.values())
    return tfidf_search_index_list_, tfidf_search_query_list_


def crawler_concurrent(search_query, search_index, start: int, end: int):
    """
    search_query一部分进行引擎搜索，得到每次搜索前十结果uri_web
    队列算法-FIFO
    [ [search_query_1], [search_query_2], [search_query_3], ... ]
    :param search_query:
    :param search_index:
    :param start: 线程数据index起始
    :param end:   线程数据index末尾+1
    :return:d
    """

    all_data_part = search_query[start: end + 1]
    all_index_part = search_index[start: end + 1]
    logger_path = global_path.__crawler_search_result_path__ + f"search_log/search_uri_{start}_{end}.log"
    poc_logger = log_init(logFilename=logger_path)

    for index in range(len(all_data_part)):
        search_list, line_index = eval(all_data_part[index]), "_".join(all_index_part[index])
        query = " ".join(search_list)
        # query = query.replace(' + ', '%20%2B%20')

        uri_list, title_list = bing_api_search(query)
        if len(uri_list) > 0:
            for uri in uri_list:
                poc_logger.info(f"{line_index} line in sanitization.json :search uri: {uri}")
        else:
            poc_logger.info(f"{line_index} line in sanitization.json google searched no result!")


if __name__ == "__main__":

    search_index_, search_query_ = load_tfidf()
    total_number = len(search_query_)

    print(f"The total bing search cnt: {total_number}")
    process_number = 10
    delta = int(total_number / process_number)
    for i in range(process_number):
        start, end = i * delta, (i + 1) * delta - 1
        if end >= total_number:
            end = total_number - 1
        p = Process(target=bing_api_search, args=(search_query_, search_index_, start, end))
        p.start()
