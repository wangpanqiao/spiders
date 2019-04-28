#!/usr/bin/env python
# -*- encoding: utf-8 -*-
 
'''
@Author  :   Anuo.
 
@License :   (C) Copyright 2019, Anuo's Studio
 
@Contact :   188512936@qq.com
 
@Software:   VS2017
 
@File    :   yahoo_weather_spider.py
 
@Time    :   Apr 28,2019
 
@Desc    :   雅虎天气API

'''

import time, uuid, urllib
import hmac, hashlib
from base64 import b64encode
import json


def get_weather(city_name):
    """
    Basic info    Richmond  Vancouver  Burnaby
    """
    url = 'https://weather-ydn-yql.media.yahoo.com/forecastrss'
    method = 'GET'
    app_id = 'Xjni966u'
    consumer_key = 'dj0yJmk9VXJvMlJZc3cwUEozJnM9Y29uc3VtZXJzZWNyZXQmc3Y9MCZ4PTJh'   # Key
    consumer_secret = '124c37555e3a8d3e847d0421bd1d4f937c1cc8d3'   # 秘钥
    concat = '&'
    query = {'location': '{0},ca'.format(city_name), 'format': 'json'}   # 地址
    oauth = {
        'oauth_consumer_key': consumer_key,
        'oauth_nonce': uuid.uuid4().hex,
        'oauth_signature_method': 'HMAC-SHA1',
        'oauth_timestamp': str(int(time.time())),
        'oauth_version': '1.0'
    }

    """
    Prepare signature string (merge all params and SORT them)
    """
    merged_params = query.copy()
    merged_params.update(oauth)
    sorted_params = [k + '=' + urllib.request.quote(merged_params[k], safe='') for k in sorted(merged_params.keys())]
    signature_base_str =  method + concat + urllib.request.quote(url, safe='') + concat + urllib.request.quote(concat.join(sorted_params), safe='')

    """
    Generate signature
    """
    composite_key = urllib.request.quote(consumer_secret, safe='') + concat
    #oauth_signature = b64encode(hmac.new(composite_key, signature_base_str, hashlib.sha1).digest())
    oauth_signature = str(b64encode(hmac.new(bytes(composite_key,'utf-8'), bytes(signature_base_str,'utf-8'), hashlib.sha1).digest()),'utf-8')


    """
    Prepare Authorization header
    """
    oauth['oauth_signature'] = oauth_signature
    auth_header = 'OAuth ' + ', '.join(['{}="{}"'.format(k,v) for k,v in oauth.items()])

    """
    Send request
    """
    url = url + '?' + urllib.parse.urlencode(query)
    request = urllib.request.Request(url)
    request.add_header('Authorization', auth_header)
    request.add_header('X-Yahoo-App-Id', app_id)
    
    try:
        response = str(urllib.request.urlopen(request).read(),'utf-8')

        js_data = json.loads(response)
        weather_msg = ''

        weather_msg += '城市：' + js_data['location']['city'] + '\n'
        #weather_msg += '天气：{0}° {1}'.format(f_to_c(js_data['current_observation']['condition']['temperature']), js_data['current_observation']['condition']['text']) + '\n'
        weather_msg += '今天天气：{0}°- {1}° {2}'.format(f_to_c(js_data['forecasts'][0]['low']), f_to_c(js_data['forecasts'][0]['high']), js_data['forecasts'][0]['text']) + '\n'
        weather_msg += '明天天气：{0}°- {1}° {2}'.format(f_to_c(js_data['forecasts'][1]['low']), f_to_c(js_data['forecasts'][1]['high']), js_data['forecasts'][1]['text']) + '\n'
        weather_msg += '后天天气：{0}°- {1}° {2}'.format(f_to_c(js_data['forecasts'][2]['low']), f_to_c(js_data['forecasts'][2]['high']), js_data['forecasts'][2]['text']) + '\n'

        return weather_msg
    except Exception as ex:
        return ''


def f_to_c(f):
    '''华氏度 -> 摄氏度
    
    F=C×1.8+32
    C=(F-32)÷1.8
    '''
    c = (int(f) - 32) / 1.8
    return int(c)


#if __name__ == "__main__":
#    get_weather('Vancouver'.lower())