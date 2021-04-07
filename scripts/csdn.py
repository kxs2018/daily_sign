# -- coding: utf-8 --
# CSDN签到
import json
import requests
import os
from QYWX_Notify import QYWX_Notify
import re


def csdn_signin():
    cookie = os.getenv('CSDN_COOKIE')
    if cookie:
        headers = {
            'cookie': cookie,
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4421.0 Safari/537.36 Edg/90.0.810.1'}
        signurl = "https://me.csdn.net/api/LuckyDraw_v2/signIn"
        resp = requests.post(signurl, headers=headers).content.decode(
            "unicode_escape")
        res = json.loads(resp)  # 将json转化为数组形式
        t = res['data']['msg']
        url = "https://me.csdn.net/api/LuckyDraw_v2/signInfo?product=&&type="
        resp1 = requests.get(url, headers=headers).content.decode("unicode_escape")
        resp1 = json.loads(resp1)  # 将json转化为数组形式
        username = re.findall(r'UserName=(.+?);', cookie)[0]
        msg = username + '\n'+t + '\n' + resp1['data']['msg']
        signdays = resp1['data']['star']
        if signdays == 5:
            sign = requests.post("https://me.csdn.net/api/LuckyDraw_v2/goodLuck", headers=headers).content.decode(
                    "unicode_escape")
            try:
                option = json.loads(sign)['data']['msg']
            except:
                option = ''
            msg = msg + '\n' + option
        QYWX_Notify().send('CSDN签到信息', msg.strip())


if __name__ == '__main__':
    csdn_signin()