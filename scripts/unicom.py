# -- coding: utf-8 --
import base64
import datetime
import random
import re
import time
from io import StringIO
import os
from QYWX_Notify import QYWX_Notify
import pytz
import requests
import rsa
from lxml.html import fromstring
import json

requests.packages.urllib3.disable_warnings()
cio = StringIO('联通APP签到日志\n\n')
dio = StringIO()
s = requests.Session()


# 获取公钥的key
def str2key(a):
    # 对字符串解码
    b_str = base64.b64decode(a)

    if len(b_str) < 162:
        return False

    hex_str = ''

    # 按位转换成16进制
    for x in b_str:
        h = hex(x)[2:]
        h = h.rjust(2, '0')
        hex_str += h

    # 找到模数和指数的开头结束位置
    m_start = 29 * 2
    e_start = 159 * 2
    m_len = 128 * 2
    e_len = 3 * 2

    modulus = hex_str[m_start:m_start + m_len]
    exponent = hex_str[e_start:e_start + e_len]

    return modulus, exponent


# 对手机号和登录密码进行加密
def encryption(message, key):
    modulus = int(key[0], 16)
    exponent = int(key[1], 16)
    rsa_pubkey = rsa.PublicKey(modulus, exponent)
    crypto = rsa.encrypt(message, rsa_pubkey)
    b64str = base64.b64encode(crypto)
    return b64str


# 进行登录
# 手机号和密码加密代码，参考自这篇文章 http://www.bubuko.com/infodetail-2349299.html?&_=1524316738826
def login(username, password, appId):
    # rsa 公钥
    pubkey = "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDc+CZK9bBA9IU+gZUOc6FUGu7yO9WpTNB0PzmgFBh96Mg1WrovD1oqZ+eIF4LjvxKXGOdI79JRdve9NPhQo07+uqGQgE4imwNnRx7PFtCRryiIEcUoavuNtuRVoBAm6qdB0SrctgaqGfLgKvZHOnwTjyNqjBUxzMeQlEC2czEMSwIDAQAB"
    # 获取公钥的 key
    key = str2key(pubkey)
    # 这里对手机号和密码加密，传入参数需是 byte 类型
    username = encryption(str.encode(username), key)
    password = encryption(str.encode(password), key)
    # appId 联通后端会验证这个值,如不是常登录设备会触发验证码登录
    # appId = os.environ.get('APPID_COVER')
    # 设置一个标志，用户是否登录成功
    flag = False
    cookies = {
        'c_sfbm': '234g_00',
        'logHostIP': 'null',
        'route': '12d5b9200d86b88f39a5fc9055490c12',
        'channel': 'GGPD',
        'city': '075|751|90413273|-99',
        'devicedId': '862802047733163',
        'mobileService1': 'ProEsSI6SM4DbWhaeVsPtve9pu7VWz0m94giTHkPBl40Gx8nebgV!-1027473388',
        'mobileServiceAll': 'a92d76b26705a45a087027f893c70618',
    }

    headers = {
        'Host': 'm.client.10010.com',
        'Accept': '/',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Connection': 'keep-alive',
        'User-Agent': 'ChinaUnicom4.x/3.0 CFNetwork/1197 Darwin/20.0.0',
        'Accept-Language': 'zh-cn',
        'Accept-Encoding': 'deflate, br',
        'Content-Length': '891',
    }

    data = {
        'reqtime': round(time.time() * 1000),
        'simCount': '1',
        'version': 'iphone_c@8.0004',
        'mobile': username,
        'netWay': 'wifi',
        'isRemberPwd': 'false',
        'appId': appId,
        'deviceId': 'b61f7efcba733583170df52d8f2f9f87521b3844d01ccbc774bbfa379eaeb3fa',
        'pip': '192.168.1.4',
        'password': password,
        'deviceOS': '14.0.1',
        'deviceBrand': 'iphone',
        'deviceModel': 'iPad',
        'remark4': '',
        'keyVersion': '',
        'deviceCode': 'B97CDE2A-D435-437D-9FEC-5D821A012972'
    }

    response = s.post('https://m.client.10010.com/mobileService/login.htm', headers=headers,
                      cookies=cookies,
                      data=data, verify=False)
    response.encoding = 'utf-8'
    try:
        result = response.json()
        if result['code'] == '0':
            cio.write(result['default'][-4:] + '登录成功' + '\n\n')
            dio.write(result['default'][-4:] + '登录成功' + '\n')
            s.headers.update({
                'User-Agent': 'Mozilla/5.0 (Linux; Android 10; YAL-AL00 Build/HUAWEIYAL-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/83.0.4103.106 Mobile Safari/537.36; unicom{version:android@8.0600,desmobile:' + str(
                    username) + '};devicetype{deviceBrand:HUAWEI,deviceModel:YAL-AL00};{yw_code:}'})
        else:
            cio.write('【登录】: ' + result['dsc'] + '\n\n')
            dio.write('【登录】: ' + result['dsc'] + '\n')
    except Exception as e:
        cio.write('【登录】: 发生错误，原因为: ' + str(e) + '\n\n')
        dio.write('【登录】: 发生错误，原因为: ' + str(e) + '\n')
    return s


