# -*-coding:utf-8-*-

import logging


def log_init(logFilename: str):

    logging.basicConfig(
            level=logging.DEBUG,  # 定义输出到文件的log级别，大于此级别的都被输出
            format='%(asctime)s  [%(filename)s: %(lineno)d] : %(levelname)s  \t%(message)s',  # 定义输出log的格式
            datefmt='%Y-%m-%d %A %H:%M:%S',  # 时间
            filename=logFilename,  # log文件名
            filemode='a')  # 写入模式“w”或“a”
    # Define a Handler and set a format which output to console
    console = logging.StreamHandler()  # 定义console handler
    console.setLevel(logging.DEBUG)  # 定义该handler级别
    formatter = logging.Formatter('%(asctime)s  [%(filename)s: %(lineno)d] : %(levelname)s  \t%(message)s')  # 定义该handler格式
    console.setFormatter(formatter)
    # Create an instance
    logging.getLogger().addHandler(console)  # 实例化添加handler

    poc_logger = logging.getLogger()

    return poc_logger


def log_init_reverse_shell(start:int, end:int):
    logFilename = f'logging_reverse_shell_{start}_{end}.log'

    logging.basicConfig(
            level=logging.DEBUG,  # 定义输出到文件的log级别，大于此级别的都被输出
            format='%(asctime)s  [%(filename)s: %(lineno)d] : %(levelname)s  \t%(message)s',  # 定义输出log的格式
            datefmt='%Y-%m-%d %A %H:%M:%S',  # 时间
            filename=logFilename,  # log文件名
            filemode='a')  # 写入模式“w”或“a”
    # Define a Handler and set a format which output to console
    console = logging.StreamHandler()  # 定义console handler
    console.setLevel(logging.DEBUG)  # 定义该handler级别
    formatter = logging.Formatter('%(asctime)s  [%(filename)s: %(lineno)d] : %(levelname)s  \t%(message)s')  # 定义该handler格式
    console.setFormatter(formatter)
    # Create an instance
    logging.getLogger().addHandler(console)  # 实例化添加handler

    poc_logger = logging.getLogger()

    return poc_logger


def log_init_dnslog(start:int, end:int):
    logFilename = f'./logging_dnslog/logging_dnslog_{start}_{end}.log'
    with open (logFilename, "w", encoding="utf-8") as f:
        pass
    
    logging.basicConfig(
            level=logging.DEBUG,  # 定义输出到文件的log级别，大于此级别的都被输出
            format='%(asctime)s  [%(filename)s: %(lineno)d] : %(levelname)s  \t%(message)s',  # 定义输出log的格式
            datefmt='%Y-%m-%d %A %H:%M:%S',  # 时间
            filename=logFilename,  # log文件名
            filemode='a')  # 写入模式“w”或“a”
    # Define a Handler and set a format which output to console
    console = logging.StreamHandler()  # 定义console handler
    console.setLevel(logging.DEBUG)  # 定义该handler级别
    formatter = logging.Formatter('%(asctime)s  [%(filename)s: %(lineno)d] : %(levelname)s  \t%(message)s')  # 定义该handler格式
    console.setFormatter(formatter)
    # Create an instance
    logging.getLogger().addHandler(console)  # 实例化添加handler

    poc_logger = logging.getLogger()

    return poc_logger


def log_out_test():
    
    # Print information              # 输出日志级别
    logging.debug('logger debug message')
    logging.info('logger info message')
    logging.warning('logger warning message')
    logging.error('logger error message')
    logging.critical('logger critical message')


if __name__ == "__main__":
    log_out_test()
