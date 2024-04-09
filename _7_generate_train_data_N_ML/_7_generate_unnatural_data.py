"""
将sinan的ResponseData进行分类后得到的其它端口信息数据进行资产标记

:input:  /raw_data/iot_assets_ip.json
:output: /raw_data/train_data/data_unnatural_response.json

"""

# from __utils import __path_util, __sort_util
from __utils.__path_util import global_path
from __utils.__sort_util import sort_dict
from __utils.__save_file_util import save_dict_to_json, save_str_file, save_list_to_csv
from __utils.__similarity_util import similarity
from __logs.__log import log_init, log_init_reverse_shell
import json
import re
from multiprocessing import Process


global_path = global_path
unnatural_path = global_path.__raw_data_path__ + "iot_assets_ip.json"
label_save_path = global_path.__raw_data_path__ + "train_data/data_unnatural_response.json"


def labeling_extend():
    iot_ip_assets = open(unnatural_path, "r", encoding="utf-8").read()
    iot_ip_dict = eval(iot_ip_assets)

    label_dict = {}
    for ip_ in iot_ip_dict:
        assets_ = iot_ip_dict[ip_]["assets"]
        if len(assets_) > 1:
            print(assets_)
        for id_ in range(len(iot_ip_dict[ip_]["response_data"])):
            if iot_ip_dict[ip_]["src"][id_] != "ori":
                label_dict[iot_ip_dict[ip_]["response_data"][id_]] = assets_

    save_dict_to_json(label_save_path, label_dict)


if __name__ == "__main__":
    labeling_extend()



