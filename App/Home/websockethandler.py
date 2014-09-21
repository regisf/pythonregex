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

import json

import tornado.websocket
from tornado.web import authenticated

from .pyregex import PyRegex
from App.models.regex import RegexModel
from App.models.user import UserModel


class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def get_current_user(self):
        return self.get_secure_cookie('user')

    def write_message(self, message, binary=False):
        message = json.dumps(message, ensure_ascii=False)
        super(WebSocketHandler, self).write_message(message, binary=binary)

    def on_message(self, message):
        result_json = json.loads(message)

        if 'action' in result_json:
            #
            # Evaluate
            #
            if result_json['action'] == 'evaluate':
                result = PyRegex().doTheJob(json.loads(message))
                self.write_message(result)
                return

            #
            # Save a regex
            #
            elif result_json['action'] == 'save':
                user = self.get_current_user() or False
                if user:
                    self.current_user = UserModel().find_by_username(user)

                try:
                    saved = RegexModel().save_for_user(result_json['name'], result_json['regex'], self.current_user)
                except AttributeError as err:
                    self.write_message({'success': False, 'error': str(err)})

                self.write_message({'success': True})
                return

            #
            # Delete a REGEX
            #
            elif result_json['action'] == 'delete':
                user = self.get_current_user() or False
                if user:
                    self.current_user = UserModel().find_by_username(user)
                    RegexModel().delete(self.current_user, result_json['id'])
                    self.write_message({'success': True})
                    return

        self.write_message({'success': False, 'error': 'Unknow action'})
