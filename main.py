from collect_frame_to_csv import collect_frame_to_csv,face_from_local,image_to_csv
import tensorflow as tf
from tkinter import *
from  tkinter import ttk
import tkinter.messagebox
from tkinter.simpledialog import *
import time
from PIL import Image, ImageTk
import detect_face
import cv2
from cal_128XVector_user_facenet import cal_128_vector,build_facenet_model,cal_dist_from_csv
import pandas as pd
from tkinter import filedialog
import numpy as np

root = Tk()
root.title('员工签到系统')

# 保存签到记录
def save_record(ID,name):
    cur_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    tmp = {
    'time':cur_time,
    "ID": ID,
    "name": name
    }
    # 将考勤记录保存到一个csv里
    record = pd.DataFrame(tmp,index = [0])
    print("*"*20)
    print(record)
    # 此信息要向文件中追加写入
    # record.to_csv('./data/record_data.csv',index=False)
    record.to_csv('./data/record_data.csv',mode='a',header=False,index=False) # 不保留左边的索引列

# 人脸识别主函数
def realtime_detect(csv_dir= './data/data.csv'):
    # csv_dir = './data/data.csv'#人脸128向量的数据
    # 调用facenet模型
    sess1, images_placeholder, phase_train_placeholder, embeddings = build_facenet_model()
    image_size = 200
    minsize = 20
    threshold = [0.6, 0.7, 0.7]
    factor = 0.709  # scale factor
    # print("Creating MTcnn networks and load paramenters..")

    # 建立MTCNN
    with tf.Graph().as_default():
        sess = tf.Session()
        with sess.as_default():
            pnet, rnet, onet = detect_face.create_mtcnn(sess, './model/')

    capture = cv2.VideoCapture(0)
    # 读取信息文件
    info_data = pd.read_csv('./data/info_data.csv')

    while (capture.isOpened()):
        ret, frame = capture.read()
        bounding_box, _ = detect_face.detect_face(frame, minsize, pnet, rnet, onet, threshold, factor)

        nb_faces = bounding_box.shape[0]  # 人脸检测的个数
        # 标记人脸
        for face_position in bounding_box:
            rect = face_position.astype(int)
            image=frame[rect[1]:rect[3],rect[0]:rect[2]]#截取人脸的ROI区域
            array=cal_128_vector(image,sess1, images_placeholder, phase_train_placeholder, embeddings)#计算人脸的128向量
            dist,label=cal_dist_from_csv(csv_dir,array) # 返回最小距离和人脸所属标签
            # 识别到人怎么输出？
            # 
            # label是得到的ID，要根据ID找到对应的姓名

            id_res = '-3'
            name = info_data[(info_data.ID == int(label))]
            if name.shape[0] == 0: # 不存在是一种异常情况
                continue
            id_res = name.values[0][1]

            # 矩形框
            cv2.rectangle(frame, (rect[0], rect[1]), (rect[2], rect[3]), (0, 255, 255), 2, 1)
            cv2.putText(frame, "faces:%d" % (nb_faces), (10, 20), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 255), 4)
            cv2.putText(frame, '%.2f' % (dist), (rect[0], rect[1] - 30), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 255), 4)
            cv2.putText(frame, id_res, (rect[0], rect[1] ), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 255), 4)
            
            # 对检测到的人脸进行询问：
            if id_res == '-3':
                continue
            else:
                ask = tkinter.messagebox.askyesno(title='Hi', message='你好！'+id_res+"!")
                if ask == True:
                    save_record(int(label),id_res)

        cv2.imshow('Video', frame)
        if cv2.waitKey(1) & 0xff == 27: #ESC键退出
            break
    capture.release()
    cv2.destroyAllWindows()

def popNote(s='提示',note='已完成'):
    answer = tkinter.messagebox.showinfo(s,note)

# 提示输入身份信息
def inputInfo():
    ID = '-1'
    name = '-1'
    ID = askstring('提示','请输入工号')
    name = askstring('提示','请输入姓名')
    return ID,name

# 从摄像头获取人脸数据
def collect_from_camera():
    ID,name = inputInfo()
    # 中途取消就返回
    if(ID == None or name == None):
        return
    collect_frame_to_csv(ID) # 考虑到重名的问题，用ID表示不同人脸
    print("信息录入完毕！")
    tmp = {
    "ID": ID,
    "name": name
    }
    # 将姓名，工号信息保存到一个csv里
    info = pd.DataFrame(tmp,index = [0])
    print("*"*20)
    print(info)
    # 此信息要向文件中追加写入
    info.to_csv('./data/info_data.csv',mode='a',header=False,index=False) # 不保留左边的索引列
    popNote('提示',"信息录入完毕！")

