# -*- coding: utf-8 -*-
#
# Python-regex.com : Regular expression as in Kodos3 but for the web
#
# (c) Régis FLORET 2013 and later - All right reserved
#

import json

import tornado.web

from .pyregex import PyRegex

print("Restart")

class AjaxHandler(tornado.web.RequestHandler, PyRegex):
    def get(self):
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            try:
                value = json.loads(self.get_argument('json', None))
                self.write(self.doTheJob(value))
            except TypeError as e:
                self.write(json.dumps({ 'success' : False, 'error' : e}))
