#!/usr/bin/env python
# -*- encoding: utf-8 -*-
 
'''
@Author  :   Anuo.
 
@License :   (C) Copyright 2019, Anuo's Studio
 
@Contact :   188512936@qq.com
 
@Software:   VS2017
 
@File    :   niutrans_spider.py
 
@Time    :   Mar 4,2019
 
@Desc    :   小牛翻译开放平台，翻译爬虫，网址：https://niutrans.vip/
 
'''


import urllib.request
import urllib.parse
import json


def translate(trans_text, trans_from, trans_to):
    url = "https://test.niutrans.vip/NiuTransServer/testtrans?&from=yue&to=en&m=0.9511117269278795&src_text=%E4%BD%A0%E5%A5%BD&url="
    data = {}
    data['from'] = trans_from
    data['to'] = trans_to
    data['m'] = '0.9511117269278795'
    data['src_text'] = trans_text
    data['url'] = ''
    data = urllib.parse.urlencode(data).encode('utf-8')

    headers = {}
    headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36'
    headers['Referer'] = 'https://niutrans.vip/'

    fanyi_re = urllib.request.Request(url, data, headers)
    fanyi_response = urllib.request.urlopen(fanyi_re)
    html = fanyi_response.read().decode('utf-8')   # {"from":"en","to":"zh","tgt_text":"你好 \n"}

    jsonObj = json.loads(html)
    text = jsonObj['tgt_text']

    print(text)


if __name__ == "__main__":

    # 英 -> 汉
    trans_text = 'hello'
    trans_from = 'en'
    trans_to = 'zh'
    translate(trans_text, trans_from, trans_to)

    # 汉 -> 英
    trans_text = '你好'
    trans_from = 'zh'
    trans_to = 'en'
    translate(trans_text, trans_from, trans_to)

    # 维 -> 汉
    trans_text = 'ياخشىمۇ سىز'
    trans_from = 'uy'
    trans_to = 'zh'
    translate(trans_text, trans_from, trans_to)
    # 汉 -> 维
    trans_text = '你好'
    trans_from = 'zh'
    trans_to = 'uy'
    translate(trans_text, trans_from, trans_to)