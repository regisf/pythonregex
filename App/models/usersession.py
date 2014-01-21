# -*- coding: utf-8 -*-
#
# Python-regex.com : Regular expression as in Kodos3 but for the web
#
# (c) Régis FLORET 2013 and later - All right reserved
#

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
        


