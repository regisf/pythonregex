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

import datetime

from . import database
from .user import UserModel

class UserSessionModel(object):
    """
    This class handle all user session stuff
    """
    def __init__(self, sessionid):
        self.db = database.usersession
        self._session = self.db.find_one({
            'sessionid':sessionid
        })

    def save_session(self, user, sessionid):
        """
        Log the user by storing.
        If the sessionid exists refresh the expiration date
        """
        prev_session = self.db.find_one({'user_id': user.get('_id')})
        new_date = datetime.datetime.now() + datetime.timedelta(days=1)

        if not prev_session:
            self.db.insert({
                'user_id': user.get('_id'),
                'sessionid': sessionid,
                'expiration': datetime.datetime.now() + datetime.timedelta(days=1)
            })
        else:
            self.db.update(
                prev_session, {
                    '$set': {
                        'expiration': new_date
                    }
                }
            )

    def find_user_by_sessionid(self, sessionid):
        """ self.db.find_one({'sessionid':sessionid})['user']"""
        


