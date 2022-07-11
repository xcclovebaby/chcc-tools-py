import requests
import urllib
from bs4 import BeautifulSoup
import json

COOKIE_NAME = "ran_sass_gym"
HEAD = {"Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
        "Connection": "keep-alive",
        "Host": "www.styd.cn",
        "Origin": "https://www.styd.cn",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome"
        }


# 登录系统
def login(username, password):
    url = "https://www.styd.cn/web/user/do_login"
    data = {
        "login_name": username,
        "login_pwd": password
    }
    res = requests.post(url, data=data, headers=HEAD)
    print("登录接口返回状态{%s}" % json.loads(res.content))
    cookie = res.cookies
    return cookie


# 获取会员列表
def followMember(cookie, page=1):
    url = "https://www.styd.cn/club/member/sale_follow_member?mix_cond=&p=" + str(page)
    result = requests.get(
        url,
        cookies=cookie,
        headers=HEAD)
    print("获取会员列表接口返回状态{%s}" % result)
    soup = BeautifulSoup(result.content, 'html.parser')
    soup = soup.find_all(name="input", attrs={"name": "member_id"})
    member_id_list = []
    for s in soup:
        value = s.get_attribute_list('value')
        member_id_list.append(int(value.pop()))
    print("获取返回数据 %s" % member_id_list)
    return member_id_list


# 获取员工id
def saleMember(cookie, memberId):
    url = "https://www.styd.cn/club/member/follow?type=sale_member&member_id=" + str(memberId)
    data = {
        "type": "sale_member",
        "member_id": memberId
    }
    result = requests.get(
        url,
        data = data,
        cookies=cookie,
        headers=HEAD)
    print("获取会员信息接口返回状态{%s}" % result)
    soup = BeautifulSoup(json.loads(result.content).get('data'), 'html.parser')
    userIdHtml = soup.find_all(name="input", attrs={"name": "current_user_id"})
    for s in userIdHtml:
        value = s.get_attribute_list('value')
        return str(value.pop())


# 提交跟进信息
def submit(cookie, staff_id, time, content, memberId, concat_type=1, contact_status=1, contact_result=1):
    url = "https://www.styd.cn/club/member/follow"
    data = {
        "shop_id": 178296502,
        "member_id": memberId,
        "type": "sale_member",
        "staff_id": staff_id,  # 员工id
        "contact_type": concat_type,  # 服务方式 1电话跟进 2短信跟进 3见面跟进 4email跟进
        "contact_status": contact_status,  # 通讯状态 1接通 0无人接听 2电话忙 3空号 4关机 5挂断 6停机
        "contact_result": contact_result,  # 通讯结果 1预约成功
        "fail_reason": 0,
        "sales_id": staff_id,  # 员工id
        "time": time,
        "class_id": "请选择",
        "content": content,
        "next_contact": ""
    }
    print("提交数据 %s" % data)
    res = requests.post(url, cookies=cookie, data=data, headers=HEAD)
    print("提交会员跟进信息返回{%s}" % json.loads(res.content))
