#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Python-regex.com : Regular expression as in Kodos3 but for the web
#
# (c) Régis FLORET 2013 and later - All right reserved
#

import os

import tornado.web
import tornado.ioloop
import tornado.autoreload

import settings
import filters
from urls import URLS

def runApp():
    """
    Run the application.
    """
    application = tornado.web.Application(
        URLS,
        debug=settings.DEBUG,
        template_path=settings.ROOT_TEMPLATE_PATH,
        cookie_secret=settings.SECRET_KEY,
        ui_modules={'simple_date': filters.SimpleDate}
        #xsrf_cookies=True,
    )

    # The watcher
    if settings.DEBUG:
        for (path, dirs, files) in os.walk(settings.ROOT_TEMPLATE_PATH):
            for item in files:
                tornado.autoreload.watch(os.path.join(path, item))

    # Start application
    application.listen(8888)
    print("Start listening on 8888")
    io = tornado.ioloop.IOLoop.instance()
    tornado.autoreload.start(io)
    io.start()

if __name__ == "__main__":
    runApp()
