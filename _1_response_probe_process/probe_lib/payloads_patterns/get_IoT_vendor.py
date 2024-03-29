import json
# sinan_iot_assets_extend_ori.json 和 sinan_iot_assets.json 无交集 是单纯的端口拓展
root_path = "../real-IoT-device-assets/3_tags4NER/part-00000-89e63ac2-fac5-4f8e-a750-3b4d80e9bac9-c000.json/"
sinan_ori_dataset_path = root_path + "sinan_iot_assets.json"
sinan_extend_dataset_path = root_path + "sinan_iot_assets_extend_ori.json"
sinan_extend_dataset = open(sinan_extend_dataset_path, "r", encoding="utf-8").readlines()
sinan_ori_dataset = open(sinan_ori_dataset_path, "r", encoding="utf-8").readlines()

quagga_txt = open("./_1_response_probe_process/probe_lib/payloads_patterns/sinan_quagga.txt", "w", encoding="utf-8")
ipp_txt = open("./_1_response_probe_process/probe_lib/payloads_patterns/sinan_ipp.txt", "w", encoding="utf-8")

quagga_txt = open("./_1_response_probe_process/probe_lib/payloads_patterns/sinan_quagga.txt", "a", encoding="utf-8")
ipp_txt = open("./_1_response_probe_process/probe_lib/payloads_patterns/sinan_ipp.txt", "a", encoding="utf-8")


quagga_json, ipp_json = [{
        "payloads": [],
        "patterns": []
    } for _ in range(2)]
all_protocols = [ "quagga", "ipp" ]


def match_pattern(line):

    import re
    # 正则表达式模式
    pattern = r'm\|(.*?)\||m=(.*?)=|m%(.*?)%|m@(.*?)@'
    matches = re.findall(pattern, line)
    matched_content = None
    # 输出所有匹配的内容
    for match in matches:
        matched_content = next(group for group in match if group)
        # print(matched_content)
    if matched_content:
        return matched_content
    else:
        print(line)


def read_dataset():
 
    for dataset in [sinan_ori_dataset, sinan_extend_dataset]:
        for line in dataset:
            # print(line)
            json_tmp = json.loads(line)
            protocol_each = json_tmp["protocol"]
            if protocol_each == "quagga":
                print(json_tmp)
                print("==========================================")
                quagga_txt.write(str(json_tmp)+"\n")
                pattern_tmp = {
                    "type": "response",
                    "pattern": json_tmp["header"] + json_tmp["body"]
                }
                if pattern_tmp not in quagga_json["patterns"]:
                    quagga_json["patterns"].append(pattern_tmp)
                    
            elif protocol_each == "ipp":
                print(json_tmp)
                print("==========================================")
                ipp_txt.write(str(json_tmp)+"\n")
                pattern_tmp = {
                    "type": "response",
                    "pattern": json_tmp["header"] + json_tmp["body"]
                }
                if pattern_tmp not in ipp_json["patterns"]:
                    ipp_json["patterns"].append(pattern_tmp)

nmap_service_probes_path = "./_1_response_probe_process/probe_lib/nmap-service-probes.txt"
nmap_service_probes = open(nmap_service_probes_path, "r", encoding="utf-8").readlines()
probe_banner = "##############################NEXT PROBE##############################"
def probe_split():
    all_probe = []
    one_probe = []
    for line in nmap_service_probes:
        if probe_banner in line:
            if one_probe is not []:
                all_probe.append(one_probe)
            one_probe = []
            continue
        elif line.startswith("match") or line.startswith("softmatch") or line.startswith("Probe"):
             one_probe.append(line)
    return all_probe

        
def probe_parse(one_probe):

        
    for protocol_type in all_protocols:
        for line in one_probe:
                protocol_json = globals()[f"{protocol_type}_json"]
                if line.startswith(f"match {protocol_type}") or line.startswith(f"softmatch {protocol_type}"):
                        if one_probe[0][:-1] not in protocol_json["payloads"]:
                                protocol_json["payloads"].append(one_probe[0][:-1])
                        pattern_tmp = match_pattern(line)
                        protocol_json["patterns"].append({
                                "type": "perl",
                                "pattern": pattern_tmp
                        })


def save_json(protocol_type):
    import json
    # 打开一个文件 把数据保存为json模式
    root_path_ = "./_1_response_probe_process/"

    clear_file = open(root_path_+f"probe_lib/payloads_patterns/IoT_{protocol_type}.txt", "w")
    file_tmp = open(root_path_+f"probe_lib/payloads_patterns/IoT_{protocol_type}.txt", "a", encoding="utf-8")
    json.dump(globals()[f"{protocol_type}_json"], file_tmp, ensure_ascii=False, indent=4)    

read_dataset()
all_probe = probe_split()
for probe in all_probe:
    probe_parse(probe)
for pro_ in all_protocols:
        save_json(pro_)
