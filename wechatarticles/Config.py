# encoding=utf-8
import os
import json

class ConfigCls:
    def __init__(self):
        self.global_wd = None
        self.conf = {}
        self.__read_json()

    def __read_json(self):
        path = os.path.abspath('.')
        path = os.path.join(path, 'config.json')
        print("全局配置文件路径{}".format(path))
        if not os.path.exists(path):
            return
        with open(path, 'r') as f:
            self.conf = json.load(f)
        print("配置:{}".format(self.conf))

    def set_global_wd(self, wd):
        self.global_wd = wd

    def get_global_wd(self):
        if self.global_wd is None:
            raise Exception("全局窗口为空")
        return self.global_wd

    def get_conf(self, name):
        return self.conf[name]

    def get_version(self):
        return '20200710'


GlobalConfig = ConfigCls()
print(GlobalConfig.get_conf('wkpdfpath'))
