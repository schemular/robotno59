#-*- coding:utf-8 -*-
#   Author  :   schemular(Tang Wei)
#   E-mail  :   schemular@gmail.com
#   Desc    :   有道词典翻译库

import urllib2
import urllib
import simplejson as json
import sys

class YoudaoDic():
    VERSION = 1.1
    URL = 'http://fanyi.youdao.com/openapi.do'
    KEY_FROM = 'EAWRVAEWR'
    KEY = '509323970'
    TYPE = 'data'
    DOC_TYPE = 'json'
    def translate(self, text, debug = True):
        params = {'keyfrom': self.KEY_FROM, 'key': self.KEY, 'type': self.TYPE, 'doctype': self.DOC_TYPE, 'version': self.VERSION ,'q': text}
        request = urllib2.urlopen(self.URL, urllib.urlencode(params))
        data = request.read()
        return json.loads(data)

    def get_result(self, text):
        data = self.translate(text)
        if data:
            translation = data.get('translation', None)
            if translation:
                for t in translation:
                    return unicode(t)
            else:
                return None
