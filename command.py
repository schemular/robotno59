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
#   Date    :   13/04/19 13:57:17
#   Desc    :   命令
#
#   Modified:   schemular(Tang Wei)
#   E-mail  :   schemular@gmail.com
#   Desc    :   删去了大部分不会用到的功能，只保留了upload_file和send_msg
#

import re
import gzip
import json
import urllib2
import httplib
import logging
import traceback
from functools import partial
from cStringIO import StringIO
from lxml import etree

from http_stream import HTTPStream, Form
from config import MAX_LENGTH

def upload_file(filename, path):
    form = Form()
    filename = filename.encode("utf-8")
    form.add_file(fieldname='img', filename=filename,
                    fileHandle=open(path))
    #img_host = "http://paste.linuxzen.com"
    img_host = "http://localhost:8800"
    req = urllib2.Request(img_host)
    req.add_header("Content-Type", form.get_content_type())
    req.add_header("Content-Length", len(str(form)))
    req.add_data(str(form))
    return urllib2.urlopen(req)

class Command(object):
    http_stream = HTTPStream.instance()

    def send_msg(self, msg, callback, nick = None):
        body = nick + msg if nick else msg
        callback(unicode(body))
