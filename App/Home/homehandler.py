# -*- coding: utf-8 -*-
#
# Python-regex.com : Regular expression as in Kodos3 but for the web
#
# (c) Régis FLORET 2013 and later - All right reserved
#

import tornado.web
import re


class HomeHandler(tornado.web.RequestHandler):
    def get(self):
        msie = re.findall(r'MSIE\s(\d+)', self.request.headers.get('user-agent'))
        if len(msie) > 0:
            if int(msie[0]) < 9:
                self.render('ie.html', page="Die IE lte 8 ! Die !")
                return

        # Debug purpose only
        self.render('index.html', page='index')