# 从本地文件获取人脸数据
def collect_from_local():
    ID,name = inputInfo()
    # 中途取消就返回
    if(ID == None or name == None):
        return
    
    # 这里添加从文件读入数据的函数
    path = tkinter.filedialog.askopenfilename() # 获取文件路径
    print(path)
    # =============================================================  注意：这个路径不能有中文!!!!!
    img = face_from_local(path)
    test_type = np.ndarray(1)
    if type(img) != type(test_type):
        popNote('提示',"人脸数大于1，无法录入！")
        return
    
    # 根据展示的结果选择是否要保存
    ask = tkinter.messagebox.askyesno(title='提示', message='是否保存？')
    if ask == False:
        return
    
    image_to_csv(img, label=ID, csv_dir='./data/data.csv')
    
    tmp = {
    "ID": ID,
    "name": name
    }
    info = pd.DataFrame(tmp,index = [0])
    print("*"*20)
    print(info)
    # 此信息要向文件中追加写入
    info.to_csv('./data/info_data.csv',mode='a',header=False,index=False)
    popNote('提示',"信息录入完毕！")

# 开启人脸识别签到
def realtime_detect_face():
    realtime_detect()

# 获取时间（年-月-日 小时：分钟：秒）
Timelb2 = tkinter.Label(root,text='',fg='black',font=("黑体",32))
def gettime():
    timestr = time.strftime("%Y-%m-%d %H:%M:%S") # 获取当前的时间并转化为字符串
    Timelb2.configure(text=timestr)   # 重新设置标签文本
    root.after(1000,gettime) # 每隔1s调用函数 gettime 自身获取时间

# 获取当前日期（年-月-日）
def get_current_time():
    current_time = time.strftime('%Y-%m-%d',time.localtime(time.time()))
    return current_time

# 查看考勤记录
def view_record():
    sign_in_record = pd.read_csv('./data/record_data.csv')
    print(sign_in_record)
    # time ID  name
    winNew = Toplevel(root)
    winNew.title('签到记录')
    # winNew.geometry("600x500+200+20")
    tree = ttk.Treeview(winNew,show="headings")      # #创建表格对象
    tree["columns"] = ("时间", "ID", "姓名")     # #定义列
    tree.column("姓名", width=100,anchor='center')          # #设置列
    tree.column("时间", width=200,anchor='center')
    tree.column("ID", width=100,anchor='center')
    tree.heading("姓名", text="姓名")        # #设置显示的表头名
    tree.heading("时间", text="签到时间")
    tree.heading("ID", text="ID")

    sign_in_data = sign_in_record.values
    # 向表格中加入数据
    for i in range(sign_in_data.shape[0]):
        tree.insert('', i, values=(sign_in_data[i][0], sign_in_data[i][1], sign_in_data[i][2]))
    tree.pack()

# ========================================================== Not yet completed ///////
# 获取帮助文档函数
def get_help_doc():
    popNote('提示',"请阅读文件目录下的Help.txt文件！")

# ========================================================== Not yet completed ///////
# 结束签到函数
def end_sign_in():
    popNote('提示',"尚未完成！")


def main():
    # root = Tk()
    # root.title('员工签到系统')
    # root.geometry('800x600')
    
    lb = Label(root,text='员工刷脸签到系统',\
            #bg='#d3fbfb',\
            fg='red',\
            font=('华文新魏',66),\
            width=20,\
            height=2,\
            relief=SUNKEN)
    lb.grid(row=0,columnspan=2)

    # Timelb = tkinter.Label(root,text='',fg='black',font=("黑体",32))
    # timestr = get_current_time() # 获取当前的时间
    # print("********************time:",timestr)
    # Timelb.configure(text=timestr)   # 重新设置标签文本
    # Timelb.grid(row=2,columnspan=2)
    
    # 设置图片
    photo=PhotoImage(file="qdu.png")
    label=Label(image=photo)
    label.image=photo
    label.grid(row=1,columnspan=2)

    # 时间显示，不断更新
    # Timelb2.grid(row=4,columnspan=2)
    Timelb2.grid(row=2,columnspan=2)
    gettime()
    
    # 设置按钮
    start_b = tkinter.Button(root, text='开始签到', font=('黑体', 12), width=10, height=5, command=realtime_detect_face)
    start_b.grid(row=3,column=0)

    end_b = tkinter.Button(root, text='结束签到', font=('黑体', 12), width=10, height=5, command=root.destroy)
    end_b.grid(row=3,column=1)


    # 设置菜单
    mainmenu = Menu(root)

    menuFace = Menu(mainmenu,tearoff=0) # tearoff=0去掉那个横线
    mainmenu.add_cascade(label="人脸录入",menu=menuFace)
    menuFace.add_command(label="摄像头录入",command=collect_from_camera) #动作只写函数名
    menuFace.add_command(label="本地文件录入",command=collect_from_local)


    menuSign = Menu(mainmenu,tearoff=0)
    mainmenu.add_cascade(label="刷脸签到",menu=menuSign)
    menuSign.add_command(label="开始签到",command=realtime_detect_face)
    menuSign.add_command(label="结束签到",command=root.destroy)

    menuLog = Menu(mainmenu,tearoff=0)
    mainmenu.add_cascade(label="考勤日志",menu=menuLog)
    menuLog.add_command(label="查看考勤记录",command=view_record)

    mainmenu.add_command(label="帮助",command=get_help_doc)


    root.config(menu=mainmenu)

    root.mainloop()


if __name__ == "__main__":
    config = tf.ConfigProto()
    config.gpu_options.allow_growth = True
    with tf.Session(config=config) as session:  # 解决GPU缓存不足报错
        main()
