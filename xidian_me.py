#!/usr/bin/python3
# -*- coding: utf-8 -*-
import requests
import json
import re

USERNAME=""
PASSWORD=""

login_page = requests.get("http://10.168.55.50:8088/searchWap/Login.aspx")
cookies_login=login_page.cookies
post_data={
    "webName":USERNAME,
    "webPass":PASSWORD
}

HEADER = {
    "AjaxPro-Method": "getLoginInput",
    'Host': '10.168.55.50:8088',
    'Connection': 'keep-alive',
    'Origin': 'http://10.168.55.50:8088'
}
login_result = requests.post("http://10.168.55.50:8088/ajaxpro/SearchWap_Login,App_Web_fghipt60.ashx",data=json.dumps(post_data),cookies=cookies_login, headers = HEADER)
login_result.status_code

balance_page=requests.get('http://10.168.55.50:8088/searchWap/webFrm/met.aspx',cookies=cookies_login)

pattern_name = re.compile('表名称：(.*?)  ',re.S)
name=re.findall(pattern_name,balance_page.text)
pattern_balance = re.compile('剩余量：(.*?) </td>',re.S)
balance=re.findall(pattern_balance,balance_page.text)
print("电费账号：",USERNAME,"\n","表名称：",name[0],"剩余量：%.2f"% float(balance[0]))