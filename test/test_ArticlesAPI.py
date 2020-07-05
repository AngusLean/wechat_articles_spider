# coding: utf-8
import os
from pprint import pprint
from wechatarticles.ReadOutfile import Reader
from wechatarticles import ArticlesAPI
from wechatarticles import tools

if __name__ == '__main__':
    username = "896173273@qq.com"
    password = "19930520Am@"
    official_cookie = "pgv_pvid=1484837112; pgv_pvi=226359296; RK=zXLJsr3WUF; ptcz=2764575081030f0512fd13960a818c0eb9417dfeb2ffdebae5b86c167d8c9e60; o_cookie=914872065; pac_uid=1_914872065; ied_qq=o0914872065; ua_id=5tkHzowxrhAcWk7sAAAAANOxAeuJSjxJTQfL9RGT2gU=; openid2ticket_oMnSW5BNc5oGKOXJW3a2rELZ-5CQ=JcdaYT0rBhh34TDRWpGOBWlDha3zpFto13RGd7AR7no=; mm_lang=zh_CN; ptui_loginuin=896173273@qq.com; noticeLoginFlag=1; rand_info=CAESICtiS65qwPUhxvWg3eYUEn0lWV4q6H51CR29yCNY7x/C; slave_bizuin=3835065394; data_bizuin=3835065394; bizuin=3835065394; data_ticket=sEhavC642dcmFT2/le/BcZ07RFNPndz2KT8pAECJHQwC1fRjsESricG9k+bBY3QQ; slave_sid=Nlc4VjB0TzIydUhSSFh4N1lwbkVLcnBBRFFhdWZMQU8wS1hmZjM5ODhhT05tVGs2Zng0UzFVeEFBN1FUZ1dWWXlLUnROU3huQzRDbGtENmRtTlI3NThfT3B1S3NnNXZwd2lJN1V2RU91QTlmUG9fRnptVDNPV2hoaXZLM09PRTVyNmMyclJuOTkwMTRWTGFn; slave_user=gh_f340b3c67d33; xid=c48a297b31181b8dce87619683ede96e; wxuin=93918055045263; ts_uid=9942437081"
    token = "2022946014"
    appmsg_token = "appmsg_token"
    wechat_cookie = "wechat_cookie"

    nickname = "秦小明"

    # 手动输入所有参数
    #  test = ArticlesAPI(official_cookie=official_cookie,
                       #  token=token,
                       #  appmsg_token=appmsg_token,
                       #  wechat_cookie=wechat_cookie)

    # 输入账号密码，自动登录公众号，手动输入appmsg_token和wechat_cookie
    #  test = ArticlesAPI(username=username,
                       #  password=password,
                       #  appmsg_token=appmsg_token,
                       #  wechat_cookie=wechat_cookie)

    # 手动输入official_cookie和token, 自动获取appmsg_token和wechat_cookie
    test = ArticlesAPI(official_cookie=official_cookie,
                       token=token,
                       outfile="outfile")
    print("开始登录")
    # 输入帐号密码，自动登陆公众号, 自动获取appmsg_token和wechat_cookie
    #  test = ArticlesAPI(username=username, password=password, outfile="outfile")
    print("登录完成")
    # 自定义爬取，每次爬取5篇以上
    data = test.complete_info(nickname=nickname, begin="0")
    print(data.__len__())
    pprint(data)

    # 自定义从某部分开始爬取，持续爬取，直至爬取失败为止，一次性最多爬取40篇（功能未测试，欢迎尝试）
    datas = test.continue_info(nickname=nickname, begin="0")

    tools.save_json("test.json", data)
