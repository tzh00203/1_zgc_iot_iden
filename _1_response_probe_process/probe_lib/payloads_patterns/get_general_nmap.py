
nmap_service_probes_path = "./_1_response_probe_process/probe_lib/nmap-service-probes.txt"
nmap_service_probes = open(nmap_service_probes_path, "r", encoding="utf-8").readlines()
root_path = "./_1_response_probe_process/"

http_file = open(root_path+"probe_lib/payloads_patterns/general_http.txt", "w")
ssh_file = open(root_path+"probe_lib/payloads_patterns/general_ssh.txt", "w")
snmp_file = open(root_path+"probe_lib/payloads_patterns/general_snmp.txt", "w")
ftp_file = open(root_path+"probe_lib/payloads_patterns/general_ftp.txt", "w")
dns_file = open(root_path+"probe_lib/payloads_patterns/general_dns.txt", "w")
rtsp_file = open(root_path+"probe_lib/payloads_patterns/general_rtsp.txt", "w")
telnet_file = open(root_path+"probe_lib/payloads_patterns/general_telnet.txt", "w")  
probe_banner = "##############################NEXT PROBE##############################"
probe_dict = {}

http_json, dns_json, ftp_json, snmp_json, ssh_json, rtsp_json, telnet_json = [{
        "payloads": [],
        "patterns": []
    } for _ in range(7)]

# : pwd sub1_paper 

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
        
        # get http
        if line.startswith("match http ") or line.startswith("softmatch http "):
                if one_probe[0][:-1] not in http_json["payloads"]:
                        http_json["payloads"].append(one_probe[0][:-1]) 
                pattern_tmp = match_pattern(line)
                http_json["patterns"].append({
                                "type": "perl",
                                "pattern": pattern_tmp
                        })

        # get ssh
        if line.startswith("match ssh ") or line.startswith("softmatch ssh "):
                if one_probe[0][:-1] not in ssh_json["payloads"]:
                        ssh_json["payloads"].append(one_probe[0][:-1]) 
                pattern_tmp = match_pattern(line)
                ssh_json["patterns"].append({
                                "type": "perl",
                                "pattern": pattern_tmp
                        })

        # get snmp
        if line.startswith("match snmp ") or line.startswith("softmatch snmp "):
                if one_probe[0][:-1] not in snmp_json["payloads"]:
                        snmp_json["payloads"].append(one_probe[0][:-1]) 
                pattern_tmp = match_pattern(line)
                snmp_json["patterns"].append({
                                "type": "perl",
                                "pattern": pattern_tmp
                        })
        
        # get ftp
        if line.startswith("match ftp ") or line.startswith("softmatch ftp "):
                if one_probe[0][:-1] not in ftp_json["payloads"]:
                        ftp_json["payloads"].append(one_probe[0][:-1]) 
                pattern_tmp = match_pattern(line)
                ftp_json["patterns"].append({
                                "type": "perl",
                                "pattern": pattern_tmp
                        })

        # get dns
        if line.startswith("match dns ") or line.startswith("softmatch dns "):
                if one_probe[0][:-1] not in dns_json["payloads"]:
                        dns_json["payloads"].append(one_probe[0][:-1]) 
                pattern_tmp = match_pattern(line)
                dns_json["patterns"].append({
                                "type": "perl",
                                "pattern": pattern_tmp
                        })
        # get rtsp
        if line.startswith("match rtsp ") or line.startswith("softmatch rtsp "):
                if one_probe[0][:-1] not in rtsp_json["payloads"]:
                        rtsp_json["payloads"].append(one_probe[0][:-1])
                pattern_tmp = match_pattern(line)
                rtsp_json["patterns"].append({
                                "type": "perl",
                                "pattern": pattern_tmp
                        })
        # get telnet
        if line.startswith("match telnet ") or line.startswith("softmatch telnet "):
                if one_probe[0][:-1] not in telnet_json["payloads"]:
                                        telnet_json["payloads"].append(one_probe[0][:-1])
                pattern_tmp = match_pattern(line)
                telnet_json["patterns"].append({
                                "type": "perl",
                                "pattern": pattern_tmp
                        })

def save_json():
    import json
    # 打开一个文件 把数据保存为json模式
    http_file = open(root_path+"probe_lib/payloads_patterns/general_http.txt", "a", encoding="utf-8")
    json.dump(http_json, http_file, ensure_ascii=False, indent=4)
    ssh_file = open(root_path+"probe_lib/payloads_patterns/general_ssh.txt", "a", encoding="utf-8")
    json.dump(ssh_json, ssh_file, ensure_ascii=False, indent=4)
    snmp_file = open(root_path+"probe_lib/payloads_patterns/general_snmp.txt", "a", encoding="utf-8")
    json.dump(snmp_json, snmp_file, ensure_ascii=False, indent=4)
    ftp_file = open(root_path+"probe_lib/payloads_patterns/general_ftp.txt", "a", encoding="utf-8")
    json.dump(ftp_json, ftp_file, ensure_ascii=False, indent=4)
    dns_file = open(root_path+"probe_lib/payloads_patterns/general_dns.txt", "a", encoding="utf-8")
    json.dump(dns_json, dns_file, ensure_ascii=False, indent=4)
    rtsp_file = open(root_path+"probe_lib/payloads_patterns/general_rtsp.txt", "a", encoding="utf-8")
    json.dump(rtsp_json, rtsp_file, ensure_ascii=False, indent=4)
    telnet_file = open(root_path+"probe_lib/payloads_patterns/general_telnet.txt", "a", encoding="utf-8")
    json.dump(telnet_json, telnet_file, ensure_ascii=False, indent=4)    

all_probe = probe_split()
for probe in all_probe:
    probe_parse(probe)

print(probe_dict)
print(len(probe_dict))
save_json()


