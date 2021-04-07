# -- coding: utf-8 --
import requests
import re
from io import StringIO
from lxml import etree
import os
from QYWX_Notify import QYWX_Notify

sio = StringIO('uiwow签到日志\n\n\n')
dio = StringIO()
signurl = 'https://www.uiwow.com/plugin.php'

headers = {
    'host': 'www.uiwow.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4437.0 Safari/537.36 Edg/91.0.831.1',
}


def get_hash(cookie):
    params = {
        'id': 'dc_signin:sign',
        'inajax': 1
    }
    try:
        req = requests.get(signurl, cookies=cookie, headers=headers, params=params).content.decode('utf-8')
        formhash = re.findall(r'name="formhash" value="(.*)?"', req)[0]
        return formhash
    except:
        return


def signin(cookie):
    formhash = get_hash(cookie)
    if formhash:
        params = {'id': 'dc_signin:sign',
                  'inajax': 1,
                  'formhash': formhash,
                  'signsubmit': 'yes',
                  'handlekey': 'signin',
                  'emotid': 1,
                  'referer': 'https://www.uiwow.com/forum.php',
                  'content': '开森的我开森的签到一下！'}
        requests.post(signurl, params=params, headers=headers, cookies=cookie)
    return


def get_stat(cookie):
    stat_url = 'http://www.uiwow.com/plugin.php?id=dc_signin&action=index'
    res = requests.get(stat_url, headers=headers, cookies=cookie)
    html = etree.HTML(res.text)
    sign_div = html.xpath('//*[@class="sign_div"]')[0]
    sign_state = sign_div.xpath('./a/text()')[0]
    date = sign_div.xpath('.//div[@class="date"]/text()')[0]
    username = html.xpath('//div[@id="um"]//strong/a/text()')[0]
    if '已' not in sign_state:
        sio.write(username + ' ' + date + ' 的签到状态是:未' + sign_state + '\n\n\n')
        dio.write(username + ' ' + date + ' 的签到状态是:未' + sign_state + '\n')
    else:
        sio.write(username + ' ' + date + ' 的签到状态是:' + sign_state + '\n\n\n')
        dio.write(username + ' ' + date + ' 的签到状态是:' + sign_state + '\n')
    mytips_data = html.xpath('//div[@class="mytips"]/p')
    for p in mytips_data:
        text = p.xpath('./text()|./b')
        for i in text:
            try:
                sio.write(i.text.strip())
            except:
                sio.write(i.strip())
    sio.write('\n')


def main():
    cookie = os.getenv('UIWOW_COOKIE')
    if cookie:
        cookie = eval(cookie)
        if type(cookie) == list:
            for i in cookie:
                signin(i)
                get_stat(i)
        elif type(cookie) == dict:
            signin(cookie)
            get_stat(cookie)
        else:
            sio.write('cookie错误，请检查cookie格式\n\n\n')
            dio.write('cookie错误，请检查cookie格式\n')
        content = sio.getvalue().strip()
        digest = dio.getvalue()
        QYWX_Notify().send('uiwow签到信息', digest, content)


if __name__ == '__main__':
    main()