# 获取沃之树首页，得到领流量的目标值
def get_woTree_glowList():
    index = s.post('https://m.client.10010.com/mactivity/arbordayJson/index.htm', verify=False)
    index.encoding = 'utf-8'
    res = index.json()
    return res['data']['flowChangeList']


# 沃之树任务
# 位置: 首页 --> 游戏 --> 沃之树
def woTree_task():
    # 领取4M流量*3
    try:
        flowList = get_woTree_glowList()
        num = 1
        for flow in flowList:
            takeFlow = s.get('https://m.client.10010.com/mactivity/flowData/takeFlow.htm?flowId=' + flow['id'],
                             verify=False)
            takeFlow.encoding = 'utf-8'
            res1 = takeFlow.json()
            if res1['code'] == '0000':
                cio.write('【沃之树-领流量】: 4M流量 x' + str(num) + '\n\n')
            else:
                cio.write('【沃之树-领流量】: 已领取过 x' + str(num) + '\n\n')
            # 等待1秒钟
            time.sleep(1)
            num = num + 1
        s.post('https://m.client.10010.com/mactivity/arbordayJson/getChanceByIndex.htm?index=0', verify=False)
        # 浇水
        grow = s.post('https://m.client.10010.com/mactivity/arbordayJson/arbor/3/0/3/grow.htm', verify=False)
        grow.encoding = 'utf-8'
        res2 = grow.json()
        cio.write('【沃之树-浇水】: 获得' + str(res2['data']['addedValue']) + '培养值' + '\n\n')
        time.sleep(1)
    except Exception as e:
        cio.write('【沃之树】: 错误，原因为: ' + str(e) + '\n\n')


