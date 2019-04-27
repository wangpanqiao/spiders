#!/usr/bin/env python
# -*- encoding: utf-8 -*-
 
'''
@Author  :   Anuo.
 
@License :   (C) Copyright 2019, Anuo's Studio
 
@Contact :   188512936@qq.com
 
@Software:   VS2017
 
@File    :   process_worker.py
 
@Time    :   Apr 17,2019
 
@Desc    :   百度图片搜索爬虫。研究下，看能否直接从百度的图片搜索结果爬取图片。
 
'''
        
from threading import Thread
import os
import requests
        
class ProcessWorker(Thread):   # 这个类还不能放在前面，不然会报参数数量不对的错
    def __init__(self, queue, key_word):
        Thread.__init__(self)
        self.queue = queue
        self.key_word = key_word

    def run(self):
        while True:
            url = self.queue.get()
            save_pic(url, self.key_word)


def save_pic(url, key_word):
    '''保存图片'''
    #print(url)
    name = os.path.basename(url)
    
    #只有名字的   + .jpg
    #如果包含 .jpg 但不以 jpg结尾 + .jpg
    #如果包含 .jpeg 但不以 jpg结尾 + .jpg
    #如果包含 .png 但不以 png结尾 + .png
    if '.' not in name:
        name += '.jpg'
    elif '.jpg' in name and not name.endswith('.jpg'):
        name += '.jpg'
    elif '.jpeg' in name and not name.endswith('.jpeg'):
        name += '.jpg'
    elif '.png' in name and not name.endswith('.png'):
        name += '.png'

    path = "{0}/{1}".format(key_word, name)
    if os.path.exists(path):
        print('已存在： ' + path)
        return  # 如果文件已存在，则不用再次下载
    
    try:
        resp = requests.get(url, timeout=3)
        if resp.status_code == 200:
            data = resp.content
            with open(path, 'wb') as f:
                f.write(data)
                print('已下载： ' + path)
    except Exception as ex:
        print('下载失败： ' + name)
        #print(ex.args)
        pass