#-*- coding:utf-8 -*-
#   Author  :   schemular(Tang Wei)
#   E-mail  :   schemular@gmail.com
#   Desc    :   信息处理模块

import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

import re
import user
import logging
import random

import database
import youdao

HELP_DOC = u"""五十九号机器人使用指南:
1.>>> <statement>
可以在执行Python语句
2.学习 <question> <answer>
可以教机器人说话
3.翻译<sentence>
可以翻译一句话
4.<word>是什么
可以查询百度百科信息
5.帮助
显示本信息"""

def do_functions(group_code, from_uin, content, sendback, appellation):
    content = unicode(content)
    add_score(group_code, from_uin)

    chat(content, appellation, sendback)

    if u"积分" in content:
        score = unicode(user.get_score(group_code, from_uin))
        sendback(u"{0}现在的积分是：{1}".format(appellation, score))

    if content.startswith(">>>"):
        sendifnotempty(run_py(content.lstrip(">").lstrip(" ")), sendback)
        return

    if content.startswith(u"学习"):
        con = content.lstrip(u"学习").lstrip(u' ')
        arr = con.split(' ')
        key = arr.pop(0)
        value = ""
        for x in arr:
            value = value + x + " "

        value = value.lstrip(' ').rstrip(' ')
        if (not (value == None or value.lstrip(' ').rstrip(' ') == '')) and (not (key == None or key.lstrip(' ').rstrip(' ') == '')):
            sendifnotempty(user.learn(key, value), sendback)
        else:
            sendback(u"如果你想让我学习什么东西，格式是这样的：学习 【关键词问题】【空格】【回答】。")
        return

    if content.startswith(u"翻译"):
        con = content.lstrip(u"翻译").lstrip(' ').rstrip(' ')
        result = user.translate(con)
        if not result == None:
            sendback(u"{0} 的翻译是 {1}。".format(con, result))
        else:
            sendback(u"没有找到{0}的翻译。".format(con))
        return

    conk = content = re.sub(u'[!?,！？，。 ]', u'', content)
    if conk.endswith(u"是什么"):
        conk = conk.rstrip(u"是什么")
        result = user.get_knowledge(conk)
        if not (result == None or result.lstrip(' ').rstrip(' ') == ''):
            sendback(result)
        else:
            sendback(u"我也不知道。")
        return

def chat(content, appellation, sendback):
    content = re.sub(u'[【】!?,！？，。]', u'', content)

    arr = []
    if content == u'帮助':
        arr.append(HELP_DOC)
    if database.dic.has_key("chat"):
        for key in database.dic["chat"].keys():
            if key in content:
                if isinstance(database.dic["chat"][key], list):
                    for item in database.dic["chat"][key]:
                        arr.append(item)
                else:
                    arr.append(database.dic["chat"][key])

    if len(arr) == 0:
        return

    index = random.randint(0, len(arr) - 1)
    sendback(arr[index])

def run_py(content):
    result = "### " + re.sub(u'\n', u'\n### ', user.eval_code(content))
    result = result.rstrip('\n### ')
    logging.debug(u"Run python code and get result {0}".format(result))
    return result
    
def sendifnotempty(content, sendback):
    if not (content == None or content.lstrip(' ').rstrip(' ') == ''):
        sendback(content)

def add_score(group_code, from_uin):
    if not database.dic.has_key("score"):
        database.dic["score"] = dict()

    key = group_code + ":" + from_uin
    if not database.dic["score"].has_key(key):
        database.dic["score"][key] = 0

    database.dic["score"][key] += 1
    database.store("score")
