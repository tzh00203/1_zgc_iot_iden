# from __utils import __path_util, __sort_util
from __utils.__path_util import global_path
from __utils.__sort_util import sort_dict
from __utils.__save_file_util import save_dict_to_json, save_str_file, save_list_to_csv
from __utils.__similarity_util import similarity
from __utils.__unicode_util import unicode_calc_proportion
from __logs.__log import log_init, log_init_reverse_shell
import json
import re
from multiprocessing import Process

global_path = global_path
root_path = global_path.__2_response_pattern_result_path__


def load_all_response():
    data_path = root_path + "raw_data/iot_assets_ip.json"
    all_response_dict = eval(open(data_path, "r", encoding="utf-8").read())
    all_ = {"all_response": []}
    for ip in all_response_dict:
        print(ip)
        for data_ in all_response_dict[ip]['response_data']:
            all_['all_response'].append(data_)

    save_dict_to_json(root_path + "raw_data/all_response.json", all_)


# -*- coding:utf-8 -*-
import numpy as np
from matplotlib import pyplot


def data_embedding():
    """
    四维：[ 空格数量 换行数量 u占比 字符串长度 ]
    :return:
    """
    embedding_dict = {}
    embedding_data_list = []
    all_response = eval(open(root_path + "raw_data/all_response.json", "r", encoding="utf-8").read())
    cnt = 0
    for line in all_response["all_response"]:
        if line == "":
            continue
        cnt += 1
        print(cnt)

        # 计算字符串各特征值
        space_count = line.count(" ")
        line_count = line.count("\r\n")
        uu_pro = unicode_calc_proportion(line)
        str_len = len(line)

        flag = 1
        if uu_pro > 0.2:
            flag = 0
        embedding_dict[f"{cnt} {space_count} {uu_pro} {str_len}"] = {
            "flag": flag,
            "response_data": line
        }
        embedding_data_list.append(
            [space_count, line_count, uu_pro, str_len, line]
        )
    # save_dict_to_json(root_path + "raw_data/all_response_dichotomy_v1.json", embedding_dict)
    return embedding_data_list


class K_Means(object):
    # k是分组数；tolerance‘中心点误差’；max_iter是迭代次数
    def __init__(self, response, k=2, tolerance=0.0001, max_iter=300):
        self.clf_ = {}
        self.centers_ = {}
        self.k_ = k
        self.tolerance_ = tolerance
        self.max_iter_ = max_iter
        self.result_clf_list = []
        self.response_data = response


    def fit(self, data):
        self.centers_ = {}
        for i in range(self.k_):
            self.centers_[i] = data[i]

        for i_ in range(self.max_iter_):
            self.clf_ = {}
            self.result_clf_list = []
            for i in range(self.k_):
                self.clf_[i] = []
            # print("质点:",self.centers_)
            for feature in data:
                # distances = [np.linalg.norm(feature-self.centers[center]) for center in self.centers]
                distances = []
                for center in self.centers_:
                    # 欧拉距离
                    # np.sqrt(np.sum((features-self.centers_[center])**2))
                    distances.append(np.linalg.norm(feature - self.centers_[center]))
                classification = distances.index(min(distances))
                self.clf_[classification].append(feature)
                self.result_clf_list.append(classification)

            # print("分组情况:",self.clf_)
            prev_centers = dict(self.centers_)
            for c in self.clf_:
                self.centers_[c] = np.average(self.clf_[c], axis=0)

            # '中心点'是否在误差范围
            optimized = True
            for center in self.centers_:
                org_centers = prev_centers[center]
                cur_centers = self.centers_[center]

                if np.sum((cur_centers - org_centers) / org_centers * 100.0) > self.tolerance_:
                    optimized = False
            if optimized:
                print("Number of iterations: ", i_)
                break

    def predict(self, p_data):
        distances = [np.linalg.norm(p_data - self.centers_[center]) for center in self.centers_]
        index = distances.index(min(distances))
        return index

    def save_result(self):
        embedding_dict_ = {
            "natural language": [],
            "unnatural language": []
        }
        for id_ in range(len(self.response_data)):
            if self.result_clf_list[id_] == 1:
                embedding_dict_["natural language"].append(self.response_data[id_])
            else:
                embedding_dict_["unnatural language"].append(self.response_data[id_])

        save_dict_to_json(root_path + "raw_data/all_response_dichotomy_v2.json", embedding_dict_)


def calc():
    """[ [space_count, line_count, uu_pro, str_len, line] ... ]"""
    xx = data_embedding()
    x = []
    response = []
    for ll in xx:
        x.append([ ll[0] + 1, ll[1] + 1, ll[2], ll[3] ])
        response.append(ll[-1])
    x = np.array(x)
    k_means = K_Means(response=response, k=2)
    k_means.fit(x)
    k_means.save_result()
    print(k_means.centers_)
    print(len(k_means.result_clf_list), len(xx))



    # for center in k_means.centers_:
    #     pyplot.scatter(k_means.centers_[center][0], k_means.centers_[center][1], marker='*', s=150)

    # for cat in k_means.clf_:
    #     for point in k_means.clf_[cat]:
    #         pyplot.scatter(point[0], point[1], c=('r' if cat == 0 else 'b'))

    # predict = [[1, 1, 1, 1]]
    # for feature in predict:
    #     cat = k_means.predict(predict)
    #     pyplot.scatter(feature[0], feature[1], c=('r' if cat == 0 else 'b'), marker='x')
    #
    # pyplot.show()


if __name__ == "__main__":
    calc()
