# -- coding: utf-8 --
import json
import requests
import os
import random

class QYWX_Notify:
    def __init__(self):
        self.corpid = os.getenv("QYWX_CORPID")
        self.corpsecret = os.getenv("QYWX_CORPSECRET")
        self.agentid = os.getenv("QYWX_AGENTID")
        self.agentid = os.getenv("QYWX_TOUSER")
        self.agentid = os.getenv("QYWX_TUPIAN")
        self.access_token = self.__get_access_token()

            
    def __get_access_token(self):
        url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken        '
        params = {
            'corpid': self.corpid,
            'corpsecret': self.corpsecret
        }
        resp = requests.get(url, params=params)
        resp.raise_for_status()
        resp_json = resp.json()
        if 'access_token' in resp_json.keys():
            return resp_json['access_token']
        else:
            raise Exception('Please check if corpid and corpsecret are correct \n' + resp.text)

    def get_ShortTimeMedia(self, img_url):
        media_url = f'https://qyapi.weixin.qq.com/cgi-bin/media/upload?access_token={self.access_token}&type=file'
        f = requests.get(img_url).content
        r = requests.post(media_url, files={'file': f}, json=True)
        return json.loads(r.text)['media_id']

    def send(self, title, digest, content=None):
        url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=' + self.access_token
        data = {
            "touser": "@all",
            "agentid": self.agentid,
            "safe": 0,
            "enable_id_trans": 0,
            "enable_duplicate_check": 0,
            "duplicate_check_interval": 1800
        }
        if content is not None:
#            img_url = f'https://gitee.com/kxs2018/imgbed/raw/master/pic/{random.randint(3, 14)}.jpg'
            img_url = f'https://gitee.com/kxs2018/imgbed/raw/master/pic/3.jpg'
            content = '<pre>' + content + '</pre>'
            data["msgtype"] = 'mpnews'
            data["mpnews"] = {
                "articles": [
                    {
                        "title": title,
                        "thumb_media_id": self.get_ShortTimeMedia(img_url),
                        "author": "",
                        "content_source_url": "",
                        "content": content,
                        "digest": digest
                    }
                ]
            }
        else:
            data["msgtype"] = "textcard"
            data["textcard"] = {
                "title": title,
                "description": digest,
                "url": "URL"}
        resp = requests.post(url, data=json.dumps(data))
        resp.raise_for_status()
        return resp.json()

  
      
function qywxamNotify(text, desp) {
  return new Promise(resolve => {
    if (QYWX_CORPID) {
#      const QYWX_AM_AY = QYWX_AM.split(',');
       const options_accesstoken = {
        url: `https://qyapi.weixin.qq.com/cgi-bin/gettoken`,
        json: {
          corpid: self.corpid,
          corpsecret: self.corpsecret
        },
        headers: {
          'Content-Type': 'application/json',
        },
        timeout
      };
      $.post(options_accesstoken, (err, resp, data) => {
        html = desp.replace(/\n/g, "<br/>")
        var json = JSON.parse(data);
        accesstoken = json.access_token;
        let options;

        switch (QYWX_TUPIAN) {
          case '0':
            options = {
              msgtype: 'textcard',
              textcard: {
                title: `${text}`,
                description: `${desp}`,
                url: 'https://github.com/lxk0301/jd_scripts',
                btntxt: '更多'
              }
            }
            break;

          case '1':
            options = {
              msgtype: 'text',
              text: {
                content: `${text}\n\n${desp}`
              }
            }
            break;

          default:
            options = {
              msgtype: 'mpnews',
              mpnews: {
                articles: [
                  {
                    title: `${text}`,
                    thumb_media_id: `${QYWX_TUPIAN}`,
                    author: `智能助手`,
                    content_source_url: ``,
                    content: `${html}`,
                    digest: `${desp}`
                  }
                ]
              }
            }
        };
        if (!QYWX_TUPIAN) {
          //如不提供第四个参数,则默认进行文本消息类型推送
          options = {
            msgtype: 'text',
            text: {
              content: `${text}\n\n${desp}`
            }
          }
        }
        options = {
          url: `https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=${accesstoken}`,
          json: {
            touser: `${ChangeUserId(desp)}`,
            agentid: `${QYWX_AGENTID}`,
            safe: '0',
            ...options
          },
          headers: {
            'Content-Type': 'application/json',
          },
        }

        $.post(options, (err, resp, data) => {
          try {
            if (err) {
              console.log('成员ID:' + ChangeUserId(desp) + '企业微信应用消息发送通知消息失败！！\n');
              console.log(err);
            } else {
              data = JSON.parse(data);
              if (data.errcode === 0) {
                console.log('成员ID:' + ChangeUserId(desp) + '企业微信应用消息发送通知消息成功🎉。\n');
              } else {
                console.log(`${data.errmsg}\n`);
              }
            }
          } catch (e) {
            $.logErr(e, resp);
          } finally {
            resolve(data);
          }
        });
      });
    } else {
      console.log('您未提供企业微信应用消息推送所需的QYWX_AM，取消企业微信应用消息推送消息通知🚫\n');
      resolve();
    }
  });
}
