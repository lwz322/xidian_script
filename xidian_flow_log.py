#!/usr/bin/python3
# -*- coding: utf-8 -*-

import requests
import re
import time

#在这里输入用户名和密码
USERNAME = "请输入用户名"
PASSOWORD = ""

agent='Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Mobile Safari/537.36'
HEADER = {
    "Host": "10.255.44.1:8800",
    "Referer": "http://10.255.44.1:8800/login",
    'User-Agent': agent
}

BASE_URL = "http://10.255.44.1:8800"
LOGIN_URL = "/login"
HOME_URL = "/home"

POST_url = BASE_URL + LOGIN_URL
GET_url = BASE_URL + HOME_URL

post_data = {
        "LoginForm[username]": USERNAME,
        "LoginForm[password]": PASSOWORD
        }

def login_init():
    login_page = requests.get(BASE_URL)
    #get_login_cookies
    cookies_login=login_page.cookies
    #get_csrf
    pattern_csrf = re.compile('name="_csrf" value="(.*?)"')
    csrf = re.findall(pattern_csrf,login_page.text)[0]
    return cookies_login,csrf

def login():
    cookies_login,csrf=login_init()
    post_data = {
            "_csrf": csrf,
            "LoginForm[username]": USERNAME,
            "LoginForm[password]": PASSOWORD
            }
    login_result = requests.post(POST_url, data=post_data, cookies=cookies_login,headers = HEADER, allow_redirects=False)
    cookies_home=login_result.cookies
    return cookies_home

if __name__ == '__main__':
    cookies_home=login()
    home_page = requests.get(GET_url,cookies=cookies_home)
    pattern = re.compile('<td data-col-seq="7">(.*?)</td>',re.S)
    balance=re.findall(pattern,home_page.text)[0]
    print(time.ctime(),balance)