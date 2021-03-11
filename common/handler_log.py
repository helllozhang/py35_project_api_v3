import logging
from common.handler_conf import conf
from common.handler_path import os, log_path


def create_log(name='111.log', level='DEBUG', filename='log.log', Terminal_level ='DEBUG', File_level='DEBUG'):
    # 创日志收集器
    log = logging.getLogger(name)
    # 设置日志收集器日志收集等级
    log.setLevel(level)
    # 创建输出渠道
    # 1.输出到控制台
    Terminal_log = logging.StreamHandler()
    Terminal_log.setLevel(Terminal_level)
    log.addHandler(Terminal_log)
    # 2.输出到日志文件
    File_log = logging.FileHandler(filename, encoding='utf-8', mode='w')
    File_log.setLevel(File_level)
    File_log.addFilter(log)
    log.addHandler(File_log)

    # 设置日志输出得格式
    log_formate = logging.Formatter('%(asctime)s - [%(filename)s-->line:%(lineno)d] - %(levelname)s: %(message)s')
    # 设置输出到控制台日志格式
    Terminal_log.setFormatter(log_formate)

    # 设置输出到文件得日志格式
    File_log.setFormatter(log_formate)

    return log


log = create_log(name=conf.get('logging', 'name'),
                 level=conf.get('logging', 'level'),
                 filename=os.path.join(log_path, conf.get('logging', 'filename')),
                 Terminal_level=conf.get('logging', 'Terminal_level'),
                 File_level=conf.get('logging', 'File_level'))


log.info('ahsfkdhshf')
