# -*- coding: utf-8 -*-
# 吾爱破解签到
# Author: kxs2018
# date：2021/11/18
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By


def pojie_signin():
    cookie = os.getenv('PJ_COOKIE')
    if cookie:        
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument("window-size=1920,1080")
        options.add_argument("--no-sandbox")
        wd = webdriver.Chrome(options=options)
        wd.get('https://www.52pojie.cn/forum.php')
        time.sleep(0.5)
        cookie = cookie.split(';')
        for c in cookie:
            a = c.split('=')
            if a[0].strip() == 'htVC_2132_auth' or a[0].strip() == 'htVC_2132_saltkey':
                cookie_dict = {'name': a[0].strip(), 'value': a[1].strip()}
                wd.add_cookie(cookie_dict)
        wd.refresh()
        try:
            try:
                wd.find_element(By.XPATH, r'.//div[@id="um"]/p/strong/a')
            except:
                raise Exception('获取用户名失败，cookie失效\n')
            wd.find_element(By.CLASS_NAME, r'qq_bind').click()
        except Exception as e:
            print(e)


if __name__ == '__main__':
    pojie_signin()
