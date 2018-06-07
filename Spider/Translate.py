# -*- coding: utf-8 -*-
"""
Created on Wed Feb 28 15:49:58 2018

Translate API, Chinese To English
translate(words)

@author: Voter
"""
import json
from Spider import SpiderTool as ns


def __getParams(words):
    data = {"type": "AUTO",
            "i": words,
            "doctype": "json",
            "xmlVersion": "1.8",
            "keyfrom:fanyi": "web",
            "ue": "UTF-8",
            "action": "FY_BY_CLICKBUTTON",
            "typoResult": "true"}
    return data


def __getJsonData(html):
    result = json.loads(html)
    result = result['translateResult']
    result = result[0][0]['tgt']
    return result


def translate(words):
    url = "http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule&smartresult=ugc&sessionFrom=dict.top"
    data = __getParams(words)
    html = ns.getHtml(url, data)
    result = __getJsonData(html)
    return result


if __name__ == "__main__":
    text = translate('新闻')
    print(text)