# coding: utf-8

import time
import json
import pdfkit
import os

from .fileutil import clean_filename,slugify
from .Config import GlobalConfig

# 一些tools，如时间戳转换
def timestamp2date(timestamp):
    """
    时间戳转换为日期
    Parameters
    ----------
    timestamp: int or str
        用户账号

    Returns
    -------
    datetime:
        转换好的日期：年-月-日 时:分:秒
    """
    time_array = time.localtime(int(timestamp))
    datetime = time.strftime("%Y-%m-%d %H:%M:%S", time_array)
    return datetime

def save_mongo(data,
                host=None,
                port=None,
                name=None,
                password="",
                dbname=None,
                collname=None):
    """
    存储数据到mongo
    Parameters
    ----------
    data: list
        需要插入的数据
    host: str
        主机名(默认为本机数据库)
    port: int
        mongo所在主机开放的端口，默认为27017
    username: str
        用户名
    password: str
        用户密码
    dbname: str
        远程连接的数据库名
    collname: str
        需要插入的集合名(collection)
    Returns
    -------
    None
    """
    HOST = "localhost"
    PORT = 27017

    # 检查参数
    host = HOST if host is None else host
    port = PORT if port is None else port

    assert isinstance(host, str)
    assert isinstance(name, str)
    assert isinstance(password, str)
    assert isinstance(dbname, str)
    assert isinstance(collname, str)

    if not isinstance(port, int):
        raise TypeError("port must be an instance of int")

    from pymongo import MongoClient
    # 连接数据库，一次性插入数据
    client = MongoClient(host, port)
    db_auth = client.admin
    db_auth.authenticate(name, password)
    coll = client[dbname][collname]
    coll.insert_many(data)

def save_json(fname, data):
    """
    保存数据为txt格式
    Parameters
    ----------
    fname: str
        保存为txt文件名
    data: list
        爬取到的数据
    Returns
    -------
    None
    """
    assert isinstance(fname, str)

    if ".json" not in fname:
        raise IOError("fname must be json", fname)
    with open(fname, "a+", encoding='utf-8') as f:
        for item in data:
            f.write(json.dumps(item))
            f.write("\n")

def read_json(path):
    result = []
    with open(path, 'r') as f:
        for line in f.readlines():
            result.append(json.loads(line))
    return result

def url_2pdf(url, dic="pdfs", title=""):
    if url is None:
        return
    #  dic = clean_filename(dic)
    config = pdfkit.configuration(
        wkhtmltopdf = GlobalConfig.get_conf('wkpdfpath')
        #  wkhtmltopdf=r"/home/anguslean/project/wechat_articles_spider/bin/wkhtmltox_0.12.6-1.bionic_amd64.deb"
    )
    (path,filename) = os.path.split(dic)
    (name, ext) = os.path.splitext(filename)
    name = slugify(name)
    #  name = clean_filename(name)
    newPath = os.path.abspath(os.path.join(GlobalConfig.get_conf('pdfpath'), name))
    options = {
        'page-size': 'A4',  # 默认是A4 Letter  etc
        # 'margin-top':'0.05in',   #顶部间隔
        # 'margin-right':'2in',   #右侧间隔
        # 'margin-bottom':'0.05in',   #底部间隔
        # 'margin-left':'2in',   #左侧间隔
        'encoding': "UTF-8",  #文本个数
        'dpi': '96',
        'image-dpi': '600',
        'image-quality': '94',
        'footer-font-size': '80',  #字体大小
        'no-outline': None,
        'quiet': '',
        "zoom": 2,  # 网页放大/缩小倍数
    }
    print("开始保存[{}]到目录:[{}]".format(title, newPath))
    if not os.path.exists(newPath):
        os.makedirs(newPath)
    pdfkit.from_url(url,
                '{}/{}.pdf'.format(newPath, title),
                configuration=config,
                options=options)
    print("保存[{}]到pdf文件成功".format(title))


