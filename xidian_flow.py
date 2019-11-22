#!/usr/bin/python3
# -*- coding: utf-8 -*-

import requests
import prettytable as pt
from lxml import etree
from lxml import html

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
    doc_login = html.document_fromstring(login_page.text)
    #get_csrf
    csrf = doc_login.cssselect('input[name="_csrf"]')[0].get('value')
    return cookies_login,csrf

def login():
    cookies_login,csrf=login_init()
    post_data = {
            "_csrf": csrf,
            "LoginForm[username]": USERNAME,
            "LoginForm[password]": PASSOWORD
            }
    login_result = requests.post(POST_url, data=post_data, cookies=cookies_login,headers = HEADER, allow_redirects=False)
    login_status_code = login_result.status_code
    if login_status_code == 302 :
        cookies_home=login_result.cookies
    return cookies_home

def home_parse(cookies_home):
    home_page = requests.get(GET_url, cookies=cookies_home)
    dom = etree.HTML(home_page.text)
    thead=[]
    tbody=[]
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

if __name__ == '__main__':
    print("用户名: %s "%USERNAME)
    cookies_home=login()
    home_parse(cookies_home)