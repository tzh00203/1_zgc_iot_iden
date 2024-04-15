import openpyxl
import json
from __utils.__save_file_util import save_dict_to_json
from _3_data_TFIDF_util import tfidf_calc
from __utils.__path_util import global_path


class EXPLANATION:
    """
    思路: 将raw_data_sanitization中str提取出来, 由空格作为分隔符
        扫过后输出一个corpus矩阵，格式为[ id1的str, id2的str ... ]
        随后将这个矩阵进行TFIDF计算，得到每一个id str中权重最高的前几个word，放入_3_TFIDF文件，作为后续爬虫的search query
        {word1, word2, word3}

    注意: 最初的产品信息标记可以来自已有厂商的历史记录数据，在后期就可以通过框架的形式去增量学习，将不断输出的新信息作为新的信息标记依据，达到增量学习的效果
        重合性
    """


raw_data_path = global_path.__raw_data_path__ + "all_response_sanitization_v2.json"
corpus_path = global_path.__raw_data_path__ + "/crawler_corpus/all_response_corpus_v2.json"
tfidf_path = global_path.__raw_data_path__ + "/crawler_corpus/all_response_tfidf_v2.json"
key_words_num = 7


def corpus_init():
    """
    将raw_data_sanitization进行corpus初始化
    :return:
    corpus_example = [
        "What is the weather like today",
        "what is for dinner tonight",
        "this is question worth pondering",
        "it is a beautiful day today"
    ]
    注意 id 对应的是 raw_data_sanitizaiton中的行号，用来保存找到在生成search query之前其原response data
    corpus_id = [
        id1,
        id2,
        ...
    ]
    """
    corpus, corpus_id, corpus_dict = [], [], {}
    data_sanitization_dict = eval(open(raw_data_path, "r", encoding="utf-8").read())
    for id_ in range(len(data_sanitization_dict["sanitization_data"])):
        line = data_sanitization_dict["sanitization_data"][id_]
        if line != "":
            corpus.append(line)
            corpus_id.append(id_+3)
            corpus_dict[id_+3] = line
    save_dict_to_json(corpus_path, corpus_dict)
    print("------the corpus N corpus_id inited successfully!------")
    return corpus, corpus_id


def TFIDF_calc(corpus, corpus_id):
    """
    corpus_example = [
        "What is the weather like today",
        "what is for dinner tonight",
        "this is question worth pondering",
        "it is a beautiful day today"
    ]
    corpus_id_example = [
        1,
        2,
        3,
        4
    ]
    :return: { (id1: [ip1's key words], id2: [ip2's key words], ...}
    """
    return tfidf_calc(corpus, corpus_id)


def search_query_4crawler_setup(words_dict):

    """{ id1: [ip1's key words], id2: [ip2's key words], ...}"""

    save_dict_to_json(tfidf_path, words_dict)
    print("----------search_query set up successfully!----------")


if __name__ == "__main__":
    corpus_, corpus_id_ = corpus_init()
    TFIDF_words_dict = TFIDF_calc(corpus_, corpus_id_)
    search_query_4crawler_setup(TFIDF_words_dict)

