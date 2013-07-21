#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright 2013 cold
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
#   Author  :   cold
#   E-mail  :   wh_linux@126.com
#   Date    :   13/03/01 11:44:05
#   Desc    :   消息调度
#
#   Modified:   schemular(Tang Wei)
#   E-mail  :   schemular@gmail.com
#   Desc    :   删减功能，将用户消息与群消息统一

import re
import logging
from functools import partial

from command import Command
from config import MAX_RECEIVER_LENGTH

import functions

code_typs = ['actionscript', 'ada', 'apache', 'bash', 'c', 'c#', 'cpp',
              'css', 'django', 'erlang', 'go', 'html', 'java', 'javascript',
              'jsp', 'lighttpd', 'lua', 'matlab', 'mysql', 'nginx',
              'objectivec', 'perl', 'php', 'python', 'python3', 'ruby',
              'scheme', 'smalltalk', 'smarty', 'sql', 'sqlite3', 'squid',
              'tcl', 'text', 'vb.net', 'vim', 'xml', 'yaml']

ABOUT_STR = u"Function Author: schemular(schemular@gmail.com)\n"\
	u"Platform Author: cold(wh_linux@126.com)\n"

HELP_DOC = u"""Robot No.59 使用指南:
    >>> <statement>  可以执行Python语句, 并为你个人将这个语句产生的定义放在服务器
    ping Pual        可以查看Pual是否在线
    about Pual       可以查看Pual相关信息
    help Pual        显示本信息
"""


URL_RE = re.compile(r"(http[s]?://(?:[-a-zA-Z0-9_]+\.)+[a-zA-Z]+(?::\d+)"
                    "?(?:/[-a-zA-Z0-9_%./]+)*\??[-a-zA-Z0-9_&%=.]*)",
                    re.UNICODE)

class MessageDispatch(object):
    """ 消息调度器 """
    def __init__(self, webqq):
        self.webqq = webqq
        self.cmd = Command()

    def send_msg(self, content, callback, nick = None):
        self.cmd.send_msg(content, callback, nick)

    def handle_qq_msg_contents(self, contents):
        content = ""
        for row in contents:
            if isinstance(row, (str, unicode)):
                content += row.replace(u"【提示：此用户正在使用Q+"
                                       u" Web：http://web.qq.com/】", "")\
                        .replace(u"【提示：此用户正在使用Q+"
                                       u" Web：http://web3.qq.com/】", "")
        return  content.replace("\r", "\n").replace("\r\n", "\n")\
                .replace("\n\n", "\n")


    def handle_qq_group_msg(self, message):
        """ 处理组消息 """
        value = message.get("value", {})
        gcode = value.get("group_code")
        uin = value.get("send_uin")
        contents = value.get("content", [])
        content = self.handle_qq_msg_contents(contents)
        uname = self.webqq.get_group_member_nick(gcode, uin)
        if content:
            logging.info(u"Got Group Message {0} from {1}".format(content, gcode))
            pre = u"{0}: ".format(uname)
            callback = partial(self.webqq.send_group_msg, gcode)
            self.handle_content(u"g" + unicode(gcode), unicode(uin), content, callback, unicode(uname))


    def handle_qq_message(self, message, is_sess = False):
        """ 处理QQ好友消息 """
        value = message.get("value", {})
        from_uin = value.get("from_uin")
        contents = value.get("content", [])
        content = self.handle_qq_msg_contents(contents)
        if content:
            typ = "Sess" if is_sess else "Friend"
            logging.info(u"Got {0} Message {1} from {2}".format(typ, content, from_uin))
            callback = self.webqq.send_sess_msg if is_sess else self.webqq.send_buddy_msg
            callback = partial(callback, from_uin)
            self.handle_content(u'b' + unicode(from_uin), unicode(from_uin), content, callback, u"您")


    def handle_content(self, group_code, from_uin, content, callback, appellation):
        """ 处理内容
        Arguments:
            `group_code`-       组代码
            `from_uin`  -       发送者uin
            `content`   -       内容
            `callback`  -       仅仅接受内容参数的回调
            `appellation`       -       称呼
        """
        send_msg = partial(self.send_msg, callback = callback, nick = None)
        content = unicode(content)
        content = content.strip()

        functions.do_functions(group_code, from_uin, content, send_msg, appellation)


    def dispatch(self, qq_source):
        if qq_source.get("retcode") == 0:
            messages = qq_source.get("result")
            for m in messages:
                if m.get("poll_type") == "group_message":
                    self.handle_qq_group_msg(m)
                if m.get("poll_type") == "message":
                    self.handle_qq_message(m)
                if m.get("poll_type") == "kick_message":
                    self.webqq.stop()
                if m.get("poll_type") == "sess_message":
                    self.handle_qq_message(m, True)
