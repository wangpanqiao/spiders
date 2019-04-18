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

import requests
from bs4 import BeautifulSoup   # pip install beatifusoup4
import re
import threading as Thread
from queue import Queue
import os
from process_worker import ProcessWorker


def get_page_urls(url):
    '''根据第一页获取其他页'''

    try:
        result = requests.get(url)

        page_soup = BeautifulSoup(result.text, features='html.parser')
        page_node = page_soup.find('div', attrs={'id':'page'})
        page_node_list = page_node.find_all('a')

        page_urls = []
        for node in page_node_list:
            sub_url = node['href']   # /search/flip?tn=baiduimage&ie=utf-8&word=55&pn=20&gsm=3c&ct=&ic=0&lm=-1&width=0&height=0
            if 'search' in sub_url:
                url = 'http://image.baidu.com/' + sub_url
                page_urls.append(url)

        return page_urls
    except requests.ConnectionError:
        print('Fail to connect !')


def get_img_urls(page_url):
    print(page_url)

    response = requests.get(page_url)

    # https://www.cnblogs.com/nnngu/p/8410903.html
    pic_urls = re.findall('"objURL":"(.*?)",', response.text, re.S)
    return pic_urls

    #soup = BeautifulSoup(response.text, features='html.parser')
    #imgitem_node_list = soup.find_all('li', attrs={'class':'imgitem'})

    #img_url_list = []
    #for node in imgitem_node_list:
    #    img_url = get_img_url(node)
    #    img_url_list.append(img_url)

    #return img_url_list
    

def get_img_url(imgitem_node):
    node = imgitem_node.find('a', attrs={'target':'_self', 'class':'down'})
    onclick_title_href = node['href']   # 以‘;'分割，然后去最后
    urltext = onclick_title_href.split(';')[-1]
    img_url = urltext.split('=')[-1]
    return img_url


if __name__ == "__main__":
    '''自启动，脚本入口'''

    # global key_word    
    key_word= input("请输入要搜索的关键字词： ")
    
    url = 'http://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&word=' + key_word + '&ct=201326592&v=flip'
    page_urls = []   # 缓存页面字典
    page_urls.append(url);   # 添加第一页
    other_page_urls = get_page_urls(url)
    if other_page_urls:
        for page_url in other_page_urls:
            page_urls.append(page_url)

    img_urls = []
    for url_item in page_urls:
        url_list = get_img_urls(url_item)
        for item in url_list:
            img_urls.append(item)

    print("共有 {} 张图片需要下载。".format(len(img_urls)))
    
    if not os.path.exists(key_word):
        try:
            os.mkdir(key_word)   # 多线程调用可能抛异常，最好放到前面创建路径
        except Exception as ex:
            pass

    # 多线程下载
    queue = Queue()   # Create a queue to communicate with the worker therads
    for x in range(4):  # 创建4个工作线程
        worker = ProcessWorker(queue, key_word)
        worker.daemon = True   # 将daemon设置为True将会使主线程退出，即使worker都阻塞了
        worker.start()

    for item in img_urls:
        queue.put(item)

    queue.join()  # 等待队列完成所有的任务
    print('下载完成，去欣赏吧。')
