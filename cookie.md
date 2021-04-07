## cookie转换代码

#### **吾爱破解**

```
var CV = '单引号里面放浏览器复制好的cookie';
var CookieValue = CV.match(/htVD_2132_auth=.+?;/) + CV.match(/htVD_2132_saltkey=.+?;/);
copy(CookieValue);
```

#### **CSDN**

```
var CV = '单引号里面放浏览器复制好的cookie';
var CookieValue = CV.match(/UserName=.+?;/) + CV.match(/UserToken=.+?;/);
copy(CookieValue);
```

#### **tool.lu**

##### 如果使用以下代码一定要到 https://plus.tool.lu/user/sign获取cookie

```
var CV = '单引号里面放浏览器复制好的cookie';
var CookieValue = CV.match(/uuid=.+?;/) + CV.match(/laravel_session=.+/);
copy(CookieValue);
```

#### **有道云笔记**

```
var CV = '单引号里面放浏览器复制好的cookie';
var CookieValue = CV.match(/YNOTE_SESS=.+?;/) + 'YNOTE_LOGIN=true';
copy(CookieValue);
```

#### **WPS**

```
var CV = '单引号里面放浏览器复制好的cookie';
var CookieValue = CV.match(/wps_sid=(.+?);/)[1];
copy(CookieValue);
```

#### **uiwow**

##### 此代码复制出来的cookie需要再手动改成字典形式

```
var CV = '单引号里面放浏览器复制好的cookie';
var CookieValue = CV.match(/discuz_2132_auth=.+?;/) + CV.match(/discuz_2132_saltkey=.+?;/);
copy(CookieValue);
```