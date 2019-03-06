#!/usr/bin/env python
# -*- encoding: utf-8 -*-
 
'''
@Author  :   Anuo.
 
@License :   (C) Copyright 2018, Anuo's Studio
 
@Contact :   188512936@qq.com
 
@Software:   VS2017
 
@File    :   meizhuo_spider.py
 
@Time    :   Aug 22,2018
 
@Desc    :   美桌网美女图片爬虫。
 
'''

import os
import sys
import requests
from bs4 import BeautifulSoup      # pip install beautifulsoup4
from multiprocessing.pool import Pool


def main():
    '''主流程：提取图集，然后启动多线程对每个图集的图进行下载'''

    url = 'http://www.win4000.com/meitu.html'
    resp = requests.get(url)
    if resp.status_code  == 200:
        soup = BeautifulSoup(resp.text,'lxml')
        lis = soup.find_all(name='div',attrs={'class':"list_cont list_cont2 w1180"})
        image_dict = {}

        for node in lis:
            lis2 = node.find_all(name = 'li')
            for node2 in lis2:
                name = node2.p.string
                url2 = node2.a.attrs['href']
                image_dict[name] = url2

        if image_dict:
            deal_image_dict(image_dict)


def deal_image_dict(image_dict):
    '''多线程下载每一个图集'''

    sys.setrecursionlimit(10000) #例如这里设置为一百万
    pool = Pool()
    pool.map(deal_each,image_dict.items())
    pool.close()
    pool.join()


def deal_each(item):
    '''下载每一个图集'''

    name = item[0]
    url = item[1]

    if not os.path.exists(name):
        os.mkdir(name)

    #替换.html      如    html  - >  _1.html
    resp = requests.get(url)
    if resp.status_code == 200:
        soup = BeautifulSoup(resp.text,'lxml')
        number = (int)(soup.select('body > div.main > div > div.pic_main > div > div.Bigimg > div.ptitle > em')[0].text)

        for i in range(0,number + 1):
            url2 = url
            if i != 0:
                new_str = '_' + str(i) + '.html'
                url2 = url.replace('.html',new_str)

            resp = requests.get(url2)
            if resp.status_code == 200:
                soup = BeautifulSoup(resp.text,'lxml')
                image_url = soup.select('#pic-meinv > a > img')[0].attrs['data-original']

                resp = requests.get(image_url)
                if resp.status_code == 200:
                    file_path = '{0}/{1}.{2}'.format(name,i,'jpg')

                    if not os.path.exists(file_path):
                        with open(file_path,'wb') as f:
                            f.write(resp.content)
                            print(file_path + '\n')

        
if __name__ == "__main__":
    main()