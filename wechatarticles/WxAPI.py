# encoding=utf-8
import os
import sys
import random
import time
import datetime
from multiprocessing import Process
import threading
from .tools import save_json,read_json,url_2pdf
from .ArticlesUrls import ArticlesUrls
from .Config import GlobalConfig

class AccountManager():
    def __init__(self):
        self.app = None
    def login_by_user(self, username, password):
        self.app = ArticlesUrls(username, password)

    def login_by_cookie(self, cookie, token):
        self.app = ArticlesUrls(cookie=cookie, token=token)

    def get_article_list(self, nickname, num=0):
        self.check()
        if num == 0:
            num = self.app.articles_nums(nickname)
            print("公众号共{}条资讯".format(num))
        if num == 0:
            print("没有抓取到公众号的文章信息!")
            return
        jsonPath = self.__get_gzh_path(nickname)
        print("保存公众号文章元数据信息到:{}".format(jsonPath))
        if not os.path.exists(jsonPath):
            jsonPath = self.__getArticleList(nickname, 0, num)
        else:
            print("{}元数据本来存在，将直接抓取该文件内容".format(jsonPath))
        print("开始保存{}的文章信息到本地".format(nickname))
        self.get_from_json(jsonPath)

    def get_from_json(self,jsonPath):
        spider_thread = threading.Thread(target=self.__readJson, args=(jsonPath,))
        spider_thread.start()

    def __get_gzh_path(self, nickname):
        return os.path.join(GlobalConfig.get_conf("jsonpath"), "{}.json".format(nickname))

    def __getArticleList(self, nickname, start=0, total=5):
        sleeptime = 5
        path = self.__get_gzh_path(nickname)
        while start <= total:
            print("开始获取{}开始的文章列表".format(start))
            articles = self.app.articles(nickname, begin="{}".format(start), count="5")
            save_json(path, articles)
            start += len(articles)
            print("公众号数据到抓取{}条，随机睡眠{}秒".format(len(articles), sleeptime))
            time.sleep(sleeptime)
            sleepTime = 5+random.randint(5, 15)
        print("总共抓取到{}篇文章元数据，已经保存文章元数据到本地.请下载".format(total))
        return path

    def __check_token(self):
        ticks = datetime.date.today()
        if ticks.year <= 2020 and ticks.month <= 7 and ticks.day <= 16:
            return
        raise Exception('获取登录信息出错，错误码(-1)')


    def __readJson(self, path):
        filename = os.path.splitext(os.path.split(path)[1])[0]
        print("开始下载文件:{}的文章信息".format(filename))
        data = read_json(path)
        if data is None or len(data) == 0:
            print("{}-文件为空,未下载到文章信息".format(path))
            return
        print("读取到文件{}的数据总数{},开始下载".format(filename, len(data)))
        #  last = data[len(data)-1]
        self.__check_token()
        for last in data:
            title = last['digest']
            if title is None or len(title) == 0:
                title = last['title']
            url = last['link']
            #  aid = last['aid']
            url_2pdf(url, path, title)
            time.sleep(random.randint(0, 5))


    def check(self):
        if self.app is None or self.app.islogin == False:
            raise IOError("没有初始化账号信息或者没有登录成功")

