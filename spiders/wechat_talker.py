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
#import he_weather_spider as he
import yahoo_weather_spider as yahoo


def get_response(msg):
    '''获取自动聊天消息'''
    apiUrl = 'http://www.tuling123.com/openapi/api'   #改成你自己的图灵机器人的api，上图红框中的内容，不过用我的也无所谓，只是每天自动回复的消息条数有限
    data = {
        'key': '769e14179d3844948f04364d92fbd14b',  # Tuling Key 
        'info': msg,  # 这是我们发出去的消息
        'userid': 'wechat-robot',  # 这里你想改什么都可以
    }
    # 我们通过如下命令发送一个post请求
    r = requests.post(apiUrl, data=data).json()
    return r.get('text')


def fun_timer():
    '''定时器'''

    global hour, minute, context
    now = datetime.datetime.now()
    if now.hour == hour and now.minute == minute:
        # 发送问候语
        send_chat_room_msg(chat_room_name, greeting_content)
        msg = "{0}> 在群[{1}]中发送问候语[{2}]。".format(now.strftime('%Y-%m-%d %H:%M:%S'), chat_room_name, greeting_content)
        print(msg)

        # 获取天气信息并发送
        #msg = he.get_weather()
        #if msg:
        #    send_chat_room_msg(chat_room_name, msg)
        #    print(msg)

        city_list = ['Richmond','Vancouver','Burnaby']
        for city_name in city_list:
            msg = yahoo.get_weather(city_name.lower())
            if msg:
                send_chat_room_msg(chat_room_name, msg)
                print(msg)
            else:
                print('获取 {0} 天气信息失败。'.format(city_name))


    global timer
    timer = threading.Timer(60, fun_timer)
    timer.start()


#@itchat.msg_register(itchat.content.TEXT)   # 监听好友消息
#def print_content(msg):
#    '''监听谁给我发消息，自动回复'''
#    return get_response(msg)


@itchat.msg_register([itchat.content.TEXT], isGroupChat=True)   # 监听群消息
def print_content(msg):
    #if msg.User['NickName'].strip() == 'F4+三菜一汤' or msg.User['NickName'].strip() == '测试' or msg.User['NickName'].strip() == '致青春':
    if msg.User['NickName'].strip() == chat_room_name:
        return get_response(msg['Text'])
    else:
        pass


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
greeting_content = "各位，早上好！"
timer = threading.Timer(1, fun_timer)
hour = 13        #  hour
minute = 31      #  minute


if __name__ == "__main__":
    '''自启动'''

    hour = int(input('请输入定时器的时间（小时）：'))
    minute = int(input("请输入定时器的时间（分钟）："))
    chat_room_name = input("请输入群名称：")
    greeting_content = input("请输入问候语：")

    itchat.auto_login(enableCmdQR=True, hotReload=True)  # 登录微信
    timer.start()  # 启动定时器
    itchat.run()



