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

import re

from tornadoext.requesthandler import RequestHandler

class HomeHandler(RequestHandler):
    def get(self):
        msie = re.findall(r'MSIE\s(\d+)', self.request.headers.get('user-agent'))
        if len(msie) > 0:
            if int(msie[0]) < 9:
                self.render('ie.html', page="Die IE lte 8 ! Die !")
                return

        # Debug purpose only
        self.render('index.html', page='index')
