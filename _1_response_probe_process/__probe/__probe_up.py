# -*- coding: UTF-8 -*-
"""
    可以使用的主机存活探测方法：
        1. nmap -sP ip_address
        2. masscan/Zmap
        3. ping ( 仅限于icmp探测， 部分主机过滤icmp包）

"""

from __logs.__log import log_init

global up_logger


def probe_init(hostname):
    global up_logger
    up_logger = log_init(f"./probe_detect_{hostname}.log")

probe_init("sasa")
up_logger.info("it is a test")

#
# def probe_up_nmap(hostname):
#     """
#     Use the "nmap -sP" command to detect the targetIP up OR down
#     :param hostname:
#     :return: result_up: True or False
#     """
#     result_up: bool
#
#     cmd = "nmap -sP "
#
#     cmd_result = nmap_command(nmap_cmd)
#     if "Host is up" in cmd_result:
#         result_up = True
#         up_logger.info(f"Probe step1_UpDetect: {ip} is UP")
#     else:
#         result_up = False
#         up_logger.info(f"Probe step1_UpDetect: {ip} is DOWN")
#
#     return result_up
