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

from App.models.preference import PreferenceModel


class PreferenceHandler(RequestHandler):
    def post(self):
        """
        Save preferences
        """
        default_email = self.get_argument('defaultemail', '')
        server_name = self.get_argument('servername', "localhost")
        server_port = self.get_argument("serverport", "")
        server_username = self.get_argument("serverusername", "")
        server_password = self.get_argument("serverpassword", "")
        PreferenceModel().save_mail_server(default_email, server_name, server_port, server_username, server_password)
        self.redirect("/admin/emails/")

