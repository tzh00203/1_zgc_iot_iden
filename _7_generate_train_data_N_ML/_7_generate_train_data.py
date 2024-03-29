import os
import time

import openpyxl
import re
import pandas as pd
import csv
from __utils.__similarity_util import similarity
from __utils.__filter_util import filter_dictionary_list, filter_chinese, filter_non_ascii

tag_data_path = "../../real-IoT-device-assets/1_host_data_product_v1.xlsx"
tag_dict_path = "../_4_DER/tags_dict_v1.txt"
train_ori_path = "../../real-IoT-device-assets/2_clean_html_v1"
train_data_v1_path = './_4_DER/train_data_v1'
train_data_id_v1_path = "./_4_DER/train_data_id_v1.csv"
train_data_v2_path = './_4_DER/train_data_v2'

train_word_list = []
train_word_id_list = []
data_MAX, cnt = 2297767, 1
tags_dict = eval(open(tag_dict_path, "r", encoding="utf-8").read().lower())


def clean_further(html: str):
    filter_sign = ["\n", "=", "?", ";", "→", "(", ")", "/", "\\", "\'", "\"", ":", "—", "|", "[", "]", "*", "$", "{", "}", "#"
                   , "&"]
    try:
        for sign in filter_sign:
            html = html.replace(sign, " ")
        html = html.replace(",", " , ").replace(".", " . ")

        html = filter_chinese(html)  # 过滤掉中文字符
        html = filter_non_ascii(html)
        html = html.lower()
        html = re.sub(r'-+', '-', html)  # 多个-缩为一个
        html = re.sub(r'\s+', ' ', html)  # 多个空格缩为一个
        return html
    except:
        return None


# TODO : ADD vendor and type
def read_tags(tag_path=tag_data_path):
    # tag_dict_ori
    tags = {}
    if not os.path.exists("../_4_DER/tags_dict_v1_backup.txt"):
        # 打开Excel文件
        workbook = openpyxl.load_workbook(tag_path)
        sheet = workbook.active  # 或者使用sheet = workbook['Sheet1']
        tag_flag = 0
        for row in sheet.iter_rows(values_only=True):
            # 跳过第一行
            if tag_flag == 0:
                tag_flag += 1
                continue

            # 在这里，row 是一个包含一行数据的元组
            try:
                tags_tmp = eval(row[0])
                for tag in tags_tmp:
                    if tag in tags:
                        tags[tag] += 1
                    else:
                        tags[tag] = 1
            except Exception as e:
                pass
        tags["HUAWEI-S5700"] += 9
    else:
        tags = eval(open("../_4_DER/tags_dict_v1_backup.txt", "r", encoding="utf-8").read().lower())

    print(tags)
    print(len(tags))
    # tag_dict_v1
    tags_dict_clean_v1 = tags
    # tags_dict_clean_v1 = {}
    # clean_list = ["公司产品", "产品"]
    # for key, value in tags.items():
    #     if clean_list[0] in key or clean_list[1] in key:
    #         tags_dict_clean_v1[key.replace(clean_list[0], "").replace(clean_list[1], "")] = value
    #         continue
    #     tags_dict_clean_v1[key] = value

    # tag_dict_v2
    tags_dict_clean_v2 = {}
    for key, value in tags_dict_clean_v1.items():
        key_tmp = key.lower()
        tags_dict_clean_v2[key_tmp] = value if key_tmp not in tags_dict_clean_v2 else (
                tags_dict_clean_v2[key_tmp] + value)
        if "-" in key:
            for wd in key.split("-"):
                key_tmp = wd.lower()
                if wd == "" or wd == " ":
                    continue
                else:
                    tags_dict_clean_v2[key_tmp] = value if key_tmp not in tags_dict_clean_v2 else (
                            tags_dict_clean_v2[key_tmp] + value)

    with open(tag_dict_path, "w", encoding="utf-8") as f:
        f.write(str(tags_dict_clean_v2))
    print(tags_dict_clean_v2)
    print(len(tags_dict_clean_v2))
    return tags_dict_clean_v2


def save_train_step_1():
    file1, file2 = open(train_data_v1_path, 'w'), open(train_data_id_v1_path, 'w', newline='')
    writer2 = csv.writer(file2, delimiter='\t')
    writer2.writerow(['ID'])  # 写入表头
    file1.write("\n".join(train_word_list))
    for index in range(len(train_word_id_list)):
        try:
            writer2.writerow([train_word_id_list[index]])
        except:
            pass


# split the whole sentence into col_list
def gen_train_step_1():
    global train_word_id_list, train_word_list
    global cnt
    for root, dirs, files in os.walk(train_ori_path):
        for file in files:
            # TODO: hold the count
            if cnt >= data_MAX:
                save_train_step_1()
                return

            print("--------", file, "--------")
            # 输出文件的完整路径
            xlsx_file_path = os.path.join(root, file)
            train_word_list_tmp = []
            # 打开Excel文件

            df = pd.read_excel(xlsx_file_path, header=None, )
            # 获取第二行数据
            second_row = df.iloc[1]
            id_tmp = file.replace(".xlsx", "")
            html_data_tmp = second_row[2]

            html_data_tmp = clean_further(html_data_tmp)
            if html_data_tmp is None:
                continue
            html_data_list_tmp = html_data_tmp.split(" ")
            # TODO: filter the common dictionary words
            html_data_list_tmp = filter_dictionary_list(html_data_list_tmp)

            # TODO: tag each word
            html_data_list_tmp = gen_train_step_2(html_data_list_tmp)
            train_word_list = train_word_list + html_data_list_tmp
            train_word_id_list += [id_tmp] * len(html_data_list_tmp)

    save_train_step_1()


# tagging each word
def gen_train_step_2(ori_list):
    #  ["word    tag", ...]
    tag_result = []
    tag_flag = 0
    global cnt
    for word in ori_list:
        if word in [" ", "-", "."] or word is None:
            continue
        tag_ = "O"
        if word == ",":
            tag_ = "O"

        else:
            for tag in tags_dict.keys():
                #  method: [edit, hamming(n), leven, jaro(y), jaro_winkler, lcs, dice(y), wordnet, cos]
                log, sim_value = similarity(word, tag, "jaro")
                if sim_value > 0.9:
                    print("\t" + log)
                    if tag_flag == 1:
                        tag_ = "I-LOC"
                    else:
                        tag_ = "B-LOC"
                    break

        word = '\t'.join([word, tag_])
        tag_flag = 0 if tag_ == "O" else 1
        tag_result.append(word)

        print(cnt, word)
        cnt += 1
    return tag_result


if __name__ == "__main__":
    # read_tags()
    time_start = time.time()
    gen_train_step_1()
    print("running the _3_generate_train_data has cost: ", time.time() - time_start)
