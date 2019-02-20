#!/usr/bin/env python
# -*- encoding: utf-8 -*-
 
'''
@Author  :   Anuo.
 
@License :   (C) Copyright 2018, Anuo's Studio
 
@Contact :   188512936@qq.com
 
@Software:   VS2017
 
@File    :   search_engine_spider.py
 
@Time    :   Feb 16,2019
 
@Desc    :   搜索引擎结果提取，界面已简单完成

'''

from bs4 import *     # pip install beautifulsoup4
from tkinter import *


class Application():

    def __init__(self):

        root = Tk()
        root.title('Hello An')
        root.geometry('400x200');
        root.resizable(width=False, height=False)
        root.iconbitmap("dolphin.ico")

        # Baidu 的部件
        baidu_frame = Frame(root)
        # Label
        Label(baidu_frame, text="百度 ", font=("Arial", 16)).pack(side = LEFT)
        # Entry
        baidu_text = StringVar()
        Entry(baidu_frame, textvariable=baidu_text, font=("Arial", 16)).pack(side = LEFT)
        # Label
        Label(baidu_frame,text=" ", font=("Arial", 16)).pack(side = LEFT)
        # Button
        Button(baidu_frame, text='Export', font=("Arial", 10), command = self.baidu_export).pack(side = LEFT)
        baidu_frame.pack(side = TOP)

        # Google 的部件
        google_frame = Frame(root)
        # Label
        Label(google_frame, text="谷歌 ", font=("Arial", 16)).pack(side = LEFT)
        # Entry
        google_text = StringVar()
        Entry(google_frame, textvariable=google_text, font=("Arial", 16)).pack(side = LEFT)
        # Label
        Label(google_frame,text=" ", font=("Arial", 16)).pack(side = LEFT)
        # Button
        Button(google_frame, text='Export', font=("Arial", 10), command = self.google_export).pack(side = LEFT)
        google_frame.pack(side = TOP)

        # Sougou 的部件
        sougou_frame = Frame(root)
        # Label
        Label(sougou_frame, text="搜狗 ", font=("Arial", 16)).pack(side = LEFT)
        # Entry
        sougou_text = StringVar()
        Entry(sougou_frame, textvariable=sougou_text, font=("Arial", 16)).pack(side = LEFT)
        # Label
        Label(sougou_frame,text=" ", font=("Arial", 16)).pack(side = LEFT)
        # Button
        Button(sougou_frame, text='Export', font=("Arial", 10), command = self.sougou_export).pack(side = LEFT)
        sougou_frame.pack(side = TOP)

         # 360 的部件
        f360_frame = Frame(root)
        # Label
        Label(f360_frame, text="360  ", font=("Arial", 16)).pack(side = LEFT)
        # Entry
        f360_text = StringVar()
        Entry(f360_frame, textvariable=f360_text, font=("Arial", 16)).pack(side = LEFT)
        # Label
        Label(f360_frame,text=" ", font=("Arial", 16)).pack(side = LEFT)
        # Button
        Button(f360_frame, text='Export', font=("Arial", 10), command = self.f360_export).pack(side = LEFT)
        f360_frame.pack(side = TOP)

        # Good Luck
        good_luck_frame = Frame(root)
        # Image
        img_gif = PhotoImage(file = 'good_luck.gif')
        Label(good_luck_frame, image = img_gif).pack(side = LEFT)
        # Label
        Label(good_luck_frame,text="Good Luck !", fg="red", font=("Calibri", 24)).pack(side = LEFT)
        good_luck_frame.pack(side = TOP)

        root.mainloop()


    def baidu_export(self):
        print('baidu_export')


    def sougou_export(self):
        print("sougou_export")


    def google_export(self):
        print('google_export')


    def f360_export(self):
        print('f360_export')


if __name__ == "__main__":
    app = Application()


