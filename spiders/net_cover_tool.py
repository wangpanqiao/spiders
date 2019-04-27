#!/usr/bin/env python
# -*- encoding: utf-8 -*-
 
'''
@Author  :   Anuo.
 
@License :   (C) Copyright 2018, Anuo's Studio
 
@Contact :   188512936@qq.com
 
@Software:   VS2017
 
@File    :   network_cover_tool.py
 
@Time    :   Mar 25,2019
 
@Desc    :   网络覆盖工具：不断的访问网络，刷新，然后覆盖之前的浏览痕迹。
            主要用于覆盖掉网警的历史记录。因为 ZF 的网络监管太可怕了。哈哈。
 
'''


import requests


def request_single_url(url):
    '''请求单个网址'''
    # 如果没有 http:// 头的，需要加上，不然会报异常
    if not "http" in url:
        url = "http://" + url
    html = requests.get(url)
    print(url)   # 请求就完事儿，无需做其他操作，目的很简单，就是单纯的访问网络。


def main_loop(url_list):
    '''主循环'''
    print("Start main loooooop...")
    while True:
        for url in url_list:
            try:
                request_single_url(url)
            except Exception as ex:
                print(ex.args)


def read_txt(txt_file):
    '''读取文件，返回url列表'''
    print("Read url list from txt file : " + txt_file)
    url_list = []
    with open(txt_file,'r') as f:
        line = f.readline()
        while(line):
            url_list.append(line)
            print(line)
            line = f.readline()

    return url_list


if __name__ == "__main__":
    '''自启动'''
    text_file = "address.txt"
    url_list = read_txt(text_file)
    if url_list != None and len(url_list) > 0:
        main_loop(url_list)



