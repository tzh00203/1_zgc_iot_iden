import openpyxl
import json
from __utils.__filter_util import filter_format_symbol, filter_dictionary_string
from _5_TFIDF_utils import tfidf_calc


class EXPLANATION:
    # TODO 指定协议？ http/rtsp/soap
    """
    思路: 将extend_data中每一个ip的所有端口中的非html/非RTSP标记data全部过滤出来，一个ip输出一个str，这个str由空格作为分隔符
        扫过所有ip后输出一个corpus矩阵，格式为[ ip1的str, ip2的str ... ]
        随后将这个矩阵进行TFIDF计算，得到每一个ip str中权重最高的前几个word，放入一个rules_library文件，根据id_去ori司南数据洗出来的产品信息，给这几个words打上标记，
        对于一个ip的rule格式为： {word1, word2, word3}   ---->   {company, product, category_name}

    注意: 最初的产品信息标记可以来自已有厂商的历史记录数据，在后期就可以通过框架的形式去增量学习，将不断输出的新信息作为新的信息标记依据，达到增量学习的效果
        重合性
    """


extendData_path = "../../real-IoT-device-assets/3_tags4NER/part-00000-89e63ac2-fac5-4f8e-a750-3b4d80e9bac9-c000.json/sinan_iot_assets_extend.json"
product_path = "../../real-IoT-device-assets/1_sinan_response_v3_sinan_ori/1_sinan_assets_v3.xlsx"
corpus_path = "../../real-IoT-device-assets/4_DER_new/DER_corpus"
corpus_id_ip_path = "../../real-IoT-device-assets/4_DER_new/DER_corpus_id_ip"
rules_path = "../../real-IoT-device-assets/4_DER_new/DER_rules"
key_words_num = 5


def read_product():

    product_data = []
    # 打开Excel文件
    workbook = openpyxl.load_workbook(product_path)
    sheet = workbook.active  # 或者使用sheet = workbook['Sheet1']

    for row in sheet.iter_rows(values_only=True):
        # 在这里，row 是一个包含一行数据的元组
        data_tmp = [row[0], row[2], row[4], row[5]]
        product_data.append(data_tmp)

    return product_data


def corpus_init():
    """
    将extend_data的非html数据进行corpus初始化
    :return:
    corpus_example = [
        "What is the weather like today",
        "what is for dinner tonight",
        "this is question worth pondering",
        "it is a beautiful day today"
    ]
    corpus_id_ip = [
        (id1, ip1),
        (id2, ip2),
        ...
    ]
    """
    corpus, corpus_id = [], []
    extendData = open(extendData_path, encoding="utf-8").readlines()
    for each_ip in extendData:
        ip_str_list = []
        json_tmp = json.loads(each_ip)
        # json_pretty = json.dumps(json_tmp, indent=4)
        # print(json_pretty)
        ports_data = json_tmp["ports_data"]
        for port in ports_data:
            if port["html_flag"] == 1 or "<!DOCTYPE html>" in port["data"]:
                continue
            print(json_tmp["ip"]+":"+str(port["port"]))
            # 需要对data字符串过滤掉一些特殊符号/换行符/stop_words等
            clean_str = filter_format_symbol(filter_dictionary_string(port["data"]))
            ip_str_list.append(clean_str)

        ip_str = " ".join(ip_str_list)
        corpus.append(ip_str)
        corpus_id.append((json_tmp['id_'], json_tmp["ip"]))
    f1 = open(corpus_path, "w", encoding="utf-8")
    f1.write(str(corpus))
    f2 = open(corpus_id_ip_path, "w", encoding="utf-8")
    f2.write(str(corpus_id))
    print("------the corpus N corpus_id_ip inited successfully!------")
    return corpus, corpus_id


def TFIDF_calc(corpus, corpus_id_ip):
    """
    corpus_example = [
        "What is the weather like today",
        "what is for dinner tonight",
        "this is question worth pondering",
        "it is a beautiful day today"
    ]
    corpus_id_ip_example = [
        (1, "123.456.456.13),
        (3, "123.456.456.13),
        (4, "123.456.456.13),
        (14, "123.456.456.13),
    ]
    :return: { (ip1_id, ip1): [ip1's key words], (ip2_id, ip2): [ip2's key words], ...}
    """
    return tfidf_calc(corpus, corpus_id_ip)


def rules4DER_setup(words_dict):
    rules = {}
    assets = read_product()
    for (rule_id, rule_ip) in words_dict:
        if not words_dict[(rule_id, rule_ip)]:
            continue
        rules[str(rule_id)] = {
            "rule_ip": rule_ip,
            "rule_words": words_dict[(rule_id, rule_ip)],
            "rule_assets": {
                "vendor": assets[rule_id][1],
                "type": assets[rule_id][2],
                "product": assets[rule_id][3]
            }
        }
    json_str = json.dumps(rules, ensure_ascii=False, indent=4)
    with open(rules_path, 'w', encoding="utf-8") as json_file:
        json_file.write(json_str)
    print("----------Rules set up successfully!----------")


if __name__ == "__main__":
    corpus_, corpus_id_ = corpus_init()

    TFIDF_words_dict = TFIDF_calc(corpus_, corpus_id_)
    rules4DER_setup(TFIDF_words_dict)


