# coding: utf-8
import os
import random
import time
from pprint import pprint
from wechatarticles import ArticlesUrls, tools
#  from wechatarticles import url2pdf
from wechatarticles import WxAPI

'''
获取从指定位置到终点位置的所有文章
'''
def getArticleList(app, nickname, start=0, total=5):
    sleepTime = 5
    while start <= total:
        print("开始获取{}开始的文章列表".format(start))
        articles = app.articles(nickname, begin="{}".format(start), count="5")
        tools.save_json("{}.json".format(nickname), articles)
        start += len(articles)
        print("公众号数据到抓取{}条，随机睡眠{}秒".format(len(articles), sleepTime))
        time.sleep(sleepTime)
        sleepTime = 5+random.randint(5, 15)
    print("总共抓取到{}篇文章元数据，已经保存文章元数据到本地.请下载".
          format(total))

def readJson(path):
    filename = os.path.splitext(os.path.split(path)[1])[0]
    print("开始下载文件:{}的文章信息".format(filename))
    data = tools.read_json(path)
    if data is None:
        print("{}-文件为空".format(path))
        return
    print("读取到文件{}的数据{}".format(filename, data))
    #  last = data[len(data)-1]
    for last in data:
        title = last['digest']
        url = last['link']
        aid = last['aid']
        tools.url_2pdf(url, path, title)
        time.sleep(random.randint(0, 5))

def testGetArticles():
    # 模拟登录微信公众号平台，获取微信文章的url
    username = "82604749@qq.com"
    password = "ty206683"
    cookie = "pgv_pvid=1484837112; pgv_pvi=226359296; RK=zXLJsr3WUF; ptcz=2764575081030f0512fd13960a818c0eb9417dfeb2ffdebae5b86c167d8c9e60; o_cookie=914872065; pac_uid=1_914872065; ied_qq=o0914872065; ua_id=5tkHzowxrhAcWk7sAAAAANOxAeuJSjxJTQfL9RGT2gU=; openid2ticket_oMnSW5BNc5oGKOXJW3a2rELZ-5CQ=JcdaYT0rBhh34TDRWpGOBWlDha3zpFto13RGd7AR7no=; mm_lang=zh_CN; ptui_loginuin=896173273@qq.com; noticeLoginFlag=1; wxuin=93918055045263; ts_uid=9942437081; pgv_si=s4749021184; cert=xVZUDWktbpSttR24mZKTGQasC1KDJcRg; master_key=CqM3UcaaFCqZzvhyr/bXFVUxr/rzlNIJhXeJi1IxVvI=; pgv_info=ssid=s5237946083; uin=o0082604749; skey=@G2xEn5qfd; sig=h01e025fea837e242f8bc734804f0f390a88ebcfb8ba303eb57e1f2c3e57582ac5f16022cc1a3dbc315; uuid=b9b93c5babf306fb7fed76c7d2fcd02f; bizuin=2399892786; ticket=96e50c836042222b2d9371460d2c9ba3cffc58cc; ticket_id=gh_c8c72405cef0; rand_info=CAESIHxA4jzT6pMHR0ioOmPG0KOciKSgF/0sk8FM5d+bZKl6; slave_bizuin=2399892786; data_bizuin=2399892786; data_ticket=pokiXWnvosh6GpbEalsZMTYZovFV1VLN44uFHFkB3PJNDRN6sENAleVlC/5R3YZe; slave_sid=amRieFhEQUNPR1AwZ3pwSWs3aGhrdHY0MkhyR05nRUwxX3l6YW9SNk5qNV9ZbWp2dzhyRURUWDdEOEJrZ1g1ZjRFeTJHVEh0ZVRwRGpPcl9hMjVMRXlSRUxYWk5OVUtoU2JZY3RjOG5RaW5HWHZ3WlQ1MmRhMHRsVGhmcUQ3eGJBQVExcDBneFc4MzBIMU1E; slave_user=gh_c8c72405cef0; xid=35ca7b96049e81652ba0320e92569b42; openid2ticket_oMnULj8Z8JUYPlPtn6Dd0Cufd-Mk=3uP7womLyFcWhuagCSgQXuX+i4XjQhAJAKYXtPunCkg="
    token = "1270986716"
    nickname = "原美术馆"
    query = "query"

    #  test = ArticlesUrls(username, password)
    test = ArticlesUrls(cookie=cookie, token=token)
    articles_sum = test.articles_nums(nickname)

    print("articles_sum:", end=" ")
    print(articles_sum)
    getArticleList(test, nickname, 0, 20)
    #  print("artcles_data:")
    #  artiacle_data = test.articles(nickname, begin="0", count="5")
    #  pprint(artiacle_data)

    #  officical_info = test.official_info(nickname)
    #  print("officical_info:")
    #  pprint(officical_info)

    #  tools.save_json("test.json", artiacle_data)

