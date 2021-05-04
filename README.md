# daily_sign 日常签到


### **最近更新**

2021.5.4  更新wps签到，每半小时执行一次，每天8:00-8:30 19:00-19:30通知一次

2021.4.27 uiwow网站似乎不稳定，暂停签到



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
| 喜马拉雅极速版                               | 是     | 手机抓包cookie，多账号换行即可                               |

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

[![](https://gitee.com/kxs2018/imgbed/raw/master/pic/getcookie.jpg)

1. 上面复制好的cookie先保存到本地，然后复制相应的代码到浏览器开发人员工具的console里，再把cookie复制粘帖到代码里并按enter，所需要的cookie就复制到剪切板了，粘帖到本地备用即可。

   ```
   # 吾爱破解cookie转换代码（这行不用复制）
   var CV = '单引号里面放前面拿到的cookie';
   var CookieValue = CV.match(/htVD_2132_auth=.+?;/) + CV.match(/htVD_2132_saltkey=.+?;/);
   copy(CookieValue);
   ```

[各网站cookie转换代码](https://github.com/kxs2018/daily_sign/blob/main/cookie.md)