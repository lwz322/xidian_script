#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import requests
import pytesseract
import prettytable as pt
from lxml import html
from lxml import etree
from PIL import Image
from io import BytesIO

#在这里输入用户名和密码
#下面预置的部分用于测试效果
USERNAME = "请输入用户名"
PASSOWORD = "密码"

MAX_login_times=10
MAX_warning_times=5
MAX_post_times=4
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
    string_len=0
    while string_len != 4:
        img_get = requests.get(img_url,cookies=cookies_login,headers = headers)
        img_binary = img_get.content
        captcha_img=Image.open(BytesIO(img_binary))
        try:
            #这里采用了 https://github.com/lllthhhh/tesseract_data_xdu_pay 训练的数据
            captcha_string = pytesseract.image_to_string(captcha_img, lang='ar',config="--psm 7 digits --tessdata-dir ./ar.traindata")
        except:
            #如果没有手动添加以上数据的话也可以正常运行
            captcha_string = pytesseract.image_to_string(captcha_img, config="--psm 7 digits")
        string_len=len(captcha_string)
    return captcha_string

def login_try():
    cookies_login,csrf,img_url=login_init()
    for trid_times in range(MAX_post_times):
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
            break
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

def hint():
    if MAX_warning_times==0:
        print("用户名、密码可能有误")
    if MAX_login_times==0:
        print("请自行检查各种可能的原因")
        sys.exit(0)

if __name__ == '__main__':
    print("用户名: %s "%USERNAME)
    while True:
        try:
            MAX_login_times=MAX_login_times-1
            MAX_warning_times=MAX_warning_times-1
            cookies_home=login_try()
            home_parse(cookies_home)
            break
        except:
            hint()
