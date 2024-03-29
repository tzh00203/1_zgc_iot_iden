# -*- coding: UTF-8 -*-
import re
from importlib import reload

import commands
import sys
reload(sys)
sys.setdefaultencoding('utf8')

# 执行命令
state, stdout = commands.getstatusoutput("masscan 指定ip -p22 --rate 10000")
# 获取命令结果
msgArr = []
discvArr = stdout.split("\n")
for discv in discvArr:
    msgArr.append("".join(discv.encode("ascii")).strip().strip("\n"))

set_addr = set()
set_ip = set()
addr = ""
for msg in msgArr[3:]:
    if "Discovered" in msg:
        discvArr = msg.split(" on ")
        ip = discvArr[1]  # 截取ip地址
        port = re.findall(".*port(.*)/tcp.*", info)  # 取出端口号
        addr = ip.strip() + ":" + str(port).strip()
        addr = addr.replace('[\' ', '').replace('\']', '').replace('[', '').replace(']', '')

        set_addr.add(addr)  # 保存扫描出的ip地址端口号
        set_ip.add(ip)  # 保存ip地址

for ip in set_ip:
    print(ip)
