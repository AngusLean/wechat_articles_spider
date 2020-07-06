# coding: utf-8
import tkinter as tk
from tkinter import scrolledtext, messagebox
from wechatarticles import WxAPI

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
        self.window.geometry('1500x900')
        self.init_ui()
        self.app = WxAPI.AccountManager()
        ##显示出来
        self.window.mainloop()
        #  self.geometry("350x200")
    def init_ui(self):
        self.usernameipt = tk.Entry(self.window)
        self.psdipt = tk.Entry(self.window)
        self.quitButton = tk.Button(self.window, text='开始', command=self.begin_spider)
        self.usernameipt.grid(column=1, row=0)
        self.psdipt.grid(column=2, row=0)
        self.quitButton.grid(column=1, row=1)
        #  self.textbox = tk.Text(self.window)
        #  self.textbox.grid(column=2, row=4)
        #重定向输出
        self.textbox = scrolledtext.ScrolledText(self.window, width=140, height=50)
        self.textbox.grid(column=2, row=4)
        import sys
        sys.stdout = TextRedirector(self.textbox, "stdout")
        sys.stderr = TextRedirector(self.textbox, "stderr")

    def createWidgets(self):
        self.helloLabel = tk.Label(self, text='输入公众平台账号')
        self.helloLabel.pack()
        self.accountInput = tk.Entry(self, text='82604749@qq.com')
        self.accountInput.pack()
        self.psdInput = tk.Entry(self, text='ty206683')
        self.psdInput.pack()
        self.quitButton = tk.Button(self, text='Quit', command=self.quit)
        self.quitButton.pack()
        self.okButton = tk.Button(self, text='开始抓取', command=self.quit)
        self.okButton.pack()

    def show_info(self, msg):
        messagebox.showinfo(message=msg)

    def begin_spider(self):
        username = self.usernameipt.get()
        password = self.psdipt.get()
        print("账号{},密码{}, --{}".format(username, password, len(username)))
        if len(username)==0 or len(password)==0:
            self.show_info("账号或者密码为空")
            return
        self.app = WxAPI.AccountManager()
        print("开始登录，账号:{},密码:{}".format(username, password))
        self.app.login_by_user(username, password)

#  class WeChartUI(object):
    #  def __init__(self):
        #  self.root = tkinter.Tk()
        #  self.root.title = '微信文章拉取'
        #  self.ip_input = tkinter.Entry(self.root,width=30)
    #  def pack(self):
        #  self.ip_input.pack()

def test():
    from PIL import Image, ImageTk
    from tkinter import Label
    import os
    import tempfile
    #  f = tempfile.TemporaryFile()

    path=os.path.join(tempfile.gettempdir(), "login.jpg")
    #  path = os.path.join(os.path.tmp, "login.png")
    print("临时二维码文件:{}".format(path))
    # 存储二维码
    #  with open(path, "wb+") as fp:
        #  fp.write(img.content)
    # 显示二维码， 这里使用plt的原因是： 等待用户扫描完之后手动关闭窗口继续运行；否则会直接运行
    root = tk.Tk()
    try:
        img = Image.open(path)
        #  from tkinter import PhotoImage, Label
        img=ImageTk.PhotoImage(img)
        #  img_png = PhotoImage(file = path)
        label_img = Label(root, image = img)
        label_img.pack()
    except Exception:
        raise TypeError(u"账号密码输入错误，请重新输入")
    root.mainloop()
    #  plt.figure()
    #  plt.imshow(img)
    #  plt.show()



def main():
      app = Application()
    # 设置窗口标题:
      app.master.title('微信导入')
    # 主消息循环:
      app.mainloop()
    #  test()
    #  FL = WeChartUI()
    #  FL.pack()
    #  tkinter.mainloop()
    #  pass

if __name__ == "__main__":
    main()
