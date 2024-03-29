"""
    Sends network layer protocol packets,
    such as icmp, to a specified ip address to check the host survival status
    Author: tzh00203
    Date: 2023.12.22
"""


import os
import platform
from scapy.all import *


def check_host(ip):
    try:
        if platform.system().lower() == "windows":
            # Windows系统
            ping = os.system(f"ping -n 1 {ip}")
            if ping == 0:
                print(f"{ip} is reachable.")
            else:
                print(f"{ip} is unreachable.")
        else:
            # 非Windows系统，使用scapy发送ICMP包
            ans = sr1(IP(dst=ip)/ICMP(), timeout=2, verbose=0)
            if ans:
                print(f"{ip} is reachable.")
            else:
                print(f"{ip} is unreachable.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


# 指定IP地址
target_ip = "192.168.1.1"  # 这里替换成你想要检测的IP地址

# 执行检测
check_host(target_ip)


