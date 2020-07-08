import tempfile
import os
from PIL import Image, ImageTk
from tkinter import Label,Tk
import tkinter as tk
path=os.path.join(tempfile.gettempdir(), "login.png")
#  path = "C:\\Users\\timoyyu\\Desktop\\test.jpeg"
#  try:
window = Tk()
usernameipt = tk.Entry(window)
psdipt = tk.Entry(window)
quitButton = tk.Button(window, text='开始')
usernameipt.grid(column=1, row=0)
psdipt.grid(column=2, row=0)
quitButton.grid(column=1, row=1)
img = Image.open(path)
#  from tkinter import PhotoImage, Label
img=ImageTk.PhotoImage(img)
#  img_png = PhotoImage(file = path)
label_img = Label(window, image = img)
#  label_img.grid(column=3, row=3)
label_img.grid(column=3, row=3)

window.mainloop()