# 经多次测试，都可加倍成功了
# 每日签到，1积分 +4 积分(翻倍)，第七天得到 1G 日包
# 位置: 我的 --> 我的金币
def daySign_task(username):
    try:
        # 参考同类项目 HiCnUnicom 待明日验证是否能加倍成功
        s.headers.update({'referer': 'https://img.client.10010.com/activitys/member/index.html'})
        param = 'yw_code=&desmobile=' + username + '&version=android@$8.0100'
        s.get('https://act.10010.com/SigninApp/signin/querySigninActivity.htm?' + param, verify=False)
        s.headers.update({'referer': 'https://act.10010.com/SigninApp/signin/querySigninActivity.htm?' + param})
        while True:
            daySign = s.post('https://act.10010.com/SigninApp/signin/daySign', verify=False)
            daySign.encoding = 'utf-8'
            res1 = daySign.json()
            if res1['status'] != '0016':
                break
        # 本来是不想加这个的，但是会出现加倍失败的状况，暂时加上也是有可能出问题
        s.post('https://act.10010.com/SigninApp/signin/todaySign')
        s.post('https://act.10010.com/SigninApp/signin/addIntegralDA')
        s.post('https://act.10010.com/SigninApp/signin/getContinuous')
        s.post('https://act.10010.com/SigninApp/signin/getIntegral')
        s.post('https://act.10010.com/SigninApp/signin/getGoldTotal')
        doubleAd = s.post('https://act.10010.com/SigninApp/signin/bannerAdPlayingLogo')
        s.headers.pop('referer')
        doubleAd.encoding = 'utf-8'
        res2 = doubleAd.json()
        if res1['status'] == '0000':
            cio.write('【每日签到】: ' + '打卡成功,' + res2['data']['statusDesc'] + '\n\n')
            dio.write('【每日签到】: ' + '打卡成功,' + res2['data']['statusDesc'] + '\n')
        elif res1['status'] == '0002':
            cio.write('【每日签到】: ' + res1['msg'] + '\n\n')
            dio.write('【每日签到】: ' + res1['msg'] + '\n')
        time.sleep(1)
    except Exception as e:
        cio.write('【每日签到】: 错误，原因为: ' + str(e) + '\n\n')
        dio.write('【每日签到】: 错误，原因为: ' + str(e) + '\n')


# 获取 encrymobile，用于抽奖
def get_encryptmobile():
    page = s.post('https://m.client.10010.com/dailylottery/static/textdl/userLogin', verify=False)
    page.encoding = 'utf-8'
    match = re.search('encryptmobile=\w+', page.text, flags=0)
    usernumber = match.group(0)[14:]
    return usernumber


# 天天抽奖
# 我的 --> 我的金币 --> 天天抽好礼
def luckDraw_task():
    try:
        numjsp = get_encryptmobile()
        # 加上这一堆，看中奖率会不会高点
        s.post('https://m.client.10010.com/mobileservicequery/customerService/share/defaultShare.htm')
        s.get('https://m.client.10010.com/dailylottery/static/doubleball/firstpage?encryptmobile=' + numjsp)
        s.get('https://m.client.10010.com/dailylottery/static/outdailylottery/getRandomGoodsAndInfo?areaCode=076')
        s.get(
            'https://m.client.10010.com/dailylottery/static/active/findActivityInfo?areaCode=076&groupByType=&mobile=' + numjsp)
        for i in range(3):
            luck = s.post(
                'https://m.client.10010.com/dailylottery/static/doubleball/choujiang?usernumberofjsp=' + numjsp)
            luck.encoding = 'utf-8'
            res = luck.json()
            cio.write('【天天抽奖】: ' + res['RspMsg'] + ' x' + str(i + 1) + '\n\n')
            # 等待1秒钟
            time.sleep(1)
    except Exception as e:
        cio.write('【天天抽奖】: 错误，原因为: ' + str(e) + '\n\n')

    # 游戏任务中心每日打卡领积分，游戏任务自然数递增至7，游戏频道每日1积分


# 位置: 首页 --> 游戏 --> 每日打卡
def gameCenterSign_Task(username):
    data1 = {
        'methodType': 'signin',
        'sVersion': '8.0600',
        'deviceType': 'Android'
    }
    data2 = {
        'methodType': 'iOSIntegralGet',
        'gameLevel': '1',
        'deviceType': 'iOS'
    }
    try:
        s.get(
            'https://img.client.10010.com/gametask/index.html?yw_code=&desmobile=' + username + '&version=android@8.0100')
        time.sleep(2)
        headers = {
            'origin': 'https://img.client.10010.com',
            'referer': 'https://img.client.10010.com/gametask/index.html?yw_code=&desmobile=' + username + '&version=android@8.0100'
        }
        s.headers.update(headers)
        # 进行游戏中心签到
        gameCenter = s.post('https://m.client.10010.com/producGame_signin', data=data1, verify=False)
        gameCenter.encoding = 'utf-8'
        res1 = gameCenter.json()
        if res1['respCode'] == '0000' and res1['respDesc'] == '打卡并奖励成功':
            cio.write('【游戏中心签到】: ' + '获得' + str(res1['currentIntegral']) + '积分' + '\n\n')
        elif res1['respCode'] == '0000':
            cio.write('【游戏中心签到】: ' + res1['respDesc'] + '\n\n')
        time.sleep(1)
        # 游戏频道积分
        gameCenter_exp = s.post('https://m.client.10010.com/producGameApp', data=data2, verify=False)
        gameCenter_exp.encoding = 'utf-8'
        res2 = gameCenter_exp.json()
        if res2['code'] == '0000':
            cio.write('【游戏频道打卡】: 获得' + str(res2['integralNum']) + '积分' + '\n\n')
        else:
            cio.write('【游戏频道打卡】: ' + res2['msg'] + '\n\n')
        s.headers.pop('referer')
        s.headers.pop('origin')
        time.sleep(1)
    except Exception as e:
        cio.write('【游戏中心签到】: 错误，原因为: ' + str(e) + '\n\n')


