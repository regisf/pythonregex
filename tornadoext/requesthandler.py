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

import pickle
import tornado.web

from App.utils.question import Question
from App.models.preference import PreferenceModel
from App.models.user import UserModel

class RequestHandler(tornado.web.RequestHandler):
    """
    Extend the tornado requesthandler with few useful
    methods, mainly for authentication
    """
    def __init__(self, *args, **kwargs):
        super(RequestHandler, self).__init__(*args, **kwargs)

    def add_flash_message(self, level, message):
        """
        Pass a message
        """
        cookie = self.get_secure_cookie("messages")
        messages = None

        if cookie:
            messages = pickle.loads(cookie)

        if not messages:
            messages = []

        messages.append({'level': level, 'message': message})
        self.set_secure_cookie("messages", pickle.dumps(messages))

    def get_template_namespace(self):
        """
        Make some variables global for all templates
        """
        ns = super(RequestHandler, self).get_template_namespace()
        pref = PreferenceModel().get_codes()
        cookie = self.get_secure_cookie("messages")
        connected = self.get_secure_cookie("connected") or False

        ns.update({
            'question': Question(),
            'analytics': pref.get("analytics"),
            'messages': pickle.loads(cookie) if cookie else None,
            'connected': connected
        })

        if connected:
            user = UserModel().find_by_id(connected)
            ns.update({
                'username': user['username'],
                'email': user['email']
            })

        # Remove messages
        self.clear_cookie("messages")
        return ns

