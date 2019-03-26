#!/usr/bin/env python
# -*- encoding: utf-8 -*-
 
'''
@Author  :   Anuo.
 
@License :   (C) Copyright 2018, Anuo's Studio
 
@Contact :   188512936@qq.com
 
@Software:   VS2017
 
@File    :   7160_spider_multi_thread.py
 
@Time    :   Mar 26,2019
 
@Desc    :   7160图片爬取，引入多线程，加快下载。地址：https://www.7160.com/
 
'''


import os
import requests
from bs4 import BeautifulSoup   # pip install beautifulsoup4
from threading import Thread
from queue import Queue


class ProcessWorker(Thread):
    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            src = self.queue.get()
            craw_each_pic(src)


def get_index_list(url):
    '''获取主页内容'''
    html = requests.get(url)
    soup_global = BeautifulSoup(html.text, features='html.parser')
    list = soup_global.find_all('a', attrs={'class':'addcss_a', "target":'_blank'})

    index_list = []
    for item in list:
        topic_url = url + item['href']
        topic_list = get_each_topic(topic_url)

        for src in topic_list:
            index_list.append(src)

    return index_list


def get_each_topic(topic_url):
    '''爬取每一个主题'''
    print(topic_url)
    html = requests.get(topic_url)
    soup = BeautifulSoup(html.text, features='html.parser')
    itempage_node = soup.find('div', attrs={'class':'itempage'})
    page_list = itempage_node.find_all('a')
    mlen = len(page_list)
    index_list = []
    for item in page_list:
        if item.text.isdigit():
            url = topic_url + item['href']
            index_list.append(url)

    return index_list


def craw_each_pic(index_url):
    '''爬取具体的图片'''
    try:
        html = requests.get(index_url)
        soup = BeautifulSoup(html.text, features='html.parser')
        picsbox_node = soup.find('div', attrs={'class':'picsbox picsboxcenter'})
        if picsbox_node != None:
            img_node = picsbox_node.find('img')
            src = img_node['src']
            title = img_node['alt']
            save_img(src, title)
    except Exception as ex:
        print(ex.args)


def save_img(src, title):
    '''下载图片'''
    print(src)
    if not os.path.exists('data'):
        os.mkdir('data')

    # 不能一直建多级目录，只能这样建目录，需要看下其他方法
    if not os.path.exists('data\\' + title):
        os.mkdir('data\\' + title)

    name = os.path.basename(src)
    path = "{0}/{1}/{2}".format('data', title, os.path.basename(src))
    if os.path.exists(path):
        return   # 如果文件已存在就不需要再次下载

    try:
        resp = requests.get(src, timeout=3)  # 设置超时时间，因有些图片下载不下来，不需要一直等待
        if resp.status_code == 200:
            data = resp.content
            with open(path, 'wb') as f:
                f.write(data)
    except Exception as ex:
        print(ex.args)


if __name__ == "__main__":
    '''启动函数'''
    url = 'https://www.7160.com/'
    list = get_index_list(url)
    if len(list) > 0:
        queue = Queue()   # Create a queue to communicate with the worker therads
        for x in range(4):  # 创建4个工作线程
            worker = ProcessWorker(queue)
            worker.daemon = True   # 将daemon设置为True将会使主线程退出，即使worker都阻塞了
            worker.start()

        for item in list:  # put the tasks into the queue
            queue.put(item)

        queue.join()   # 让主线程等待队列完成所有的任务
        print('下载完成，去欣赏吧。')
    else:
        print('没有下载到地址哦，sorry')