# 开宝箱，赢话费任务 100M 流量
# 位置: 首页 --> 游戏 --> 每日打卡 --> 宝箱任务
def openBox_task():
    s.headers.update({'referer': 'https://img.client.10010.com'})
    s.headers.update({'origin': 'https://img.client.10010.com'})
    data1 = {
        'thirdUrl': 'https://img.client.10010.com/shouyeyouxi/index.html#/youxibaoxiang'
    }
    data2 = {
        'methodType': 'reward',
        'deviceType': 'Android',
        'sVersion': '8.0600',
        'isVideo': 'N'
    }
    param = '?methodType=taskGetReward&taskCenterId=187&sVersion=8.0100&deviceType=Android'
    data3 = {
        'methodType': 'reward',
        'deviceType': 'Android',
        'sVersion': '8.0600',
        'isVideo': 'Y'
    }
    try:
        # 在分类中找到宝箱并开启
        box = s.post('https://m.client.10010.com/mobileService/customer/getShareRedisInfo.htm', data=data1,
                     verify=False)
        box.encoding = 'utf-8'
        time.sleep(1)
        # 观看视频领取更多奖励
        watchAd = s.post('https://m.client.10010.com/game_box', data=data2, verify=False)
        watchAd.encoding = 'utf-8'
        # 等待随机秒钟
        time.sleep(1)
        # 完成任务领取100M流量
        drawReward = s.get('https://m.client.10010.com/producGameTaskCenter' + param, verify=False)
        time.sleep(1)
        watchAd = s.post('https://m.client.10010.com/game_box', data=data3, verify=False)
        drawReward.encoding = 'utf-8'
        res = drawReward.json()
        if res['code'] == '0000':
            cio.write('【100M寻宝箱】: ' + '获得100M流量' + '\n\n')
        else:
            cio.write('【100M寻宝箱】: ' + '任务失败' + '\n\n')
        time.sleep(1)
        s.headers.pop('referer')
        s.headers.pop('origin')
    except Exception as e:
        cio.write('【100M寻宝箱】: 错误，原因为: ' + str(e) + '\n\n')


# 领取 4G 流量包任务，看视频、下载软件每日可获得 240M 流量
# 位置: 我的 --> 我的金币 --> 4G流量包
def collectFlow_task():
    data1 = {
        'stepflag': '22'
    }

    try:
        for i in range(3):
            # 看视频
            watchVideo = s.post('https://act.10010.com/SigninApp/mySignin/addFlow', data1, verify=False)
            watchVideo.encoding = 'utf-8'
            res1 = watchVideo.json()
            if res1['reason'] == '00':
                cio.write('【4G流量包-看视频】: 获得' + res1['addNum'] + 'M流量 x' + str(i + 1) + '\n\n')
            elif res1['reason'] == '01':
                cio.write('【4G流量包-看视频】: 已完成' + ' x' + str(i + 1) + '\n\n')
            else:
                raise Exception('reason:03')
            # 等待1秒钟
            time.sleep(1)
    except Exception as e:
        cio.write('【4G流量包】: 错误，原因为: ' + str(e) + '\n\n')


