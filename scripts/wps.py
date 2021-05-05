# -- coding: utf-8 --
import requests
import time
import json
import pytz
import datetime
import re
import random
from io import StringIO
import os
from QYWX_Notify import QYWX_Notify

# 参考以下代码解决https访问警告
from requests.packages.urllib3.exceptions import InsecureRequestWarning, InsecurePlatformWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
requests.packages.urllib3.disable_warnings(InsecurePlatformWarning)

invite_sid = [
    "V02StVuaNcoKrZ3BuvJQ1FcFS_xnG2k00af250d4002664c02f",
    "V02SWIvKWYijG6Rggo4m0xvDKj1m7ew00a8e26d3002508b828",
    "V02Sr3nJ9IicoHWfeyQLiXgvrRpje6E00a240b890023270f97",
    "V02SBsNOf4sJZNFo4jOHdgHg7-2Tn1s00a338776000b669579",
    "V02ScVbtm2pQD49ArcgGLv360iqQFLs014c8062e000b6c37b6",
    "V02S2oI49T-Jp0_zJKZ5U38dIUSIl8Q00aa679530026780e96",
    "V02ShotJqqiWyubCX0VWTlcbgcHqtSQ00a45564e002678124c",
    "V02SFiqdXRGnH5oAV2FmDDulZyGDL3M00a61660c0026781be1",
    "V02S7tldy5ltYcikCzJ8PJQDSy_ElEs00a327c3c0026782526",
    "V02SPoOluAnWda0dTBYTXpdetS97tyI00a16135e002684bb5c",
    "V02Sb8gxW2inr6IDYrdHK_ywJnayd6s00ab7472b0026849b17",
    "V02SwV15KQ_8n6brU98_2kLnnFUDUOw00adf3fda0026934a7f",
    "V02SC1mOHS0RiUBxeoA8NTliH2h2NGc00a803c35002693584d"

]

# 初始化日志
cio = StringIO("WPS签到日志\n\n")
cio.seek(0, 2)  # 将读写位置移动到结尾
dio = StringIO()
s = requests.session()
tz = pytz.timezone('Asia/Shanghai')
nowtime = datetime.datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
signtime = datetime.datetime.now(tz).strftime("%H %M")
notifytime = [8, 19]
cio.write("---" + nowtime + "---\n\n")


# WPS客户端签到，每周三天会员左右，需手动兑换
def wps_client_clockin(sid):
    cio.write("          ---wps PC客户端签到---↓\n\n")
    if len(sid) == 0:
        cio.write("签到失败: 用户sid为空, 请重新输入\n\n")
        return 0
    elif "*" in sid or sid[0] != "V":
        cio.write("签到失败: 用户sid错误, 请重新输入\n\n")
        return 0
    url = "https://vipapi.wps.cn/wps_clock/v1"
    headers = {
        "Cookie": "wps_sid=" + sid,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2486.0 Safari/537.36 Edge/13.10586"
    }
    data = {
        'double': 0
    }
    req = requests.get(url, headers=headers)
    if not ("msg" in req.text):
        # 判断wps_sid是否失效
        cio.write("wps_sid无效")
        return 0
    else:
        if json.loads(req.text)["result"] == "ok":
            req = requests.post(url, headers=headers, data=data)
            if json.loads(req.text)["result"] == "ok":
                cio.write("客户端签到成功，请手动去客户端兑换时长\n")
                return 1
            else:
                if json.loads(req.text)["data"] == "ClockAgent":
                    cio.write("你已经签到过了\n")
                else:
                    cio.write('未知错误:' + json.loads(req.text)["data"] + "\n")
                return 0
        else:
            if json.loads(req.text)["result"] == "UserNotLogin":
                cio.write("您貌似没有在电脑上登陆过\n")
            else:
                cio.write('未知错误:' + json.loads(req.text)["result"] + "\n")
            return 0


# WPS简历助手稻壳会员签到
def wps_miniapp_sign(sid):
    cio.write("          ---WPS简历助手小程序签到---↓\n\n")
    if len(sid) == 0:
        cio.write("签到失败: 用户sid为空, 请重新输入\n\n")
        return 0
    elif "*" in sid or sid[0] != "V":
        cio.write("签到失败: 用户sid错误, 请重新输入\n\n")
        return 0
    url = "https://vipapi.wps.cn/miniapp_sign_in/v1/user/sign_in"
    headers = {
        "sid": sid,
    }
    req = requests.post(url, headers=headers)
    if not ("msg" in req.text):
        # 判断wps_sid是否失效
        cio.write("wps_sid无效")
        return 0
    else:
        if (json.loads(req.text)["result"] == "ok"):
            cio.write("WPS简历助手小程序签到成功（签到七天给5天会员）\n\n")
            return 1
        else:
            cio.write('未知错误:' + json.loads(req.text)["msg"] + "\n\n")
            return 0


