# -- coding: utf-8 --
import os
from urllib import parse
import requests
import json
from io import StringIO
from QYWX_Notify import QYWX_Notify

requests.packages.urllib3.disable_warnings()
sio = StringIO()


def get_params(u):
    l1 = dict(parse.parse_qsl(parse.urlsplit(u).query))
    params = {}
    for key in l1:
        if key in ["from", "uid", "s", "gsid", "c", 'aid']:
            params[key] = l1[key]
    return params


def sign(params):
    headers = {"User-Agent": "ua=HUAWEI-YAL-AL00__weibo__11.3.4__android__android10"}
    url = 'https://api.weibo.cn/2/checkin/add'
    req = requests.get(url, params=params, headers=headers, verify=False).content.decode('utf-8')
    result = json.loads(req)
    if result.get("status") == 10000:
        sio.write(f'连续签到: {result.get("data").get("continuous")}天\n本次收益: {result.get("data").get("desc")}\n')
    elif result.get("errno") == 30000:
        sio.write(f"每日签到: 已签到\n")
    elif result.get("status") == 90005:
        sio.write(f'每日签到: {result.get("msg")}\n')
    else:
        sio.write(f"每日签到: 签到失败\n")


def card(params):
    headers = {"User-Agent": "HUAWEI-YAL-AL00__weibo__11.3.4__android__android10"}
    url = "https://api.weibo.cn/2/!/ug/king_act_home"
    response = requests.get(url, params=params, headers=headers, verify=False)
    result = response.json()
    if result.get("status") == 10000:
        nickname = result.get("data").get("user").get("nickname")
        sio.write(
            f'用户昵称: {nickname}\n每日打卡: {result.get("data").get("signin").get("title").split("<")[0]}天\n'
            f'积分总计: {result.get("data").get("user").get("energy")}\n'
        )
    else:
        sio.write(f"每日打卡: 活动过期或失效\n")


def pay(params):
    headers = {
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded",
        "Host": "pay.sc.weibo.com",
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; YAL-AL00 Build/HUAWEIYAL-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/83.0.4103.106 Mobile Safari/537.36 Weibo (HUAWEI-YAL-AL00__weibo__11.3.4__android__android10)",
    }
    params['lang'] = "zh_CN"
    params["wm"] = "9006_2001"
    url = "https://pay.sc.weibo.com/aj/mobile/home/welfare/signin/do"
    response = requests.post(url, headers=headers, params=params, verify=False)
    result = response.json()
    if result.get("status") == 1:
        sio.write(f'微博钱包: {result.get("score")} 积分\n')
    elif result.get("status") == 2:
        sio.write(f"微博钱包: 已签到\n")
    else:
        sio.write(f"微博钱包: Cookie失效\n")


if __name__ == '__main__':
    u = os.getenv('WEIBO_URL')
    if u:
        u = u.split('\n')
        for i in u:
            params = get_params(i)
            card(params)
            sign(params)
            pay(params)
        digest = sio.getvalue().strip()
        QYWX_Notify().send('微博签到信息', digest)