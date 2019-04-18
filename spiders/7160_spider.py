#!/usr/bin/env python
# -*- encoding: utf-8 -*-
 
'''
@Author  :   Anuo.
 
@License :   (C) Copyright 2010, Anuo's Studio
 
@Contact :   188512936@qq.com
 
@Software:   VS2017
 
@File    :   7160_spider.py
 
@Time    :   Mar 25,2019
 
@Desc    :   7160图片爬取。地址：https://www.7160.com/
 
'''


import os
import requests
from bs4 import BeautifulSoup   # pip install beautifulsoup4


def main_url(url):
    '''获取主页内容'''
    print(url)
    html = requests.get(url)
    soup_global = BeautifulSoup(html.text, features='html.parser')
    list = soup_global.find_all('a', attrs={'class':'addcss_a', "target":'_blank'})
    print(len(list))
    for item in list:
        title = item['title'].encode('UTF-8')
        topic_url = url + item['href']
        craw_each_topic(title, topic_url)


def craw_each_topic(title, topic_url):
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

    for item in index_list:
        craw_each_pic(item)


def craw_each_pic(index_url):
    '''爬取具体的图片'''
    html = requests.get(index_url)
    soup = BeautifulSoup(html.text, features='html.parser')
    picsbox_node = soup.find('div', attrs={'class':'picsbox picsboxcenter'})
    img_node = picsbox_node.find('img')
    src = img_node['src']
    title = img_node['alt']
    save_img(src, title)


def save_img(src, title):
    '''下载图片'''
    print(src)
    if not os.path.exists(title):
        os.mkdir(title)

    name = os.path.basename(src)
    path = "{0}/{1}".format(title, os.path.basename(src))
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
    main_url(url)