# -*- coding: utf-8 -*-
#
# Python-regex.com : Regular expression as in Kodos3 but for the web
#
# (c) Régis FLORET 2013 and later - All right reserved
#

from tornado.web import RequestHandler

from App.models.preference import PreferenceModel


class PreferenceHandler(RequestHandler):
    def post(self, ):
        mail = self.get_argument('defaultemail')
        name = self.get_argument('servername')
        port = self.get_argument('serverport')
        username = self.get_argument('serverusername')
        password = self.get_argument('serverpassword')

        pref = PreferenceModel()
        pref.save(mail, name, port, username, password)

        self.redirect('/admin/emails/')