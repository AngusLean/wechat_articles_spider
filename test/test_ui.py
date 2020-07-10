# coding: utf-8
import tkinter as tk
from tkinter import scrolledtext, messagebox
from wechatarticles import WxAPI,Config
from wechatarticles.Config import GlobalConfig
import tempfile
import os
from PIL import Image, ImageTk
from tkinter import Label,Toplevel,filedialog
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
        self.window.title('微信公众号文章抓取'+GlobalConfig.get_version())
        ##窗口尺寸
        self.window.geometry('900x500')
        self.init_ui()
        self.app = WxAPI.AccountManager()
        Config.GlobalConfig.set_global_wd(self.window)
        ##显示出来
        self.window.mainloop()

    def init_ui(self):
        frame1 = tk.Frame(self.window, borderwidth=2,
                          highlightbackground="black",highlightthickness=1)

        frame1.grid(row=0, column=0, sticky=tk.E, padx=10, ipadx=5, ipady=5)

        self.usernameipt = tk.Entry(frame1)
        self.psdipt = tk.Entry(frame1)
        self.unlabel = tk.Label(frame1, text='个人公众号账号')
        self.psdlabel = tk.Label(frame1, text='个人公众号密码')

        #  账号输入框
        self.index = 0
        self.unlabel.grid(row=self.index)
        self.usernameipt.grid(row=self.index, column=1, sticky='N')
        self.usernameipt.insert("end", GlobalConfig.get_conf('username'))
        self.psdipt.insert("end", GlobalConfig.get_conf('password'))
        #密码输入框
        self.index = self.index+1
        self.psdlabel.grid(row=self.index)
        self.psdipt.grid(row=self.index, column=1, sticky='W')

        ##  登录按钮
        self.index = self.index+1
        self.quitbutton = tk.Button(frame1, text='开始登录', command=self.begin_login)
        self.quitbutton.grid(row=self.index)

        #  公众号名称
        self.index = self.index+1
        self.nicknamelabel = tk.Label(frame1, text='公众号名称(已经关注)')
        self.nicknamelabel.grid(row=self.index)
        self.nicknameipt = tk.Entry(frame1)
        self.nicknameipt.grid(row=self.index, column=1, sticky='W')

        #  开始抓取按钮
        self.index = self.index+1
        self.spibutton = tk.Button(frame1, text='开始抓取', command=self.begin_spider)
        self.spibutton.grid(row=self.index)

        self.init_spider_ui()


    def init_spider_ui(self):
        frame1 = tk.Frame(self.window, borderwidth=2,
                        height = 50,
                          highlightbackground="black",highlightthickness=1)
        frame1.grid(row=0, column=1, sticky=tk.W, ipadx=5, ipady=5)
        #  frame1.pack(fill=tk.X,side=tk.RIGHT)
        index = 1
        self.jsonlabel = tk.Label(frame1, text='手动输入元数据位置')
        self.jsonlabel.grid(row=index)
        self.jsonipt = tk.Entry(frame1)
        self.jsonipt.grid(row=index, column=1, sticky='W')

        #开始抓取
        index = 2
        self.jsonbtn = tk.Button(frame1, text='手动选择配置文件抓取', command=self.begin_from_json)
        self.jsonbtn.grid(row=index)

        frame2 = tk.Frame(self.window, pady=10)
        frame2.grid(row=1, columnspan=3, padx=10, ipadx=5, ipady=5)
        #  frame2.pack(side=tk.BOTTOM)
        #重定向输出
        self.index = 0
        self.textboxlabel = tk.Label(frame2, text='输出')
        self.textboxlabel.grid(row=index)
        self.textbox = scrolledtext.ScrolledText(frame2)
        self.textbox.grid(row=index, column=1)
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
        #  cookie = 'pgv_pvid=1484837112; pgv_pvi=226359296; RK=zXLJsr3WUF; ptcz=2764575081030f0512fd13960a818c0eb9417dfeb2ffdebae5b86c167d8c9e60; o_cookie=914872065; pac_uid=1_914872065; ied_qq=o0914872065; ua_id=5tkHzowxrhAcWk7sAAAAANOxAeuJSjxJTQfL9RGT2gU=; openid2ticket_oMnSW5BNc5oGKOXJW3a2rELZ-5CQ=JcdaYT0rBhh34TDRWpGOBWlDha3zpFto13RGd7AR7no=; mm_lang=zh_CN; ptui_loginuin=896173273@qq.com; noticeLoginFlag=1; wxuin=93918055045263; ts_uid=9942437081; pgv_si=s4749021184; cert=xVZUDWktbpSttR24mZKTGQasC1KDJcRg; master_key=CqM3UcaaFCqZzvhyr/bXFVUxr/rzlNIJhXeJi1IxVvI=; pgv_info=ssid=s5237946083; uin=o0082604749; skey=@G2xEn5qfd; sig=h01e025fea837e242f8bc734804f0f390a88ebcfb8ba303eb57e1f2c3e57582ac5f16022cc1a3dbc315; openid2ticket_oMnULj8Z8JUYPlPtn6Dd0Cufd-Mk=3uP7womLyFcWhuagCSgQXuX+i4XjQhAJAKYXtPunCkg=; rewardsn=; wxtokenkey=777; uuid=7b832c1bf88e650b960fd5396f802699; rand_info=CAESIE1/2G1M6MXbJBW9M5wUWiow2sBsFkRL05T5RR65wAyT; slave_bizuin=2399892786; data_bizuin=2399892786; bizuin=2399892786; data_ticket=JThB+nkN/Gwkx1CTxDcpUJFlnXM2mF7x8f1gakoWL7y91azjSsGiGu8tpT0NqyJq; slave_sid=QnpsX3FUc3pnVXFZaVZXMGlaRjZaU2VrVkw1bmJsb0NPdDlxaVhobmw5c3lNN21COXo3SlhudmJmTW5WZVdOVzBjeG5USjYwVWY4V185TW9wdXZrZFRkeHlhenU5ejRWajB4WFlMSHc1d1Q2RGxMY25jVlVOS1BDTlREVE9nUGlqTHlxV05CYWREM3dGYVNh; slave_user=gh_c8c72405cef0; xid=fed3098d37bb0fce79c677c966714412'
        #  token = '1930579147'
        self.app.login_by_user(username, password)
        #  self.app.login_by_cookie(cookie, token)

    def begin_spider(self):
        if self.nicknameipt.get() is None or len(self.nicknameipt.get()) == 0:
            print("请输入关注的公众号名称")
            return
        self.app.get_article_list(self.nicknameipt.get())

    def begin_from_json(self):
        jsonPath =  tk.filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("json files","*.json"),("all files","*.*")))
        if jsonPath is None:
            jsonPath = self.jsonipt.get()
            if jsonPath is None:
                print("没有选择配置文件位置")
                return
        if jsonPath is None or len(jsonPath) == 0:
            print("未输入元数据位置")
            return
        if not os.path.exists(jsonPath):
            print("文件不存在!:{}".format(jsonPath))
            return
        self.app.get_from_json(jsonPath)

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
