# encoding=utf-8
class ConfigCls:
    def __init__(self):
        self.global_wd = None
    def set_global_wd(self, wd):
        self.global_wd = wd
    def get_global_wd(self):
        if self.global_wd is None:
            raise Exception("全局窗口为空")
        return self.global_wd


GlobalConfig = ConfigCls()
