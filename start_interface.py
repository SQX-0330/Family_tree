from tkinter import *
from PIL import Image, ImageTk
from person import management_interface
import wx


# 开始界面
def main():
    s = Image.open("main.jfif")
    win = Tk()
    win.title("家谱信息管理系统")
    win.geometry("680x480+50+50")

    image3 = ImageTk.PhotoImage(s)

    label = Label(win, text="家族传承由此开始！", image=image3, compound="center", font="小篆 30 bold")
    label.bind("<Button-1>", open_management_interface)
    label.pack()
    win.mainloop()


# 家谱所有信息界面
def information_interface(information):
    image = Image.open("information_interface.jpg")
    win = Toplevel()
    image1 = ImageTk.PhotoImage(image)

    label = Label(win, image=image1, text=information, font="楷书 10 bold", compound="center", wraplength= 600)
    label.pack()

    win.mainloop()


# 管理家谱界面
def open_management_interface(event):
    app = wx.App()
    frame = management_interface.TreeCtrlFrame(None)
    frame.Show()
    app.MainLoop()


if __name__ == "__main__":
   main()
