#-*- coding:utf-8 -*-
#   Author  :   schemular(Tang Wei)
#   E-mail  :   schemular@gmail.com
#   Desc    :   用户空间和用户信息处理模块

import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

import os
import re
import database
import traceback
import StringIO
import urllib
import urllib2
from bs4 import BeautifulSoup

import functions
import user
from youdao import YoudaoDic

def eval_code(code):
    try:
        obj = eval(code)
        if obj == None:
            obj = u'None'
        else:
            obj = unicode(obj)
        return obj
    except:
        fp = StringIO.StringIO()
        traceback.print_exc(file=fp)
        return fp.getvalue()

def learn(key, value):
    key = key.decode('utf-8')
    value = value.encode('utf-8')
    key = re.sub(u'[【】!?,！？，。]', u'', key)

    if not database.dic.has_key("chat"):
        database.dic["chat"] = dict()

    if not database.dic["chat"].has_key(key):
        database.dic["chat"][key] = []

    if isinstance(database.dic["chat"][key], str) or isinstance(database.dic["chat"][key], unicode):
        database.dic["chat"][key] = [ database.dic["chat"][key] ]

    database.dic["chat"][key].append(value)
    database.store("chat")
    return u"Learn {0} => {1} OK!".format(key, value)

def get_score(group_code, from_uin):
    key = group_code + ":" + from_uin
    if not database.dic.has_key("score"):
        database.dic["score"] = dict()

    if not database.dic["score"].has_key(key):
        database.dic["score"][key] = 0

    return database.dic["score"][key]

def translate(text):
    youdao = YoudaoDic()
    return youdao.get_result(text)

def reload_functions():
    reload(functions)
    reload(user)
    return u'Reload functions OK!'

def list_learnt():
    if not database.dic.has_key("chat"):
        return None

    result = ""
    for key in database.dic["chat"].keys():
        result += key
        result += ' => '
        result += unicode(database.dic["chat"][key])
        result += '\n'
        
    return result.rstrip('\n')

def delete_learnt(key):
    if not database.dic.has_key("chat"):
        return u"Failed!"

    if not database.dic["chat"].has_key(key):
        return u"Failed!"

    database.dic["chat"].pop(key)
    database.store("chat")
    return u"OK!"

def get_knowledge(keyword):
    try:
        url = "http://baike.baidu.com/search?word=" + urllib.quote(keyword.encode('gbk'))
        doc = urllib.urlopen(url).read()
        soup = BeautifulSoup(doc)
        items = soup.findAll('div', {'class':'abstract'})
        if items == []:
            return None
        item = items[0]
        text = unicode(item.get_text())
        while(text.startswith('\n') or text.startswith('\r') or text.startswith(' ')):
            text = text.lstrip('\n')
            text = text.lstrip('\r')
            text = text.lstrip(' ')
        while(text.endswith('\n') or text.endswith('\r') or text.endswith(' ')):
            text = text.rstrip('\n')
            text = text.rstrip('\r')
            text = text.rstrip(' ')
        return text
    except:
        return None
