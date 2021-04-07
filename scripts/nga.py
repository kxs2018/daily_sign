# -- coding: utf-8 --
import requests
import time
import json
import os
from QYWX_Notify import QYWX_Notify
from io import StringIO

requests.packages.urllib3.disable_warnings()
sio = StringIO()


class Nga_signin:
    def __init__(self, num, uid, token):
        self.num = num
        self.url = 'https://ngabbs.com/nuke.php'
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 10; NOH-AN00 Build/HUAWEINOH-AN00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/83.0.4103.106 Mobile Safari/537.36 Nga_Official/90021",
            "X-Requested-With": "gov.pianzong.androidnga",
            "X-USER-AGENT": "Nga_Official/90021(HUAWEI NOH-AN00;Android 10)"
        }
        self.uid = uid
        self.token = token

    def signin(self):
        data = {"access_token": self.token,
                "t": round(time.time()),
                "access_uid": self.uid,
                "app_id": "1010",
                "__act": "check_in",
                "__lib": "check_in",
                "__output": "12"
                }
        req = requests.post(self.url, headers=self.headers, data=data, verify=False).content
        return json.loads(req)

    def get_stat(self):
        data = {"access_token": self.token,
                "t": round(time.time()),
                "access_uid": self.uid,
                "sign": "",
                "app_id": "1010",
                "__act": "get_stat",
                "__lib": "check_in",
                "__output": "14"
                }
        res = requests.post(self.url, headers=self.headers, data=data, verify=False).content
        res = json.loads(res)
        result = res['result'][0]
        continued = result['continued']
        total = result['sum']
        return continued, total

    def get_user(self):
        data = {"access_token": self.token,
                "t": round(time.time()),
                "access_uid": self.uid,
                "sign": "",
                "app_id": "1010",
                "__act": "iflogin",
                "__lib": "login",
                "__output": "12"
                }
        req = requests.post(self.url, headers=self.headers, data=data, verify=False).content
        req = json.loads(req)['result']['username']
        return req

    def start(self):
        req = self.signin()
        try:
            if '先登录' in req["msg"]:
                sio.write(f'签到失败，token已失效或uid与token不对应\n')
            else:
                continued, total = self.get_stat()
                username = self.get_user()
                if '已经' in req["msg"]:
                    sio.write(f'账号{self.num}:{username} 今天已签过到，当前已连续签到{continued}天，总共签到{total}天\n')
                elif req["code"] == 0:
                    sio.write(f'账号{self.num}:{username} 签到成功，当前已连续签到{continued}天，总共签到{total}天\n')
        except Exception as result:
            sio.write(str(result))


if __name__ == '__main__':
    uid = os.getenv('NGA_UID')
    token = os.getenv('NGA_TOKEN')
    if uid and token:
        uid = uid.split('&')
        token = token.split('&')
        if len(uid) != len(token):
            msg = "签到失败，UID和token个数不相等"
            QYWX_Notify().send("NGA签到信息", msg)
            raise Exception
        for i in range(len(uid)):
            n = Nga_signin(i + 1, uid[i], token[i])
            n.start()
        msg = sio.getvalue().strip()
        QYWX_Notify().send("NGA签到信息", msg)
