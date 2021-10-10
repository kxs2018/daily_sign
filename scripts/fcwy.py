# -- coding: utf-8 --
# @Author  : kxs2018
# @Time    : 2021/10/10 15:05
import re
import requests
import os
from QYWX_Notify import QYWX_Notify

username = os.getenv('FCWY_USERNAME')
psw = os.getenv('FCWY_PSW')
s = requests.Session()
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36 Edg/94.0.992.38'
}
data = {'username': username, 'password': psw}
login_url = 'http://bbs.combpm.com/member.php?mod=logging&action=login&loginsubmit=yes&infloat=yes&lssubmit=yes&inajax=1'
s.post(login_url, headers=headers, data=data)
url = 'http://bbs.combpm.com/plugin.php'
params = {
    'id': 'k_misign:sign',
    'operation': 'qiandao',
    'format': 'empty',
    'inajax': 1,
    'ajaxtarget': 'JD_sign'
}
req = s.get(url, data=params, headers=headers, verify=False).text
formhash = re.findall(r'name="formhash" value="(.*)?"', req)[0]
params['formhash'] = formhash
s.get(url, params=params, headers=headers, verify=False)
req = s.get('http://bbs.combpm.com/k_misign-sign.html', data=params, headers=headers, verify=False).text
m = re.findall(r'您的签到排名', req)
if m:
    msg = username + ' 今日已签到'
else:
    msg = username + ' 签到失败'
QYWX_Notify().send('蜂巢物业论坛签到信息', msg)
