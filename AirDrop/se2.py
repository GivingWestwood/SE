# -*- coding:utf-8 -*-
import psutil  # 用其获取IP地址
import qrcode
from tkinter import *  # GUI
from PIL import ImageTk
from flask import *
import os, json
import tkinter as tk  # 使用Tkinter前需要先导入
import threading
import tkinter.messagebox
import logging

from tkinter import Tk  #  获取剪切板Tk().clipboard_get()

app = Flask(__name__)
app.config.from_object(__name__)

# 禁用控制台
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


def GetNameByEveryDir(file_dir):
    # Input   Root Dir and get all img in per Dir.
    # Out     Every img with its filename and its dir and its path
    FileNameWithPath = []
    FileName = []
    FileDir = []
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            FileNameWithPath.append(os.path.join(root, file))  # 保存图片路径
            FileName.append(file)  # 保存图片名称
            FileDir.append(root[len(file_dir):])  # 保存图片所在文件夹
    return FileName, FileNameWithPath, FileDir


# 首页
@app.route('/')
def index():
    try:
        clip = Tk().clipboard_get()
    except BaseException:
        clip=''
#如果没有复制内容，会出错，所以如果没有复制内容就设为剪切板内容为''
    filepath = os.path.join(os.path.dirname(os.path.abspath('__file__')), 'tmp_file\\')
    # filepath="D:\\"
    if not os.path.exists(filepath):
        os.makedirs(filepath)
    FileName, FileNameWithPath, FileDir = GetNameByEveryDir(filepath)
    page = 1
    limit = 10
    start = (page - 1) * limit
    end = page * limit if len(FileName) > page * limit else len(FileName)
    ret = [FileName[i] for i in range(start, end)]
    all_page = int(len(FileName) / limit) + 1
    return render_template('up_video.html', file_list=ret, all_file=len(FileName), pages=page, all_page=all_page,clip=clip)


@app.route('/next_page/<int:page>/', methods=['GET'])
def next_page(page):
    filepath = os.path.join(os.path.dirname(os.path.abspath('__file__')), 'tmp_file\\')
    if not os.path.exists(filepath):
        os.makedirs(filepath)
    FileName, FileNameWithPath, FileDir = GetNameByEveryDir(filepath)
    limit = 10
    all_page = int(len(FileName) / limit) + 1
    pages = int(page)
    if pages <= 0:
        pages = 1
    elif pages >= all_page:
        pages = int(all_page)
    else:
        pages = int(page)
    start = (pages - 1) * limit
    end = pages * limit if len(FileName) > pages * limit else len(FileName)
    ret = [FileName[i] for i in range(start, end)]

    return render_template('up_video.html', file_list=ret, all_file=len(FileName), pages=pages, all_page=all_page)


@app.route('/tmp_file/<file_name>', methods=['GET'])
def tmp_file(file_name):
    try:
        filepath = os.path.join(os.path.dirname(os.path.abspath('__file__')), 'tmp_file')
        if not os.path.exists(filepath):
            os.makedirs(filepath)
        filename = file_name
        # #print(file_name)
        file = os.path.join(filepath, filename)
        return send_file(file)
    except Exception as e:
        return json.dumps({'code': "502"}, ensure_ascii=False)


@app.route('/up_video', methods=['post'])
def up_video():
    try:
        filepath = os.path.join(os.path.dirname(os.path.abspath('__file__')), 'tmp_file')
        if not os.path.exists(filepath):
            os.makedirs(filepath)
        for f in request.files.getlist('file'):
            if f and '/' in f.filename:
                # print('这是文件夹')
                temp_path = filepath + os.sep + f.filename.split('/')[0]
                if not os.path.exists(temp_path):
                    os.makedirs(temp_path)
                filename = f.filename.split('/')[1]
                upload_path = os.path.join(temp_path, filename)
                f.save(upload_path)
            elif f:
                # print('这是多文件')
                filename = f.filename
                upload_path = os.path.join(filepath, filename)
                f.save(upload_path)
            else:
                continue
        return render_template('up_video_ok.html')
    except Exception as e:
        print(e)
        return json.dumps({'code': "502"}, ensure_ascii=False)


def run_sever():
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)


def start():
    global l, l1, count, ip_list, len_list, chiose
    global tips
    if chiose == 0:
        thre = threading.Thread(target=run_sever)  # 创建一个线程运行服务器
        thre.setDaemon(True)
        thre.start()  # 运行线程

        tips.config(text='扫描二维码或输入最上面的地址访问管理页面')

        l1.config(text=ip_list[count])
        img = qrc_img(ip_list[count])
        QRCode_website = ImageTk.PhotoImage(img)
        l.config(image=QRCode_website)
        l.image = QRCode_website  # keep a reference
        count += 1
        chiose = 1
        tkinter.messagebox.showinfo('成功', '已开启服务！')
    else:
        tkinter.messagebox.showinfo('提示', '服务已运行！')


