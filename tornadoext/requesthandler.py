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

import functools
import pickle
import tornado.web

from App.utils.question import Question
from App.models.preference import Config
from App.models.user import UserModel


def admin_auth_required(method):
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        user = self.get_current_user()
        if user:
            profile = self.get_user_profile()
            if profile['is_admin']:
                return method(self, *args, **kwargs)
        return self.redirect('/admin/login/')
    return wrapper



class RequestHandler(tornado.web.RequestHandler):
    """
    Extend the tornado requesthandler with few useful
    methods, mainly for authentication
    """
    def __init__(self, *args, **kwargs):
        super(RequestHandler, self).__init__(*args, **kwargs)
        self.current_user = self.get_user_profile()

    def get_current_user(self):
        """
        Return the current user. Used for tornado for authentication
        """
        return self.get_secure_cookie('user')

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
        # pref = PreferenceModel().get_codes()
        cookie = self.get_secure_cookie("messages")
        user = self.get_current_user() or False
        if user:
            self.current_user = UserModel().find_by_username(user)

        config = Config()

        ns.update({
            'question': Question(),
            'analytics': config.get("google_analytics_id"),
            'msvalidate': config.get('msvalidate'),
            'messages': pickle.loads(cookie) if cookie else None,
            'connected': bool(self.current_user)
        })

        if self.current_user:
            ns.update({
                'username': self.current_user['username'],
                'email': self.current_user['email']
            })

        # Remove messages
        self.clear_cookie("messages")
        return ns

    def get_user_profile(self):
        """
        Get the user if she/he's connected
        :return: The user db entry
        """
        user = self.get_current_user() or False
        return UserModel().find_by_username(user) if user else None

    def login(self, user):
        """
        Log the user. Convinient function
        :param user: the user db entry
        :return: None
        """
        self.set_secure_cookie('user', user['username'])
        self.current_user = user

    def logout(self):
        self.clear_cookie('user')
        self.current_user = None
