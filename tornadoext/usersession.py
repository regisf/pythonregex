# -*- coding: utf-8 _*_

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
