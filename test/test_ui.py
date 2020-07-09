# coding: utf-8
import tkinter as tk
from tkinter import scrolledtext, messagebox
from wechatarticles import WxAPI,Config
import tempfile
import os
from PIL import Image, ImageTk
from tkinter import Label,Toplevel
import sys

class TextRedirector(object):
    def __init__(self, widget, tag="stdout"):
        self.widget = widget
        self.tag = tag

    def write(self, str):
        self.widget.configure(state="normal")
        self.widget.insert("end", str, (self.tag,))
        self.widget.configure(state="disabled")

class Application():
    def __init__(self,):
        self.window = tk.Tk()
        self.window.title('微信公众号文章抓取')
        ##窗口尺寸
        self.window.geometry('1200x700')
        self.init_ui()
        self.app = WxAPI.AccountManager()
        Config.GlobalConfig.set_global_wd(self.window)
        ##显示出来
        self.window.mainloop()

    def init_ui(self):
        self.usernameipt = tk.Entry(self.window)
        self.psdipt = tk.Entry(self.window)
        self.unlabel = tk.Label(self.window, text='个人公众号账号')
        self.psdlabel = tk.Label(self.window, text='个人公众号密码')
        self.unlabel.grid(row=0)
        self.usernameipt.grid(row=0, column=1, sticky='W')
        self.psdlabel.grid(row=1)
        self.psdipt.grid(row=1, column=1, sticky='W')

        self.quitbutton = tk.Button(self.window, text='开始登录', command=self.begin_login)
        self.quitbutton.grid(row=2)
        self.usernameipt.insert("end", "82604749@qq.com")
        self.psdipt.insert("end", "ty206683")
        self.spibutton = tk.Button(self.window, text='开始抓取', command=self.begin_spider)
        self.spibutton.grid(row=3)
        #-----------------------
        #  path=os.path.join(tempfile.gettempdir(), "login.png")
        #  try:
            #  self.img = Image.open(path)
            #  from tkinter import PhotoImage, Label
            #  self.img=ImageTk.PhotoImage(self.img)
            #  img_png = PhotoImage(file = path)
            #  newWd = Toplevel()
            #  newWd.wm_title("微信登录二维码,扫描后手动关闭")
            #  label_img = Label(newWd, image = self.img)
            #  label_img.pack()
        #  except Exception:
            #  raise TypeError(u"账号密码输入错误，请重新输入")
        #-----------------------
        #重定向输出
        self.textboxlabel = tk.Label(self.window, text='输出')
        self.textboxlabel.grid(row=4)
        self.textbox = scrolledtext.ScrolledText(self.window, width=100, height=20)
        self.textbox.grid(row=4, column=1)
        sys.stdout = TextRedirector(self.textbox, "stdout")
        sys.stderr = TextRedirector(self.textbox, "stderr")

    def quit(self):
        None

    def show_info(self, msg):
        messagebox.showinfo(message=msg)
    def begin_login(self):
        username = self.usernameipt.get()
        password = self.psdipt.get()
        print("账号{},密码{}, --{}".format(username, password, len(username)))
        if len(username)==0 or len(password)==0:
            self.show_info("账号或者密码为空")
            return
        self.app = WxAPI.AccountManager()
        print("开始登录，账号:{},密码:{}".format(username, password))
        cookie = 'pgv_pvid=1484837112; pgv_pvi=226359296; RK=zXLJsr3WUF; ptcz=2764575081030f0512fd13960a818c0eb9417dfeb2ffdebae5b86c167d8c9e60; o_cookie=914872065; pac_uid=1_914872065; ied_qq=o0914872065; ua_id=5tkHzowxrhAcWk7sAAAAANOxAeuJSjxJTQfL9RGT2gU=; openid2ticket_oMnSW5BNc5oGKOXJW3a2rELZ-5CQ=JcdaYT0rBhh34TDRWpGOBWlDha3zpFto13RGd7AR7no=; mm_lang=zh_CN; ptui_loginuin=896173273@qq.com; noticeLoginFlag=1; wxuin=93918055045263; ts_uid=9942437081; pgv_si=s4749021184; cert=xVZUDWktbpSttR24mZKTGQasC1KDJcRg; master_key=CqM3UcaaFCqZzvhyr/bXFVUxr/rzlNIJhXeJi1IxVvI=; pgv_info=ssid=s5237946083; uin=o0082604749; skey=@G2xEn5qfd; sig=h01e025fea837e242f8bc734804f0f390a88ebcfb8ba303eb57e1f2c3e57582ac5f16022cc1a3dbc315; openid2ticket_oMnULj8Z8JUYPlPtn6Dd0Cufd-Mk=3uP7womLyFcWhuagCSgQXuX+i4XjQhAJAKYXtPunCkg=; rewardsn=; wxtokenkey=777; uuid=7b832c1bf88e650b960fd5396f802699; rand_info=CAESIE1/2G1M6MXbJBW9M5wUWiow2sBsFkRL05T5RR65wAyT; slave_bizuin=2399892786; data_bizuin=2399892786; bizuin=2399892786; data_ticket=JThB+nkN/Gwkx1CTxDcpUJFlnXM2mF7x8f1gakoWL7y91azjSsGiGu8tpT0NqyJq; slave_sid=QnpsX3FUc3pnVXFZaVZXMGlaRjZaU2VrVkw1bmJsb0NPdDlxaVhobmw5c3lNN21COXo3SlhudmJmTW5WZVdOVzBjeG5USjYwVWY4V185TW9wdXZrZFRkeHlhenU5ejRWajB4WFlMSHc1d1Q2RGxMY25jVlVOS1BDTlREVE9nUGlqTHlxV05CYWREM3dGYVNh; slave_user=gh_c8c72405cef0; xid=fed3098d37bb0fce79c677c966714412'
        token = '1930579147'
        self.app.login_by_user(username, password)
        #  self.app.login_by_cookie(cookie, token)

    def begin_spider(self):
        self.app.get_article_list('融创西南', 3)

def test():
    from PIL import Image, ImageTk
    from tkinter import Label
    import os
    import tempfile
    #  f = tempfile.TemporaryFile()

    path=os.path.join(tempfile.gettempdir(), "login.png")
    #  path = os.path.join(os.path.tmp, "login.png")
    print("临时二维码文件:{}".format(path))
    # 存储二维码
    #  with open(path, "wb+") as fp:
        #  fp.write(img.content)
    # 显示二维码， 这里使用plt的原因是： 等待用户扫描完之后手动关闭窗口继续运行；否则会直接运行
    #  root = tk.Tk()
    try:
        img = Image.open(path)
        #  from tkinter import PhotoImage, Label
        img=ImageTk.PhotoImage(img)
        #  img_png = PhotoImage(file = path)
        label_img = Label(Toplevel(), image = img)
        label_img.pack()
    except Exception:
        raise TypeError(u"账号密码输入错误，请重新输入")
    #  root.mainloop()
    #  plt.figure()
    #  plt.imshow(img)
    #  plt.show()


def startUI():
    app = Application()
    # 设置窗口标题:
    #  app.master.title('微信导入')
    # 主消息循环:
    #  app.mainloop()

def main():
    #  test()
    startUI()
    #  test()
    #  FL = WeChartUI()
    #  FL.pack()
    #  tkinter.mainloop()
    #  pass

if __name__ == "__main__":
    main()
