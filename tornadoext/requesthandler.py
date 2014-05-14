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

import hashlib
import datetime

import tornado.web

from tornadoext.usersession import UserSession
from App.utils.question import Question

class RequestHandler(tornado.web.RequestHandler):
    """
    Extend the tornado requesthandler with few useful
    methods, mainly for authentication
    """
    def __init__(self, *args, **kwargs):
        super(RequestHandler, self).__init__(*args, **kwargs)
        self.user = UserSession(self.get_secure_cookie('sessionid'))


    def get_template_namespace(self):
        """
        Make some variables global for all templates
        """
        ns = super(RequestHandler, self).get_template_namespace()
        ns.update({
            'question': Question()
        })
        return ns

    def login(self, user):
        """
        Log in the user
        Create as sessionid based on the datetime
        """
        if user and user.get('is_admin'):
            salt = "{}{}".format(user.get('username'), str(datetime.datetime.now()))
            sessionid = hashlib.md5(salt.encode('utf-8')).hexdigest()
            self.set_secure_cookie('sessionid', sessionid)
            self.user.login(user, sessionid)


    def logout(self):
        """
        Logout the user
        """
        self.clear_cookie('sessionid', None)