# wps网页签到
def wps_webpage_clockin(sid: str):
    cio.write("          ---wps网页签到---↓\n\n")
    if len(sid) == 0:
        cio.write("签到失败: 用户sid为空, 请重新输入\n\n")
        return 0
    elif "*" in sid or sid[0] != "V":
        cio.write("签到失败: 用户sid错误, 请重新输入\n\n")
        return 0

    url = "https://vip.wps.cn/sign/v2"
    headers = {
        "Cookie": "wps_sid=" + sid,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2486.0 Safari/537.36 Edge/13.10586"
    }
    data = {
        "platform": "8",
        "captcha_pos": "137.00431974731889, 36.00431593261568",
        "img_witdh": "275.164",
        "img_height": "69.184"
    }  # 带验证坐标的请求
    data0 = {"platform": "8"}  # 不带验证坐标的请求
    yz_url = "https://vip.wps.cn/checkcode/signin/captcha.png?platform=8&encode=0&img_witdh=275.164&img_height=69.184"

    req = requests.post(url=url, headers=headers, data=data)
    if not ("msg" in req.text):
        # 判断wps_sid是否失效
        cio.write("wps_sid无效")
        return 0
    else:
        sus = json.loads(req.text)["result"]  # 第一次：不带验证码的请求结果
        if sus == "error":
            for n in range(50):
                requests.get(url=yz_url, headers=headers)
                req = requests.post(url=url, headers=headers, data=data)
                sus = json.loads(req.text)["result"]
                time.sleep(random.randint(0, 5) / 10)
                if sus == "ok":
                    break
        cio.write("签到结果-->" + sus + "\n\n")
        return 1


# Docer网页签到
def docer_webpage_clockin(sid: str):
    cio.write("\n\n          ---稻壳网页签到---↓\n\n")
    docer_url = 'https://zt.wps.cn/2018/docer_check_in/api/checkin_today'
    r = s.post(docer_url, headers={'sid': sid})
    if len(r.history) != 0:
        if r.history[0].status_code == 302:
            cio.write("签到失败: 用户sid错误, 请重新输入\n\n")
            return 0
    resp = json.loads(r.text)
    if resp['result'] == 'ok':
        cio.write("签到信息: {}\n\n".format(r.text))
        return 1
    elif resp['msg'] == 'recheckin':
        cio.write("签到信息: 重复签到\n\n")
        return 1


# Docer网页补签
def docer_webpage_earlyclockin(sid, checkinEarly_times, checkinrecord, max_days):
    now = datetime.datetime.now(tz)
    this_month_start = datetime.datetime(now.year, now.month, 1).date()
    checkin_Earliestdate = datetime.datetime.strptime(checkinrecord[0]['checkin_date'], '%Y-%m-%d').date()
    for i in range(checkinEarly_times):
        if checkin_Earliestdate.day > this_month_start.day:
            checkin_date = checkin_Earliestdate - datetime.timedelta(days=(i + 1))
            checkin_date = datetime.datetime.strptime(str(checkin_date), '%Y-%m-%d').strftime('%Y%m%d')
            checkinEarly_url = 'https://zt.wps.cn/2018/docer_check_in/api/checkin_early'
            s.post(checkinEarly_url, data={'date': checkin_date}, headers={'sid': sid})
        else:
            if i == 0:
                cio.write("无需补签\n\n")
                return max_days
            else:
                cio.write("使用补签卡{}张\n\n".format(i))
                checinRecord_url = 'https://zt.wps.cn/2018/docer_check_in/api/checkin_record'
                r = s.get(checinRecord_url, headers={'sid': sid})
                resp = json.loads(r.text)
                cio.write("补签后连续签到: {}天\n\n".format(resp['data']['max_days']))
                return resp['data']['max_days']
    cio.write("使用补签卡{}张\n\n".format(i))
    checinRecord_url = 'https://zt.wps.cn/2018/docer_check_in/api/checkin_record'
    r = s.get(checinRecord_url, headers={'sid': sid})
    resp = json.loads(r.text)
    cio.write("补签后连续签到: {}天\n\n".format(resp['data']['max_days']))
    return resp['data']['max_days']


