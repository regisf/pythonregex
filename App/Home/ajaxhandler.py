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

import tornado.web

from .pyregex import PyRegex

print("Restart")

class AjaxHandler(tornado.web.RequestHandler, PyRegex):
    def get(self):
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            try:
                value = json.loads(self.get_argument('json', None))
                print(value)
                self.write(self.doTheJob(value))
            except TypeError as e:
                self.write(json.dumps({'success': False, 'error': e}))
