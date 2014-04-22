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

from tornado.web import RequestHandler

from App.utils.email import is_email
from App.models.user import UserModel


class ConnectHandler(RequestHandler):
    def post(self):
        """ A user connection
        """
        email = self.get_argument("email")
        password = self.get_argument('password')

        if not (email and password):
            return

        if not is_email(email):
            return

        model = UserModel()

        if not model.user_exists(email, password):
            return

