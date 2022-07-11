import requests
import urllib
from bs4 import BeautifulSoup
import json

COOKIE_NAME = "wsToken"
HEAD = {"Content-Type": "application/json", "Connection": "keep-alive"}

def login(username,password):
    url = "https://www.styd.cn/web/user/do_login"
    data = {
        "login_name": username,
        "login_pwd": password
    }
    res = requests.post(url, json=data)
    cookie = res.cookies[COOKIE_NAME]
    return cookie

def followMember(cookie, page=1):
    url = "https://www.styd.cn/club/member/sale_follow_member?mix_cond=&p=" + page
    result = requests.get(
        url,
        cookies=cookie)
    soup = BeautifulSoup(result.content, 'lxml')
    print("获取返回数据 %s" % (soup.get_text()))
    memberIdList = soup.find_all(name="member_id")
    print("获取返回数据 %s" % (str(memberIdList)))
    return memberIdList

