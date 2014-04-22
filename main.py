#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Python-regex.com : Regular expression as in Kodos3 but for the web
# (c) Régis FLORET 2013 and later
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

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
        ui_modules={'simple_date': filters.SimpleDate},
        login_url="/auth/login/",
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
