# -*- coding: utf-8 -*-
#
# Python-regex.com : Regular expression as in Kodos3 but for the web
#
# (c) Régis FLORET 2013 and later - All right reserved
#

"""
Contains all public urls for the WebSite
"""

import os
import re

import tornado.web

import settings

from App.Home.homehandler import HomeHandler
from App.Home.ajaxhandler import AjaxHandler
from App.Home.websockethandler import WebSocketHandler
from App.Home.registerhandler import RegisterHandler, CheckEmailHandler

from App.Admin.urls import URLS as AdminURLS

URLS = [
    (r'^/assets/(.*)', tornado.web.StaticFileHandler, {'path': settings.STATIC_FILES}),

    (r'^/$', HomeHandler),

    (r'^/auth/register/$', RegisterHandler),

    (r'^/wsa/$', AjaxHandler),
    (r'^/ws/$', WebSocketHandler),
] + AdminURLS

