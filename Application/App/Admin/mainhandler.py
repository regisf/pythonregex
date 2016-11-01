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

from tornadoext.requesthandler import RequestHandler, admin_auth_required

from App.models.user import UserModel
from App.models.regex import RegexModel

class AdminHandler(RequestHandler):
    @admin_auth_required
    def get(self):
        self.render(
            'admin/index.html',
            last_users=UserModel().get_last_ten(),
            regex_stored=RegexModel().count()
        )


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
            self.render('admin/login.html', error="Unknow user or wrong password")
        else:
            self.login(user)
            self.redirect('/admin/')


class LogoutHandler(RequestHandler):
    @admin_auth_required
    def get(self):
        self.logout()
        self.redirect('/admin/login/')
