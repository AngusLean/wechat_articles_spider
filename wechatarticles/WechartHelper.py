#encoding=utf-8

import time
import re
import requests
import random
import math
from bs4 import BeautifulSoup
from lxml import etree
#  from lxml.etree import XML
from .const import agents


backgroud_image_p = re.compile('background-image:[ ]+url\(\"([\w\W]+?)\"\)')
js_content = re.compile('js_content.*?>((\s|\S)+)</div>')
find_article_json_re = re.compile('var msgList = (.*?)}}]};')
get_post_view_perm = re.compile('<script>var account_anti_url = "(.*?)";</script>')


def format_image_url(url):
    if isinstance(url, list):
        return [format_image_url(i) for i in url]

    if url.startswith('//'):
        url = 'https:{}'.format(url)
    return url



class WechartHelper:
    def __init__(self, captcha_break_time=1, headers=None, **kwargs):
        """初始化参数

        Parameters
        ----------
        captcha_break_time : int
            验证码输入错误重试次数
        proxies : dict
            代理
        timeout : float
            超时时间
        """
        assert isinstance(captcha_break_time, int) and 0 < captcha_break_time < 20

        self.captcha_break_times = captcha_break_time
        self.requests_kwargs = kwargs
        self.headers = headers
        if self.headers:
            self.headers['User-Agent'] = random.choice(agents)
        else:
            self.headers = {'User-Agent': random.choice(agents)}

    def refresh_wechart_cotent4_download(self, url, title, targetPath):
        '''
        使用pdfkit生成pdf文件
        :param url: 文章url
        :param title: 文章标题
        :param targetPath: 存储pdf文件的路径
        '''
        try:
            content_info = self.get_article_content(url)
        except Exception as e:
            raise e
            #  print(e)
            #  return False
        # 处理后的html
        html = f'''
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <title>{title}</title>
            </head>
            <body>
            <h2 style="text-align: center;font-weight: 400;">{title}</h2>
            {content_info['content_html']}
            </body>
            </html>
            '''
        return html

    def __get_by_unlock(self, url, referer=None, unlock_platform=None, unlock_callback=None, identify_image_callback=None, session=None):
        assert unlock_platform is None or callable(unlock_platform)
        assert unlock_callback is None or callable(unlock_callback)

        if not session:
            session = requests.session()
        resp = self.__get(url, session, headers=self.__set_cookie(referer=referer))
        resp.encoding = 'utf-8'
        if 'antispider' in resp.url or '请输入验证码' in resp.text:
            for i in range(self.captcha_break_times):
                try:
                    unlock_platform(url=url, resp=resp, session=session, unlock_callback=unlock_callback, identify_image_callback=identify_image_callback)
                    break
                except Exception as e:
                    if i == self.captcha_break_times - 1:
                        raise Exception(e)

            if '请输入验证码' in resp.text:
                resp = session.get(url)
                resp.encoding = 'utf-8'
            else:
                headers = self.__set_cookie(referer=referer)
                headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; WOW64)'
                resp = self.__get(url, session, headers)
                resp.encoding = 'utf-8'

        return resp


    def get_article_content(self, url, del_qqmusic=True, del_mpvoice=True, unlock_callback=None,
                            identify_image_callback=None, hosting_callback=None, raw=False):
        """获取文章原文，避免临时链接失效

        Parameters
        ----------
        url : str or unicode
            原文链接，临时链接
        raw : bool
            True: 返回原始html
            False: 返回处理后的html
        del_qqmusic: bool
            True:微信原文中有插入的qq音乐，则删除
            False:微信源文中有插入的qq音乐，则保留
        del_mpvoice: bool
            True:微信原文中有插入的语音消息，则删除
            False:微信源文中有插入的语音消息，则保留
        unlock_callback : callable
            处理 文章明细 的时候出现验证码的函数，参见 unlock_callback_example
        identify_image_callback : callable
            处理 文章明细 的时候处理验证码函数，输入验证码二进制数据，输出文字，参见 identify_image_callback_example
        hosting_callback: callable
            将微信采集的文章托管到7牛或者阿里云回调函数，输入微信图片源地址，返回托管后地址

        Returns
        -------
        content_html
            原文内容
        content_img_list
            文章中图片列表

        Raises
        ------
        WechatSogouRequestsException
        """

        resp = self.__get_by_unlock(url,
                                    unlock_platform=self.__unlock_wechat,
                                    unlock_callback=unlock_callback,
                                    identify_image_callback=identify_image_callback)

        resp.encoding = 'utf-8'
        if '链接已过期' in resp.text:
            raise Exception('get_article_content 链接 [{}] 已过期'.format(url))
        if raw:
            return resp.text
        content_info = self.get_article_detail(resp.text, del_qqmusic=del_qqmusic,
                                               del_voice=del_mpvoice)
        if hosting_callback:
            content_info = self.__hosting_wechat_img(content_info, hosting_callback)
        return content_info

    def __hosting_wechat_img(self, content_info, hosting_callback):
        """将微信明细中图片托管到云端，同时将html页面中的对应图片替换

        Parameters
        ----------
        content_info : dict 微信文章明细字典
            {
                'content_img_list': [], # 从微信文章解析出的原始图片列表
                'content_html': '', # 从微信文章解析出文章的内容
            }
        hosting_callback : callable
            托管回调函数，传入单个图片链接，返回托管后的图片链接

        Returns
        -------
        dict
            {
                'content_img_list': '', # 托管后的图片列表
                'content_html': '',  # 图片链接为托管后的图片链接内容
            }
        """
        assert callable(hosting_callback)

        content_img_list = content_info.pop("content_img_list")
        content_html = content_info.pop("content_html")
        for idx, img_url in enumerate(content_img_list):
            hosting_img_url = hosting_callback(img_url)
            if not hosting_img_url:
                # todo 定义标准异常
                raise Exception()
            content_img_list[idx] = hosting_img_url
            content_html = content_html.replace(img_url, hosting_img_url)

        return dict(content_img_list=content_img_list, content_html=content_html)

    #  def __format_url(self, url, referer, text, unlock_callback=None, identify_image_callback=None, session=None):
        #  def _parse_url(url, pads):
            #  b = math.floor(random.random() * 100) + 1
            #  a = url.find("url=")
            #  c = url.find("&k=")
            #  if a != -1 and c == -1:
                #  sum = 0
                #  for i in list(pads) + [a, b]:
                    #  sum += int(must_str(i))
                #  a = url[sum]

            #  return '{}&k={}&h={}'.format(url, may_int(b), may_int(a))

        #  if url.startswith('/link?url='):
            #  url = 'https://weixin.sogou.com{}'.format(url)

            #  pads = re.findall(r'href\.substr\(a\+(\d+)\+parseInt\("(\d+)"\)\+b,1\)', text)
            #  url = _parse_url(url, pads[0] if pads else [])
            #  resp = self.__get_by_unlock(url,
                                        #  referer=referer,
                                        #  unlock_platform=None,
                                        #  unlock_callback=unlock_callback,
                                        #  identify_image_callback=identify_image_callback,
                                        #  session=session)
            #  uri = ''
            #  base_url = re.findall(r'var url = \'(.*?)\';', resp.text)
            #  if base_url and len(base_url) > 0:
                #  uri = base_url[0]

            #  mp_url = re.findall(r'url \+= \'(.*?)\';', resp.text)
            #  if mp_url:
                #  uri = uri + ''.join(mp_url)
            #  url = uri.replace('@', '')
        #  return url


    def __get(self, url, session, headers):
        h = {}
        if headers:
            for k, v in headers.items():
                h[k] = v
        if self.headers:
            for k, v in self.headers.items():
                h[k] = v
        resp = session.get(url, headers=h, **self.requests_kwargs)

        if not resp.ok:
            raise Exception('WechatSogouAPI get error', resp)

        return resp

    def get_article_detail(self, text, del_qqmusic=True, del_voice=True):
        """根据微信文章的临时链接获取明细

        1. 获取文本中所有的图片链接列表
        2. 获取微信文章的html内容页面(去除标题等信息)

        Parameters
        ----------
        text : str or unicode
            一篇微信文章的文本
        del_qqmusic: bool
            删除文章中的qq音乐
        del_voice: bool
            删除文章中的语音内容

        Returns
        -------
        dict
        {
            'content_html': str # 微信文本内容
            'content_img_list': list[img_url1, img_url2, ...] # 微信文本中图片列表

        }
        """
        # 1. 获取微信文本content
        html_obj = BeautifulSoup(text, "lxml")
        content_text = html_obj.find('div', {'class': 'rich_media_content', 'id': 'js_content'})

        # 2. 删除部分标签
        if del_qqmusic:
            qqmusic = content_text.find_all('qqmusic') or []
            for music in qqmusic:
                music.parent.decompose()

        if del_voice:
            # voice是一个p标签下的mpvoice标签以及class为'js_audio_frame db'的span构成，所以将父标签删除
            voices = content_text.find_all('mpvoice') or []
            for voice in voices:
                voice.parent.decompose()

        # 3. 获取所有的图片 [img标签，和style中的background-image]
        all_img_set = set()
        all_img_element = content_text.find_all('img') or []
        for ele in all_img_element:
            # 删除部分属性
            img_url = format_image_url(ele.attrs['data-src'])
            del ele.attrs['data-src']

            ele.attrs['src'] = img_url

            if not img_url.startswith('http'):
                raise Exception('img_url [{}] 不合法'.format(img_url))
            all_img_set.add(img_url)

        backgroud_image = content_text.find_all(style=re.compile("background-image")) or []
        for ele in backgroud_image:
            # 删除部分属性
            if ele.attrs.get('data-src'):
                del ele.attrs['data-src']

            if ele.attrs.get('data-wxurl'):
                del ele.attrs['data-wxurl']
            img_url = re.findall(backgroud_image_p, str(ele))
            if not img_url:
                continue
            all_img_set.add(img_url[0])

        # 4. 处理iframe
        all_img_element = content_text.find_all('iframe') or []
        for ele in all_img_element:
            # 删除部分属性
            img_url = ele.attrs['data-src']
            del ele.attrs['data-src']
            ele.attrs['src'] = img_url

        # 5. 返回数据
        all_img_list = list(all_img_set)
        content_html = content_text.prettify()
        # 去除div[id=js_content]
        content_html = re.findall(js_content, content_html)[0][0]
        return {
            'content_html': content_html,
            'content_img_list': all_img_list
        }
    def __unlock_wechat(self, url, resp, session, unlock_callback=None, identify_image_callback=None):
        if unlock_callback is None:
            unlock_callback = self.unlock_weixin_callback_example

        r_captcha = session.get('https://mp.weixin.qq.com/mp/verifycode?cert={}'.format(time.time() * 1000))
        if not r_captcha.ok:
            raise Exception('WechatSogouAPI unlock_history get img', resp)

        r_unlock = unlock_callback(url, session, resp, r_captcha.content, identify_image_callback)

        if r_unlock['ret'] != 0:
            raise Exception(
                '[WechatSogouAPI identify image] code: {ret}, msg: {errmsg}, cookie_count: {cookie_count}'.format(
                    ret=r_unlock.get('ret'), errmsg=r_unlock.get('errmsg'), cookie_count=r_unlock.get('cookie_count')))
    def unlock_weixin_callback_example(self, url, req, resp, img, identify_image_callback):
        """手动打码解锁

        Parameters
        ----------
        url : str or unicode
            验证码页面 之前的 url
        req : requests.sessions.Session
            requests.Session() 供调用解锁
        resp : requests.models.Response
            requests 访问页面返回的，已经跳转了
        img : bytes
            验证码图片二进制数据
        identify_image_callback : callable
            处理验证码函数，输入验证码二进制数据，输出文字，参见 identify_image_callback_example

        Returns
        -------
        dict
            {
                'ret': '',
                'errmsg': '',
                'cookie_count': '',
            }
        """
        # no use resp

        unlock_url = 'https://mp.weixin.qq.com/mp/verifycode'
        data = {
            'cert': time.time() * 1000,
            'input': identify_image_callback(img)
        }
        headers = {
            'Host': 'mp.weixin.qq.com',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Referer': url
        }
        r_unlock = req.post(unlock_url, data, headers=headers)
        if not r_unlock.ok:
            raise Exception(
                'unlock[{}] failed: {}[{}]'.format(unlock_url, r_unlock.text, r_unlock.status_code))

        return r_unlock.json()
    def __set_cookie(self, suv=None, snuid=None, referer=None):
        _headers = {'Cookie': 'SUV={};SNUID={};'.format(suv, snuid)}
        if referer is not None:
            _headers['Referer'] = referer
        return _headers

weChartHelper = WechartHelper()
