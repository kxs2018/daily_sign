# -- coding: utf-8 --
import random
import requests
from QYWX_Notify import QYWX_Notify
import os


def UserAgent():  # 随机获取请求头
    user_agent_list = [
        'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1464.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.16 Safari/537.36',
        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.3319.102 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS i686 3912.101.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36',
        'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:17.0) Gecko/20100101 Firefox/17.0.6',
        'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1468.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2224.3 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS i686 3912.101.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36']
    UserAgent = {'User-Agent': random.choice(user_agent_list)}
    return UserAgent


def main():
    judge = os.getenv('JUDGE')
    if judge:
        provice = os.getenv('PROVINCE')
        url = "https://c.m.163.com/ug/api/wuhan/app/data/list-total"
        url_json = requests.get(url=url, headers=UserAgent()).json()
        today_confirm = str(url_json['data']['chinaTotal']['today']['confirm'])  # 全国累计确诊较昨日新增
        today_input = str(url_json['data']['chinaTotal']['today']['input'])  # 全国较昨日新增境外输入
        today_storeConfirm = str(url_json['data']['chinaTotal']['today']['storeConfirm'])  # 全国现有确诊较昨日
        today_dead = str(url_json['data']['chinaTotal']['today']['dead'])  # 累计死亡较昨日新增
        today_heal = str(url_json['data']['chinaTotal']['today']['heal'])  # 累计治愈较昨日新增
        today_incrNoSymptom = str(url_json['data']['chinaTotal']['extData']['incrNoSymptom'])  # 无症状感染者较昨日
        total_confirm = str(url_json['data']['chinaTotal']['total']['confirm'])  # 全国累计确诊
        total_input = str(url_json['data']['chinaTotal']['total']['input'])  # 境外输入
        total_dead = str(url_json['data']['chinaTotal']['total']['dead'])  # 累计死亡
        total_heal = str(url_json['data']['chinaTotal']['total']['heal'])  # 累计治愈
        total_storeConfirm = str(
            url_json['data']['chinaTotal']['total']['confirm'] - url_json['data']['chinaTotal']['total']['dead'] -
            url_json['data']['chinaTotal']['total']['heal'])  # 全国现有确诊
        total_noSymptom = str(url_json['data']['chinaTotal']['extData']['noSymptom'])  # 无症状感染者
        lastUpdateTime = url_json['data']['lastUpdateTime']  # 截止时间
        if provice:
            areatree = url_json['data']['areaTree']
            for i in areatree:
                if i['name'] == '中国':
                    provices = i['children']
                    break
            for i in provices:
                if i['name'] == provice:
                    p_today_confirm = str(i['today'].get('confirm'))
                    if p_today_confirm == 'None':
                        p_today_confirm = '0'
                    p_today_suspect = str(i['today'].get('suspect'))
                    if p_today_suspect == 'None':
                        p_today_suspect = '0'
                    p_total_suspect = str(i['total'].get('suspect'))
                    if p_today_suspect == 'None':
                        p_today_suspect = '0'
                    p_today_severe = str(i['today'].get('severe'))
                    if p_today_severe == 'None':
                        p_today_severe = '0'
                    p_total_severe = str(i['total'].get('severe'))
                    if p_total_severe == 'None':
                        p_total_severe = '0'
                    p_today_noSymptom = str(i['today'].get('noSymptom'))
                    if p_today_noSymptom == 'None':
                        p_today_noSymptom = '0'
                    p_today_heal = str(i['today'].get('heal'))
                    if p_today_heal == 'None':
                        p_today_heal = '0'
                    p_today_dead = str(i['today'].get('dead'))
                    if p_today_dead == 'None':
                        p_today_dead = '0'
                    p_today_input = str(i['today'].get('input'))
                    if p_today_input == 'None':
                        p_today_input = '0'
                    p_today_storeConfirm = str(i['today'].get('storeConfirm'))
                    if p_today_storeConfirm == 'None':
                        p_today_storeConfirm = '0'
                    p_lastUpdateTime = i['lastUpdateTime']
                    p_total_confirm = str(i['total'].get('confirm'))
                    if p_total_confirm == 'None':
                        p_total_confirm = '0'
                    p_total_noSymptom = str(i['total'].get('noSymptom'))
                    if p_total_noSymptom == 'None':
                        p_total_noSymptom = '0'
                    p_total_storeConfirm = str(i['total'].get('storeConfirm'))
                    if p_total_storeConfirm == 'None':
                        p_total_storeConfirm = '0'
                    p_total_input = str(i['total'].get('input'))
                    if p_total_input == 'None':
                        p_total_input = '0'
                    p_total_dead = str(i['total'].get('dead'))
                    if p_total_dead == 'None':
                        p_total_dead = '0'
                    p_total_heal = str(i['total'].get('heal'))
                    if p_total_heal == 'None':
                        p_total_heal = '0'
                    digest = f'\n{provice}新增确诊病例{p_today_confirm}'
                    content = "-" * 32 + "\n\n\n" + \
                              "-" * 8 + f"{provice}疫情数据实时统计" + "-" * 8 + "\n\n统计截至时间：" + p_lastUpdateTime + "\n\n" + "-" * 32 + "\n\n" + \
                              "  累计确诊：" + p_total_confirm + " ; " + "较昨日：" + p_today_confirm + \
                              "\n\n  现有确诊：" + p_total_storeConfirm + " ; " + "较昨日：" + p_today_storeConfirm + \
                              "\n\n  累计死亡：" + p_total_dead + " ; " + "较昨日：" + p_today_dead + \
                              "\n\n  累计治愈：" + p_total_heal + " ; " + "较昨日：" + p_today_heal + \
                              "\n\n  境外输入：" + p_total_input + " ; " + "较昨日：" + p_today_input + \
                              "\n\n  无症状感染者：" + p_total_noSymptom + " ; " + "较昨日：" + p_today_noSymptom + \
                              "\n\n  重症患者：" + p_total_severe + " ; " + "较昨日：" + p_today_severe + \
                              "\n\n  疑似病例：" + p_total_suspect + " ; " + "较昨日：" + p_today_suspect

        content = "-" * 8 + "全国疫情数据实时统计" + "-" * 8 + "\n\n\n统计截至时间：" + lastUpdateTime + "\n\n" + "-" * 32 + "\n\n" + \
                  "  累计确诊：" + total_confirm + " ; " + "较昨日：" + today_confirm + \
                  "\n\n  现有确诊：" + total_storeConfirm + " ; " + "较昨日：" + today_storeConfirm + \
                  "\n\n  累计死亡：" + total_dead + " ; " + "较昨日：" + today_dead + \
                  "\n\n  累计治愈：" + total_heal + " ; " + "较昨日：" + today_heal + \
                  "\n\n  境外输入：" + total_input + " ; " + "较昨日：" + today_input + \
                  "\n\n  无症状感染者：" + total_noSymptom + " ; " + "较昨日：" + today_incrNoSymptom + "\n\n\n" + content
        digest = f'全国新增确诊病例{today_confirm}' + digest
        QYWX_Notify().send('疫情通报', digest, content)


if __name__ == '__main__':
    main()