# 每日领取100定向积分
# 位置: 发现 --> 定向积分 --> 领取定向积分兑爆款
def day100Integral_task():
    data = {
        'from': random.choice('123456789') + ''.join(random.choice('0123456789') for i in range(10))
    }
    try:
        integral = s.post('https://m.client.10010.com/welfare-mall-front/mobile/integral/gettheintegral/v1',
                          data=data)
        integral.encoding = 'utf-8'
        res = integral.json()
        cio.write("【100定向积分】: " + res['msg'] + '\n\n')
        time.sleep(1)
    except Exception as e:
        cio.write('【100定向积分】: 错误，原因为: ' + str(e) + '\n\n')


# 积分抽奖，可在环境变量中设置抽奖次数，否则每天将只会抽奖一次
# 需要注意的是，配置完抽奖次数，程序每运行一次都将触发积分抽奖，直至达每日30次抽奖用完或积分不够(测试过程中未中过奖)
# 位置: 发现 --> 定向积分 --> 小积分，抽好礼
def pointsLottery_task(n):
    try:
        numjsp = get_encryptmobile()
        # 每日首次免费
        oneFree = s.post(
            'https://m.client.10010.com/dailylottery/static/integral/choujiang?usernumberofjsp=' + numjsp)
        oneFree.encoding = 'utf-8'
        res1 = oneFree.json()
        cio.write("【积分抽奖】: " + res1['RspMsg'] + ' x免费' + '\n\n')
        # 如果用户未设置此值，将不会自动抽奖
        # 预防用户输入30以上，造成不必要的抽奖操作
        num = min(30, int(n))
        for i in range(num):
            # 用积分兑换抽奖机会
            s.get(
                'https://m.client.10010.com/dailylottery/static/integral/duihuan?goldnumber=10&banrate=30&usernumberofjsp=' + numjsp)
            # 进行抽奖
            payx = s.post(
                'https://m.client.10010.com/dailylottery/static/integral/choujiang?usernumberofjsp=' + numjsp + '&flag=convert')
            payx.encoding = 'utf-8'
            res2 = payx.json()
            cio.write("【积分抽奖】: " + res2['RspMsg'] + ' x' + str(i + 1) + '\n\n')
            # 等待随机秒钟
            time.sleep(1)
    except Exception as e:
        cio.write('【积分抽奖】: 错误，原因为: ' + str(e) + '\n\n')


# 冬奥积分活动，第1和7天，可领取600定向积分，其余领取300定向积分,有效期至下月底
# 位置: 发现 --> 定向积分 --> 每日领积分超值兑东奥特许商品
def dongaoPoints_task():
    data = {
        'from': random.choice('123456789') + ''.join(random.choice('0123456789') for i in range(10))
    }
    trance = [600, 300, 300, 300, 300, 300, 300]
    try:
        # 领取积分奖励
        dongaoPoint = s.post('https://m.client.10010.com/welfare-mall-front/mobile/winterTwo/getIntegral/v1',
                             data=data)
        dongaoPoint.encoding = 'utf-8'
        res1 = dongaoPoint.json()
        # 查询领了多少积分
        dongaoNum = s.post('https://m.client.10010.com/welfare-mall-front/mobile/winterTwo/winterTwoShop/v1',
                           data=data)
        dongaoNum.encoding = 'utf-8'
        res2 = dongaoNum.json()
        # 领取成功
        if res1['resdata']['code'] == '0000':
            # 当前为连续签到的第几天
            day = int(res2['resdata']['signDays'])
            # 签到得到的积分
            point = trance[day % 7] + 300 if day == 1 else trance[day % 7]
            cio.write('【东奥积分活动】: ' + res1['resdata']['desc'] + '，' + str(point) + '积分' + '\n\n')
        else:
            cio.write('【东奥积分活动】: ' + res1['resdata']['desc'] + '，' + res2['resdata']['desc'] + '\n\n')
        time.sleep(1)
    except Exception as e:
        cio.write('【东奥积分活动】: 错误，原因为: ' + str(e) + '\n\n')


