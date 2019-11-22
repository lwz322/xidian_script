#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 16 00:30:03 2018

@author: lwz322@qq.com
"""
import os
import sys
import threading
from threading import Thread
import requests
import pytesseract
import prettytable as pt
from lxml import html
from lxml import etree
from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt

#在这里输入用户名和密码
#下面预置的部分用于测试效果
USERNAME = "请输入用户名"
PASSOWORD = "密码"

MAX_trid_times=2
THREADS_NUM=20
agent=r'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
headers = {
    "Host": "10.255.44.1:8800",
    "Referer": r"http://10.255.44.1:8800/login",
    'User-Agent': agent
}

BASE_URL = "http://10.255.44.1:8800"
LOGIN_URL = "/login"
HOME_URL = "/home"

POST_url = BASE_URL + LOGIN_URL
GET_url = BASE_URL + HOME_URL

class MyThread(Thread):

    def __init__(self, number):
        Thread.__init__(self)
        self.number = number

    def run(self):
        cookies_home=login_try()
        self.result = cookies_home

    def get_result(self):
        return self.result

def login_init():
    login_page = requests.get(BASE_URL, allow_redirects=False,timeout = 5)
    #get_login_cookies
    cookies_login=login_page.cookies
    doc_login = html.document_fromstring(login_page.text)
    #get_csrf
    csrf = doc_login.cssselect('input[name="_csrf"]')[0].get('value')
    #get_captcha
    captcha_link = doc_login.cssselect('form img')[0].get('src')
    img_url = BASE_URL + captcha_link
    return cookies_login,csrf,img_url

def get_captcha_string(cookies_login,img_url):
    #get_captcha_string by pytesseract and BytesIO
    img_get = requests.get(img_url,cookies=cookies_login,headers = headers)
    img_binary = img_get.content
    captcha_img=Image.open(BytesIO(img_binary))
    captcha_string = pytesseract.image_to_string(captcha_img)
    #plt.imshow(captcha_img)
    #plt.show()
    #print(captcha_string)
    return captcha_string

def login_try():
    cookies_login,csrf,img_url=login_init()
    for trid_times in range(MAX_trid_times):
        if trid_times == MAX_trid_times-1:
            #print("用户名密码错误或验证码识别次数超限")
            #print("Threading %s is offline"%threading.current_thread().name)
            sys.exit(0)
            break
        captcha_string=get_captcha_string(cookies_login,img_url)
        post_data = {
                "_csrf": csrf,
                "LoginForm[username]": USERNAME,
                "LoginForm[password]": PASSOWORD,
                "LoginForm[verifyCode]": captcha_string,
                }
        login_result = requests.post(POST_url, data=post_data, cookies=cookies_login,headers = headers, allow_redirects=False,timeout = 15)
        login_status_code = login_result.status_code
        if login_status_code == 302 :
            cookies_home=login_result.cookies
            #print("Trid %d times to get capcha string"%trid_times)
            #print("Threading %s is logined"%threading.current_thread().name)
            break
    return cookies_home

def home_parse(cookies_home):
    home_page = requests.get(GET_url, cookies=cookies_home)
    dom = etree.HTML(home_page.text)
    thead=[]
    tbody=[]
    print("用户名: %s "%USERNAME)
    for i in range(1,6):
        thead_xpath='//*[@id="w3-container"]/table/thead/tr/th['+str(i)+']/text()'
        tbody_xpath='//*[@id="w3-container"]/table/tbody/tr/td['+str(i)+']/text()'
        thead.append(dom.xpath(thead_xpath)[0])
        tbody.append(dom.xpath(tbody_xpath)[0])
    tb = pt.PrettyTable()
    tb.field_names = thead
    tb.add_row(tbody)
    tb.set_style(pt.PLAIN_COLUMNS)
    print(tb)

def stat():
    statics=[]
    for i in range(0,5):
        times=login_try()
        statics.append(times)
    return statics

if __name__ == '__main__':
    threads=[]
    cookies_list=[]
    i=0
    for i in range(THREADS_NUM):
        t=MyThread(1)
        threads.append(t)
    for t in threads:
        t.start()
        #print("%s started"%t.getName)
    while len(cookies_list)==0:
        try:
            #print("try to get result")
            cookies_list.append(threads[i].get_result())
            #print("\n Got it %s ,print_result"%threads[i].getName)
            break
        except:
            i=(i+1)%THREADS_NUM
            #print(i)
            continue
    home_parse(cookies_list[0])
