#!/usr/bin/env python
# -*- encoding: utf-8 -*-
 
'''
@Author  :   Anuo.
 
@License :   (C) Copyright 2018, Anuo's Studio
 
@Contact :   188512936@qq.com
 
@Software:   VS2017
 
@File    :   toutiao_spider.py
 
@Time    :   Aug 21,2018
 
@Desc    :   头条街拍图片爬虫。
 
'''

import os
import requests
from hashlib import md5
from urllib.parse import urlencode
from multiprocessing.pool import Pool


def get_page(offset):
    '''爬取网页'''

    parms = {
        'offset':offset,
        'format':'json',
        'keyword':'街拍',
        'autoload':'true',
        'count':'20',
        'cur_tab':'1',
        'from':'search_tab'
        }
    url = 'https://www.toutiao.com/search_content/?' + urlencode(parms)
    try:
        resp = requests.get(url)
        if resp.status_code == 200:
            return resp.json()
    except requests.ConnectionError:
        return None


def get_image(json):
    '''爬取图片'''

    if json:
        items =  json.get('data')
        if items:
            for item in items:
                title = item.get('title')
                images = item.get('image_list')
                if images:
                    for image in images:
                        yield {
                            'image':'http:' + image.get('url'),
                            'title':title
                            }


def save_image(item):
    '''保存图片'''

    if not os.path.exists(item.get('title')):
        os.mkdir(item.get('title'))
    try:
        resp = requests.get(item.get('image'))
        if resp.status_code == 200:
            file_path = '{0}/{1}.{2}'.format(item.get('title'), md5(resp.content).hexdigest(), 'jpg')
            if not os.path.exists(file_path):
                with open(file_path, 'wb') as f:
                    f.write(resp.content)
            else:
                print('Already Downloaded', file_path)
    except requests.ConnectionError:
        print('File to save image.')


def main(offset):
    '''主流程'''

    json = get_page(offset)
    for item in get_image(json):
        print(item)
        save_image(item)

GROUP_START = 1
GROUP_END = 20

if __name__ == '__main__':
    pool = Pool()
    groups = ([x * 20 for x in range(GROUP_START, GROUP_END + 1)])
    pool.map(main, groups)
    pool.close()
    pool.join()
