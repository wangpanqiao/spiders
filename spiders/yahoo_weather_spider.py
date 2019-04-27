#!/usr/bin/env python3
# coding: utf-8
import os
from datetime import datetime
from urllib import request 
from xml.parsers.expat import ParserCreate 

file_name = "weather.txt"
for root, dirs, files in os.walk("."):
    if file_name in files:
        os.remove(os.path.join(root, file_name))

def yahoo_weather(data):
    flag = False
    weather = {"city": "", "pubdate": "", "forecast": []}

    def start_element(name, attrs):
        if name == "yweather:location":
            weather["city"] = weather["city"] + attrs["city"]
            weather["city"] = weather["city"] + " " + attrs["country"]
        if name == "yweather:forecast":
            forecast = {}
            forecast["date"] = attrs["date"]
            forecast["day"] = attrs["day"]
            forecast["high"] = attrs["high"]
            forecast["low"] = attrs["low"]
            forecast["text"] = attrs["text"]
            weather["forecast"].append(forecast)
        if name == "pubDate":
            nonlocal flag
            flag = True
   
    def char_data(text):
        nonlocal flag
        if flag:
            weather["pubdate"] = text
            flag = False

    parser = ParserCreate()
    parser.StartElementHandler = start_element
    parser.CharacterDataHandler = char_data
    parser.Parse(data)
    return weather

def print_weather(weather):
    with open(file_name, "a") as f:
        s = "City: %s\nPub date: %s" %(weather["city"], weather["pubdate"])
        print("%s" %(weather["city"]))
        f.write(s + "\n")
        for forecast in weather["forecast"]:
            date = datetime.strptime(forecast["date"], "%d %b %Y").strftime("%Y-%m-%d")
            s = "Date: %s High: %s Low: %s Weather: %s" %(date, forecast["high"], forecast["low"], forecast["text"])
            f.write(s + "\n")
        f.write("\n")

citys = ["2151330", "2151849", "44418", "615702", "2514815"]
for city in citys:
    url = "https://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20weather.forecast%20where%20woeid%20%3D%20"
    url = url + city
    url = url + "&format=xml"
    with request.urlopen(url, timeout=4) as f:
        weather = yahoo_weather(f.read())
        print_weather(weather)
print("weather conditions has written to %s" %(file_name))