def getIP():
    """获取ipv4地址"""
    dic = psutil.net_if_addrs()
    ipv4_list = []
    for adapter in dic:
        # 网线端口：以太网，wifi端口：WLAN
        if '以太' in adapter or 'WLAN' in adapter:
            snicList = dic[adapter]
            for snic in snicList:
                if snic.family.name == 'AF_INET':
                    ipv4 = snic.address
                    if ipv4 != '127.0.0.1':
                        ipv4_list.append("http://" + ipv4 + ":5000")
    if len(ipv4_list) >= 1:
        return ipv4_list[::-1], len(ipv4_list)
    else:
        return []


def qrc_img(url):
    qr = qrcode.QRCode(version=2, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=11, border=2, )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image()
    return img


def show_qrc():
    global l, l1, count, ip_list, len_list, chiose
    global tips
    #tips='扫描二维码或输入最上面的地址访问管理页面'

    #l:二维码
    #l1:地址
    if chiose == 0:
        tkinter.messagebox.showinfo('错误', '请先开启服务')
    else:
        if count < len_list:
            # print(ip_list[count])
            tips.config(text='扫描二维码或输入最上面的地址访问管理页面')

            l1.config(text=ip_list[count])
            img = qrc_img(ip_list[count])
            QRCode_website = ImageTk.PhotoImage(img)
            l.config(image=QRCode_website)
            l.image = QRCode_website  # keep a reference

            count += 1

            #print(type(l))
            #print(type(l1))

        else:
            tkinter.messagebox.showinfo('错误', '设备未处于同一局域网下')
            count = 0
            tips.config(text='扫描二维码或输入最上面的地址访问管理页面')

            l1.config(text=ip_list[count])
            img = qrc_img(ip_list[count])
            QRCode_website = ImageTk.PhotoImage(img)
            l.config(image=QRCode_website)
            l.image = QRCode_website  # keep a reference

            count += 1


def open_dir():
    filepath = os.path.join(os.path.dirname(os.path.abspath('__file__')), 'tmp_file\\')
    if not os.path.exists(filepath):
        os.makedirs(filepath)
    os.system("start explorer %s" % filepath)

def delete_dir():
    filepath = os.path.join(os.path.dirname(os.path.abspath('__file__')), 'tmp_file\\')
    if not os.path.exists(filepath):
        os.makedirs(filepath)
    os.system("del /F /S /Q %s" % filepath)

def clipboard():
    clip = Tk().clipboard_get()
    #global clip2
    #clip2.config(text=clip)
    tkinter.messagebox.showinfo('剪切板内容', clip)

    #print(clip)
    #clip = clip.split()

def about():
    tkinter.messagebox.showinfo('帮助',
                                '开启服务后手机扫描显示的二维码等待页面打开，\n页面打不开说明有多个网口，\n需要切换二维码进行尝试。\n进入页面查看电脑下的文件，点击文件名下载文件到手机。\n选择手机页面中的上传文件将手机文件传到手机。')


def source():
    import webbrowser
    webbrowser.open("https://github.com/GivingWestwood?tab=repositories")


if __name__ == '__main__':
    root = Tk()
    winWidth = 700
    winHeight = 500

    # 获取屏幕分辨率
    screenWidth = root.winfo_screenwidth()
    screenHeight = root.winfo_screenheight()
    x = int((screenWidth - winWidth) / 2)
    y = int((screenHeight - winHeight) / 2)
    # 设置主窗口标题
    root.title("局域网传输文件")
    # 设置窗口初始位置在屏幕居中
    root.geometry("%sx%s+%s+%s" % (winWidth, winHeight, x, y))
    # 设置窗口图标
    root.iconbitmap("./img/logo.ico")
    # 设置窗口宽高固定
    root.resizable(0, 0)
    # 添加菜单栏
    f = tkinter.Menu(root)
    root['menu'] = f
    #f.add_command(label='关于', command=about)
    f.add_command(label='源码', command=source)
    # 增加背景图片
    photo = tk.PhotoImage(file="./img/bg.png")
    theLabel = tk.Label(root, text="", justify=tk.LEFT, image=photo, compound=tk.CENTER)
    #theLabel.place(relx=0.8, rely=0.63, anchor=CENTER)
    theLabel.place(relx=0.5, rely=0.5, anchor=CENTER)

    count = 0
    chiose = 0
    ip_list, len_list = getIP()
    Button(root, text='开启服务', command=start).place(relx=0.9, rely=0.05, anchor=CENTER)
    Button(root, text='更换网址', command=show_qrc).place(relx=0.9, rely=0.15, anchor=CENTER)
    Button(root, text='文件所在', command=open_dir).place(relx=0.9, rely=0.25, anchor=CENTER)
    Button(root, text='关闭服务', command=delete_dir).place(relx=0.9, rely=0.35, anchor=CENTER)#删除tmpfiles里的文件
    #Button(root, text='粘贴剪切板内容', command=clipboard).place(relx=0.9, rely=0.45, anchor=CENTER)#共享剪切板内容

    l = Label(root)
    l.place(relx=0.3, rely=0.5, anchor=CENTER) #二维码位置

    l1 = Label(root)
    l1.place(relx=0.3, rely=0.1, anchor=CENTER) #地址显示位置

    tips = Label(root)
    tips.place(relx=0.3, rely=0.9, anchor=CENTER) #提示信息位置

    #clip2 = Label(root)
    #clip2.place(relx=0.5, rely=0.9, anchor=CENTER) #粘贴板

    root.mainloop()
