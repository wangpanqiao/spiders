#!/usr/bin/env python
# -*- encoding: utf-8 -*-
 
'''
@Author  :   Anuo.
 
@License :   (C) Copyright 2019, Anuo's Studio
 
@Contact :   188512936@qq.com
 
@Software:   VS2017
 
@File    :   wechat_talker.py
 
@Time    :   Apr 27,2019
 
@Desc    :   微信自动聊天助手：定时发送消息 + 自动聊天

'''

import itchat      # pip install itchat
from itchat.content import *
import requests
import threading
import datetime
import time



def fun_timer():
    '''定时器'''

    global hour, minute, context
    now = datetime.datetime.now()
    if now.hour == hour and now.minute == minute:
        send_chat_room_msg(chat_room_name, context)

    global timer
    timer = threading.Timer(60, fun_timer)
    timer.start()


#@itchat.msg_register(INCOME_MSG)
def text_replay(msg):
    '''监听谁给我发消息，自动回复'''
    print(msg)
    itchat.send("你好，微信正处于托管状态，我看到消息之后会立即回复您。")


def send_chat_room_msg(room_name, msg):
    '''发送群消息'''

    # 获取群组所有的相关信息（注意最好保存到通信录）
    my_rooms = itchat.get_chatrooms(update=True)
    # 传入制定群名进行搜索，只说是搜索，是因为群员的名称信息也在里面
    my_rooms = itchat.search_chatrooms(name=room_name)
    success = False
    for room in my_rooms:
        if room['NickName'] == room_name:
            username = room['UserName']
            # 得到群名的唯一标识，然后发送信息
            itchat.send_msg(msg, username)
            success = True
            break
        
    if not success:
        print("发送群消息[ {0} ]失败！", msg)


        

chat_room_name = "测试"
context = "abcdefg"
timer = threading.Timer(1, fun_timer)
hour = 13  # hour
minute = 31      #  minute


if __name__ == "__main__":
    '''自启动'''

    itchat.auto_login(enableCmdQR=True, hotReload=True)
    timer.start();

    itchat.run()
    start_time_to_send_thread()