# Docer网页领取礼物
def docer_webpage_giftReceive(sid, max_days):
    userinfo_url = 'https://vip.wps.cn/userinfo'
    r = s.get(userinfo_url, headers={'sid': sid})
    resp = json.loads(r.text)
    memberid = [0]
    if len(resp['data']['vip']['enabled']) > 0:
        for i in range(len(resp['data']['vip']['enabled'])):
            memberid.append(resp['data']['vip']['enabled'][i]['memberid'])
    rewardRecord_url = 'https://zt.wps.cn/2018/docer_check_in/api/reward_record'
    rewardReceive_url = 'https://zt.wps.cn/2018/docer_check_in/api/receive_reward'
    r = s.get(rewardRecord_url, headers={'sid': sid})
    resp = json.loads(r.text)
    rewardRecord_list = resp['data']
    if len(rewardRecord_list) > 0:
        for i in rewardRecord_list:
            if i['reward_type'] == 'vip' or i['reward_type'] == 'code':
                if int(i['limit_days']) <= max_days and int(i['limit_vip']) in memberid and i['status'] == 'unreceived':
                    r1 = s.post(rewardReceive_url, data={'reward_id': i['id'], 'receive_from': 'pc_client'},
                                headers={'sid': sid})
                    cio.write('领取礼物: {} '.format(i['reward_name']))
                    if 'reward_info' in r1.text:
                        resp1 = json.loads(r1.text)
                        cio.write('礼物信息: {}'.format(resp1['data']['reward_info']))
                    else:
                        cio.write('领取信息: {}'.format(r1.text))
                    cio.write("\n\n")
                elif i['status'] == 'received':
                    cio.write('已领取礼物: {} '.format(i['reward_name']))
                    if 'reward_info' in i:
                        cio.write('礼物信息: {}'.format(i['reward_info']))
                    cio.write("\n\n")


# wps小程序签到
def wps_miniprogram_clockin(sid: str):
    cio.write("\n\n          ---wps小程序签到---↓\n\n")
    if len(sid) == 0:
        cio.write("签到失败: 用户sid为空, 请重新输入\n\n")
        return 0
    elif "*" in sid or sid[0] != "V":
        cio.write("签到失败: 用户sid错误, 请重新输入\n\n")
        return 0
    # 打卡签到
    clockin_url = 'http://zt.wps.cn/2018/clock_in/api/clock_in'
    r = s.get(clockin_url, headers={'sid': sid})
    if len(r.history) != 0:
        if r.history[0].status_code == 302:
            cio.write("签到失败: 用户sid错误, 请重新输入\n\n")
            return 0
    resp = json.loads(r.text)
    # 判断是否已打卡
    if resp['msg'] == '已打卡':
        cio.write("签到信息: {}\n\n".format(r.text))
        return 1
    # 判断是否绑定手机
    elif resp['msg'] == '未绑定手机':
        cio.write('签到失败: 未绑定手机, 请绑定手机后重新运行签到\n\n')
        return 0
    # 判断是否重新报名
    elif resp['msg'] == '前一天未报名':
        cio.write("前一天未报名\n\n")
        signup_url = 'http://zt.wps.cn/2018/clock_in/api/sign_up'
        r = s.get(signup_url, headers={'sid': sid})
        resp = json.loads(r.text)
        if resp['result'] == 'ok':
            cio.write("报名信息: 已自动报名, 报名后第二天签到\n\n")
            return 1
        else:
            cio.write("报名失败: 请手动报名, 报名后第二天签到\n\n")
            return 0
    # 打卡签到需要参加活动
    elif resp['msg'] == '答题未通过':
        getquestion_url = 'http://zt.wps.cn/2018/clock_in/api/get_question?member=wps'
        r = s.get(getquestion_url, headers={'sid': sid})
        answer_set = {
            'WPS会员全文检索',
            '100G',
            'WPS会员数据恢复',
            'WPS会员PDF转doc',
            'WPS会员PDF转图片',
            'WPS图片转PDF插件',
            '金山PDF转WORD',
            'WPS会员拍照转文字',
            '使用WPS会员修复',
            'WPS全文检索功能',
            '有，且无限次',
            '文档修复'
        }
        resp = json.loads(r.text)
        # cio.write(resp['data']['multi_select'])
        # 只做单选题 multi_select==1表示多选题
        while resp['data']['multi_select'] == 1:
            r = s.get(getquestion_url, headers={'sid': sid})
            resp = json.loads(r.text)
            # cio.write('选择题类型: {}'.format(resp['data']['multi_select']))
        answer_id = 3
        for i in range(4):
            opt = resp['data']['options'][i]
            if opt in answer_set:
                answer_id = i + 1
                break
        cio.write("选项: {}\n\n".format(resp['data']['options']))
        cio.write("选择答案: {}\n\n".format(answer_id))
        # 提交答案
        answer_url = 'http://zt.wps.cn/2018/clock_in/api/answer?member=wps'
        r = s.post(answer_url, headers={'sid': sid}, data={'answer': answer_id})
        resp = json.loads(r.text)
        # 答案错误
        if resp['msg'] == 'wrong answer':
            cio.write("答案不对, 挨个尝试\n\n")
            for i in range(4):
                r = s.post(answer_url, headers={'sid': sid}, data={'answer': i + 1})
                resp = json.loads(r.text)
                cio.write(str(i + 1))
                if resp['result'] == 'ok':
                    cio.write(r.text)
                    break
        # 打卡签到
        clockin_url = 'http://zt.wps.cn/2018/clock_in/api/clock_in?member=wps'
        r = s.get(clockin_url, headers={'sid': sid})
        cio.write("签到信息: {}\n\n".format(r.text))
        return 1
    elif resp['msg'] == 'ParamData Empty':
        cio.write("签到失败信息: {}\n\n".format(r.text))
        signup_url = 'http://zt.wps.cn/2018/clock_in/api/sign_up'
        r = s.get(signup_url, headers={'sid': sid})
        cio.write('签到接口失效, 请手动打卡\n\n')
        return 1
    elif resp['msg'] == '不在打卡时间内':
        cio.write("签到失败: 不在打卡时间内\n\n")
        signup_url = 'http://zt.wps.cn/2018/clock_in/api/sign_up'
        r = s.get(signup_url, headers={'sid': sid})
        resp = json.loads(r.text)
        if resp['result'] == 'ok':
            cio.write("已自动报名, 报名后请设置在规定时间内签到\n\n")
            return 1
        else:
            cio.write("报名失败: 请手动报名, 报名后第二天签到\n\n")
            return 0
    # 其他错误
    elif resp['result'] == 'error':
        cio.write("签到失败信息: {}\n\n".format(r.text))
        signup_url = 'http://zt.wps.cn/2018/clock_in/api/sign_up'
        r = s.get(signup_url, headers={'sid': sid})
        resp = json.loads(r.text)
        if resp['result'] == 'ok':
            cio.write("已自动报名, 报名后请设置在规定时间内签到\n\n")
            return 1
        else:
            cio.write("报名失败: 请手动报名, 报名后第二天签到\n\n")
            return 0


