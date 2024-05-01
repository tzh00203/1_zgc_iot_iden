"""
将sinan的ResponseData进行分类后得到的其它端口信息数据进行资产标记
并将其它端口数据进行分词和词向量筛选处理

:input:  /raw_data/iot_assets_ip.json
:output: /raw_data/train_data/data_unnatural_response.json

"""

# from __utils import __path_util, __sort_util
from _7_generate_util import tokenize
from _3_data_processing._3_data_TFIDF_util import tfidf_calc
from __utils.__path_util import global_path
from __utils.__sort_util import sort_dict
from __utils.__save_file_util import save_dict_to_json, save_str_file, save_list_to_csv
from __utils.__similarity_util import similarity
from __logs.__log import log_init, log_init_reverse_shell
import json
from _3_data_processing._3_data_sanitization import sanitization_string


global_path = global_path
unnatural_path = global_path.__raw_data_path__ + "iot_assets_ip.json"
label_save_path = global_path.__raw_data_path__ + "train_data/data_other_str_response.json"
other_response_bmes4ner_path = global_path.__raw_data_path__ + "train_data/other_response_train.bmes"
other_response_tfidf_path = global_path.__raw_data_path__ + "train_data/other_response_tokens.tfidf"
other_train_path = global_path.__raw_data_path__ + "train_data/other_train.bmes"
other_test_path = global_path.__raw_data_path__ + "train_data/other_test.bmes"


def labeling_extend():
    iot_ip_assets = open(unnatural_path, "r", encoding="utf-8").read()
    iot_ip_dict = eval(iot_ip_assets)

    label_dict = {}
    cnt_ = 1
    for ip_ in iot_ip_dict:

        print(cnt_)
        assets_ = iot_ip_dict[ip_]["assets"]
        if len(assets_) > 1:
            continue
        for id_ in range(len(iot_ip_dict[ip_]["response_data"])):
            if iot_ip_dict[ip_]["src"][id_] != "ori":
                key_string = iot_ip_dict[ip_]["response_data"][id_]
                # key_string = sanitization_string(key_string)
                if key_string == "":
                    continue
                print("\t", key_string)
                label_dict[cnt_] = [ key_string, assets_]
                cnt_ += 1
    save_dict_to_json(label_save_path, label_dict)


def word_embedding():
    other_response = open(label_save_path, "r", encoding="utf-8").read()
    other_response = eval(other_response)
    print(len(other_response))
    corpus = []
    corpus_id = []
    tokens_dict = {}

    for id_ in other_response:
        print(id_)
        str_ = other_response[id_][0]
        tokens = tokenize(str_)
        print("\t", tokens)
        tokens_dict[id_] = tokens

        tokens_str = " ".join(tokens)
        corpus.append(tokens_str)
        corpus_id.append(id_)
    TFIDF_words_dict = tfidf_calc(corpus, corpus_id)
    save_dict_to_json(other_response_tfidf_path, TFIDF_words_dict)

    bmes_ner_list = []
    for id_ in TFIDF_words_dict:
        assets = other_response[id_][1][0]
        key_words = TFIDF_words_dict[id_]
        all_words = tokens_dict[id_]
        print("=======================================")
        print(all_words)
        print(key_words)
        if len(key_words) == 0 or len(all_words) == 0:
            continue
        for word in all_words:
            line_tmp = word
            if word in key_words:
                line_tmp += "\t" + "B-PER"
            else:
                line_tmp += "\tO"
            bmes_ner_list.append(line_tmp)
        bmes_ner_list[-1] += "\n"

    with open(other_response_bmes4ner_path, "w", encoding="utf-8") as ff:
        ff.write("\n".join(bmes_ner_list))


def modify_bmes():
    """
    修改bmes标注格式，并分成train和test两个数据集
    """
    bmes_data = open(other_response_bmes4ner_path, "r", encoding="utf-8").read().replace("\n\n\n", "\n\n")
    bmes_data = bmes_data.split("\n\n")
    bmes_data_ori = []
    bmes_data_new = []
    for sentence in bmes_data:
        bmes_data_ori.append(sentence.split("\n"))

    """[ [ word1 B-PER, word2 B-PER, ... ], ... ]"""
    cnt = 1
    for sentence in bmes_data_ori:
        word_num = len(sentence)
        sentence_new = []
        for id_ in range(word_num):
            word, tag = sentence[id_].split("\t")[0], sentence[id_].split("\t")[1]

            # 首单词处理
            if id_ == 0 and tag != "O":
                if word_num == 1:
                    tag = "S-PER"
                elif word_num > 1:
                    tag_next = sentence[id_+1].split("\t")[1]
                    if tag_next != "O":
                        tag = "B-PER"

            # 末尾单词处理
            elif id_ == word_num-1 and word_num > 1 and tag != "O":
                tag_prev = sentence[id_-1].split("\t")[1]
                if tag_prev != "O":
                    tag = "E-PER"
                else:
                    tag = "S-BER"

            # 中间部分单词处理
            elif word_num > 2 and tag != "O" and 0 < id_ < word_num - 1:
                tag_prev = sentence[id_-1].split("\t")[1]
                tag_next = sentence[id_+1].split("\t")[1]

                if tag_prev != "O" and tag_next != "O":
                    tag = 'M-PER'
                elif tag_prev != "O" and tag_next == "O":
                    tag = 'E-PER'
                elif tag_prev == "O" and tag_next != "O":
                    tag = 'B-PER'
                else:
                    tag = 'S-PER'
            print(cnt,  word, tag)
            cnt += 1
            sentence_new.append(word+"\t"+tag)
        bmes_data_new.append(sentence_new)
    bmes_data_new_train = bmes_data_new[:int(5/6*len(bmes_data_new))]
    bmes_data_new_test = bmes_data_new[int(5/6*len(bmes_data_new)):]

    bmes_str_train, bmes_str_test = [], []
    for sent in bmes_data_new_train:
        str_tmp = "\n".join(sent)
        str_tmp += "\n"
        bmes_str_train.append(str_tmp)
    for sent in bmes_data_new_test:
        str_tmp = "\n".join(sent)
        str_tmp += "\n"
        bmes_str_test.append(str_tmp)
    with open(other_train_path, "w", encoding="utf-8") as ff:
        ff.write("\n".join(bmes_str_train))
    with open(other_test_path, "w", encoding="utf-8") as ff:
        ff.write("\n".join(bmes_str_test))


if __name__ == "__main__":
    # labeling_extend()
    # word_embedding()
    modify_bmes()


