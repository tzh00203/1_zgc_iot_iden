"""
将sinan的ResponseData进行分类
    1.利用probe的patterns协议进行人工分类
    2.将同个主机下的各端口数据进行ip绑定
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
result_path = global_path.__2_response_pattern_result_path__ + "raw_data/"


protocol_list = [
    "general_ftp.txt", "general_http.txt", "general_rtsp.txt", "general_snmp.txt",
    "general_ssh.txt", "general_telnet.txt",
    "IoT_amqp.txt", "IoT_coap.txt", "IoT_ipp.txt", "IoT_mqtt.txt", "IoT_quagga.txt",
    "IoT_stomp.txt", "IoT_xmpp.txt",
    "private_cisco.txt", "private_cisco_application.txt", "private_citrix_apps.txt",
    "private_citrix_ica.txt", "private_citrix_licensing.txt", "private_dahua.txt",
    "private_dji.txt", "private_hikvision.txt", "private_zebra.txt"
]
"""
iot_assets_ip_dict = {  ip1: {  tags, [ {port1, data1} ]   }
                      }
"""
iot_assets_ip_dict, iot_assets_pro_dict = {}, {}

protocol_patterns_dict = {}
ori_data = open(sinan_ip_data_path, "r", encoding="utf-8").readlines()
extend_data = open(sinan_ip_extend_data_path, "r", encoding="utf-8").readlines()

all_data = ori_data + extend_data


def classify_ip():
    print(ori_data[0])
    print(extend_data[0])
    for line in ori_data:
        json_tmp = json.loads(line)
        ip = json_tmp['ip']
        port = json_tmp['port']
        protocol_ori = json_tmp['protocol']
        header = json_tmp['header']
        body = json_tmp['body']
        col = json_tmp["col"]
        res_data = header + body
        if ip not in iot_assets_ip_dict:
            print(ip)
            iot_assets_ip_dict[ip] = {
                "assets": [
                    { "vendor": col["company"], "type": col["second_cat_name"], "product": col["product"] }
                ],
                "ports": [port],
                "src": ['ori'],
                "protocol": [protocol_ori],
                "response_data": [res_data]
            }
            continue
        else:
            if port not in iot_assets_ip_dict[ip]['ports']:
                assets_tmp = { "vendor": col["company"], "type": col["second_cat_name"], "product": col["product"] }
                if assets_tmp not in iot_assets_ip_dict[ip]["assets"]:
                    iot_assets_ip_dict[ip]["assets"].append(
                        assets_tmp
                    )
                iot_assets_ip_dict[ip]["ports"].append(port)
                iot_assets_ip_dict[ip]["src"].append('ori')
                iot_assets_ip_dict[ip]["protocol"].append(protocol_ori)
                iot_assets_ip_dict[ip]["response_data"].append(res_data)
    print(len(iot_assets_ip_dict))
    for line in extend_data:
        json_tmp = json.loads(line)
        ip = json_tmp['ip']
        port = json_tmp['port']
        protocol_ori = json_tmp['protocol']
        header = json_tmp['header']
        body = json_tmp['body']
        res_data = header + body
        if ip in iot_assets_ip_dict:
            if port not in iot_assets_ip_dict[ip]['ports']:

                iot_assets_ip_dict[ip]["ports"].append(port)
                iot_assets_ip_dict[ip]["src"].append('extend')
                iot_assets_ip_dict[ip]["protocol"].append(protocol_ori)
                iot_assets_ip_dict[ip]["response_data"].append(res_data)

    save_dict_to_json(result_path+"iot_assets_ip.json", iot_assets_ip_dict)


def classify_protocol():
    """
        iot_assets_pro_dict = {
            protocol1: [
                            {"ip": ip1, "port": port1, response_data: "data1"},
                            ...
                        ],
            protocol2: [],
            protocol3: [],
            ...
        }
    """
    record_list = []
    for pro in protocol_list:
        iot_assets_pro_dict[pro.replace(".txt", "")] = []
    for line in all_data:
        json_tmp = json.loads(line)
        ip = json_tmp['ip']
        port = json_tmp['port']
        protocol_ori = json_tmp['protocol']
        header = json_tmp['header']
        body = json_tmp['body']
        res_data = header + body
        print(ip)
        if ip + str(port) in record_list:
            continue
        record_list.append(ip+str(port))
        for pro in protocol_list:
            pro_ = pro.replace(".txt", "")
            if pro_.split("_")[-1] in protocol_ori.lower() or protocol_ori.lower() in pro_.split("_")[-1]:
                iot_assets_pro_dict[pro_].append(
                    {
                        "ip": ip,
                        "port": port,
                        "response_data": res_data
                    }
                )
    for ii in iot_assets_pro_dict:
        if not iot_assets_pro_dict[ii]:
            print(ii)
    save_dict_to_json(result_path+"iot_assets_pro.json", iot_assets_pro_dict)


if __name__ == "__main__":
    classify_protocol()



