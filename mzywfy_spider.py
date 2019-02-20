#!/usr/bin/env python
# -*- encoding: utf-8 -*-
 
'''
@Author  :   Anuo.
 
@License :   (C) Copyright 2019, Anuo's Studio
 
@Contact :   188512936@qq.com
 
@Software:   VS2017
 
@File    :   mzywfyj_spider.py
 
@Time    :   Feb 20,2019
 
@Desc    :   中国民族语文翻译局，翻译爬虫，网址：http://www.mzywfy.org.cn/translate.jsp
 
'''


import urllib.request
import urllib.parse
import json


def mzywfyj_translate(trans_text, trans_from, trans_to, trans_url):
    '''翻译'''

    mzywfyj_url = "http://www.mzywfy.org.cn/ajaxservlet"
    data = {}

    data['src_text'] = trans_text
    data['from'] = trans_from
    data['to'] = trans_to
    data['url'] = trans_url

    data = urllib.parse.urlencode(data).encode('utf-8')

    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36"}
    headers['Referer'] = 'http://www.mzywfy.org.cn/translate.jsp';  # 这个头必须加，不然不能成功
    fanyi_re = urllib.request.Request(mzywfyj_url, data, headers)
    fanyi_response = urllib.request.urlopen(fanyi_re)
    ret = fanyi_response.read().decode('utf-8')
    print(ret)


if __name__ == "__main__":

    # 可根据自己的情况设置好参数，然后调用方法 mzywfyj_translate()
    # 汉文 -> 维吾尔文
    trans_text = '你好'
    trans_from = 'zh'
    trans_to = 'uy'
    trans_url = 2
    mzywfyj_translate(trans_text, trans_from, trans_to, trans_url)
    # 维吾尔文 -> 汉文
    trans_text = 'ياخشىمۇ سىز'
    trans_from = 'uy'
    trans_to = 'zh'
    trans_url = 7
    mzywfyj_translate(trans_text, trans_from, trans_to, trans_url)
    
    
    # 汉文 ->  藏文
    trans_text = '你好'
    trans_from = 'zh'
    trans_to = 'ti'
    trans_url = 1
    mzywfyj_translate(trans_text, trans_from, trans_to, trans_url)
    # 藏文 ->  汉文
    trans_text = 'སྐུ་ཁམས་བཟང་'
    trans_from = 'ti'
    trans_to = 'zh'
    trans_url = 6
    mzywfyj_translate(trans_text, trans_from, trans_to, trans_url)


    # 汉文 ->  蒙古文
    trans_text  = '你好'
    trans_from = 'zh'
    trans_to = 'mo'
    trans_url = 0
    mzywfyj_translate(trans_text, trans_from, trans_to, trans_url)
    # 蒙古文 ->  汉文
    trans_text = '︽ ᠰᠠᠢᠢᠨ ᠪᠠᠶᠢᠨ᠎ᠠ ᠤᠣ ︖ '
    trans_from = 'mo'
    trans_to = 'zh'
    trans_url = 5
    mzywfyj_translate(trans_text, trans_from, trans_to, trans_url)