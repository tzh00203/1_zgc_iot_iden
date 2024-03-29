
nmap_service_probes_path = "./_1_response_probe_process/probe_lib/nmap-service-probes.txt"
nmap_service_probes = open(nmap_service_probes_path, "r", encoding="utf-8").readlines()
root_path = "./_1_response_probe_process/"

probe_banner = "##############################NEXT PROBE##############################"
probe_dict = {}

coap_json, xmpp_json, mqtt_json, amqp_json, stomp_json= [{
        "payloads": [],
        "patterns": []
    } for _ in range(5)]
all_protocols = [ "coap", "xmpp", "mqtt", "amqp", "stomp"]


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

    for line in one_probe:
        if line.startswith("Probe"):
                # print(line, end="")
                if line.split()[1] not in probe_dict:
                    # probe_dict[line.split()[1]] = 1
                    probe_dict[line] = 1

        
    for protocol_type in all_protocols:
        for line in one_probe:
                protocol_json = globals()[f"{protocol_type}_json"]
                if line.startswith(f"match {protocol_type} ") or line.startswith(f"softmatch {protocol_type} "):
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
    clear_file = open(root_path+f"probe_lib/payloads_patterns/IoT_{protocol_type}.txt", "w")
    file_tmp = open(root_path+f"probe_lib/payloads_patterns/IoT_{protocol_type}.txt", "a", encoding="utf-8")
    json.dump(globals()[f"{protocol_type}_json"], file_tmp, ensure_ascii=False, indent=4)    



all_probe = probe_split()
for probe in all_probe:
    probe_parse(probe)

print(probe_dict)
print(len(probe_dict))
for pro_ in all_protocols:
        save_json(pro_)


