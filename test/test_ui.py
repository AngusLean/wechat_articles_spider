# coding: utf-8
import tkinter as tk
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
        self.textbox = tk.Text(self.window)
        self.textbox.grid(column=2, row=4)
        #重定向输出
        import sys
        sys.stdout = TextRedirector(self.textbox, "stdout")
        sys.stderr = TextRedirector(self.textbox, "stderr")

    def createWidgets(self):
        self.helloLabel = tk.Label(self, text='输入公众平台账号')
        self.helloLabel.pack()
        self.accountInput = tk.Entry(self)
        self.accountInput.pack()
        self.psdInput = tk.Entry(self)
        self.psdInput.pack()
        self.quitButton = tk.Button(self, text='Quit', command=self.quit)
        self.quitButton.pack()
        self.okButton = tk.Button(self, text='开始抓取', command=self.quit)
        self.okButton.pack()

    def show_info(self, msg):
        tk.messagebox.showinfo(message=msg)

    def begin_spider(self):
        username = self.usernameipt.get()
        password = self.psdipt.get()
        print("{}.{}".format(username, password))
        if username is None or password is None:
            self.show_info("账号或者密码错误")
            return
        self.app = WxAPI.AccountManager()
        self.app.login_by_user(username, password)

#  class WeChartUI(object):
    #  def __init__(self):
        #  self.root = tkinter.Tk()
        #  self.root.title = '微信文章拉取'
        #  self.ip_input = tkinter.Entry(self.root,width=30)
    #  def pack(self):
        #  self.ip_input.pack()

def main():
    app = Application()
    # 设置窗口标题:
    app.master.title('微信导入')
    # 主消息循环:
    app.mainloop()
    #  FL = WeChartUI()
    #  FL.pack()
    #  tkinter.mainloop()
    #  pass

if __name__ == "__main__":
    main()
