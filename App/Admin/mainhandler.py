# -*- coding: utf-8 -*-
#
# Python-regex.com : Regular expression as in Kodos3 but for the web
#
# (c) Régis FLORET 2013 and later - All right reserved
#

from tornadoext.requesthandler import RequestHandler

from App.models.user import UserModel


class AdminHandler(RequestHandler):
    def get(self):
        if not self.user.is_authenticated:
            self.redirect("/admin/login/")
            return
        last_users = UserModel().get_last_ten()
        self.render('admin/index.html', last_users=last_users, regex_stored=0)


class LoginHandler(RequestHandler):
    def get(self):
        self.render('admin/login.html', error=None)

    def post(self):
        user_model = UserModel()
        user = user_model.exists(
            username=self.get_argument('username'),
            password=self.get_argument('password'),
            is_admin=True
        )

        if not user:
            self.render('admin/login.html',error="Unknow user or wrong password")
        else:
            self.login(user)
            self.redirect('/admin/')


class LogoutHandler(RequestHandler):
    def get(self):
        self.logout()
        self.redirect('/admin/login/')
