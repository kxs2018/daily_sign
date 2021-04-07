# -- coding: utf-8 --
from io import StringIO
import requests
import re
from lxml import etree
import time
import os
from QYWX_Notify import QYWX_Notify

headers = {
    'host': 'www.uiwow.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4437.0 Safari/537.36 Edg/91.0.831.1',
}
sio = StringIO('uiwow签到日志\n\n')
dio = StringIO()


class Uiwow_Signin:
    def __init__(self, username, psw):
        self.url = 'https://www.uiwow.com/member.php'
        self.signurl = 'https://www.uiwow.com/plugin.php'
        self.username = username
        self.psw = psw
        self.s = requests.Session()

    def login(self):
        params = {"mod": "logging",
                  "action": "login"}
        req = self.s.get(self.url, params=params, headers=headers).content.decode('utf-8')
        loginhash = re.findall(r'loginhash=(.*)?"', req)
        loginhash = loginhash[0]
        formhash = re.findall(r'name="formhash" value="(.*)?"', req)[0]
        params = {
            'mod': 'logging',
            'action': 'login',
            'loginsubmit': 'yes',
            'handlekey': 'login',
            'loginhash': loginhash,
            'inajax': 1
        }
        data = {
            'formhash': formhash,
            'referer': 'https://www.uiwow.com/forum.php',
            'loginfield': 'username',
            'username': self.username,
            'password': self.psw,
            'questionid': 0
        }
        req = self.s.post(self.url, params=params, data=data, headers=headers).content.decode('utf-8')
        if '欢迎您回来' in req:
            return '登录成功'
        else:
            sio.write(self.username + '\t登录失败\n\n')
            dio.write(self.username + '\t登录失败\n')

    def signin(self):
        params = {
            'id': 'dc_signin:sign',
            'inajax': 1
        }
        try:
            req = self.s.get(self.signurl, params=params, headers=headers).content.decode('utf-8')
        except:
            return
        formhash = re.findall(r'name="formhash" value="(.*)?"', req)[0]
        params = {'id': 'dc_signin:sign',
                  'inajax': 1,
                  'formhash': formhash,
                  'signsubmit': 'yes',
                  'handlekey': 'signin',
                  'emotid': 1,
                  'referer': 'https://www.uiwow.com/forum.php',
                  'content': '开森的我开森的签到一下！'}
        self.s.post(self.signurl, params=params, headers=headers)

    def get_stat(self):
        state_url = 'http://www.uiwow.com/plugin.php?id=dc_signin&action=index'
        res = self.s.get(state_url, headers=headers)
        html = etree.HTML(res.text)
        sign_div = html.xpath('//*[@class="sign_div"]')[0]
        sign_state = sign_div.xpath('./a/text()')[0]
        date = sign_div.xpath('.//div[@class="date"]/text()')[0]
        if '已' not in sign_state:
            sio.write(self.username + ' ' + date + ' 的签到状态是:未' + sign_state + '\n\n')
            dio.write(self.username + ' ' + date + ' 的签到状态是:未' + sign_state + '\n')
        else:
            sio.write(self.username + ' ' + date + ' 的签到状态是:' + sign_state + '\n\n')
            dio.write(self.username + ' ' + date + ' 的签到状态是:' + sign_state + '\n')
        mytips_data = html.xpath('//div[@class="mytips"]/p')
        for p in mytips_data:
            text = p.xpath('./text()|./b')
            for i in text:
                try:
                    sio.write(i.text.strip())
                except:
                    sio.write(i.strip())
        sio.write('\n')

    def start(self):
        self.login()
        self.signin()
        self.get_stat()


def main():
    username = os.getenv('UIWOW_USERNAME')
    psw = os.getenv('UIWOW_PSW')
    if username and psw:
        username = username.split('&')
        psw = psw.split('&')
        if len(username) != len(psw):
            sio.write('签到失败，用户名和密码数量不等\n\n\n')
            dio.write('签到失败，用户名和密码数量不等\n')
            return
        else:
            for i in range(len(username)):
                u = Uiwow_Signin(username[i], psw[i])
                u.start()
                time.sleep(5)


if __name__ == '__main__':
    main()
    content = sio.getvalue()
    digest = dio.getvalue().strip()
    QYWX_Notify().send('uiwow签到信息', digest, content)
