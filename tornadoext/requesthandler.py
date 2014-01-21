# -*- coding: utf-8 -*-

import hashlib
import datetime

import tornado.web

from tornadoext.usersession import UserSession

class RequestHandler(tornado.web.RequestHandler):
    """
    Extend the tornado requesthandler with few useful
    methods, mainly for authentication
    """
    def __init__(self, *args, **kwargs):
        super(RequestHandler, self).__init__(*args, **kwargs)
        self.user = UserSession(self.get_secure_cookie('sessionid'))

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

