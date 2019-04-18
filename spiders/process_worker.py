#!/usr/bin/env python
# -*- encoding: utf-8 -*-
 
'''
@Author  :   Anuo.
 
@License :   (C) Copyright 2019, Anuo's Studio
 
@Contact :   188512936@qq.com
 
@Software:   VS2017
 
@File    :   baidu_image_spider.py
 
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


num = 1

def save_pic(url, key_word):
    '''保存图片'''
    print(url)
    global num

    if not os.path.exists(key_word):
        os.mkdir(key_word)

    name = str(num) + '.jpg'
    path = "{0}/{1}".format(key_word, name)
    
    try:
        resp = requests.get(url, timeout=3)
        num += 1
        if resp.status_code == 200:
            data = resp.content
            with open(path, 'wb') as f:
                f.write(data)
    except Exception as ex:
        print(ex.args)