import requests
import urllib
from bs4 import BeautifulSoup
import json

# 获取门店id
def shop(HEAD):
    url = "https://pro.styd.cn/_api/v1/shop?size=999"
    data = {}
    result = requests.get(
        url,
        headers=HEAD)
    print("获取获取门店id{%s}" % json.loads(result.content))
    list = json.loads(result.content).get('data').get('list');
    for l in list:
        data[l.get('shop_name')] = l.get('shop_id')
    return data;

# 切换门店
def switchShop(HEAD, shopId):
    url = "https://pro.styd.cn/_api/v1/account/switch/shop"
    data = {
        "shop_id": shopId
    }
    result = requests.put(
        url,
        json=data,
        headers=HEAD)

    print("获取切换门店返回状态{%s}" % result.content.decode('utf8'))
    token = json.loads(result.content.decode('utf8')).get('data').get('token')
    HEAD['token'] = token
    HEAD['app-shop-id'] = shopId
    cookie = result.cookies
    return cookie

# 获取会员列表
def followMember(HEAD, cookie, shopId, type=1, page=1):
    url = "https://pro.styd.cn/_api/v1/member/club_member?" + \
    "app_brand_id=1786679887724597&app_shop_id=ASI&member_level=ML&follow_salesman_id=-1&follow_coach_id=-1&follow_status=-1&tag_id=-1&buy_personal_course=-1&current_page=CP&has_face=-1&has_physical=-1&has_finger=-1&register_way=-1&status=1"
    url = url.replace("ASI", str(shopId))
    url = url.replace("ML", str(type))
    url = url.replace("CP", str(page))
    result = requests.get(
        url,
        cookies=cookie,
        headers=HEAD)
    list = json.loads(result.content.decode('utf8')).get('data').get('list');
    memberIds = []
    for m in list:
        memberIds.append(m.get('member_id'))
    return memberIds

# 提交跟进信息
def submit(HEAD, cookie, time, content, memberId, concat_type=1, contact_status=1):
    url = "https://pro.styd.cn/_api/v1/member/follow/history/" + str(memberId)
    print(url)
    data = {
        "follow_way": concat_type,
        "follow_status": contact_status,
        "follow_next_time": time,
        "follow_content": content
    }
    print("提交数据 %s" % data)
    res = requests.put(url, cookies=cookie, json=data, headers=HEAD)
    print("提交会员跟进信息返回{%s}" % json.loads(res.content))