# 获取积分余额
# 分类：奖励积分、定向积分、通信积分
def getIntegral():
    try:
        integral = s.post('https://m.client.10010.com/welfare-mall-front/mobile/show/bj2205/v2/Y')
        integral.encoding = 'utf-8'
        res = integral.json()
        for r in res['resdata']['data']:
            if r['name'] is not None and r['number'] is not None:
                cio.write('【' + str(r['name']) + '】: ' + str(r['number']) + '\n\n')
                dio.write('【' + str(r['name']) + '】: ' + str(r['number']) + '\n')
        time.sleep(1)
    except Exception as e:
        cio.write('【积分余额】: 错误，原因为: ' + str(e) + '\n\n')
        dio.write('【积分余额】: 错误，原因为: ' + str(e) + '\n')


# 获得我的礼包页面对象
def getQuerywinning(username):
    # 获得我的礼包页面
    querywinninglist = s.get(
        'http://m.client.10010.com/myPrizeForActivity/querywinninglist.htm?yw_code=&desmobile=' + str(
            username) + '&version=android@8.0100')
    querywinninglist.encoding = 'utf-8'
    # 将页面格式化
    doc = f"""{querywinninglist.text}"""
    # 转换为html对象
    html = fromstring(doc)
    return html


# 存储并返回未使用的流量包
def getStorageFlow(username):
    # 获得我的礼包页面
    html = getQuerywinning(username)
    # 寻找ul下的所有li，在未使用流量包栏页面
    ul = html.xpath('/html/body/div[1]/div[7]/ul/li')
    # 存储流量包数据
    datas = []
    # 获得所有流量包的标识并存储
    for li in ul:
        data = {
            'activeCode': None,
            'prizeRecordID': None,
            'phone': None
        }
        tran = {1: 'activeCode', 2: 'prizeRecordID', 3: 'phone'}
        line = li.attrib.get('onclick')
        # 正则匹配字符串 toDetailPage('2534','20210307073111185674422127348889','18566669999');
        pattern = re.finditer(r'\'[\dA-Za-z]+\'', line)
        i = 1
        for match in pattern:
            data[tran[i]] = match.group()[1:-1]
            i = i + 1
        datas.append(data)
    return datas


# 获取Asia/Shanghai时区时间戳
def getTimezone():
    timezone = pytz.timezone('Asia/Shanghai')
    dt = datetime.datetime.now(timezone).strftime("%Y-%m-%d %H:%M:%S")
    timeArray = time.strptime(dt, "%Y-%m-%d %H:%M:%S")
    timeStamp = int(time.mktime(timeArray))
    return timeStamp


# 获得流量包的还剩多长时间结束，返回形式时间戳
def getflowEndTime(username):
    # 获得中国时间戳
    now = getTimezone()
    # 获得我的礼包页面对象
    html = getQuerywinning(username)
    # 获得流量包到期的时间戳
    endStamp = []
    endTime = html.xpath('/html/body/div[1]/div[7]/ul/li[*]/div[2]/p[3]')
    for end in endTime:
        # 寻找起止时间间隔位置
        # end为空，可能无到期时间和开始时间
        end = end.text
        if end is not None:
            index = end.find('-') + 1
            # 切割得到流量包失效时间
            end = end[index:index + 10] + ' 23:59:59'
            end = end.replace('.', '-')
            # 将时间转换为时间数组
            timeArray = time.strptime(end, "%Y-%m-%d %H:%M:%S")
            # 得到时间戳
            timeStamp = int(time.mktime(timeArray))
            endStamp.append(timeStamp - now)
        else:
            # 将找不到结束时间的流量包设置为不激活
            endStamp.append(86401)
    return endStamp


