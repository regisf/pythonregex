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

from tornado.web import authenticated
from tornadoext.requesthandler import RequestHandler

from App.models.user import UserModel


class LoginHandler(RequestHandler):
    """
    Connect the user
    """
    def post(self):
        model = UserModel()
        email = self.get_argument("email")
        password = self.get_argument("password")
        message = "Unknow user (bad email or wrong password). You should retry."
        message_level = 1

        if email and password:
            user = model.validate_user(email, password)
            self.set_secure_cookie('user', user['username'])
            self.current_user = user

            message = "You are now connected."
            message_level = 0

        self.add_flash_message(message_level, message)
        self.redirect('/')


class LogoutHandler(RequestHandler):
    """
    Disconnect the user and go to the main page
    """
    @authenticated
    def get(self):
        self.add_flash_message(0, "You are now disconnected.")
        self.clear_cookie("user")
        self.redirect('/')