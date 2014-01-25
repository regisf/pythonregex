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

"""
User session manager all user in
a session storage
"""

from App.models.usersession import UserSessionModel
from App.models.user import UserModel

class UserSession(object):
    def __init__(self, sessionid):
        """ Try to find the user by its session key """
        self._anonymous = True if not sessionid else False
        self._user = UserSessionModel(sessionid)

    @property
    def user(self):
        """
        Return the UserSessionModel stored as private
        """
        return self._user

    @property
    def is_authenticated(self):
        """
        """
        return self._user is not None

    def login(self, user, sessionid):
        """
        Log the user
        """
        self._anonymous = False
        if not self._user:
            self._user = UserSessionModel()
        self._user.save_session(user, sessionid)

    def logout(self):
        pass

    def admin_authenticate(self, username, password):
        """
        Find if an user exists and he's admin.
        If so, add the sessionkey and add an expiration date (now + 1 day)
        """
        UserModel().exists(username, password, True)
