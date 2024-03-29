import shodan
import json

API_KEY = "OuPKGX55GDyJOaWc4al0Z8n2Gu7AwWgQ"
api = shodan.Shodan(API_KEY)
cnt_data = 1000
sinan_iot_assets_path = "../../real-IoT-device-assets/3_tags4NER/part-00000-89e63ac2-fac5-4f8e-a750-3b4d80e9bac9-c000.json/sinan_iot_assets.json"
sinan_iot_assets_extend_path = "../../real-IoT-device-assets/3_tags4NER/part-00000-89e63ac2-fac5-4f8e-a750-3b4d80e9bac9-c000.json/sinan_iot_assets_extend.json"


def shodanRaw2clean(portDict):
    port_result = {
        'port': portDict["port"],
        'data': portDict['data'],
        'domains': portDict['domains'],
        'hostnames': portDict['hostnames'],
        'isp': portDict['isp'],
        'org': portDict['org'],
        'html_flag': 0
    }
    if 'http' in portDict:
        if 'html' in portDict['http']:
            port_result['html_body'] = portDict['http']['html']
            port_result['html_flag'] = 1
    if port_result['data'].startswith("HTTP") or port_result['data'].startswith("RTSP") or port_result['data'].startswith("<?xml version=\"1.0\""):
        port_result['html_flag'] = 1

    return port_result


def getShodan(ip):
    print("\t-------Shodan-------")

    try:
        info = api.host(ip)
        ports_data = info["data"]
        for port in ports_data:
            print(f"\t{ip}:{port['port']}")
        ports_data_filter = [shodanRaw2clean(port) for port in ports_data]
        print("\t--------------------")
        return ports_data_filter
        # return ("""
        #         IP: {}
        #         HOSTNAMES: {}
        #         COUNTRYNAME: {}
        #         PORTS: {}
        #         ORGANIZATION: {}
        #         OPERATINGSYSTEM: {}
        #         """.format(ip, info.get('hostnames'), info.get('country_name'), info.get('ports'), info.get('org'), info.get('os')))
    except shodan.exception.APIError as e:
        print('\tError:' + ' %s\n\t---------------------------------' % e)


def sinanDataExtend():
    # 读取司南基础数据源
    sinan_iot_assets = open(sinan_iot_assets_path, "r", encoding="utf-8").readlines()
    sinan_iot_assets_extend = open(sinan_iot_assets_extend_path, "w", encoding="utf-8")
    sinan_iot_assets_extend_str = ""

    sinan_iot_ip_port_dict = {}
    cnt_tmp, cnt_id = 0, 0  # cnt_tmp记录搜索成功的ip数量， cnt_id记录对应ip序号，和原始数据对齐
    for line in sinan_iot_assets:
        cnt_id += 1
        each_json = json.loads(line)
        print(cnt_tmp+1, each_json)
        ip_tmp, port_tmp = each_json["ip"], str(each_json["port"])

        # 检查这个ip以及端口是否记录过，重复的话则略过
        ele_dict = ip_tmp + ":" + port_tmp
        if ele_dict not in sinan_iot_ip_port_dict:
            sinan_iot_ip_port_dict[ele_dict] = 1
        else:
            print(f"{ele_dict} has been used...")
            continue

        # 获取指定ip所有开放端口信息, 返回一个list，每个元素是一个端口信息字典
        ip_data_list = getShodan(ip_tmp)
        sinan_extend_each = {
            'id_': cnt_id,
            "ip": ip_tmp,
            'ports_data': ip_data_list
        }
        """
        { id_: 1, ip:xxx.xxx.xxx.xxx, [{port: 123, data: "aaaaa", ...}, {}, ...] }
        { id_: 4, ip:xxx.xxx.xxx.xxx, [{port: 123, data: "aaaaa", ...}, {}, ...] }
        ...
        """

        if ip_data_list is None:
            continue

        sinan_iot_assets_extend_str += json.dumps(sinan_extend_each)
        cnt_tmp += 1
        # if cnt_tmp == cnt_data:
        #     break
        sinan_iot_assets_extend_str += "\n"

    sinan_iot_assets_extend.write(sinan_iot_assets_extend_str)


if __name__ == "__main__":
    sinanDataExtend()
