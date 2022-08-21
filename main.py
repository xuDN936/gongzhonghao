from datetime import date, datetime
from time import time, localtime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

today = datetime.now()
start_date = os.environ['START_DATE']
city = os.environ['CITY']
birthday = os.environ['BIRTHDAY']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
user_id2 = os.environ["USER_ID2"]
template_id = os.environ["TEMPLATE_ID"]

def get_today():
  week_list = ["星期日", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六"]
  year = localtime().tm_year
  month = localtime().tm_mon
  day = localtime().tm_mday
  today = datetime.date(datetime(year=year, month=month, day=day))
  week = week_list[today.isoweekday() % 7]
  return "{} {}".format(today, week)

def get_weather():
  url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
  res = requests.get(url).json()
  weather = res['data']['list'][0]
  return weather['weather'], math.floor(weather['temp']), math.floor(weather['low']), math.floor(weather['high'])

def get_count():
  delta = today - datetime.strptime("2022-07-29", "%Y-%m-%d")
  return delta.days

def get_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + "06-22", "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days


def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
wea, temperature,low,high = get_weather()
data = {"date":{"value":get_today(), "color":get_random_color()},"city":{"value":city, "color":get_random_color()},"low":{"value":str(low)+"℃", "color":get_random_color()},"high":{"value":str(high)+"℃", "color":get_random_color()},"weather":{"value":wea, "color":get_random_color()},"temperature":{"value":temperature, "color":get_random_color()},"love_days":{"value":get_count(), "color":get_random_color()},"birthday":{"value":get_birthday(), "color":get_random_color()},"words":{"value":get_words(), "color":get_random_color()}}
res = wm.send_template(user_id, template_id, data)
#res2 = wm.send_template(user_id2, template_id, data)
print(res)