# 激活即将过期的流量包
def actionFlow(username):
    # 获得所有未使用的流量包
    datas = getStorageFlow(username)
    # 获得流量包还剩多长时间到期时间戳
    endTime = getflowEndTime(username)
    # 流量包下标
    i = 0
    flag = True
    for end in endTime:
        # 如果时间小于1天就激活
        # 程序早上7：30运行，正好当天可使用
        if end < 86400:
            flag = False
            activeData = {
                'activeCode': datas[i]['activeCode'],
                'prizeRecordID': datas[i]['prizeRecordID'],
                'activeName': '做任务领奖品'
            }
            # 激活流量包
            res = s.post('http://m.client.10010.com/myPrizeForActivity/myPrize/activationFlowPackages.htm',
                         data=activeData)
            res.encoding = 'utf-8'
            res = res.json()
            if res['status'] == '200':
                cio.write('【即将过期流量包】: ' + '激活成功' + '\n\n')
            else:
                cio.write('【即将过期流量包】: ' + '激活失败' + '\n\n')
            time.sleep(8)
        i = i + 1
    if flag:
        cio.write('【即将过期流量包】: 暂无' + '\n\n')


# 防刷校验
def check():
    s.headers.update({'referer': 'https://img.client.10010.com'})
    s.headers.update({'origin': 'https://img.client.10010.com'})
    data4 = {
        'methodType': 'queryTaskCenter',
        'taskCenterId': '',
        'videoIntegral': '',
        'isVideo': '',
        'sVersion': '8.0600',
        'deviceType': 'Android'
    }
    # 在此之间验证是否有防刷校验
    taskCenter = s.post('https://m.client.10010.com/producGameTaskCenter', data=data4)
    try:
        taskCenters = taskCenter.json()
        gameId = ''
        for t in taskCenters['data']:
            if t['task_title'] == '宝箱任务':
                gameId = t['game_id']
                break
        data5 = {
            'userNumber': 'queryTaskCenter',
            'methodType': 'flowGet',
            'gameId': gameId,
            'sVersion': '8.0100',
            'deviceType': 'Android'
        }
        producGameApp = s.post('https://m.client.10010.com/producGameApp', data=data5)
        producGameApp.encoding = 'utf-8'
        res = producGameApp.json()
        s.headers.pop('referer')
        s.headers.pop('origin')
        if res['code'] == '9999':
            return True
        else:
            cio.write('【娱乐中心任务】: 触发防刷，跳过' + '\n\n')
            return False
    except:
        cio.write('【娱乐中心任务】:访问页面出错\n\n')
        return False


# 每月领取1G流量包，仅限湖北用户
# 位置：暂时不清楚
def monthOneG(username):
    # 获取当前是本月几号
    now = getTimezone()
    timeArray = time.localtime(now)
    day = time.strftime("%d", timeArray)
    ## 联通活动 不需要登录
    url = f'https://wap.10010hb.net/zinfo/activity/mobilePrize/getAward?serialNumber={username}'
    # 每月3号领取
    if day == 3:
        award = s.post(url, '{}')
        award.encoding = 'utf-8'
        res = award.json()
        cio.write('【每月领取1G】: ' + res['alertMsg'] + '\n\n')


def main():
    users = os.getenv('UNICOM_USER')
    if users:
        users = json.loads(users)
        for user in users:
            login(user['username'], user['password'], user['appId'])
            daySign_task(user['username'])
            getIntegral()
            luckDraw_task()
            if 'lotteryNum' in user:
                pointsLottery_task(user['lotteryNum'])
            else:
                pointsLottery_task(0)
            day100Integral_task()
            dongaoPoints_task()
            if check():
                gameCenterSign_Task(user['username'])
                openBox_task()
            collectFlow_task()
            woTree_task()
            actionFlow(user['username'])
            monthOneG(user['username'])
        content = cio.getvalue()
        digest = dio.getvalue()
        QYWX_Notify().send('联通APP签到信息', digest, content)


# 主函数入口
if __name__ == '__main__':
    main()
