# -- coding: utf-8 --
import requests
import json
import time
import os
from QYWX_Notify import QYWX_Notify
from io import StringIO

requests.packages.urllib3.disable_warnings()
sio = StringIO('')


def note_youdao_signin():
    url = 'https://note.youdao.com/yws/mapi/user?method=checkin'
    cookie = os.getenv('YD_COOKIE')
    ck_list = cookie.split('&')
    for i in range(len(ck_list)):
        if ck_list[i]:
            headers = {'cookie': ck_list[i],
                       'User-Agent': 'YNote',
                       'Host': 'note.youdao.com'
                       }
            req = requests.post(url, headers=headers, verify=False)
            if req.status_code == 200:
                info = json.loads(req.text)
                total = info['total'] / 1048576
                space = info['space'] / 1048576
                t = time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time() + 28800))
                sio.write(
                    f'帐号{i + 1}：' + '签到成功，本次获取 ' + str(space) + ' M, 总共获取 ' + str(total) + ' M, 签到时间 ' + str(t) + '\n')
            elif req.status_code > 400:
                sio.write(f'帐号{i + 1}：签到失败，请检查cookie\n')
            msg = sio.getvalue().replace('\n\n', '\n').strip()
    QYWX_Notify().send('有道云笔记签到信息', msg)


if __name__ == '__main__':
    note_youdao_signin()
