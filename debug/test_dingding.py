import json

import requests


# 发送文本
def sendDingDing(text, url):
    print(text)
    headers = {'Content-Type': 'application/json'}
    data = {
        "msgtype": "text",
        "text": {
            "content": text + '\n'
        },
        "at": {
            "atMobiles": [

            ],
            "isAtAll": False
        }
    }

    response = requests.post(url=url, data=json.dumps(data), headers=headers)

    re = response.json()

    print(re)


# 发送链接
def send_msg(url):
    headers = {'Content-Type': 'application/json;charset=utf-8'}
    data = {
        "msgtype": "a",
        "link": {
            "text": 'fiddler学习',
            "title": "https://www.cnblogs.com/yyhh/p/5140852.html",
            "messageUrl": "https://www.cnblogs.com/yyhh/p/5140852.html"

        },
    }
    response = requests.post(url, data=json.dumps(data), headers=headers)
    re = response.json()

    print(re)


if __name__ == '__main__':
    text = '上班 @刘洋 '
    # 西安测试群
    # webhook = "https://oapi.dingtalk.com/robot/send?access_token=5e4612d5274b8640e44a121809f9174af1521a2600cd9a96b5709d009bbaf9ca"
    # 采购测试群
    url = "https://oapi.dingtalk.com/robot/send?access_token=a403defb479a378a60c64c6163b0d7480218b9691d0b4a4c0bb784f0c20ccb8b"
    # sendDingDing(text, url)
    send_msg(url)
