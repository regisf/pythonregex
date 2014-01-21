# -*- coding: utf-8 -*-
#
# Python-regex.com : Regular expression as in Kodos3 but for the web
#
# (c) Régis FLORET 2013 and later - All right reserved
#

import json

import tornado.websocket

from .pyregex import PyRegex

class WebSocketHandler(tornado.websocket.WebSocketHandler, PyRegex):
    def open(self):
        print("Open the web socket")

    def on_message(self, message):
        result = self.doTheJob(json.loads(message))
        self.write_message(result)

    def on_close(self):
        print("Close socket")
