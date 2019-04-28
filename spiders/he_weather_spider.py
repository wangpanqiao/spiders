#!/usr/bin/env python
# -*- encoding: utf-8 -*-
 
'''
@Author  :   Anuo.
 
@License :   (C) Copyright 2019, Anuo's Studio
 
@Contact :   188512936@qq.com
 
@Software:   VS2017
 
@File    :   he_weather_spider.py
 
@Time    :   Apr 28,2019
 
@Desc    :   和风天气API

'''

import urllib,json

def get_weather():

    try:
        #调用和风天气的API city可以通过https://cdn.heweather.com/china-city-list.txt城市列表获取
        url = 'https://free-api.heweather.com/v5/weather?city=CA6173331&key=8a439a7e0e034cdcb4122c918f55e5f3'
        #用urllib2创建一个请求并得到返回结果
        req = urllib.request.Request(url)
        resp = urllib.request.urlopen(req).read()
        # print resp
        # print type(resp)

        #将JSON转化为Python的数据结构
        json_data = json.loads(resp)
        city_data=json_data['HeWeather5'][0]
        weather_msg = ''
        #hourly_data= json_data['HeWeather5'][0]['hourly_forecast']
        daily_data = json_data['HeWeather5'][0]['daily_forecast']
        #print(json_data)
        #print (u'当前时间：' + daily_data[0]['date'])
        #print (u'城市：' + city_data['basic']['city'])
        ##print (u'PM指数：' + city_data['aqi']['city']['pm25'])
        #print (u'白天天气：' + daily_data[0]['cond']['txt_d'])
        #print (u'夜间天气：' + daily_data[0]['cond']['txt_n'])
        #print (u'今天{0}: 气温：{1}°/{2}°'.format(str(daily_data[0]['date']),daily_data[0]['tmp']['min'],daily_data[0]['tmp']['max']))
        ##print (u'未来小时天气：{0} {1}'.format(str(hourly_data[0]['date']).split()[1],hourly_data[0]['cond']['txt']))
        ##print (u'未来小时天气：{0} {1}'.format(str(hourly_data[1]['date']).split()[1],hourly_data[1]['cond']['txt']))
        ##print (u'未来小时天气：{0} {1}'.format(str(hourly_data[2]['date']).split()[1],hourly_data[2]['cond']['txt']))
        #print (u'未来{0} 天气：{1}°/{2}°'.format(daily_data[1]['date'],daily_data[1]['tmp']['min'],daily_data[1]['tmp']['max']))
        #print (u'未来{0} 天气：{1}°/{2}°'.format(daily_data[2]['date'],daily_data[1]['tmp']['min'],daily_data[2]['tmp']['max']))
        ##print (u'穿衣建议：' + json_data['HeWeather5'][0]['suggestion']['drsg']['txt'])

        weather_msg += '时间：' + daily_data[0]['date'] + '\n'
        weather_msg += '城市：' + city_data['basic']['city'] + '\n'
        weather_msg += '天气：' + daily_data[0]['cond']['txt_d'] + '\n'
        weather_msg += '今天气温：{0}°- {1}°'.format(daily_data[0]['tmp']['min'],daily_data[0]['tmp']['max']) + '\n'
        weather_msg += '明天气温：{0}°- {1}°'.format(daily_data[1]['tmp']['min'],daily_data[1]['tmp']['max']) + '\n'
        weather_msg += '后天气温：{0}°- {1}°'.format(daily_data[1]['tmp']['min'],daily_data[2]['tmp']['max']) + '\n'

        return weatger_msg
    except Exception as ex:
        return ''