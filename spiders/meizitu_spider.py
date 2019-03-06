#!/usr/bin/env python
# -*- encoding: utf-8 -*-
 
'''
@Author  :   Anuo.
 
@License :   (C) Copyright 2018, Anuo's Studio
 
@Contact :   188512936@qq.com
 
@Software:   VS2017
 
@File    :   meizitu_spider.py
 
@Time    :   Mar 6,2019
 
@Desc    :   妹子图图片爬取。地址：https://www.mzitu.com/tag/ugirls/
             写到最后才发现，403 了！！！！！！！！
 
'''

import os
import sys
import requests
from bs4 import BeautifulSoup   # pip install beatifulsoup4
import urllib


def crawl_page(page_url):
    '''爬取每一个 page'''

    #找到每一页有多少主题（地址）
    print(page_url)
    page_html = requests.get(page_url)
    soup_page_html = BeautifulSoup(page_html.text, features='html.parser')
    topic_soup_list = soup_page_html.find_all("a", attrs={"target":"_blank"})
    print(len(topic_soup_list))

    for topic_soup in topic_soup_list:
        topic_url = topic_soup['href']
        crawl_topic(topic_url)


def crawl_topic(topic_url):
    '''爬取每一个 topic'''

    # 找标题
    print(topic_url)
    topic_html = requests.get(topic_url)
    topic_soup = BeautifulSoup(topic_html.text, features='html.parser')
    main_title = topic_soup.find('h2', attrs={'class':'main-title'}).contents[0]

    # 找导航，最大值
    navi_soup = topic_soup.find('div', attrs={'class':'pagenavi'})
    navi_nades_soup = navi_soup.find_all('a')
    href_list = []
    for navi_node in navi_nades_soup:
        tt = navi_node['href']
        href_list.append(navi_node['href'])

    # 去除杂项，如“上一组”，并转换到页码
    new_href_list = [int(n.replace(topic_url + '/', '')) for n in href_list if topic_url in n]
    max_page = max(new_href_list)

    for i in range(1, max_page + 1):
        crawl_picture(main_title, topic_url, i)

    
def crawl_picture(main_title, topic_url, page_number):
    '''爬取图片'''

    url = topic_url + '/' + str(i)
    html = requests.get(url)
    pic_soup = BeautifulSoup(html.text, features='html.parser')
    main_image_node_soup = pic_soup.find('div', attrs={'class':'main-image'})
    image_node = main_image_node_soup.find('img')
    pic_src = image_node['src']

    # 保存图片，分主题路径保存
    save_pic(main_title, pic_src, page_number)

def save_pic(main_title, pic_src, page_number):
    '''保存图片'''

    img = url_open(pic_src)

    if not os.path.exists(main_title):
        os.mkdir(main_title)

    file_path = '{0}/{1}/{2}'.format('Meizitu', main_title, os.path.basename(pic_src))

    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'}

    try:
        resp = requests.get(pic_src, headers = headers)
        if resp.status_code == 200:
            if not os.path.exists(file_path):
                with open(file_path, 'wb') as f:
                    f.writelines(resp.content)
    except requests.ConnectionError:
        print('Fail to save image.')


if __name__ == "__main__":

    #爬取顺序：先爬取页，然后爬取页下主题列表，再爬取主题，主题里面就有多张图片。
    base_url = 'https://www.mzitu.com/tag/ugirls/'
    for i in range(1,10):
        #https://www.mzitu.com/tag/ugirls/page/2/
        page_url = base_url + 'page/' + str(i) + '/'
        crawl_page(page_url)