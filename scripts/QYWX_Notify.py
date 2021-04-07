# -- coding: utf-8 --
import json
import requests
import os


class QYWX_Notify:
    def __init__(self):
        self.corpid = os.getenv("QYWX_CORPID")
        self.corpsecret = os.getenv("QYWX_CORPSECRET")
        self.agentid = os.getenv("QYWX_AGENTID")
        self.access_token = self.__get_access_token()
        self.img_url = 'https://gitee.com/kxs2018/imgbed/raw/master/pic/0.jpg'

    def __get_access_token(self):
        url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken'
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

    def get_ShortTimeMedia(self):
        media_url = f'https://qyapi.weixin.qq.com/cgi-bin/media/upload?access_token={self.access_token}&type=file'

        f = requests.get(self.img_url).content
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
            data["msgtype"] = 'mpnews'
            data["mpnews"] = {
                "articles": [
                    {
                        "title": title,
                        "thumb_media_id": self.get_ShortTimeMedia(),
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
