# -*- coding: utf-8 -*-
#
# Python-regex.com : Regular expression as in Kodos3 but for the web
#
# (c) Régis FLORET 2013 and later - All right reserved
#

import hashlib
import datetime

from . import database
import settings


class UserModel:
    """
    The UserModel is a wrapper to avoid direct database calls in the program
    """
    def __init__(self):
        """
        Ctor. Load the User collection
        """
        self.users = database.user

    def _generate_password(self, password):
        """
        Generate the hash password
        """
        return hashlib.sha256(settings.SECRET_KEY.encode() + password.encode()).hexdigest()

    def is_email_exists(self, email):
        """
        Test if an email exists
        """
        return self.users.find_one({'email':email}) is not None

    def create_user(self, username, email, password, temp=True, is_admin=False):
        """
        Create an user
        If temp is set to True, an hash is generated
        """
        return self.users.insert({
            'username': username,
            'email': email,
            'password': self._generate_password(password),
            'creation_date': datetime.datetime.now(),
            'is_admin': is_admin
        })

    def edit(self, username, creation_date, email, is_admin):
        """
        Modify entry
        """
        self.users.update(
            {'username': username},
            {'$set': {
                'username': username,
                'creation_date': datetime.datetime.strptime(creation_date, "%Y-%m-%d %H:%M:%S.%f"),
                'is_admin': is_admin,
                'email': email
            }}
        )

    def find_user_by_session_id(self, sessionid):
        """
        Retreive an user by the sessionid key
        """

    def exists(self, username):
        """
        Find an user admin matching the username and his the password
        """
        return self.users.find_one({
            'username': username
        })

    def all(self, ):
        """
        Get all users at once
        """
        return self.users.find()

    def get_last_ten(self):
        """ Get last 10 users for the admin front page
        """
        return self.users.find()[:9]

    def get_by_name(self, name):
        """ Get a user by its username
        """
        return self.users.find_one({'username':name})

    def delete(self, name):
        """
        Delete the entry
        """
        self.users.remove({'username': name})
