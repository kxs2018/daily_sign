# -- coding: utf-8 --
import requests
from lxml import etree
from QYWX_Notify import QYWX_Notify
import os


def toollu_signin():
    cookie = os.getenv('TOOLLU_COOKIE')
    if cookie:
        url = 'https://plus.tool.lu/user/sign'
        headers = {'cookie': cookie,
                   'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4421.0 Safari/537.36 Edg/90.0.810.1'}
        resp = requests.get(url, headers=headers).text
        html = etree.HTML(resp)
        msg = html.xpath('//section[@class="panel-body"]/p/text()')[0]
        QYWX_Notify().send('tool.lu签到信息', msg)


if __name__ == '__main__':
    toollu_signin()