from configparser import ConfigParser
from common.handler_path import os,conf_path


class Config(ConfigParser):
    # 在创建对象时,直接加载配置文件中得内容

    def __init__(self,conf_file):
        super().__init__()
        self.read(conf_file,encoding='utf-8')

conf = Config(os.path.join(conf_path,'config.ini'))


# if __name__ == '__main__':
#     # conf = ConfigParser()
#     # conf.read(r'D:\pycharm\py35_project\conf\config.ini',encoding='utf-8')
#     # conf = Config(r'D:\pycharm\py35_project\conf\config.ini')
#     name = conf.get("logging", 'name')
#     level = conf.get('logging', 'level')
#     filename = conf.get("logging", 'filename')
#     Terminal_level = conf.get('logging', 'Terminal_level')
#     File_level = conf.get('logging', 'File_level')
#
#     print(name)
#     print(level)
#     print(filename)
#     print(Terminal_level)
#     print(File_level)
