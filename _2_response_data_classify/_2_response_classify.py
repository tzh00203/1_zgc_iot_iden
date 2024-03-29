"""
将不同协议的ResponseData进行基础分类, 期望将人眼可以观察和用于机器交互的数据分离开来
:input:  /sinan_iot_assets.json+/other_ports.json
:output:

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
root_path = global_path.__sinan_cluster_root_path__
sinan_ip_data_path = global_path.__sinan_ori_ip_path__
sinan_ip_extend_data_path = global_path.__sinan_ori_extend_path__
unity_path = global_path.__sinan_ori_unity_path__
sinan_protocol_path = global_path.__sinan_cluster_root_path__ + "protocol_type.json"
root_pattern_path = global_path.__probe_payloads_patterns_root_path__
protocol_list = [
    "general_ftp.txt", "general_http.txt", "general_rtsp.txt", "general_snmp.txt",
    "general_ssh.txt", "general_telnet.txt",
    "IoT_amqp.txt", "IoT_coap.txt", "IoT_ipp.txt", "IoT_mqtt.txt", "IoT_quagga.txt",
    "IoT_stomp.txt", "IoT_xmpp.txt",
    "private_cisco.txt", "private_cisco_application.txt", "private_citrix_apps.txt",
    "private_citrix_ica.txt", "private_citrix_licensing.txt", "private_dahua.txt",
    "private_dji.txt", "private_hikvision.txt", "private_zebra.txt"
]
protocol_patterns_dict = {}
all_data = open(sinan_ip_extend_data_path, "r", encoding="utf-8").readlines()

for line in all_data:
    json_tmp = json.loads(line)
    ip = json_tmp['ip']
    port = json_tmp['port']
    protocol_ori = json_tmp['protocol']
    header = json_tmp['header']
    body = json_tmp['body']
    if protocol_ori == "mqtt":
        print(json_tmp)

#
# def ip_ports_unity():
#     """
#     先把一个ip的所有端口数据整理在同个数据结构中， 存储地址为_2_cluster_result
#     顺便记录protocol的种类以及数量
#     :return:    {   ip1 : [ "data1", "data2", ... ],
#                     ip2 : [ "data1", "data2", ... ],
#                     ...
#                 }
#     """
#     ip_cnt = 0
#     data_unity_dict = {}
#     protocol_type_dict = {}
#
#     f1 = open(sinan_ip_data_path, "r", encoding="utf-8").readlines()
#     f2 = open(sinan_ip_extend_data_path, "r", encoding="utf-8").readlines()
#
#     for line in f1:
#         json_tmp = json.loads(line)
#         if json_tmp["ip"] in data_unity_dict:
#             continue
#         data_unity_dict[json_tmp["ip"]] = [json_tmp["header"] + " " + json_tmp["body"]]
#
#         protocol_tmp = json_tmp["protocol"]
#         if protocol_tmp == "":
#             protocol_tmp = "unknown"
#         if protocol_tmp not in protocol_type_dict:
#             protocol_type_dict[protocol_tmp] = 1
#         else:
#             protocol_type_dict[protocol_tmp] += 1
#         print(f"{json_tmp['ip']} recorded... ")
#         ip_cnt += 1
#     print(f"----------------{ip_cnt} in total----------------")
#
#     for line in f2:
#         json_tmp = json.loads(line)
#         if json_tmp["ip"] in data_unity_dict:
#             data_unity_dict[json_tmp["ip"]].append(json_tmp["header"] + " " + json_tmp["body"])
#             protocol_tmp = json_tmp["protocol"]
#             if protocol_tmp == "":
#                 protocol_tmp = "unknown"
#             if protocol_tmp not in protocol_type_dict:
#                 protocol_type_dict[protocol_tmp] = 1
#             else:
#                 protocol_type_dict[protocol_tmp] += 1
#
#     for ip in data_unity_dict.keys():
#         ports_list_str = str(data_unity_dict[ip])
#         path_tmp = root_path + "ip_ports/" + ip + ".txt"
#         save_str_file(path_tmp, ports_list_str)
#
#     protocol_type_dict = sort_dict(protocol_type_dict)
#     save_dict_to_json(sinan_protocol_path, protocol_type_dict)
#
#
# def load_patterns():
#     """
#     加载probe中的patterns匹配知识
#     :return: {
#         protocol1: [ patterns1, patterns2 ... ]
#     }
#     """
#     patterns_dict = {
#     }
#
#     for protocol_path in protocol_list:
#         try:
#             with open(root_pattern_path+protocol_path, "r", encoding="utf-8") as ff:
#                 dict_tmp = eval(ff.read())
#                 # print(dict_tmp)
#                 patterns_dict[protocol_path.replace(".txt", "")] = dict_tmp['patterns']
#                 #
#         except Exception as e:
#             print(protocol_path, e, "error")
#
#     print("===load _1_probe_patterns success===")
#     return patterns_dict
#
#
# def data_cluster_patterns(pattern_dict_txt, response_str):
#     """
#     根据step _1_response_probe_process 中得到的patterns对sinan_iot_response 进行数据分类
#     输入为单个pattern文件和待匹配的字符串
#     :return:    match_flag(0/1), type, pattern_str
#     """
#     """使用perl匹配 ./_1_response_probe_process/probe_lib/payloads_patterns/"""
#
#     protocol_name = pattern_dict_txt.replace(".txt", "").split("/")[-1]
#     patterns = protocol_patterns_dict[protocol_name]
#     for pattern in patterns:
#         type_ = pattern['type']
#         pattern_str = pattern['pattern']
#
#         """patterns: perl/regex/response_real/response_qax/response/prefix"""
#         if type_ in ["perl", "regex"]:
#             if re.match(pattern_str, response_str):
#                 return 1, type_, pattern_str
#         if type_.startswith("response"):
#             [result_, similarity_value] = similarity(response_str, pattern_str, method="jaro_winkler")
#             if similarity_value > 0.85:
#                 return 1, type_, pattern_str
#         if type_ == "prefix":
#             if response_str.startswith(pattern_str):
#                 return 1, type_, pattern_str
#
#     return 0, "null", "null"
#
#
# def read_qax_response_match(start:int, end:int):
#     """
#     读取sinan_iot_extend数据 对header+body / body分别进行一轮匹配
#     输入: all extend ports
#     输出: cluster_result = [ip, port, ori_protocol, pattern_protocol(unknown/...)]
#     """
#     cluster_result = []
#
#     all_data_part = all_data[start: end+1]
#     cnt_pattern_success = 0
#     logger_path = f"./log_probe_pattern_result/sinan_response_probe_{start}_{end}.log"
#     poc_logger = log_init(logFilename=logger_path)
#     log_id = 0
#     poc_logger.info(f"[+] Read IP({start}_{end}) and use the _1_probe to match ")
#     for line in all_data_part:
#         log_id += 1
#         json_tmp = json.loads(line)
#         ip = json_tmp['ip']
#         port = json_tmp['port']
#         protocol_ori = json_tmp['protocol']
#         header = json_tmp['header']
#         body = json_tmp['body']
#
#         # print(f"======{ip}=======")
#         # print(body)
#         match_record = None
#         probe_pattern_list, probe_type_list = [], []
#         for pattern_ in protocol_list:
#             pro_path = root_pattern_path + pattern_
#             flag, pattern_type, pattern_string = data_cluster_patterns(pro_path, header + body)
#             if flag:
#                 probe_pattern_list.append(pattern_.replace(".txt", ""))
#                 probe_type_list.append(pattern_type)
#                 match_record = [ip, port, protocol_ori, pattern_.replace(".txt", ""), pattern_type]
#
#         match_record = [ip, port, protocol_ori, probe_pattern_list, probe_type_list]
#         if len(probe_pattern_list) > 0:
#             flag = 1
#         else:
#             flag = 0
#         cluster_result.append(match_record)
#
#         print(f" log_id: {log_id}--flag: {flag}--ip: {ip}--ori_pro: {protocol_ori}--probe_pro: {match_record[3]}--{match_record[4]}--{match_record[5]} ")
#         poc_logger.info(f" log_id: {log_id}--flag: {flag}--ip: {ip}--ori_pro: {protocol_ori}--probe_pro: {match_record[3]}--{match_record[4]}--{match_record[5]} ")
#
#         cnt_pattern_success += flag
#     save_list_to_csv(f"./response_probe_protocol_header_body_{start}_{end}.csv", data_list=cluster_result)
#
#
# if __name__ == "__main__":
#
#     import os
#     print(os.getcwd())
#     protocol_patterns_dict = load_patterns()
#
#     total_number = 129084
#     process_number = 2
#     delta = int(total_number / process_number)
#     for i in range(process_number):
#         start, end = i*delta, (i+1)*delta - 1
#         if end >= total_number:
#             end = total_number - 1
#         p = Process(target=read_qax_response_match, args=(start, end))
#         p.start()

