# daily_sign

### 日常签到

### **更新历史**

2021.4.6 新增新冠疫情自动通报

2021.4.5 新增联通营业厅APP签到

2021.4.1 增加微博签到

2021.3.31 增加uiwow签到，修改企业微信通知模块，QYWX_Notify().send(title, digest[, content])

 只传入2个参数时，发送文本卡片消息（通知示例1）

```
			 传入3个参数时，发送图文消息（通知示例2、3），图片可以在QYWX_Notify.py第13行更改
```

2021.3.30 增加NGA签到

2021.3.27 改变签到方式，每个签到程序单独运行。增加WPS签到

2021.3.26 增加有道云笔记签到

2021.3.23 为避免index.py太过臃肿，修改了代码结构。正在尝试多线程签到

2021.3.21 增加tool.lu签到

2021.3.20 增加CSDN、天翼云盘签到

2021.3.19 创建项目，建立吾爱破解签到

### **通知示例**

[![通知示例1](https://camo.githubusercontent.com/1e285b19b60425c48fee3757d0d2b5d38c5eef1f9497102aecc3686de8327155/68747470733a2f2f696d616765732e67697465652e636f6d2f75706c6f6164732f696d616765732f323032312f303331392f3232343130355f63646431303566645f373934333931362e706e67)](https://camo.githubusercontent.com/1e285b19b60425c48fee3757d0d2b5d38c5eef1f9497102aecc3686de8327155/68747470733a2f2f696d616765732e67697465652e636f6d2f75706c6f6164732f696d616765732f323032312f303331392f3232343130355f63646431303566645f373934333931362e706e67)

![示例2](https://gitee.com/kxs2018/imgbed/raw/master/pic/1.jpg)

![示例三](https://gitee.com/kxs2018/imgbed/raw/master/pic/2.png)

### **签到列表**

| 网站名称                                     | 多账号 | 说明                                                         |
| -------------------------------------------- | ------ | ------------------------------------------------------------ |
| [吾爱破解](https://www.52pojie.cn/forum.php) | 否     |                                                              |
| [CSDN](https://blog.csdn.net/)               | 否     |                                                              |
| [天翼云盘](https://cloud.189.cn/)            | 是     | 帐号：手机号，密码：不能带&。                                |
|                                              |        | 帐号和帐号、密码和密码间用&连接                              |
| [在线工具](https://tool.lu/)                 | 否     |                                                              |
| [有道云笔记](https://note.youdao.com/web)    | 是     |                                                              |
| [WPS](https://vip.wps.cn/taskcenter/)        | 否     | 网页、客户端、小程序多渠道签到                               |
| [NGA](https://bbs.nga.cn/)                   | 是     | 手机APP刮墙签到，填secrets时uid之间、token之间               |
|                                              |        | 用&连接，应注意uid和token的对应关系                          |
| [uiwow](https://www.uiwow.com/)（登录）      | 是     | 账号和密码，用&连接。注意对应关系                            |
| [uiwow](https://www.uiwow.com/)（cookie）    | 是     | [secrets](https://github.com/lqkxs3608/daily_signin/blob/main/secrets.md)：单个账号cookie用字典的形式，多个账号用列表套字典的形式 |
| [微博](https://weibo.com/)                   | 是     | API链接，用手机抓包APP获取，https://api.weibo.cn/2/users/show开头的一长串，多账号换行即可 |
| 联通APP                                      | 是     | 列表套字典 [{"username": "手机号", "password": "服务密码", "appId": "appid"}] |
| 新冠疫情通报                                 |        | JUDGE填入任意字符通报，不添加secret不通报；PROVINCE填入需要通报的省市区（包括34个省/直辖市/自治区/特别行政区） |

注：

1. 无特殊说明多账号cookie之间用&分隔。uiwow列表套字典，微博换行

2. 签到时间为北京时间上午7:30左右，复签8:30左右；

   如需更改签到时间，到.github\workflows\xxxx.yml中更改

3. 不需要签到的网站不需要加secrets

### secrets

- 添加方式：setting-secrets-add a new secret
- [secrets说明](https://github.com/kxs2018/daily_sign/blob/main/secrets.md)

### **获取cookie**

1. 浏览器登录网站——按F12打开开发人员工具——NETWORK拉动右边的滚动条到最顶部，点击最上面的选项（如下图）

[![img](https://camo.githubusercontent.com/9a789c22c5051d1d8b66fa5496a90e86df80bf57a7ef94759eef403768fb4b69/68747470733a2f2f67697465652e636f6d2f6b7873323031382f696d676265642f7261772f6d61737465722f7069632f676574636f6f6b69652e6a7067)](https://camo.githubusercontent.com/9a789c22c5051d1d8b66fa5496a90e86df80bf57a7ef94759eef403768fb4b69/68747470733a2f2f67697465652e636f6d2f6b7873323031382f696d676265642f7261772f6d61737465722f7069632f676574636f6f6b69652e6a7067)

1. 上面复制好的cookie先保存到本地，然后复制相应的代码到浏览器开发人员工具的console里，再把cookie复制粘帖到代码里并按enter，所需要的cookie就复制到剪切板了，粘帖到本地备用即可。

   ```
   # 吾爱破解cookie转换代码（这行不用复制）
   var CV = '单引号里面放前面拿到的cookie';
   var CookieValue = CV.match(/htVD_2132_auth=.+?;/) + CV.match(/htVD_2132_saltkey=.+?;/);
   copy(CookieValue);
   ```

[各网站cookie转换代码](https://github.com/kxs2018/daily_signin/blob/main/cookie.md)