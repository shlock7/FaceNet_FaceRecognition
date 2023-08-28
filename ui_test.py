from tkinter import *
import tkinter.messagebox
from tkinter.simpledialog import *
import time

from tkinter import filedialog
import cv2 as cv

def xz(s='提示'):
    answer=tkinter.messagebox.askokcancel(s,'请选择确定或取消')

def Input():
     s1 = askstring('提示','请输入工号')
     print(s1)
     s2 = askstring('提示','请输入姓名')
     print(s2)

def camera():
     s = '摄像头录入'
     xz(s)

def gettime():
      timestr = time.strftime("%H:%M:%S") # 获取当前的时间并转化为字符串
      Timelb.configure(text=timestr)   # 重新设置标签文本
      root.after(1000,gettime) # 每隔1s调用函数 gettime 自身获取时间

root = Tk()
root.title('菜单实验')
root.geometry('800x600')

Timelb = tkinter.Label(root,text='',bg='#d3fbfb',fg='black',font=("黑体",66))
Timelb.pack()
gettime()

lb = Label(root,text='员工刷脸签到系统',\
        bg='#d3fbfb',\
        fg='red',\
        font=('华文新魏',32),\
        width=20,\
        height=2,\
        relief=SUNKEN)
lb.pack()

def newwind():
      winNew = Toplevel(root)
      help_text = "人脸录入："
      txt2 = "摄像头录入：录入时会出现人脸的小窗口，待人脸被完整的框出是按ESC键结束即可\n"
      winNew.geometry('320x240')
      winNew.title('Help')
      lb1 = Label(winNew,text=help_text)
      lb2 = Label(winNew,text=txt2)
      # lb2.place(relx=0.2,rely=0.2)
      lb1.grid(row=0)
      lb2.grid(row=1)
      btClose=Button(winNew,text='关闭',command=winNew.destroy)
      btClose.place(relx=0.7,rely=0.5)
      
      
# print(tkinter.messagebox.askyesno(title='Hi', message='你好！'))     # return 'True', 'False'
# path = tkinter.filedialog.askopenfilename() # 获取文件路径
# print(path)

# ID = askstring('提示','请输入工号')
# name = askstring('提示','请输入姓名')

# print(ID)
# print(name)
# print(name == None)

newwind()

mainmenu = Menu(root)

menuFace = Menu(mainmenu,tearoff=0) # tearoff=0去掉那个横线
mainmenu.add_cascade(label="人脸录入",menu=menuFace)
menuFace.add_command(label="摄像头录入",command=Input) #动作只写函数名
menuFace.add_command(label="本地文件录入",command=camera)


menuSign = Menu(mainmenu,tearoff=0)
mainmenu.add_cascade(label="刷脸签到",menu=menuSign)
menuSign.add_command(label="开始签到",command=newwind)
menuSign.add_command(label="结束签到",command=camera)

menuLog = Menu(mainmenu,tearoff=0)
mainmenu.add_cascade(label="考勤日志",menu=menuLog)
menuLog.add_command(label="查看考勤记录",command=camera)

mainmenu.add_command(label="帮助",command=camera)


root.config(menu=mainmenu)

root.mainloop()