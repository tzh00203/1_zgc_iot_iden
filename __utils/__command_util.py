import os
import subprocess
from subprocess import PIPE
from func_timeout import func_set_timeout
import func_timeout


def nc_command(port, filename, time_):
    cmd = f"timeout {time_} nc -lvp {port} > {filename}"
    subprocess.run(cmd, shell=True, stdout=PIPE, stderr=PIPE)


@func_set_timeout(1) # 设定函数超执行时间
def nmap_command_limit(command):

    result = subprocess.run(command, shell=True, stdout=PIPE, stderr=PIPE)
    # 检查命令的执行结果
    if result.returncode == 0:
        result_str = result.stdout.decode()
        return result_str
    else:
        result_str = "failed"
        return result_str
   
    
    
def nmap_command(command):
    try:
        result = nmap_command_limit(command)
        return result
    except func_timeout.exceptions.FunctionTimedOut as e:
        return "failed"
    
def common_command(command):
    result = subprocess.run(command, shell=True, stdout=PIPE, stderr=PIPE)
    # 检查命令的执行结果
    if result.returncode == 0:
        result_str = result.stdout.decode()
        return result_str
    else:
        result_str = "failed"
        return result_str