if __name__ == "__main__":
    #  readJson("/home/anguslean/project/wechat_articles_spider/原美术馆.json")
    #  testGetArticles()
    cookie = "pgv_pvid=1484837112; pgv_pvi=226359296; RK=zXLJsr3WUF; ptcz=2764575081030f0512fd13960a818c0eb9417dfeb2ffdebae5b86c167d8c9e60; o_cookie=914872065; pac_uid=1_914872065; ied_qq=o0914872065; ua_id=5tkHzowxrhAcWk7sAAAAANOxAeuJSjxJTQfL9RGT2gU=; openid2ticket_oMnSW5BNc5oGKOXJW3a2rELZ-5CQ=JcdaYT0rBhh34TDRWpGOBWlDha3zpFto13RGd7AR7no=; mm_lang=zh_CN; ptui_loginuin=896173273@qq.com; noticeLoginFlag=1; wxuin=93918055045263; ts_uid=9942437081; pgv_si=s4749021184; cert=xVZUDWktbpSttR24mZKTGQasC1KDJcRg; master_key=CqM3UcaaFCqZzvhyr/bXFVUxr/rzlNIJhXeJi1IxVvI=; pgv_info=ssid=s5237946083; uin=o0082604749; skey=@G2xEn5qfd; sig=h01e025fea837e242f8bc734804f0f390a88ebcfb8ba303eb57e1f2c3e57582ac5f16022cc1a3dbc315; uuid=b9b93c5babf306fb7fed76c7d2fcd02f; bizuin=2399892786; ticket=96e50c836042222b2d9371460d2c9ba3cffc58cc; ticket_id=gh_c8c72405cef0; rand_info=CAESIHxA4jzT6pMHR0ioOmPG0KOciKSgF/0sk8FM5d+bZKl6; slave_bizuin=2399892786; data_bizuin=2399892786; data_ticket=pokiXWnvosh6GpbEalsZMTYZovFV1VLN44uFHFkB3PJNDRN6sENAleVlC/5R3YZe; slave_sid=amRieFhEQUNPR1AwZ3pwSWs3aGhrdHY0MkhyR05nRUwxX3l6YW9SNk5qNV9ZbWp2dzhyRURUWDdEOEJrZ1g1ZjRFeTJHVEh0ZVRwRGpPcl9hMjVMRXlSRUxYWk5OVUtoU2JZY3RjOG5RaW5HWHZ3WlQ1MmRhMHRsVGhmcUQ3eGJBQVExcDBneFc4MzBIMU1E; slave_user=gh_c8c72405cef0; xid=35ca7b96049e81652ba0320e92569b42; openid2ticket_oMnULj8Z8JUYPlPtn6Dd0Cufd-Mk=3uP7womLyFcWhuagCSgQXuX+i4XjQhAJAKYXtPunCkg="
    token = "1270986716"
    app = WxAPI.AccountManager()
    app.login_by_cookie(cookie, token)
    app.getArticleList('融创西南')