# wps小程序接受邀请
def wps_miniprogram_invite(invite_sid: list, invite_userid: int) -> None:
    invite_url = 'http://zt.wps.cn/2018/clock_in/api/invite'
    k = 0
    for index, i in enumerate(invite_sid):

        headers = {
            'sid': i
        }
        time.sleep(2 + random.random())
        r = s.post(invite_url, headers=headers, data={
            'invite_userid': invite_userid,
            "client_code": "040ce6c23213494c8de9653e0074YX30",
            "client": "alipay"})
        if r.status_code == 200:
            try:
                resp = json.loads(r.text)
                if resp['result'] == 'ok':
                    k += 1
                else:
                    cio.write("邀请对象: {}, Result: {}\n\n".format(invite_sid[i], resp['msg']))
            except:
                cio.write("邀请对象: {}, Result: ID已失效\n\n".format(invite_sid[i]))
        else:
            cio.write("邀请对象: {}, 状态码: {},\n\n 请求信息{}\n\n".format(invite_sid[i], r.status_code, r.text[:25]))
        return k


# 主函数
def main():
    sid = os.getenv('WPS_COOKIE')
    if sid:
        b0 = wps_webpage_clockin(sid)
        if b0 == 1:
            # 获取当前网页签到信息
            dio.write("wps网页签到成功\n\n")
            taskcenter_url = 'https://vipapi.wps.cn/task_center/task/summary'
            r = s.post(taskcenter_url, headers={'sid': sid})
            resp = json.loads(r.text)
            r = s.post(taskcenter_url, headers={'sid': sid})
            resp = json.loads(r.text)
            cio.write("已领取积分: {}\n\n".format(resp['data']['wpsIntegral']))
            cio.write("已领取会员: {}天\n\n".format(resp['data']['member']))
            cio.write("已完成任务: {}项\n\n".format(resp['data']['taskNum']))
            cio.write("\n")
        else:
            dio.write("wps网页签到失败\n\n")
            content = cio.getvalue()
            digest = dio.getvalue()
            if digest[-2:] == "\n\n":
                digest = digest[0:-2]
            content = content.replace("\n\n", '\n')
            digest = digest.replace("\n\n", '\n')
            QYWX_Notify().send('WPS签到信息', digest, content)
            print(content)
            return content

        b0 = wps_client_clockin(sid)
        if b0 == 1:
            # 获取当前网页签到信息
            dio.write("wps PC客户端签到成功\n\n")
        else:
            dio.write("wps PC客户端签到失败\n\n")

        # WPS简历助手小程序
        b0 = wps_miniapp_sign(sid)
        if b0 == 1:
            # 获取当前网页签到信息
            dio.write("WPS简历助手小程序签到成功\n\n")
        else:
            dio.write("WPS简历助手小程序签到失败\n\n")

        b1 = docer_webpage_clockin(sid)
        if b1 == 1:
            checinRecord_url = 'https://zt.wps.cn/2018/docer_check_in/api/checkin_record'
            r = s.get(checinRecord_url, headers={'sid': sid})
            resp = json.loads(r.text)
            cio.write('本期连续签到: {}天\n\n'.format(resp['data']['max_days']))
            checkinEarlytimes_url = 'https://zt.wps.cn/2018/docer_check_in/api/checkin_early_times'
            r1 = s.get(checkinEarlytimes_url, headers={'sid': sid})
            resp1 = json.loads(r1.text)
            cio.write('拥有补签卡: {}张\n\n'.format(resp1['data']))
            max_days = resp['data']['max_days']
            if resp1['data'] > 0 and len(resp['data']['records']) > 0:
                max_days = docer_webpage_earlyclockin(sid, resp1['data'], resp['data']['records'], max_days)
            if len(resp['data']['records']) > 0:
                docer_webpage_giftReceive(sid, max_days)
            dio.write("稻壳网页签到成功\n\n")
        else:
            dio.write("稻壳网页签到失败\n\n")

        b2 = wps_miniprogram_clockin(sid)
        if b2 == 1:
            # 获取小程序当前会员奖励信息
            member_url = 'https://zt.wps.cn/2018/clock_in/api/get_data?member=wps'
            r = s.get(member_url, headers={'sid': sid})
            # 累计在小程序打卡中获得会员天数
            total_add_day = re.search('"total_add_day":(\d+)', r.text).group(1)
            cio.write("小程序打卡中累计获得会员: {}天\n\n".format(total_add_day))
            dio.write("小程序打卡成功\n\n")
        else:
            dio.write("小程序打卡失败\n\n")

        # wps签到邀请
        cio.write("\n\n          ---wps小程序邀请---↓\n\n")
        userinfo_url = 'https://vip.wps.cn/userinfo'
        r = s.get(userinfo_url, headers={'sid': sid})
        resp = json.loads(r.text)
        if type(resp['data']['userid']) == int:
            k = wps_miniprogram_invite(invite_sid, resp['data']['userid'])
            cio.write("邀请完成，成功邀请{}人\n\n".format(k))
            dio.write('小程序成功邀请{}人\n\n'.format(k))
        else:
            cio.write("邀请失败: 用户ID错误, 请检查用户sid\n\n")
            dio.write("小程序邀请失败\n\n")

        # 获取当前用户信息
        cio.write("\n\n          ---当前用户信息---↓\n\n")
        summary_url = 'https://vip.wps.cn/2019/user/summary'
        r = s.post(summary_url, headers={'sid': sid})
        resp = json.loads(r.text)
        cio.write("会员积分:{}\n\n'稻米数量':{}\n\n".format(resp['data']['integral'], resp['data']['wealth']))
        userinfo_url = 'https://vip.wps.cn/userinfo'
        r = s.get(userinfo_url, headers={'sid': sid})
        resp = json.loads(r.text)
        if len(resp['data']['vip']['enabled']) > 0:
            cio.write("会员信息:\n\n")
            for i in range(len(resp['data']['vip']['enabled'])):
                cio.write("'类型':{}, '过期时间':{}\n\n".format(resp['data']['vip']['enabled'][i]['name'],
                                                          datetime.datetime.fromtimestamp(
                                                              resp['data']['vip']['enabled'][i][
                                                                  'expire_time']).strftime("%Y--%m--%d %H:%M:%S")))
                dio.write("'类型':{}, '过期时间':{}\n\n".format(resp['data']['vip']['enabled'][i]['name'],
                                                          datetime.datetime.fromtimestamp(
                                                              resp['data']['vip']['enabled'][i][
                                                                  'expire_time']).strftime("%Y/%m/%d")))
        if int(signtime.split()[0]) in notifytime:
            content = cio.getvalue()
            digest = dio.getvalue()
            if digest[-2:] == "\n\n":
                digest = digest[0:-2]
            content = content.replace("\n\n", "\n")
            digest = digest.replace("\n\n", "\n")
            QYWX_Notify().send('WPS签到信息', digest, content)


if __name__ == '__main__':
    main()
