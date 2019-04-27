#!/usr/bin/env python
# -*- encoding: utf-8 -*-
 
'''
@Author  :   Anuo.
 
@License :   (C) Copyright 2018, Anuo's Studio
 
@Contact :   188512936@qq.com
 
@Software:   VS2017
 
@File    :   baidu_tupian_spider.py
 
@Time    :   Mar 31,2019
 
@Desc    :   百度图片爬虫，既然你百度的图片都是爬别人的，那我就来爬你的，哈哈哈。
 
             本脚本的目的就是根据你要搜索的关键字，然后爬取相关的图片。
'''



def seacrch_url(word):
    '''关键词 图片搜索'''   
    pass 








if __name__ == "__main__":
    '''自启动'''

    word = input()
    list = seacrch_url(word)

    base_url = "http://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&queryWord=%E5%A8%9C%E7%BE%8E%E7%9A%84%E8%BA%AB%E6%9D%90%E5%A6%B9&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=&z=&ic=&hd=&latest=&copyright=&word=%E5%A8%9C%E7%BE%8E%E7%9A%84%E8%BA%AB%E6%9D%90%E5%A6%B9&s=&se=&tab=&width=&height=&face=&istype=&qc=&nc=&fr=&expermode=&force=&pn={0}&rn={1}&gsm={2}&1554034006162=".format(pn, rn, gsm )

    # 启动多线程


